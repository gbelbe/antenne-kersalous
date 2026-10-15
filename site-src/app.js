/* Application du site : routage par ancre (#/...), données lues dans data/*.json. Aucune dépendance sauf Leaflet. */
"use strict";

const $ = (s, r = document) => r.querySelector(s);
const cache = {};
const load = (n) => (cache[n] ||= fetch(`data/${n}.json`).then((r) => { if (!r.ok) throw new Error(n); return r.json(); }));
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const md = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/`([^`]+)`/g, "<code>$1</code>")
  .replace(/\n{2,}/g, "</p><p>").replace(/^/, "<p>").replace(/$/, "</p>");
const fmtDate = (d) => (d ? new Date(d + "T12:00:00").toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" }) : "");
const TODAY = new Date(new Date().toISOString().slice(0, 10) + "T12:00:00");
const daysTo = (d) => Math.round((new Date(d + "T12:00:00") - TODAY) / 86400000);
const rel = (n) => (n === 0 ? "aujourd'hui" : n > 0 ? `dans ${n} jour${n > 1 ? "s" : ""}` : `il y a ${-n} jour${n < -1 ? "s" : ""}`);
const link = (r) => `<a href="#/e/${encodeURIComponent(r.id)}">${esc(r.label)}</a>`;
const links = (a) => (a && a.length ? a.map(link).join(", ") : "");
const chip = (t, k = "") => `<span class="chip ${k}">${esc(t)}</span>`;
const forceChip = (m) => chip(m.force || "—", { "skt:force-forte": "ok", "skt:force-moyenne": "info", "skt:force-a-verifier": "warn", "skt:force-faible": "bad", "skt:force-ecarte": "bad" }[m.force_id] || "");
const gm = (ll) => `https://www.google.com/maps/search/?api=1&query=${ll[0]},${ll[1]}`;
const gsv = (ll) => `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${ll[0]},${ll[1]}`;

const ROUTES = {
  "": home, carte, chronologie, dossier, jurisprudence, reseau, sources, explorer,
};

