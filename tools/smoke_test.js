// Test de fumée sans navigateur : exécute chaque vue de app.js avec un DOM minimal et les vrais fichiers JSON.
// Usage : node tools/smoke_test.js   (après python tools/build_site.py)
const fs = require("fs"), vm = require("vm"), path = require("path");
const site = path.join(__dirname, "..", "_site");
const nodeEl = () => new Proxy(function () {}, {
  get(t, k) {
    if (k === "innerHTML" || k === "textContent") return t[k] ?? "";
    if (k === "classList") return { toggle() {}, remove() {}, add() {} };
    if (k === "dataset") return {};
    if (k === "forEach") return () => {};
    return t[k] ?? (() => nodeEl());
  },
  set(t, k, v) { t[k] = v; return true; },
});
const app = nodeEl();
const deep = () => new Proxy(function () {}, { get: () => deep(), apply: () => deep(), construct: () => deep() });
const L = deep();
const ctx = {
  console, L, Promise, JSON, Math, Date, URL, Array, Object, String, Number, Set, Map, Error, encodeURIComponent, decodeURIComponent, setTimeout,
  location: { hash: "" },
  window: { addEventListener() {}, scrollTo() {} },
  document: { title: "", querySelector: (s) => (s === "#app" ? app : nodeEl()), querySelectorAll: () => ({ forEach() {} }) },
  fetch: async (u) => {
    const f = path.join(site, u);
    if (!fs.existsSync(f)) return { ok: false, json: async () => { throw new Error("404 " + u); } };
    return { ok: true, json: async () => JSON.parse(fs.readFileSync(f, "utf8")) };
  },
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(site, "app.js"), "utf8"), ctx);
(async () => {
  const ents = JSON.parse(fs.readFileSync(path.join(site, "data/entities.json"), "utf8"));
  const routes = ["", "carte", "chronologie", "dossier", "jurisprudence", "corpus", "corpus/skt:m-abords-mh-pc", "reseau", "sources", "explorer",
    "e/dos:projet-pylone", "e/dos:moyen-seuil-pc", "e/src:dim-bouygues", "e/dos:phoenix-france", "e/inexistant", "recherche/phoenix"];
  let bad = 0;
  for (const r of routes) {
    app.innerHTML = "";
    ctx.location.hash = "#/" + encodeURIComponent(r).replace(/%2F/g, "/");
    await vm.runInContext("router()", ctx);
    const html = app.innerHTML;
    const expectMissing = r === "e/inexistant";
    const ok = expectMissing ? html.includes("Introuvable") : html.length > 150 && !html.includes("Oups") && !html.includes("undefined") && !html.includes("[object");
    if (!ok) bad++;
    console.log((ok ? "ok  " : "FAIL"), r.padEnd(26), html.length, "octets");
  }
  // toutes les fiches d'entités doivent se rendre
  let n = 0;
  for (const id of Object.keys(ents)) {
    app.innerHTML = "";
    ctx.location.hash = "#/e/" + encodeURIComponent(id);
    await vm.runInContext("router()", ctx);
    if (app.innerHTML.includes("Oups") || app.innerHTML.includes("undefined")) { console.log("FAIL fiche", id); bad++; }
    n++;
  }
  console.log(n, "fiches d'entités rendues ;", bad ? bad + " échec(s)" : "aucun échec");
  process.exit(bad ? 1 : 0);
})();
