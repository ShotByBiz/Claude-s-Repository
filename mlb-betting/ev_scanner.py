"""
MLB +EV / arbitrage decision-support scanner.

This is an ALERTING tool, not an auto-betting bot: it surfaces mispriced
lines for you to act on manually. Automatically placing wagers through a
sportsbook's site/app typically violates that book's terms of service;
scanning and alerting does not.

Quick start (no setup required):
    python3 ev_scanner.py --demo

To use real odds, implement OddsProvider.fetch_odds() to call a live feed
(e.g. https://the-odds-api.com/) and return Quote objects in the same
shape produced by DemoOddsProvider below.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from itertools import combinations


# ---------------------------------------------------------------------------
# Odds math
# ---------------------------------------------------------------------------

def american_to_prob(odds: int) -> float:
    """Implied probability (with vig) from American odds."""
    if odds > 0:
        return 100 / (odds + 100)
    return -odds / (-odds + 100)


def american_to_decimal(odds: int) -> float:
    if odds > 0:
        return 1 + odds / 100
    return 1 + 100 / -odds


def no_vig_probs(prob_a: float, prob_b: float) -> tuple[float, float]:
    """Remove vig from a two-way market via simple multiplicative devigging."""
    overround = prob_a + prob_b
    return prob_a / overround, prob_b / overround


def kelly_fraction(prob_win: float, decimal_odds: float) -> float:
    """Full Kelly stake as a fraction of bankroll. Negative means no edge."""
    b = decimal_odds - 1
    q = 1 - prob_win
    return (b * prob_win - q) / b


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Quote:
    game: str          # e.g. "BOS @ NYY"
    market: str        # e.g. "moneyline", "total_8.5"
    side: str          # e.g. "NYY", "Over"
    book: str          # sportsbook name
    odds: int          # American odds


@dataclass
class Opportunity:
    kind: str          # "arbitrage" or "+ev"
    game: str
    market: str
    detail: str
    edge_pct: float
    recommended_stake_pct: float = 0.0
    tags: list[str] = field(default_factory=list)


class OddsProvider:
    """Override fetch_odds() with a real feed for live use."""

    def fetch_odds(self) -> list[Quote]:
        raise NotImplementedError


class DemoOddsProvider(OddsProvider):
    """Sample data so the scanner runs with zero configuration."""

    def fetch_odds(self) -> list[Quote]:
        return [
            # Best MIL price (BookA) + best ARI price (BookB) cross to a real arb.
            Quote("MIL @ ARI", "moneyline", "MIL", "BookA", -150),
            Quote("MIL @ ARI", "moneyline", "ARI", "BookA", +130),
            Quote("MIL @ ARI", "moneyline", "MIL", "BookB", -170),
            Quote("MIL @ ARI", "moneyline", "ARI", "BookB", +160),
            # Pinnacle is the sharp reference; BookC is stale/soft on Under.
            Quote("TOR @ SEA", "total_7.5", "Under", "Pinnacle", -115),
            Quote("TOR @ SEA", "total_7.5", "Over", "Pinnacle", -105),
            Quote("TOR @ SEA", "total_7.5", "Under", "BookA", -110),
            Quote("TOR @ SEA", "total_7.5", "Over", "BookA", -110),
            Quote("TOR @ SEA", "total_7.5", "Under", "BookC", +105),
            Quote("TOR @ SEA", "total_7.5", "Over", "BookC", -125),
        ]


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

class EVScanner:
    def __init__(
        self,
        bankroll: float,
        kelly_multiplier: float = 0.25,
        max_stake_pct: float = 0.03,
        edge_threshold_pct: float = 2.0,
        sharp_books: frozenset[str] = frozenset({"Pinnacle"}),
    ):
        self.bankroll = bankroll
        self.kelly_multiplier = kelly_multiplier
        self.max_stake_pct = max_stake_pct
        self.edge_threshold_pct = edge_threshold_pct
        self.sharp_books = sharp_books

    def scan(self, quotes: list[Quote]) -> list[Opportunity]:
        opportunities: list[Opportunity] = []
        by_market: dict[tuple[str, str], list[Quote]] = {}
        for q in quotes:
            by_market.setdefault((q.game, q.market), []).append(q)

        for (game, market), qs in by_market.items():
            opportunities += self._find_arbitrage(game, market, qs)
            opportunities += self._find_plus_ev(game, market, qs)

        opportunities.sort(key=lambda o: o.edge_pct, reverse=True)
        return opportunities

    def _find_arbitrage(self, game: str, market: str, qs: list[Quote]) -> list[Opportunity]:
        found = []
        by_side: dict[str, list[Quote]] = {}
        for q in qs:
            by_side.setdefault(q.side, []).append(q)
        sides = list(by_side.keys())
        if len(sides) != 2:
            return found

        best_a = max(by_side[sides[0]], key=lambda q: american_to_decimal(q.odds))
        best_b = max(by_side[sides[1]], key=lambda q: american_to_decimal(q.odds))

        implied = american_to_prob(best_a.odds) + american_to_prob(best_b.odds)
        if implied < 1.0:
            profit_pct = (1 / implied - 1) * 100
            stake_a_pct = american_to_prob(best_a.odds) / implied
            found.append(Opportunity(
                kind="arbitrage",
                game=game,
                market=market,
                detail=(
                    f"{best_a.side}@{best_a.book} ({best_a.odds:+d}) + "
                    f"{best_b.side}@{best_b.book} ({best_b.odds:+d}) -> "
                    f"guaranteed profit; stake {stake_a_pct:.1%} on {best_a.side}, "
                    f"{1 - stake_a_pct:.1%} on {best_b.side}"
                ),
                edge_pct=profit_pct,
            ))
        return found

    def _find_plus_ev(self, game: str, market: str, qs: list[Quote]) -> list[Opportunity]:
        found = []
        by_side: dict[str, list[Quote]] = {}
        for q in qs:
            by_side.setdefault(q.side, []).append(q)
        sides = list(by_side.keys())
        if len(sides) != 2:
            return found

        # Prefer a designated sharp book (e.g. Pinnacle) as the fair-price
        # reference if one is quoting both sides — averaging every book,
        # including a mispriced one, dilutes the very edge you're trying
        # to detect. Fall back to a same-side-excluded consensus average.
        sharp_a = next((q for q in by_side[sides[0]] if q.book in self.sharp_books), None)
        sharp_b = next((q for q in by_side[sides[1]] if q.book in self.sharp_books), None)
        if sharp_a and sharp_b:
            fair_a, fair_b = no_vig_probs(american_to_prob(sharp_a.odds), american_to_prob(sharp_b.odds))
        else:
            avg_a = sum(american_to_prob(q.odds) for q in by_side[sides[0]]) / len(by_side[sides[0]])
            avg_b = sum(american_to_prob(q.odds) for q in by_side[sides[1]]) / len(by_side[sides[1]])
            fair_a, fair_b = no_vig_probs(avg_a, avg_b)
        fair = {sides[0]: fair_a, sides[1]: fair_b}

        for q in qs:
            book_prob = american_to_prob(q.odds)
            edge_pct = (fair[q.side] - book_prob) * 100
            if edge_pct >= self.edge_threshold_pct:
                dec = american_to_decimal(q.odds)
                full_kelly = max(kelly_fraction(fair[q.side], dec), 0.0)
                stake_pct = min(full_kelly * self.kelly_multiplier, self.max_stake_pct)
                found.append(Opportunity(
                    kind="+ev",
                    game=game,
                    market=market,
                    detail=(
                        f"{q.side}@{q.book} ({q.odds:+d}) — fair prob "
                        f"{fair[q.side]:.1%} vs book-implied {book_prob:.1%}"
                    ),
                    edge_pct=edge_pct,
                    recommended_stake_pct=stake_pct,
                ))
        return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="run against sample odds")
    parser.add_argument("--bankroll", type=float, default=1000.0)
    parser.add_argument("--kelly-multiplier", type=float, default=0.25,
                         help="fraction of full Kelly to actually stake (default 0.25 = quarter Kelly)")
    parser.add_argument("--max-stake-pct", type=float, default=0.03,
                         help="hard cap on stake as a fraction of bankroll (default 3%%)")
    parser.add_argument("--edge-threshold", type=float, default=2.0,
                         help="minimum +EV edge in percentage points to report (default 2.0)")
    args = parser.parse_args()

    provider: OddsProvider = DemoOddsProvider() if args.demo else DemoOddsProvider()
    if not args.demo:
        print("No live provider configured — falling back to --demo sample odds.\n"
              "Implement OddsProvider.fetch_odds() with a real feed for live use.\n")

    scanner = EVScanner(
        bankroll=args.bankroll,
        kelly_multiplier=args.kelly_multiplier,
        max_stake_pct=args.max_stake_pct,
        edge_threshold_pct=args.edge_threshold,
    )
    opportunities = scanner.scan(provider.fetch_odds())

    if not opportunities:
        print("No +EV or arbitrage opportunities found in the current odds set.")
        return

    for opp in opportunities:
        stake_note = ""
        if opp.recommended_stake_pct:
            stake_note = f" | suggested stake: {opp.recommended_stake_pct:.2%} of bankroll (${opp.recommended_stake_pct * args.bankroll:.2f})"
        print(f"[{opp.kind.upper():9}] {opp.game} — {opp.market} | edge {opp.edge_pct:.2f}%{stake_note}")
        print(f"            {opp.detail}\n")


if __name__ == "__main__":
    main()