async function router() {
  const h = decodeURIComponent(location.hash.replace(/^#\/?/, ""));
  const [name, ...rest] = h.split("/");
  document.querySelectorAll("nav a").forEach((a) => a.classList.toggle("on", a.dataset.r === name));
  $("#nav").classList.remove("open");
  const app = $("#app");
  try {
    if (name === "e") await entity(rest.join("/"));
    else if (name === "recherche") await recherche(rest.join("/"));
    else await (ROUTES[name] || home)();
  } catch (e) {
    app.innerHTML = `<h1>Oups</h1><p>Impossible de charger cette page : ${esc(e.message)}.</p>`;
    console.error(e);
  }
  window.scrollTo(0, 0);
}

/* ───────────────────────── Accueil ───────────────────────── */
async function home() {
  const [meta, tl, ents, dos] = await Promise.all([load("meta"), load("timeline"), load("entities"), load("dossier")]);
  const up = tl.filter((i) => i.date >= TODAY.toISOString().slice(0, 10) && ["Délais", "Actions", "Procédure"].includes(i.cat)).slice(0, 6);
  const p = ents["dos:projet-pylone"];
  const keys = ["dos:m-hauteur-sommitale", "dos:m-massif-beton", "dos:m-dalle-technique", "dos:m-position-operateur"];
  const meas = dos.mesures.filter((m) => keys.includes(m.id));
  const s = meta.stats;
  $("#app").innerHTML = `
    <h1>${esc(meta.title)}</h1>
    <p class="lead">${esc(meta.subtitle)}. Une antenne-relais de 30 m (32,65 m avec ses équipements) est projetée sur la parcelle YX 26, à proximité d'habitations.
      Ce site rassemble les faits, les délais, les précédents de justice et les données sur les propriétaires de pylônes, avec leurs sources.</p>
    <div class="banner">${esc(meta.disclaimer)}</div>
    <div class="grid">
      <div class="card"><div class="stat">${s.supports}<small>supports d'antennes cartographiés</small></div></div>
      <div class="card"><div class="stat">${s.phoenix_supports}<small>supports de Phoenix en Bretagne</small></div></div>
      <div class="card"><div class="stat">${s.decisions}<small>décisions de justice comparées</small></div></div>
      <div class="card"><div class="stat">${s.sources}<small>sources documentées</small></div></div>
    </div>
    <h2>Par où commencer</h2>
    <div class="grid">
      <a class="card" href="#/carte"><h3>🗺️ Carte</h3><p class="muted">Le site projeté, les antennes existantes, les pylônes de Phoenix, la couverture 4G. Vues OpenStreetMap, orthophoto IGN et Google Maps.</p></a>
      <a class="card" href="#/chronologie"><h3>🕒 Chronologie</h3><p class="muted">Dépôt, décision, panneau, délais de recours, travaux prévus : ce qui est passé et ce qui arrive.</p></a>
      <a class="card" href="#/dossier"><h3>⚖️ Moyens &amp; actions</h3><p class="muted">Les arguments juridiques, leur force estimée, leurs preuves et ce qu'il reste à faire.</p></a>
      <a class="card" href="#/jurisprudence"><h3>📚 Jurisprudence</h3><p class="muted">Ce qui a fonctionné, retardé ou échoué dans d'autres affaires d'antennes-relais.</p></a>
      <a class="card" href="#/reseau"><h3>🏗️ Pylônes &amp; propriétaires</h3><p class="muted">Qui possède les pylônes en Bretagne et en France ; Phoenix et ses opérations.</p></a>
      <a class="card" href="#/sources"><h3>🔎 Sources</h3><p class="muted">D'où vient chaque information et à quel point s'y fier. Téléchargements.</p></a>
    </div>
    ${up.length ? `<h2>À venir</h2><div class="tl">${up.map((i) => tlItem(i)).join("")}</div><p><a href="#/chronologie">Toute la chronologie →</a></p>` : ""}
    ${meas.length ? `<h2>Le projet en chiffres</h2><div class="grid">${meas.map((m) => `<a class="card" href="#/e/${encodeURIComponent(m.id)}"><div class="stat">${esc(m.value)} <span class="muted" style="font-size:1rem">${esc(m.unit)}</span><small>${esc(m.label)}</small></div></a>`).join("")}</div>` : ""}
    ${p ? `<h2>Résumé</h2><div class="card md">${md(p.note || "")}</div>` : ""}`;
}

/* ───────────────────────── Carte ───────────────────────── */
let LMAP = null;
async function carte() {
  const [meta, data, cover] = await Promise.all([load("meta"), load("map"), load("coverage")]);
  const c = data.center;
  $("#app").innerHTML = `
    <h1>Carte</h1>
    <div class="toolbar">
      <button class="chip sel" data-eng="leaflet">Carte interactive</button>
      <button class="chip" data-eng="google">Google Maps (satellite)</button>
      <a class="chip info" href="${gm(c)}" target="_blank" rel="noopener">Ouvrir dans Google Maps ↗</a>
      <a class="chip info" href="${gsv(c)}" target="_blank" rel="noopener">Street View ↗</a>
    </div>
    <div id="mapzone"></div>
    <div class="legend" id="legend"></div>
    <p class="muted small">Positions des supports arrondies par l'ANFR (≈ 30 m). Le point rouge est le centre de la parcelle ; l'opérateur place le pylône à son angle, côté route, à environ 64 m de là. Propriétaire d'un support = code du registre ANFR (fichier du 8 octobre 2026), à lire comme un plancher pour Phoenix.</p>`;
  const show = (eng) => {
    document.querySelectorAll("[data-eng]").forEach((b) => b.classList.toggle("sel", b.dataset.eng === eng));
    if (LMAP) { LMAP.remove(); LMAP = null; }
    if (eng === "google") {
      const src = meta.google_maps_key
        ? `https://www.google.com/maps/embed/v1/view?key=${encodeURIComponent(meta.google_maps_key)}&center=${c[0]},${c[1]}&zoom=17&maptype=satellite`
        : `https://maps.google.com/maps?q=${c[0]},${c[1]}&t=k&z=17&output=embed`;
      $("#mapzone").innerHTML = `<iframe class="gframe" src="${esc(src)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Google Maps"></iframe>
        <p class="muted small">${meta.google_maps_key ? "Google Maps Embed API." : "Intégration Google Maps sans clé (vue du site seulement ; pour y superposer les antennes, utilisez la carte interactive)."}</p>`;
      $("#legend").innerHTML = "";
    } else {
      $("#mapzone").innerHTML = `<div id="map" role="application" aria-label="Carte interactive"></div>`;
      drawMap(data, cover);
    }
  };
  document.querySelectorAll("[data-eng]").forEach((b) => (b.onclick = () => show(b.dataset.eng)));
  show("leaflet");
}

function drawMap(data, cover) {
  const c = data.center;
  const osm = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19, attribution: "© OpenStreetMap" });
  const ign = L.tileLayer("https://data.geopf.fr/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&STYLE=normal&FORMAT=image%2Fjpeg&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}", { maxZoom: 19, attribution: "© IGN" });
  LMAP = L.map("map", { layers: [osm] }).setView(c, 13);
  const colors = { projet: "#d92d20", phoenix: "#e8710a", support: "#6b7a90", bouygues: "#1570ef" };
  const groups = { projet: L.layerGroup(), phoenix: L.layerGroup(), bouygues: L.layerGroup(), support: L.layerGroup(), autres: L.layerGroup(), rings: L.layerGroup() };
  const popup = (f) => {
    const ll = f.geom.ll;
    const rows = [f.owner && `<b>Propriétaire :</b> ${esc(f.owner)}`, f.operators?.length && `<b>Opérateurs :</b> ${esc(f.operators.join(", "))}`,
      f.status && `<b>Statut :</b> ${esc(f.status)}`, f.height && `<b>Hauteur :</b> ${esc(f.height)} m`, f.anfr && `<b>Support ANFR :</b> ${esc(f.anfr)}`].filter(Boolean);
    return `<strong>${esc(f.label)}</strong><br>${rows.join("<br>")}<br><a href="#/e/${encodeURIComponent(f.id)}">Fiche</a> · <a target="_blank" rel="noopener" href="${gm(ll)}">Google Maps</a> · <a target="_blank" rel="noopener" href="${gsv(ll)}">Street View</a>`;
  };
  for (const f of data.features) {
    if (f.geom.type === "Point") {
      const kind = f.kind === "projet" ? "projet" : f.kind === "phoenix" ? "phoenix" : (f.operators || []).includes("Bouygues Telecom") ? "bouygues" : "support";
      const m = L.circleMarker(f.geom.ll, { radius: kind === "projet" ? 10 : kind === "support" ? 5 : 6, color: "#fff", weight: 1.5, fillColor: colors[kind], fillOpacity: 0.95 }).bindPopup(popup(f));
      groups[kind].addLayer(m);
    } else {
      const poly = L.polygon(f.geom.rings, { color: "#7a5af8", weight: 2, fillOpacity: 0.12 }).bindPopup(`<strong>${esc(f.label)}</strong><br><a href="#/e/${encodeURIComponent(f.id)}">Fiche</a>`);
      groups.autres.addLayer(poly);
    }
  }
  [100, 500, 1000, 2000].forEach((r) => groups.rings.addLayer(L.circle(c, { radius: r, color: "#d92d20", weight: 1, fill: false, dashArray: "4 4" }).bindTooltip(`${r} m`, { permanent: false })));
  const covLayers = {};
  const covColor = { "Très bonne couverture": "#12b76a", "Bonne couverture": "#f79009", "Couverture limitée": "#f04438" };
  for (const z of cover) {
    covLayers[z.label] ||= L.layerGroup();
    L.polygon(z.geom.rings, { color: covColor[z.label.split(" — ")[0]] || "#667085", weight: 1, fillOpacity: 0.12, interactive: false }).addTo(covLayers[z.label]);
  }
  const overlays = {
    "Site projeté": groups.projet, "Supports de Phoenix": groups.phoenix, "Autres supports hébergeant Bouygues": groups.bouygues,
    "Autres supports": groups.support, "Parcelles et zones": groups.autres, "Cercles 100 m · 500 m · 1 km · 2 km": groups.rings, ...covLayers,
  };
  L.control.layers({ "OpenStreetMap": osm, "Orthophoto IGN": ign }, overlays, { collapsed: false }).addTo(LMAP);
  ["projet", "phoenix", "bouygues", "support", "autres"].forEach((k) => groups[k].addTo(LMAP));
  groups.projet.eachLayer((l) => l.openPopup());
  LMAP.setView(c, 14);
  $("#legend").innerHTML = [["projet", "Site projeté"], ["phoenix", "Supports de Phoenix"], ["bouygues", "Hébergent Bouygues Telecom"], ["support", "Autres supports"]]
    .map(([k, t]) => `<span><i class="dot" style="background:${colors[k]}"></i>${t}</span>`).join("");
}

