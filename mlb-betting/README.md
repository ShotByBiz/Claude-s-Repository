# MLB Betting Analysis — July 3, 2026 Slate Grading + Systems Research

This folder captures a one-time deep-dive: grading a YouTube handicapping
video's picks against actual results, researching the specific "systems"
you cited, and shipping a decision-support (not auto-wagering) EV/arbitrage
scanner you can extend with a real odds feed.

**Read this first:** the three games break down below (Brewers/D-backs,
Blue Jays/Mariners, Padres/Dodgers) all actually happened on **Friday,
July 3, 2026**, not "today" (Saturday, July 4). The pitchers, matchups,
and stat lines in the video's chart match the real July 3 box scores
exactly, so the video was almost certainly a recap/preview for Friday's
card. If you want tonight's (July 4) slate broken down prospectively,
say so and I'll pull that separately — everything below is a
postmortem, not a live lean.

## 1. Grading the video's picks vs. what actually happened

| Game | Video's lean | Confidence | Projected score | Actual result | SU call | Score accuracy |
|---|---|---|---|---|---|---|
| Brewers @ D-backs | MIL | 7/10 | MIL 5–3 | **MIL 7, ARI 4 (11 innings)** | ✅ Hit | Off — game went to extras |
| Blue Jays @ Mariners | TOR (soft; recommended fading the ML for total/props instead) | 5.5/10 | TOR 4–3 | **TOR 2, SEA 0** | ✅ Hit | Off, but correctly low-scoring |
| Padres @ Dodgers | LAD ("strongest play") | 8/10 | LAD 6–4 | **LAD 4, SD 3** | ✅ Hit | Off — much tighter than modeled |

All three moneyline leans went 3-for-3 straight-up. That's a good day, but a
3-game sample proves nothing about process quality — and the underlying
pitching lines show exactly the variance you flagged going in.

**What the box scores actually showed:**

- **Kyle Harrison (MIL)** got knocked around: 2.2 IP, 3 ER, 5 H, 3 K, 1 BB —
  pulled early. **Jose Cabrera (ARI)**, the pitcher the video said was
  "much harder to trust," matched him pitch-for-pitch that night (3.1 IP,
  3 ER, 6 H, 3 K, 3 BB). The Brewers won anyway, in the 11th, on the
  strength of the bullpen and a bottom-of-the-lineup hit — not the starting
  pitching edge the model was built on.
- **Dylan Cease (TOR)** was excellent (7 IP, 9 K, 3 H, 1 BB), beating his
  7.5 K prop. **Luis Castillo (SEA)** also delivered the "capable quality
  start" the video expected (6 IP, 5 H, 4 K, 1 BB). This is the one game
  where the underlying metrics and the outcome lined up cleanly — and
  notably, the video's *most disciplined* call (avoid the moneyline, look
  at unders/Cease Ks) is the one that aged best.
- **Shohei Ohtani (LAD)** battled control problems all night (6 IP, 3 ER,
  7 H, 2 BB, 9 K — good strikeouts papering over a shaky command outing),
  and the Dodgers trailed until Teoscar Hernández's 7th-inning grand slam
  won it. The **highest-confidence pick (8/10) was, in practice, the
  closest and most fragile win of the three** — decided by one swing.

**The real finding:** confidence ranking (LAD 8 > MIL 7 > TOR 5.5) moved in
the *opposite* direction of how comfortable each win actually was (TOR was
a shutout; LAD needed a walk-off-caliber slam; MIL needed extras). That's
a clean, concrete illustration of your own thesis — xFIP/K9/BB9 tell you
about the pitcher, not about bullpen usage, lineup availability, sequencing,
or one bad Ohtani first inning. Grading this video: **B+**. Directionally
useful pitcher evaluation, correctly hedged on the Blue Jays game, but the
confidence numbers imply more precision than a single-game sample can
support — dial back exactly as you suspected, especially on the Dodgers
"strongest play" framing.

## 2. Winning bettors' strategies (general research)

- **Closing Line Value (CLV) is the best predictor of a real edge.**
  Beating the closing number consistently matters more than whether any
  single bet won — it's the metric that separates skill from variance.
- **Unit sizing: 1–3% of bankroll per bet.** Professional-sized bankrolls
  ($10k–$50k+ for full-time bettors) exist specifically to survive
  drawdowns; recreational bankrolls should scale the same percentages down.
- **Line shop everything.** Holding multiple book accounts and always
  taking the best number is one of the highest-value, lowest-effort habits
  available — half-points and a few cents of juice compound over volume.
- **Sample size discipline.** Real ROI benchmarks are far lower than
  people expect — 3–10% ROI over thousands of bets is a strong long-run
  result. Only a small fraction of bettors are net profitable long-term.
  Grading any system (including the video above, and including the
  "systems" below) on a handful of games is close to meaningless.
- **Fade the public only when it's confirmed by reverse line movement**
  (money moving against the betting percentage) — betting against the
  crowd with no market confirmation is not itself an edge.

