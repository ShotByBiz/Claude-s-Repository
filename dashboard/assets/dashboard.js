"use strict";

// Self-contained dashboard. No external dependencies, no network calls
// beyond loading the local data file — works fully offline.

const DATA_URL = "data/status.json";

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

function timeAgo(iso) {
  if (!iso) return "—";
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return "—";
  const secs = Math.max(0, Math.round((Date.now() - then) / 1000));
  if (secs < 60) return secs + "s ago";
  if (secs < 3600) return Math.round(secs / 60) + "m ago";
  if (secs < 86400) return Math.round(secs / 3600) + "h ago";
  return Math.round(secs / 86400) + "d ago";
}

function show(id) {
  const node = document.getElementById(id);
  if (node) node.hidden = false;
}

function renderMode(d) {
  const badge = document.getElementById("modeBadge");
  const mode = (d.mode || "unknown").toLowerCase();
  badge.textContent = mode;
  badge.className = "mode " + (mode === "online" ? "online" : "offline");

  if (d.modeNote) {
    const note = document.getElementById("modeNote");
    note.textContent = d.modeNote;
    show("modeNote");
  }
}

function renderCards(s) {
  const cards = document.getElementById("cards");
  cards.innerHTML = "";
  const items = [
    { label: "Active processes", value: s.activeProcesses, cls: "good" },
    { label: "Efficiency", value: s.efficiencyPct + "%", cls: "accent" },
    { label: "Completed tasks", value: s.completedTasks, cls: "" },
    { label: "Pending tasks", value: s.pendingTasks, cls: "warn" },
    { label: "Skipped (needs perm.)", value: s.skippedNeedsPermission, cls: "warn" },
    { label: "Uptime", value: s.uptimePct + "%", cls: "good" },
  ];
  for (const it of items) {
    const card = el("div", "card " + it.cls);
    card.appendChild(el("div", "value", String(it.value)));
    card.appendChild(el("div", "label", it.label));
    cards.appendChild(card);
  }
  show("cards");
}

function renderUsage(u) {
  if (!u) return;
  show("usagePanel");
  document.getElementById("usageLabel").textContent = "Daily budget (" + u.unitLabel + ")";
  document.getElementById("usageNums").textContent =
    u.usedToday + " / " + u.dailyBudget + " used · " + u.remaining + " left";
  const fill = document.getElementById("usageFill");
  fill.style.width = Math.min(100, u.usedPct) + "%";
  fill.style.background = u.usedPct >= 90 ? "var(--bad)" : u.usedPct >= 70 ? "var(--warn)" : "var(--good)";
  const note = document.getElementById("usageNote");
  note.textContent = (u.onTrack ? "On track. " : "Over budget. ") + u.pacingNote;
  note.style.color = u.onTrack ? "var(--muted)" : "var(--bad)";

  const peak = document.getElementById("peakHour");
  peak.textContent = "peak " + String(u.peakHourUtc).padStart(2, "0") + ":00";

  const hours = document.getElementById("hours");
  hours.innerHTML = "";
  const pattern = u.hourlyPattern || [];
  const max = Math.max(1, ...pattern);
  pattern.forEach((v, h) => {
    const col = el("div", "hour");
    const bar = el("div", "hour-bar");
    bar.style.height = Math.round((v / max) * 100) + "%";
    if (h === u.peakHourUtc) bar.classList.add("peak");
    bar.title = String(h).padStart(2, "0") + ":00 — " + v;
    col.appendChild(bar);
    if (h % 6 === 0) col.appendChild(el("span", "hour-label", String(h)));
    hours.appendChild(col);
  });
}

function renderTrend(series) {
  if (!Array.isArray(series) || series.length === 0) return;
  show("trendPanel");
  const canvas = document.getElementById("trend");
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height, pad = 24;
  ctx.clearRect(0, 0, W, H);

  const min = Math.min(...series), max = Math.max(...series);
  const range = max - min || 1;
  const stepX = (W - pad * 2) / (series.length - 1 || 1);
  const x = (i) => pad + i * stepX;
  const y = (v) => H - pad - ((v - min) / range) * (H - pad * 2);

  // grid baseline
  ctx.strokeStyle = "#2b3645";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pad, H - pad);
  ctx.lineTo(W - pad, H - pad);
  ctx.stroke();

  // area fill
  ctx.beginPath();
  ctx.moveTo(x(0), y(series[0]));
  series.forEach((v, i) => ctx.lineTo(x(i), y(v)));
  ctx.lineTo(x(series.length - 1), H - pad);
  ctx.lineTo(x(0), H - pad);
  ctx.closePath();
  ctx.fillStyle = "rgba(88,166,255,0.12)";
  ctx.fill();

  // line
  ctx.beginPath();
  ctx.moveTo(x(0), y(series[0]));
  series.forEach((v, i) => ctx.lineTo(x(i), y(v)));
  ctx.strokeStyle = "#58a6ff";
  ctx.lineWidth = 2;
  ctx.stroke();

  // points + last label
  series.forEach((v, i) => {
    ctx.beginPath();
    ctx.arc(x(i), y(v), 3, 0, Math.PI * 2);
    ctx.fillStyle = "#58a6ff";
    ctx.fill();
  });
  ctx.fillStyle = "#e6edf3";
  ctx.font = "12px sans-serif";
  ctx.fillText(series[series.length - 1] + "%", x(series.length - 1) - 18, y(series[series.length - 1]) - 8);
}