/* ───────────────────────── Chronologie ───────────────────────── */
function tlItem(i) {
  const d = daysTo(i.date);
  const cls = d < 0 ? "past" : d <= 14 ? "soon" : "";
  const start = i.start ? ` <span class="muted small">(depuis le ${fmtDate(i.start)})</span>` : "";
  return `<div class="it ${cls}"><div><span class="when">${fmtDate(i.date)}</span><span class="cnt">${rel(d)}</span> ${chip(i.cat)}${i.status ? chip(i.status, i.status === "À faire" ? "warn" : "") : ""}${i.sites ? chip(i.sites + " sites", "info") : ""}</div>
    <div><a href="#/e/${encodeURIComponent(i.id)}">${esc(i.title)}</a>${start}</div></div>`;
}
async function chronologie() {
  const tl = await load("timeline");
  const cats = [...new Set(tl.map((i) => i.cat))];
  const on = new Set(["Procédure", "Délais", "Actions"]);
  const draw = () => {
    const items = tl.filter((i) => on.has(i.cat));
    const todayIso = TODAY.toISOString().slice(0, 10);
    const future = items.filter((i) => i.date >= todayIso), past = items.filter((i) => i.date < todayIso).reverse();
    $("#tl").innerHTML = `<h2>À venir (${future.length})</h2><div class="tl">${future.map(tlItem).join("") || '<p class="muted">Rien à venir pour ces catégories.</p>'}</div>
      <div class="today">Aujourd'hui — ${fmtDate(todayIso)}</div><h2>Passé (${past.length})</h2><div class="tl">${past.map(tlItem).join("")}</div>`;
    document.querySelectorAll("[data-cat]").forEach((b) => b.classList.toggle("sel", on.has(b.dataset.cat)));
  };
  $("#app").innerHTML = `<h1>Chronologie</h1>
    <p class="lead">Les dates du dossier. Les évènements du 14 octobre et du 29 septembre 2026 sont lus sur le panneau d'affichage ; les délais de recours donnés sont des échéances prudentes, à confirmer.</p>
    <div class="toolbar">${cats.map((c) => `<button class="chip" data-cat="${esc(c)}">${esc(c)}</button>`).join("")}</div><div id="tl"></div>`;
  document.querySelectorAll("[data-cat]").forEach((b) => (b.onclick = () => { on.has(b.dataset.cat) ? on.delete(b.dataset.cat) : on.add(b.dataset.cat); draw(); }));
  draw();
}

