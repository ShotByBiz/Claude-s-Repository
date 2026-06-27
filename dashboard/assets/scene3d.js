"use strict";
/* Real WebGL 3D "task universe" using vendored Three.js (global THREE).
   A glowing core (the monitor) with completed-task nodes orbiting it,
   colored by work area, over a depth starfield. Pointer-drag to orbit,
   slow auto-rotation otherwise. Degrades gracefully if WebGL is absent. */

(function () {
  const AREA_COLORS = {
    monitoring: 0x58a6ff, optimization: 0x3fb950, reporting: 0xd29922,
    integration: 0xbc8cff, delivery: 0xf778ba,
  };

  let renderer, scene, camera, core, coreWire, group, starField;
  let nodes = [];
  let raf = null, started = false;
  let dragging = false, lastX = 0, lastY = 0, yaw = 0, pitch = 0.3, autoYaw = 0;
  let focusIdx = 0, focusTimer = 0;

  function haloTexture() {
    const c = document.createElement("canvas");
    c.width = c.height = 64;
    const ctx = c.getContext("2d");
    const g = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    g.addColorStop(0, "rgba(255,255,255,0.9)");
    g.addColorStop(0.3, "rgba(255,255,255,0.4)");
    g.addColorStop(1, "rgba(255,255,255,0)");
    ctx.fillStyle = g; ctx.fillRect(0, 0, 64, 64);
    return new THREE.CanvasTexture(c);
  }
  let HALO = null;

  function makeStars() {
    const n = 700;
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      const r = 40 + Math.random() * 80;
      const th = Math.random() * Math.PI * 2;
      const ph = Math.acos(2 * Math.random() - 1);
      pos[i * 3] = r * Math.sin(ph) * Math.cos(th);
      pos[i * 3 + 1] = r * Math.sin(ph) * Math.sin(th);
      pos[i * 3 + 2] = r * Math.cos(ph);
    }
    geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const mat = new THREE.PointsMaterial({ color: 0x8b97a7, size: 0.5, transparent: true, opacity: 0.7 });
    return new THREE.Points(geo, mat);
  }

  function clearNodes() {
    nodes.forEach((nd) => { group.remove(nd.mesh); group.remove(nd.halo); });
    nodes = [];
  }

  function buildNodes(events) {
    clearNodes();
    const list = (events || []).slice(0, 14);
    list.forEach((ev, i) => {
      const color = AREA_COLORS[ev.area] || 0x58a6ff;
      const geo = new THREE.SphereGeometry(0.5 + Math.min(1, (ev.files || 1) / 8) * 0.5, 24, 24);
      const mat = new THREE.MeshStandardMaterial({
        color, emissive: color, emissiveIntensity: 0.6, roughness: 0.4, metalness: 0.3,
      });
      const mesh = new THREE.Mesh(geo, mat);
      const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: HALO, color, transparent: true, opacity: 0.55, depthWrite: false }));
      halo.scale.setScalar(2.2);
      const nd = {
        mesh, halo, title: ev.title, area: ev.area,
        radius: 6 + (i % 4) * 2.2,
        speed: 0.15 + Math.random() * 0.2,
        phase: Math.random() * Math.PI * 2,
        incl: (Math.random() - 0.5) * 0.8,
        pulse: 0,
      };
      group.add(mesh); group.add(halo);
      nodes.push(nd);
    });
  }

  let theCanvas = null;
  function onResize(canvas) {
    canvas = canvas || theCanvas;
    if (!canvas) return;
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;            // panel still hidden -> skip until visible
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }

  function animate(canvas, label) {
    const t = performance.now() / 1000;
    if (!dragging) autoYaw += 0.0016;
    group.rotation.y = yaw + autoYaw;
    group.rotation.x = pitch;

    if (core) { core.rotation.y += 0.004; core.rotation.x += 0.002; }
    if (coreWire) { coreWire.rotation.y -= 0.003; }

    nodes.forEach((nd) => {
      const a = nd.phase + t * nd.speed;
      const x = Math.cos(a) * nd.radius;
      const z = Math.sin(a) * nd.radius;
      const y = Math.sin(a * 0.8) * nd.radius * nd.incl;
      nd.mesh.position.set(x, y, z);
      nd.halo.position.set(x, y, z);
      if (nd.pulse > 0) {
        nd.pulse -= 0.02;
        const s = 1 + nd.pulse * 1.4;
        nd.mesh.scale.setScalar(s);
        nd.halo.scale.setScalar(2.2 + nd.pulse * 3);
        nd.mesh.material.emissiveIntensity = 0.6 + nd.pulse;
      } else {
        nd.mesh.scale.setScalar(1);
        nd.halo.scale.setScalar(2.2);
        nd.mesh.material.emissiveIntensity = 0.6;
      }
    });

    // cycle a focused node and surface its title
    focusTimer += 1;
    if (label && nodes.length && focusTimer > 150) {
      focusTimer = 0;
      focusIdx = (focusIdx + 1) % nodes.length;
      label.textContent = "◉ " + nodes[focusIdx].area + " — " + nodes[focusIdx].title;
    }

    renderer.render(scene, camera);
    raf = requestAnimationFrame(() => animate(canvas, label));
  }

  function initScene3d(data) {
    if (started) { buildNodes(data && data.events); return true; }
    const canvas = document.getElementById("scene3d");
    const label = document.getElementById("scene3dLabel");
    if (!canvas || typeof THREE === "undefined") return false;
    theCanvas = canvas;

    try {
      renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    } catch (e) { return false; }
    if (!renderer.getContext()) return false;

    renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
    HALO = haloTexture();

    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0f1419, 0.012);
    camera = new THREE.PerspectiveCamera(55, 16 / 9, 0.1, 400);
    camera.position.set(0, 4, 26);

    group = new THREE.Group();
    scene.add(group);

    // core
    const coreGeo = new THREE.IcosahedronGeometry(3, 1);
    core = new THREE.Mesh(coreGeo, new THREE.MeshStandardMaterial({
      color: 0x102236, emissive: 0x1f6feb, emissiveIntensity: 0.5, roughness: 0.3, metalness: 0.6,
    }));
    group.add(core);
    coreWire = new THREE.LineSegments(
      new THREE.WireframeGeometry(new THREE.IcosahedronGeometry(3.4, 1)),
      new THREE.LineBasicMaterial({ color: 0x58a6ff, transparent: true, opacity: 0.35 })
    );
    group.add(coreWire);

    scene.add(new THREE.AmbientLight(0x404a5a, 1.0));
    const p1 = new THREE.PointLight(0x58a6ff, 1.2, 200); p1.position.set(20, 20, 20); scene.add(p1);
    const p2 = new THREE.PointLight(0xbc8cff, 0.8, 200); p2.position.set(-20, -10, -10); scene.add(p2);

    starField = makeStars();
    scene.add(starField);

    buildNodes(data && data.events);

    // pointer-drag orbit
    canvas.addEventListener("pointerdown", (e) => { dragging = true; lastX = e.clientX; lastY = e.clientY; });
    window.addEventListener("pointerup", () => { dragging = false; });
    window.addEventListener("pointermove", (e) => {
      if (!dragging) return;
      yaw += (e.clientX - lastX) * 0.005;
      pitch += (e.clientY - lastY) * 0.005;
      pitch = Math.max(-1.2, Math.min(1.2, pitch));
      lastX = e.clientX; lastY = e.clientY;
    });

    const resize = () => onResize(canvas);
    window.addEventListener("resize", resize);
    resize();

    if (label && nodes.length) {
      label.textContent = "◉ " + nodes[0].area + " — " + nodes[0].title;
    }
    started = true;
    animate(canvas, label);
    return true;
  }

  function pulseScene3d() {
    nodes.forEach((nd, i) => { setTimeout(() => { nd.pulse = 1; }, i * 90); });
  }

  window.initScene3d = initScene3d;
  window.pulseScene3d = pulseScene3d;
  window.resizeScene3d = function () { onResize(theCanvas); };
})();
