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

## Online access (CI artifact)

The workflow at `.github/workflows/pages.yml` regenerates the data, validates
the dashboard, and publishes the whole `dashboard/` folder as a downloadable
build artifact (`cowork-dashboard`) on every push. This needs no extra plan
or permissions and works on private repos.

To view the published build:

1. Open the latest **Build dashboard** run under the repo's **Actions** tab.
2. Download the **cowork-dashboard** artifact and unzip it.
3. Serve it locally (`python3 -m http.server` inside the folder) and open it.

> GitHub Pages was intentionally dropped: Pages on a private repo requires a
> paid plan and the CI token cannot create the Pages site. If you later enable
> Pages (or make the repo public), swap the upload step for
> `actions/upload-pages-artifact` + `actions/deploy-pages` to get a live URL.

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