/* ───────────────────────── Moyens & actions ───────────────────────── */
async function dossier() {
  const d = await load("dossier");
  $("#app").innerHTML = `<h1>Moyens juridiques &amp; actions</h1>
    <p class="lead">Les arguments identifiés contre le projet, classés par force estimée, avec leurs preuves, les précédents qui les éclairent et les actions à mener. Une force « à vérifier » n'est pas une faiblesse : c'est qu'une pièce manque.</p>
    <h2>Moyens juridiques</h2>
    <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(320px,1fr))">${d.moyens.map((m) => `<div class="card">
      <div>${forceChip(m)}</div><h3><a href="#/e/${encodeURIComponent(m.id)}">${esc(m.label)}</a></h3>
      <div class="md small">${md((m.note || "").slice(0, 420) + ((m.note || "").length > 420 ? "…" : ""))}</div>
      ${m.fondements.length ? `<p class="small"><b>Fondement :</b> ${links(m.fondements)}</p>` : ""}
      ${m.preuves.length ? `<p class="small"><b>Preuves :</b> ${links(m.preuves)}</p>` : ""}
      ${m.jurisprudence.length ? `<p class="small"><b>Précédents :</b> ${links(m.jurisprudence)}</p>` : ""}
      ${m.actions.length ? `<p class="small"><b>Actions :</b> ${links(m.actions)}</p>` : ""}</div>`).join("")}</div>
    <h2>Délais</h2><div class="scroll"><table><tr><th>Délai</th><th>Début</th><th>Échéance</th></tr>
      ${d.delais.map((x) => `<tr><td><a href="#/e/${encodeURIComponent(x.id)}">${esc(x.label)}</a></td><td>${fmtDate(x.start) || "—"}</td><td>${fmtDate(x.end) || "—"} ${x.end ? `<span class="muted small">${rel(daysTo(x.end))}</span>` : ""}</td></tr>`).join("")}</table></div>
    <h2>Actions</h2><div class="scroll"><table><tr><th>Échéance</th><th>Action</th><th>Statut</th></tr>
      ${d.actions.map((a) => `<tr><td>${a.date ? fmtDate(a.date) : "—"}</td><td><a href="#/e/${encodeURIComponent(a.id)}">${esc(a.label)}</a></td><td>${chip(a.status || "—", a.status === "À faire" ? "warn" : "")}</td></tr>`).join("")}</table></div>`;
}

