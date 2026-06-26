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

## Data feed

`data/status.json` is **generated from real signals**, not hand-written.
`generate_status.py` derives the metrics from the repository's own git
history — commit cadence becomes the efficiency trend, files changed per
area become area health scores, the last commit time becomes each
process's last tick, and recent commit subjects become completed tasks.
It makes no network calls, so it runs in offline mode with no new
permissions.

Regenerate locally:

```bash
python3 dashboard/generate_status.py
```

In CI, the Pages workflow runs the generator before publishing, so the
live dashboard always reflects current repo state.

### Offline-skip config

Permission-gated work lives in `config.json` (`skippedProcesses`,
`skippedTasks`). These are surfaced as **skipped** while offline and are
never attempted by the generator. Move an item out of the skipped lists
once it's authorized. The dashboard auto-refreshes every 30s (toggle in
the footer) and on **Refresh**.
