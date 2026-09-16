let LANG = (localStorage.getItem("lang") || (navigator.language || "en")).slice(0, 2);
if (LANG !== "es") LANG = "en";
let STEP_TIMER = null;

function t(key) {
  return (window.I18N[LANG] && window.I18N[LANG][key]) || key;
}

function applyI18n() {
  document.documentElement.lang = LANG;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = t(el.getAttribute("data-i18n"));
  });
  document.querySelectorAll("[data-i18n-ph]").forEach((el) => {
    el.setAttribute("placeholder", t(el.getAttribute("data-i18n-ph")));
  });
  document.getElementById("lang-en").classList.toggle("active", LANG === "en");
  document.getElementById("lang-es").classList.toggle("active", LANG === "es");
}

async function loadVerticals() {
  const sel = document.getElementById("vertical");
  const current = sel.value;
  try {
    const res = await fetch(`/api/config?lang=${LANG}`);
    const cfg = await res.json();
    sel.innerHTML =
      `<option value="" disabled selected>${t("f_vertical_ph")}</option>` +
      cfg.verticals.map((v) => `<option value="${v.id}">${v.label}</option>`).join("");
    if (current) sel.value = current;
    // default offline toggle to whatever the server reports (no creds -> offline)
    if (cfg.offline_default) document.getElementById("offline").checked = true;
  } catch (e) {
    /* noop */
  }
}

function setLang(lang) {
  LANG = lang;
  localStorage.setItem("lang", lang);
  applyI18n();
  loadVerticals();
  refreshSiteTypeLabels();
}

// Detailed sites
const SITE_KINDS = ["campus", "planta", "datacenter", "sucursal"];

function siteTypeOptions(selected) {
  const labels = window.I18N[LANG].site_types || {};
  return SITE_KINDS.map(
    (k) => `<option value="${k}"${k === selected ? " selected" : ""}>${labels[k] || k}</option>`
  ).join("");
}

function addSiteRow(data) {
  data = data || {};
  const row = document.createElement("div");
  row.className = "site-row";
  row.innerHTML = `
    <input type="text" class="s-name" placeholder="${t("site_name_ph")}" value="${data.name || ""}" />
    <select class="s-kind">${siteTypeOptions(data.kind || "campus")}</select>
    <input type="number" min="0" class="s-users" placeholder="${t("site_users_ph")}" value="${data.users ?? ""}" />
    <button type="button" class="rm" title="remove">×</button>`;
  row.querySelector(".rm").addEventListener("click", () => row.remove());
  document.getElementById("sitesList").appendChild(row);
}

function collectSites() {
  return Array.from(document.querySelectorAll("#sitesList .site-row"))
    .map((r) => {
      const name = r.querySelector(".s-name").value.trim();
      const kind = r.querySelector(".s-kind").value;
      const usersRaw = r.querySelector(".s-users").value;
      const site = { name: name || "Sede", kind };
      if (usersRaw !== "") site.users = parseInt(usersRaw, 10) || 0;
      return { site, hasData: !!name || usersRaw !== "" };
    })
    .filter((x) => x.hasData)
    .map((x) => x.site);
}

function refreshSiteTypeLabels() {
  document.querySelectorAll("#sitesList .s-kind").forEach((sel) => {
    const cur = sel.value;
    sel.innerHTML = siteTypeOptions(cur);
  });
}

// Dropzone
function initDropzone() {
  const dz = document.getElementById("dropzone");
  const input = document.getElementById("install_base");
  const nameEl = document.getElementById("fileName");
  const show = () => {
    if (input.files && input.files.length) {
      nameEl.textContent = "📄 " + input.files[0].name;
      nameEl.hidden = false;
    }
  };
  dz.addEventListener("click", () => input.click());
  input.addEventListener("change", show);
  ["dragover", "dragenter"].forEach((ev) =>
    dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.add("drag"); })
  );
  ["dragleave", "drop"].forEach((ev) =>
    dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.remove("drag"); })
  );
  dz.addEventListener("drop", (e) => {
    if (e.dataTransfer.files.length) { input.files = e.dataTransfer.files; show(); }
  });
}