/* ───────────────────────── Jurisprudence ───────────────────────── */
async function jurisprudence() {
  const rows = await load("jurisprudence");
  let f = "all", q = "";
  const draw = () => {
    const list = rows.filter((r) => (f === "all" || (f === "fav" && r.favorable === true) || (f === "def" && r.favorable === false) || (f === "regle" && r.favorable === null)) &&
      (!q || (r.label + r.court + r.commune + r.operator + r.note).toLowerCase().includes(q)));
    $("#jl").innerHTML = list.map((r) => `<div class="card" style="margin:0 0 12px">
      <div>${r.favorable === true ? chip("A fonctionné pour les riverains", "ok") : r.favorable === false ? chip("A échoué pour les riverains", "bad") : chip("Précision de règle", "info")}
        ${chip(r.issue)} ${r.verified ? chip("vérifié sur le texte", "ok") : chip("non vérifié sur le texte", "warn")}</div>
      <h3 style="margin-top:6px"><a href="#/e/${encodeURIComponent(r.id)}">${esc(r.label)}</a></h3>
      <p class="small muted">${esc(r.court)}${r.date ? " · " + fmtDate(r.date) : ""}${r.ref ? " · " + esc(r.ref) : ""}${r.commune ? " · " + esc(r.commune) : ""}${r.operator ? " · " + esc(r.operator) : ""}</p>
      <details><summary>Détails</summary><div class="md small">${md(r.note)}</div>
      ${r.moyens.length ? `<p class="small"><b>Éclaire :</b> ${links(r.moyens)}</p>` : ""}${r.sources.length ? `<p class="small"><b>Sources :</b> ${links(r.sources)}</p>` : ""}</details></div>`).join("") || '<p class="muted">Aucune décision.</p>';
    document.querySelectorAll("[data-f]").forEach((b) => b.classList.toggle("sel", b.dataset.f === f));
  };
  const n = (x) => rows.filter(x).length;
  $("#app").innerHTML = `<h1>Jurisprudence comparée</h1>
    <p class="lead">Décisions rendues sur d'autres antennes-relais en France : ce qui a fait annuler, suspendre ou démonter, et ce qui a échoué. Aucune n'a été lue sur le texte original : ce sont des lectures de billets d'avocats ou de presse. <b>À vérifier avant toute citation.</b></p>
    <div class="toolbar"><button class="chip" data-f="all">Toutes (${rows.length})</button><button class="chip" data-f="fav">Ont fonctionné (${n((r) => r.favorable === true)})</button>
      <button class="chip" data-f="def">Ont échoué (${n((r) => r.favorable === false)})</button><button class="chip" data-f="regle">Règles (${n((r) => r.favorable === null)})</button>
      <input type="search" id="jq" placeholder="Filtrer…"></div><div id="jl"></div>`;
  document.querySelectorAll("[data-f]").forEach((b) => (b.onclick = () => { f = b.dataset.f; draw(); }));
  $("#jq").oninput = (e) => { q = e.target.value.toLowerCase(); draw(); };
  draw();
}