Sources: [VSIN — Closing Line Value](https://vsin.com/how-to-bet/the-importance-of-closing-line-value/), [OddsJam — Bankroll Management](https://oddsjam.com/betting-education/bankroll-management), [Sports Insights — MLB Reverse Line Movement](https://www.sportsinsights.com/blog/mlb-sharp-money-profiting-reverse-line-movement/).

## 3. Checking your specific "systems" claims

I want to be straight with you on this part rather than just validate the
numbers, because the pattern matters more than any one figure.

**What I could verify:** Action Network documents a real, sourced MLB
July 4th trend: since 2005, **home teams on July 4 are 119-74 (62% SU,
+11% ROI)**. When the closing line moves toward the home team (a sharp/RLM
signal), that improves to **82-39 (68% SU, +20% ROI)**. That's the same
*shape* as what you described (base rate → jumps when a market-confirmation
filter is added) — but it's a **home-team moneyline** system, not the
**unders** system you cited, and the numbers are meaningfully lower than
yours (68%/20% here vs. your 76%/47%).

Separately, Sports Insights' Bet Labs research on the general "fade the
public + reverse line movement" family of systems (favorites/dogs
receiving under ~40% of bets while the line still moves their way) shows
**290-249 ATS (53.8%), 4.8% ROI** over a broad sample, and **75-57 (56.8%),
13.9% ROI** in the strongest recent 2-year window. That's structurally
close to your "less than 60% of bet size → jumps to 82% WR" framing, but
again, real documented numbers top out around 57% WR / ~14–20% ROI, not
82% WR / 57% ROI.

**What I could not verify:** your specific figures — "visiting favorite,
66% WR / 15% ROI over 8 years," the jump to "82% WR / 57% ROI" below 60%
of bet share, and the "4th of July unders, 56% WR / 10% ROI, jumping to
76% WR / 47% ROI when the total drops at the open" — don't match anything
in public sports-betting trend databases I can access (Action Network,
Odds Shark, Bet Labs writeups). That doesn't mean they're wrong; it likely
means they come from a proprietary tool (Bet Labs/Unabated subscription
backtest) or the same video/channel and weren't published externally.

**Why I'd treat them cautiously either way:**

1. **The math is internally consistent but the win rates are unusually
   high.** A 76% WR at roughly -110 pricing works out to ~45% ROI, and an
   82% WR works out to ~56% ROI — so the numbers aren't nonsense, they're
   just describing a level of edge that essentially never persists in a
   liquid market like MLB totals. Every verified, published system above
   caps out well under 20% ROI.
2. **Holiday-specific angles have tiny samples.** "July 4th" is ~15 games
   a year. Eight years is ~120 games. Splitting that further by "total
   moved down at open" plausibly leaves you with 20–40 games — small
   enough that a couple of favorable results skew the win rate hard. This
   is the textbook setup for an overfit backtest: slice a small sample by
   enough conditions and you'll always find a subset that looks amazing
   in hindsight.
3. **A jump from 56%→76% WR from one filter is a big swing.** Real,
   durable signals (like the RLM example above) typically move win rate
   by mid-to-high single digits when you add a confirming filter, not
   20 points.

**My recommendation:** treat these as a *small directional tilt* (lean
slightly toward home teams and confirmed-sharp unders on July 4th-style
spots), not as a system worth sizing up on. If you can point me to the
original source (the video, or a specific tool/site), I'll dig into the
actual methodology and sample rather than take the headline numbers at
face value.

## 4. The EV/arbitrage scanner (`ev_scanner.py`)

`ev_scanner.py` is a decision-support tool, **not an auto-betting bot** —
it surfaces +EV and true-arbitrage prices for you to act on manually.
I built it that way deliberately: automatically placing wagers violates
most sportsbooks' terms of service and is a fast way to get accounts
limited or closed, whereas an alerting/scanning tool that you execute on
is both compliant and just as useful for catching short-lived pricing gaps.

What it does:

- **No-vig fair pricing**: converts American odds to implied probability
  and removes the vig from a two-way market to estimate a "true" price.
- **+EV detection**: flags a book's price as +EV when it beats the no-vig
  consensus (or a designated sharp reference book like Pinnacle) by more
  than a configurable edge threshold.
- **True arbitrage detection**: checks whether opposite sides of the same
  market, priced at two different books, guarantee a profit regardless of
  outcome, and computes the stake split.
- **Fractional Kelly sizing**: sizes recommended stakes at a conservative
  fraction of full Kelly (defaults to 25%) against your bankroll, capped
  at a max % per bet — full Kelly is too volatile for a recreational
  bankroll you want to protect.
- **Contextual tags (off by default)**: optional flags for holiday/park/
  public-betting-style angles like the ones above, so a spot gets labeled
  `july4_home_team` or `rlm_fade_public` for your own tracking — these are
  informational tags, not scoring inputs, given the verification caveats
  in section 3.

It ships with a `--demo` mode using sample odds so it runs with no setup.
For real use, plug in a live odds feed (e.g. [The Odds API](https://the-odds-api.com/)
or similar) by implementing `OddsProvider.fetch_odds()` — see the comment
in the file for the expected shape.

```bash
python3 ev_scanner.py --demo
```

## 5. Bottom line

- Your instinct to dial back confidence was right, and today's box scores
  are a clean real-world example of why (bullpen/lineup/sequencing/variance
  all showed up in exactly the ways you described).
- The general "winning bettor" playbook — CLV, small flat units, line
  shopping, huge sample sizes — is a better long-run lever than any single
  angle, including the systems above.
- The specific system numbers you quoted are plausible in structure but
  unverified in magnitude; use them as a tilt, not a staking rule, until
  you can trace the exact source/sample.
- The scanner gives you a repeatable way to catch genuine mispricing
  (true arb, or a book lagging the market) without needing to trust any
  single narrative-driven pick.
