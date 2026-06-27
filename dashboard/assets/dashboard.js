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

// ---------- Approvals inbox ("on your desk") ----------
const PENDING_URL = "data/pending.json";
const REPO_ISSUES = "https://github.com/ShotByBiz/Claude-s-Repository/issues/new";

function decisionKey(id) { return "decision:" + id; }

function renderDesk(data) {
  const items = (data && data.items) || [];
  document.getElementById("deskCount").textContent = items.length;
  if (data && data.note) document.getElementById("deskSub").textContent = data.note;
  show("deskPanel");
  const wrap = document.getElementById("deskItems");
  wrap.innerHTML = "";
  if (!items.length) {
    wrap.appendChild(el("p", "desk-empty", "Nothing waiting — your desk is clear. ✅"));
    return;
  }
  items.forEach((it) => wrap.appendChild(deskCard(it)));
}

function deskCard(it) {
  const card = el("div", "desk-card");
  const saved = localStorage.getItem(decisionKey(it.id));
  card.appendChild(el("div", "desk-title", it.title));
  if (it.detail) card.appendChild(el("div", "desk-detail", it.detail));
  if (saved) {
    card.classList.add("decided");
    renderDecided(card, it, JSON.parse(saved));
  } else {
    const actions = el("div", "desk-actions");
    (it.options || ["Approve", "Deny"]).forEach((opt, i) => {
      const b = el("button", "desk-btn" + (i === 0 ? " primary" : ""), opt);
      b.addEventListener("click", () => decide(card, it, opt));
      actions.appendChild(b);
    });
    card.appendChild(actions);
  }
  return card;
}

function decide(card, it, choice) {
  const rec = { choice, at: new Date().toISOString() };
  localStorage.setItem(decisionKey(it.id), JSON.stringify(rec));
  card.classList.add("decided");
  const a = card.querySelector(".desk-actions");
  if (a) a.remove();
  renderDecided(card, it, rec);
  burst();
}

function renderDecided(card, it, rec) {
  const relay = "[decision] " + it.id + ": " + rec.choice;
  const box = el("div", "desk-decided");
  box.appendChild(el("span", "desk-chosen", "✓ You chose: " + rec.choice));
  const copyBtn = el("button", "desk-btn small", "Copy & relay to Claude");
  copyBtn.addEventListener("click", () => {
    if (navigator.clipboard) navigator.clipboard.writeText(relay);
    copyBtn.textContent = "Copied ✓ — paste in chat";
  });
  box.appendChild(copyBtn);
  const link = el("a", "desk-link", "or open a GitHub issue");
  link.href = REPO_ISSUES + "?title=" + encodeURIComponent("Decision: " + it.id) +
              "&body=" + encodeURIComponent(relay);
  link.target = "_blank"; link.rel = "noopener";
  box.appendChild(link);
  const undo = el("button", "desk-btn small ghost", "Undo");
  undo.addEventListener("click", () => { localStorage.removeItem(decisionKey(it.id)); loadPending(); });
  box.appendChild(undo);
  card.appendChild(box);
}

async function loadPending() {
  try {
    const res = await fetch(PENDING_URL, { cache: "no-store" });
    if (!res.ok) return;
    renderDesk(await res.json());
  } catch (_) { /* desk is optional */ }
}

// ---------- Live activity feed ----------
let knownEventIds = new Set();
let feedInitialized = false;
let lastEvents = null;

const AREA_COLORS = {
  monitoring: "#58a6ff", optimization: "#3fb950", reporting: "#d29922",
  integration: "#bc8cff", delivery: "#f778ba",
};
function areaColor(area) { return AREA_COLORS[area] || "#58a6ff"; }

function feedCard(ev) {
  const card = el("div", "feed-item");
  card.style.setProperty("--accent", areaColor(ev.area));
  const ring = el("div", "feed-ring");
  ring.innerHTML =
    '<svg viewBox="0 0 36 36"><circle class="bg" cx="18" cy="18" r="16"></circle>' +
    '<circle class="fg" cx="18" cy="18" r="16"></circle></svg><span class="check">✓</span>';
  card.appendChild(ring);
  const body = el("div", "feed-body");
  body.appendChild(el("div", "feed-title", ev.title));
  const meta = el("div", "feed-meta");
  meta.appendChild(el("span", "feed-area", ev.area));
  meta.appendChild(el("span", null, " · " + (ev.files || 0) + " files · " + timeAgo(ev.ts)));
  body.appendChild(meta);
  card.appendChild(body);
  return card;
}

function renderFeed(events, opts) {
  events = events || [];
  opts = opts || {};
  show("feedPanel");
  const feed = document.getElementById("feed");
  const stagger = opts.stagger !== undefined ? opts.stagger : !feedInitialized;

  if (!feedInitialized || opts.replace) {
    feed.innerHTML = "";
    knownEventIds = new Set();
    events.forEach((ev, i) => {
      const card = feedCard(ev);
      feed.appendChild(card);
      knownEventIds.add(ev.id);
      if (stagger) setTimeout(() => card.classList.add("show"), i * 160);
      else card.classList.add("show");
    });
    feedInitialized = true;
  } else {
    const incoming = events.filter((ev) => !knownEventIds.has(ev.id));
    incoming.reverse().forEach((ev) => {
      const card = feedCard(ev);
      feed.prepend(card);
      knownEventIds.add(ev.id);
      requestAnimationFrame(() => card.classList.add("show"));
      burst();
    });
  }
}

function replayFeed() {
  if (lastEvents) renderFeed(lastEvents, { replace: true, stagger: true });
  burst();
}

// Completion particle burst on the feed panel's canvas overlay.
function burst() {
  const canvas = document.getElementById("burst");
  const panel = document.getElementById("feedPanel");
  if (!canvas || !panel) return;
  canvas.width = panel.clientWidth;
  canvas.height = panel.clientHeight;
  const ctx = canvas.getContext("2d");
  const cx = canvas.width - 48, cy = 56;
  const colors = ["#58a6ff", "#3fb950", "#d29922", "#bc8cff", "#f778ba"];
  const parts = [];
  for (let i = 0; i < 28; i++) {
    const a = Math.random() * Math.PI * 2, s = 2 + Math.random() * 4.5;
    parts.push({ x: cx, y: cy, vx: Math.cos(a) * s, vy: Math.sin(a) * s - 1.2,
      life: 1, c: colors[i % colors.length] });
  }
  let frame = 0;
  (function anim() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    parts.forEach((p) => {
      p.x += p.vx; p.y += p.vy; p.vy += 0.13; p.life -= 0.024;
      ctx.globalAlpha = Math.max(0, p.life);
      ctx.fillStyle = p.c;
      ctx.beginPath(); ctx.arc(p.x, p.y, 3, 0, Math.PI * 2); ctx.fill();
    });
    ctx.globalAlpha = 1;
    if (++frame < 48) requestAnimationFrame(anim);
    else ctx.clearRect(0, 0, canvas.width, canvas.height);
  })();
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
    lastEvents = d.events || [];
    renderFeed(lastEvents);
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
document.getElementById("replayBtn").addEventListener("click", replayFeed);
document.getElementById("liveToggle").addEventListener("change", (e) => {
  document.getElementById("liveDot").classList.toggle("off", !e.target.checked);
});
syncAutoRefresh();
loadPending();
load();