/* ───────────────────────── Pylônes & propriétaires ───────────────────────── */
async function reseau() {
  const [r, ents] = await Promise.all([load("reseau"), load("entities")]);
  let ensId = "dos:ens-finistere", mode = "all";
  const bars = (rows) => rows.map((o) => `<div class="row ${o.owner_id === "skt:prop-73" ? "ph" : ""}"><div>${link({ id: o.owner_id, label: o.owner })}</div><div class="bar"><i style="width:${Math.min(100, o.pct * 2.2)}%"></i></div><div>${o.pct.toFixed(1)} % <span class="muted small">(${o.n})</span></div></div>`).join("");
  const draw = () => {
    const e = r.ensembles.find((x) => x.id === ensId);
    const rows = mode === "all" ? e.owners : e.bouygues_owners;
    const tot = mode === "all" ? e.total : e.bouygues_total;
    $("#bars").innerHTML = `<h3>${esc(e.label)} — ${tot ?? "?"} supports${mode === "bouygues" ? " hébergeant Bouygues Telecom" : ""}</h3>
      <div class="bars">${bars(rows) || '<p class="muted">Pas de mesure détaillée pour cet ensemble (seul Phoenix est mesuré).</p>'}</div>`;
  };
  const lim = ents["src:act-proprietaires-anfr"]?.note || "";
  $("#app").innerHTML = `<h1>Pylônes &amp; propriétaires</h1>
    <p class="lead">Qui possède les supports d'antennes ? Les chiffres viennent du registre de l'ANFR (fichier du 8 octobre 2026). Phoenix France Infrastructures, demandeur de la déclaration préalable, est une société de pylônes liée à Bouygues Telecom ; la part mesurée est un <b>plancher</b>.</p>
    <div class="banner md">${md(lim)}</div>
    <div class="toolbar"><label>Territoire <select id="ens">${r.ensembles.map((e) => `<option value="${esc(e.id)}"${e.id === ensId ? " selected" : ""}>${esc(e.label)}</option>`).join("")}</select></label>
      <button class="chip sel" data-m="all">Tous les supports</button><button class="chip" data-m="bouygues">Seulement ceux qui hébergent Bouygues Telecom</button></div>
    <div id="bars"></div>
    <h2>Phoenix et ses opérations</h2>
    <div class="tl">${r.operations.map((o) => `<div class="it"><div><span class="when">${fmtDate(o.date)}</span> ${chip(o.sites.toLocaleString("fr-FR") + " sites", "info")}</div>
      <div><a href="#/e/${encodeURIComponent(o.id)}">${esc(o.label)}</a></div><div class="small muted">Acquéreur : ${esc(o.buyer)}${o.sellers.length ? " · Cédant(s) : " + esc(o.sellers.join(", ")) : ""}</div></div>`).join("")}</div>
    <h2>Sociétés de pylônes</h2><div class="scroll"><table><tr><th>Société</th><th>Code ANFR</th><th>Groupe</th></tr>
      ${r.societes.map((t) => `<tr><td><a href="#/e/${encodeURIComponent(t.id)}">${esc(t.label)}</a></td><td>${t.code ?? ""}</td><td>${esc(t.parent)}</td></tr>`).join("")}</table></div>`;
  $("#ens").onchange = (ev) => { ensId = ev.target.value; draw(); };
  document.querySelectorAll("[data-m]").forEach((b) => (b.onclick = () => { mode = b.dataset.m; document.querySelectorAll("[data-m]").forEach((x) => x.classList.toggle("sel", x === b)); draw(); }));
  draw();
}