function renderAreas(areas) {
  if (!Array.isArray(areas)) return;
  show("areasPanel");
  const wrap = document.getElementById("areas");
  wrap.innerHTML = "";
  for (const a of areas) {
    const row = el("div", "area-row");
    const head = el("div", "area-head");
    head.appendChild(el("span", null, a.name + (a.improving ? " ↑" : "")));
    head.appendChild(el("span", null, a.score + "%"));
    row.appendChild(head);
    const bar = el("div", "area-bar");
    const fill = el("span");
    fill.style.width = Math.max(2, a.score) + "%";
    bar.appendChild(fill);
    row.appendChild(bar);
    wrap.appendChild(row);
  }
}

function renderProcesses(procs) {
  if (!Array.isArray(procs)) return;
  show("procPanel");
  const tbody = document.querySelector("#procTable tbody");
  tbody.innerHTML = "";
  for (const p of procs) {
    const tr = el("tr");
    const name = el("td");
    name.appendChild(el("strong", null, p.name));
    if (p.note) name.appendChild(el("div", "label", p.note));
    tr.appendChild(name);
    tr.appendChild(el("td", null, p.area));
    const st = el("td"); st.appendChild(el("span", "pill " + p.status, p.status)); tr.appendChild(st);
    const hl = el("td"); hl.appendChild(el("span", "pill " + p.health, p.health)); tr.appendChild(hl);
    tr.appendChild(el("td", null, (p.throughputPerMin || 0) + "/min"));
    tr.appendChild(el("td", null, timeAgo(p.lastTickIso)));
    tbody.appendChild(tr);
  }
}

function renderTasks(tasks) {
  if (!Array.isArray(tasks)) return;
  show("taskPanel");
  const tbody = document.querySelector("#taskTable tbody");
  tbody.innerHTML = "";
  for (const t of tasks) {
    const tr = el("tr");
    tr.appendChild(el("td", null, t.title));
    tr.appendChild(el("td", null, t.area));
    const st = el("td"); st.appendChild(el("span", "pill " + t.status, t.status.replace("_", " "))); tr.appendChild(st);
    const perm = el("td");
    if (t.needsNewPermission) perm.appendChild(el("span", "pill needs", "needs permission"));
    else perm.appendChild(el("span", "pill good", "ok"));
    tr.appendChild(perm);
    tbody.appendChild(tr);
  }
}

async function load() {
  const loading = document.getElementById("loading");
  try {
    const res = await fetch(DATA_URL, { cache: "no-store" });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const d = await res.json();

    loading.hidden = true;
    renderMode(d);
    if (d.summary) renderCards(d.summary);
    renderUsage(d.usage);
    renderTrend(d.efficiencyTrend);
    renderAreas(d.areas);
    renderProcesses(d.processes);
    renderTasks(d.tasks);

    const gen = document.getElementById("generatedAt");
    gen.textContent = "Generated: " + (d.generatedAt ? new Date(d.generatedAt).toLocaleString() : "—");
    const src = document.getElementById("dataSource");
    src.textContent = d.dataSource ? " · " + d.dataSource : "";
  } catch (err) {
    loading.textContent = "Could not load status data (" + err.message + "). Serve this folder over HTTP and ensure data/status.json exists.";
  }
}

// Auto-refresh every 30s when enabled, so an updated status.json shows up live.
let autoTimer = null;
function syncAutoRefresh() {
  const on = document.getElementById("autoRefresh").checked;
  if (autoTimer) { clearInterval(autoTimer); autoTimer = null; }
  if (on) autoTimer = setInterval(load, 30000);
}

document.getElementById("refresh").addEventListener("click", load);
document.getElementById("autoRefresh").addEventListener("change", syncAutoRefresh);
syncAutoRefresh();
load();
