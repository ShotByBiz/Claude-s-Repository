# Metrics That Matter

Track these. Most are computed by `tools/pipeline_report.py` once you log real
leads in `crm/leads.csv`.

## Acquisition funnel
- **Leads contacted** → **demos booked** → **demos done** → **won**.
- Watch the biggest drop-off and fix that stage first. Usually it's
  contacted→demo (outreach copy) or demo→won (price framing / ROI clarity).

## Money
- **MRR** — sum of `monthly_price` for `won` clients. The north star.
- **ARR** — MRR × 12 (run-rate).
- **CAC** — total outreach cost (your time + any ad/tool spend) ÷ clients won.
- **Gross margin** — (price − voice/LLM/number cost) ÷ price. Keep > 80%.
- **Payback** — months of revenue to recover CAC. Target < 1.

## Retention (the one that kills you if ignored)
- **Churn %** — clients lost ÷ clients at start of month.
- **The fix is the weekly value report.** Clients churn when they forget what
  you do. Show calls answered + bookings made every week.

## Self-funding loop (the operator's core KPI)
- **Credit Sustainability ratio** = monthly revenue ÷ monthly costs (API +
  tools + voice). Below 1.0 you're subsidizing; above 1.0 you're profitable and
  every new client compounds. Get the **first** client to push this past 1.0.

## How to read the dashboard
The repo's existing `/dashboard` derives status honestly from git history. If
you want a business dashboard, feed it `pipeline_report.py` output rather than
hand-writing numbers — keep the same honest-by-construction discipline: no
metric exists until a real event produced it.