/* ───────────────────────── Sources ───────────────────────── */
async function sources() {
  const [s, meta] = await Promise.all([load("sources"), load("meta")]);
  const lvl = (id) => (id === "src:primaire" ? "ok" : id === "src:assertion-modele" ? "bad" : "warn");
  $("#app").innerHTML = `<h1>Sources &amp; provenance</h1>
    <p class="lead">Chaque information du graphe renvoie à sa source, avec un niveau de preuve. Une source primaire lue est opposable ; un résumé de moteur de recherche est à revérifier.</p>
    <div class="grid">${s.levels.map((l) => `<div class="card"><h3>${chip(l.label, lvl(l.id))}</h3><div class="md small">${md(l.note)}</div></div>`).join("")}</div>
    <h2>Téléchargements</h2><ul>
      <li><a href="data/graphe-public.ttl" download>Graphe public complet (Turtle)</a></li>
      ${meta.published_files.map((f) => `<li><a href="files/${encodeURIComponent(f)}" download>${esc(f)}</a></li>`).join("")}
      <li><a href="${esc(meta.repo_url)}" target="_blank" rel="noopener">Dépôt GitHub ↗</a></li></ul>
    <h2>Sources documentées (${s.sources.length})</h2><div class="scroll"><table><tr><th>Source</th><th>Niveau</th><th>Millésime</th><th>Utilisée</th></tr>
    ${s.sources.map((x) => `<tr><td><a href="#/e/${encodeURIComponent(x.id)}">${esc(x.label)}</a>${x.url ? ` <a class="small" href="${esc(x.url)}" target="_blank" rel="noopener">↗</a>` : ""}</td>
      <td>${chip(x.level || "—", lvl(x.level_id))}</td><td class="small">${esc(x.date)}</td><td>${x.used}×</td></tr>`).join("")}</table></div>`;
}

/* ───────────────────────── Explorer ───────────────────────── */
async function explorer() {
  const ents = await load("entities");
  const byType = {};
  Object.values(ents).forEach((e) => (byType[e.types[0] || "Autre"] ||= []).push(e));
  const types = Object.keys(byType).sort((a, b) => byType[b].length - byType[a].length);
  $("#app").innerHTML = `<h1>Explorer le graphe</h1><p class="lead">${Object.keys(ents).length} entités. Choisissez un type, ou utilisez la recherche en haut de page.</p>
    <div class="toolbar">${types.map((t) => `<button class="chip" data-t="${esc(t)}">${esc(t)} (${byType[t].length})</button>`).join("")}</div><div id="el"></div>`;
  const show = (t) => {
    document.querySelectorAll("[data-t]").forEach((b) => b.classList.toggle("sel", b.dataset.t === t));
    $("#el").innerHTML = `<ul>${byType[t].sort((a, b) => a.label.localeCompare(b.label, "fr")).map((e) => `<li>${link(e)}</li>`).join("")}</ul>`;
  };
  document.querySelectorAll("[data-t]").forEach((b) => (b.onclick = () => show(b.dataset.t)));
  show(types[0]);
}