function startSteps() {
  const steps = t("steps");
  const el = document.getElementById("loadingStep");
  let i = 0;
  el.textContent = steps[0];
  STEP_TIMER = setInterval(() => {
    i = Math.min(i + 1, steps.length - 1);
    el.textContent = steps[i];
  }, 4500);
}
function stopSteps() { if (STEP_TIMER) clearInterval(STEP_TIMER); STEP_TIMER = null; }

function renderResult(data) {
  const m = data.metrics || {};
  const cov = Math.round((m.evidence_coverage || 0) * 100);
  const chips = (data.specialists || [])
    .map((s) => `<span class="chip">${s.replace(/_/g, " ")}</span>`).join("");
  const pdf = data.pdf_file ? `<a class="primary" href="/files/${data.pdf_file}" target="_blank">⬇ ${t("open_pdf")}</a>` : "";
  const pptx = data.pptx_file ? `<a href="/files/${data.pptx_file}">⬇ ${t("open_pptx")}</a>` : "";
  const docx = data.docx_file ? `<a href="/files/${data.docx_file}">⬇ ${t("open_docx")}</a>` : "";
  const html = data.html_file ? `<a href="/files/${data.html_file}" target="_blank">↗ ${t("open_html")}</a>` : "";
  const note = data.install_base_note ? `<div class="note">⚠ ${data.install_base_note}</div>` : "";
  document.getElementById("resultsBody").innerHTML = `
    <div class="metrics">
      <div class="metric"><div class="n">${m.n_findings ?? "-"}</div><div class="l">${t("m_arch")}</div></div>
      <div class="metric"><div class="n">${m.bom_lines ?? "-"}</div><div class="l">${t("m_bom")}</div></div>
      <div class="metric"><div class="n">${cov}%</div><div class="l">${t("m_evi")}</div></div>
      <div class="metric"><div class="n">${m.duration_s ?? "-"}</div><div class="l">${t("m_time")}</div></div>
    </div>
    <div class="l" style="font-size:11px;color:#5b6b7a;text-transform:uppercase;margin-bottom:6px">${t("specialists")}</div>
    <div class="chips">${chips}</div>
    <div class="actions">${pdf}${pptx}${docx}${html}</div>
    ${data.html_file ? `<iframe class="preview" src="/files/${data.html_file}"></iframe>` : ""}
    ${note}
  `;
}

async function submitForm(e) {
  e.preventDefault();
  const form = document.getElementById("oppForm");
  const errEl = document.getElementById("formErr");
  errEl.hidden = true;
  const btn = document.getElementById("submitBtn");

  const fd = new FormData(form);
  fd.set("lang", LANG);
  fd.set("offline", document.getElementById("offline").checked ? "true" : "false");
  const clouds = Array.from(document.querySelectorAll("#cloudChecks input:checked"))
    .map((c) => c.value);
  fd.set("cloud_providers", clouds.join(", "));
  fd.set("sites_json", JSON.stringify(collectSites()));

  document.getElementById("overlay").hidden = false;
  startSteps();
  btn.disabled = true;
  try {
    const res = await fetch("/api/proposal", { method: "POST", body: fd });
    const data = await res.json();
    if (!res.ok || !data.ok) throw new Error(data.error || t("err_generic"));
    renderResult(data);
  } catch (err) {
    errEl.textContent = "⚠ " + (err.message || t("err_generic"));
    errEl.hidden = false;
  } finally {
    stopSteps();
    document.getElementById("overlay").hidden = true;
    btn.disabled = false;
  }
}

window.setLang = setLang;
document.addEventListener("DOMContentLoaded", () => {
  applyI18n();
  loadVerticals();
  initDropzone();
  document.getElementById("addSite").addEventListener("click", () => addSiteRow());
  document.getElementById("oppForm").addEventListener("submit", submitForm);
});
