# Cowork Process Monitor — Dashboard

A simple, self-contained visual dashboard for monitoring Cowork process
efficiency. No frameworks, no CDNs, no backend — it loads a single local
JSON file, so it runs fully **offline** and needs **no new permissions**.

## What it shows

- **Mode banner** — online / offline, with a note on offline behaviour.
- **Summary cards** — active processes, efficiency %, completed/pending
  tasks, tasks skipped because they need new permissions, uptime.
- **Efficiency trend** — a lightweight canvas sparkline (no chart library).
- **Work areas** — per-area health scores so effort can be focused on the
  areas that are already permitted and improvable.
- **Processes** table — status, health, throughput, last tick.
- **Tasks** table — including which tasks are skipped pending permission.

## Offline-mode behaviour

By design, anything marked `needsNewPermission: true` is shown as
**skipped** rather than attempted. While offline, effort is redirected to
improving already-permitted areas (monitoring, optimization, reporting).
The skipped items stay visible so they can be picked up once online /
authorized.

## Run it locally

It must be served over HTTP (browsers block `fetch` of local files):

```bash
cd dashboard
python3 -m http.server 8000
# open http://localhost:8000
```

## Online access (GitHub Pages)

A workflow at `.github/workflows/pages.yml` publishes the `dashboard/`
folder. To turn it on once:

1. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Push to the configured branch (or run the workflow manually).
3. The dashboard URL appears in the workflow run summary.

## Updating the data

Edit `data/status.json`. Any monitoring job can overwrite this file; the
dashboard reads it fresh on load and on **Refresh**. The schema is in that
file — keep the same keys.