async function entity(id) {
  const ents = await load("entities");
  const e = ents[id];
  if (!e) { $("#app").innerHTML = `<h1>Introuvable</h1><p>Aucune entité « ${esc(id)} ».</p>`; return; }
  const ll = e.geom ? (await load("map")).features.find((f) => f.id === id)?.geom?.ll : null;
  const src = e.sources || [];
  $("#app").innerHTML = `<div class="crumb"><a href="#/explorer">Explorer</a> › ${esc(e.types.join(", ") || "entité")}</div>
    <h1>${esc(e.label)}</h1>
    ${e.types.map((t) => chip(t, "info")).join("")}
    ${ll ? `<p><a href="#/carte">Voir sur la carte</a> · <a href="${gm(ll)}" target="_blank" rel="noopener">Google Maps ↗</a> · <a href="${gsv(ll)}" target="_blank" rel="noopener">Street View ↗</a></p>` : ""}
    ${e.note ? `<div class="card md">${md(e.note)}</div>` : ""}
    ${e.props.length ? `<h2>Propriétés</h2><dl class="props">${e.props.map((p) => `<dt>${esc(p.p)}</dt><dd>${p.ref ? link(p.ref) : esc(p.v)}</dd>`).join("")}</dl>` : ""}
    ${src.length ? `<h2>Sources</h2><p>${links(src)}</p>` : ""}
    ${e.incoming?.length ? `<h2>Liée depuis</h2><ul>${e.incoming.map((i) => `<li>${link(i.ref)} <span class="muted small">— ${esc(i.p)}</span></li>`).join("")}</ul>` : ""}`;
}

async function recherche(q) {
  const ents = await load("entities");
  const t = q.toLowerCase().trim();
  const hits = t ? Object.values(ents).filter((e) => (e.label + " " + e.note).toLowerCase().includes(t)).slice(0, 120) : [];
  $("#app").innerHTML = `<h1>Recherche : « ${esc(q)} »</h1><p class="muted">${hits.length} résultat${hits.length > 1 ? "s" : ""}${hits.length === 120 ? " (limité aux 120 premiers)" : ""}.</p>
    <ul>${hits.map((e) => `<li>${link(e)} <span class="muted small">${esc(e.types.join(", "))}</span></li>`).join("")}</ul>`;
}

/* ───────────────────────── Démarrage ───────────────────────── */
(async () => {
  const meta = await load("meta").catch(() => null);
  if (meta) {
    document.title = meta.title;
    $("#brand-title").textContent = meta.title;
    $("#disclaimer").textContent = meta.disclaimer;
    const d = meta.commit_date ? new Date(meta.commit_date).toLocaleString("fr-FR") : "";
    $("#build").innerHTML = `Mis à jour le ${esc(d)} · version ${esc(meta.commit)} · ${meta.stats.triples.toLocaleString("fr-FR")} triplets · <a href="${esc(meta.repo_url)}" target="_blank" rel="noopener">code et données</a>`;
  }
  $("#menu-btn").onclick = () => { const o = $("#nav").classList.toggle("open"); $("#menu-btn").setAttribute("aria-expanded", o); };
  $("#search").onsubmit = (e) => { e.preventDefault(); location.hash = "#/recherche/" + encodeURIComponent($("#q").value); };
  window.addEventListener("hashchange", router);
  router();
})();
