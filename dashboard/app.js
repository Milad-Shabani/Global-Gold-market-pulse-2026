// Global Gold Market Pulse — dashboard logic
(function () {
  const D = window.GOLD_DATA;
  const GOLD = "#b8860b", GOLD2 = "#d9a441", INK_SOFT = "#6b5b3a", GREEN = "#2e7d32", RED = "#c62828";
  const PALETTE = ["#b8860b", "#d9a441", "#8b6508", "#e8c874", "#a9987a", "#5a4004", "#c9a227", "#8f7a3c"];

  const fmt = (n, d = 1) => Number(n).toLocaleString(undefined, { minimumFractionDigits: d, maximumFractionDigits: d });
  const fmtPct = (n, d = 1) => (n * 100).toFixed(d) + "%";

  // ---------------- scroll-spy nav ----------------
  const navLinks = [...document.querySelectorAll("nav.tabs a")];
  const sections = navLinks.map(a => document.querySelector(a.getAttribute("href")));
  window.addEventListener("scroll", () => {
    let idx = 0;
    sections.forEach((s, i) => { if (s && s.getBoundingClientRect().top < 140) idx = i; });
    navLinks.forEach((a, i) => a.classList.toggle("active", i === idx));
  }, { passive: true });

  // ---------------- KPI band ----------------
  const top = D.reserves[0];
  const topBuyer3yr = D.topBuyers3yr[0];
  const kpis = [
    ["🪙", `${fmt(D.worldTotalReserves, 0)} t`, "World official gold reserves", "IMF IFS, Sep 2026"],
    ["🏅", `${fmt(top.tonnes, 0)} t`, `Largest single holder: ${top.country}`, `${fmtPct(top.pctWorld)} of world total · IMF IFS`],
    ["💰", `$${fmt(D.worldValueUsdBn, 0)}bn`, "World reserves' total value", `At $${fmt(D.valuePriceUsed,0)}/oz, 2025 avg price`],
    ["📈", "$3,432", "2025 avg gold price (USD/oz)", "+43.8% y/y · LBMA / metalcharts.org"],
    ["🏦", `${fmt(D.demandTotal2025, 0)} t`, "Record full-year 2025 demand", `$${fmt(D.demandValue2025UsdBn,0)}bn · WGC Gold Demand Trends`],
    ["⛏️", `${fmt(D.productionWorldTotal2025, 0)} t`, "2025 world mine production", "USGS MCS 2026"],
    ["🚀", `+${fmt(topBuyer3yr.tonnes,0)} t`, `Top 3-yr buyer: ${topBuyer3yr.country}`, "2023-2025 cumulative · IMF IFS"],
    ["🌍", `${fmt(D.regionalBreakdown[0].tonnes,0)} t`, `Largest region: ${D.regionalBreakdown[0].region}`, "Computed from IFS country data"],
    ["🏛️", `${fmtPct(D.concentration.top5Pct,1)}`, "Held by just the top 5 countries", "Reserve concentration · computed"],
  ];
  document.getElementById("kpi-band").innerHTML = kpis.map(([icon, val, lbl, src]) => `
    <div class="kpi"><div class="icon">${icon}</div><div class="val">${val}</div>
      <div class="lbl">${lbl}</div><div class="src">${src}</div></div>`).join("");

  document.getElementById("reserves-sub").textContent =
    `Official gold reserves by country, as of ${D.reservesAsOf}. World total across all IFS-reporting entities: ${fmt(D.worldTotalReserves,0)} tonnes.`;
  document.getElementById("buyers-sub").textContent =
    "Snapshot totals rank the usual suspects (US, Germany) at the top — but net annual change reveals a very different, much more dynamic story.";
  document.getElementById("production-sub").textContent =
    `USGS-estimated 2025 mine production. World total ${fmt(D.productionWorldTotal2025,0)}t vs ${fmt(D.productionWorldTotal2024,0)}t in 2024. Note: production ≠ reserves — Australia and the US mine heavily but hold comparatively modest official reserves relative to their output.`;
  document.getElementById("price-sub").textContent =
    `LBMA annual average, USD per troy ounce — the world benchmark gold price. 2025's $3,432 average was a +43.8% jump, and the year touched an intraday range of $${fmt(D.price2025Range.low,0)}-$${fmt(D.price2025Range.high,0)} — the sharpest annual move of the last 15 years.`;
  document.getElementById("demand-sub").textContent =
    `Full-year 2025 demand hit a record ${fmt(D.demandTotal2025,0)}t / $${fmt(D.demandValue2025UsdBn,0)}bn, driven by investment flows even as jewellery volumes fell.`;
  document.getElementById("forecast-sub").textContent =
    "A transparent trend-extrapolation model built from real 2015–2025 CAGRs — shown for planning-workflow illustration, not as a price call.";
  document.getElementById("regions-sub").textContent =
    `Europe still holds the largest bloc of official reserves (mainly legacy US/UK/France-era holdings and the euro-area countries), but ${D.regionalBreakdown[1] ? D.regionalBreakdown[1].region : "other regions"} and Asia-Pacific are growing fastest in relative terms thanks to China, India, Poland and the Gulf states.`;
  document.getElementById("value-sub").textContent =
    `Using the 2025 average LBMA price ($${fmt(D.valuePriceUsed,0)}/oz), the world's official gold reserves are worth roughly $${fmt(D.worldValueUsdBn,0)} billion. At 2025's intraday peak (~$${fmt(D.price2025Range.high,0)}/oz) that figure would be meaningfully higher — reserve value swings with the price even when tonnage doesn't move.`;
  document.getElementById("poland-note").textContent = D.polandNote;
  document.getElementById("cbga-sub").textContent =
    "Three successive agreements capped European central banks' coordinated gold sales at up to 400-500t/year. Sales collapsed from ~400t/year to under 10t/year by 2012 — the agreements were quietly left to lapse after 2019.";
  document.getElementById("forecast-note").textContent = D.forecastNote;
  document.getElementById("footer-note").textContent = D.generatedNote + "  ·  Dashboard generated " + new Date().toISOString().slice(0,10);

  // ---------------- reserve leaderboard table ----------------
  let sortKey = "rank", sortDir = 1;
  const maxTonnes = Math.max(...D.reserves.map(r => r.tonnes));
  function renderTable(filter = "") {
    const rows = D.reserves
      .filter(r => r.country.toLowerCase().includes(filter.toLowerCase()))
      .sort((a, b) => (a[sortKey] > b[sortKey] ? 1 : -1) * sortDir);
    document.querySelector("#reserve-table tbody").innerHTML = rows.map(r => `
      <tr>
        <td>${r.rank}</td>
        <td>${r.country}</td>
        <td>${fmt(r.tonnes)}</td>
        <td>${fmtPct(r.pctWorld, 2)}</td>
        <td>${fmtPct(r.pctFx)}</td>
        <td>${r.asOf}</td>
        <td><div class="bar-cell" style="width:${Math.max(4, (r.tonnes / maxTonnes) * 100)}%"></div></td>
      </tr>`).join("");
  }
  renderTable();
  document.getElementById("reserve-search").addEventListener("input", e => renderTable(e.target.value));
  document.querySelectorAll("#reserve-table th[data-key]").forEach(th => {
    th.addEventListener("click", () => {
      const key = th.dataset.key;
      sortDir = sortKey === key ? -sortDir : -1;
      sortKey = key;
      renderTable(document.getElementById("reserve-search").value);
    });
  });
  document.getElementById("export-csv").addEventListener("click", () => {
    const header = "Rank,Country,Tonnes,% of world,% of FX reserves,As of\n";
    const body = D.reserves.map(r => `${r.rank},${r.country},${r.tonnes},${fmtPct(r.pctWorld,2)},${fmtPct(r.pctFx)},${r.asOf}`).join("\n");
    const blob = new Blob([header + body], { type: "text/csv" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "gold_reserves_by_country.csv";
    a.click();
  });

  // ---------------- Chart.js defaults ----------------
  Chart.defaults.font.family = "Segoe UI, Inter, system-ui, sans-serif";
  Chart.defaults.color = INK_SOFT;
  Chart.defaults.borderColor = "#ece2c8";

  new Chart(document.getElementById("top10-chart"), {
    type: "bar",
    data: {
      labels: D.reserves.slice(0, 10).map(r => r.country),
      datasets: [{ data: D.reserves.slice(0, 10).map(r => r.tonnes), backgroundColor: GOLD, borderRadius: 4 }],
    },
    options: { indexAxis: "y", plugins: { legend: { display: false } },
      scales: { x: { title: { display: true, text: "Tonnes" } } } },
  });

  new Chart(document.getElementById("top10-share-chart"), {
    type: "bar",
    data: {
      labels: D.reserves.slice(0, 10).map(r => r.country),
      datasets: [{ data: D.reserves.slice(0, 10).map(r => r.pctWorld * 100), backgroundColor: GOLD2, borderRadius: 4 }],
    },
    options: { indexAxis: "y", plugins: { legend: { display: false },
      tooltip: { callbacks: { label: c => `${c.raw.toFixed(1)}% of world reserves` } } },
      scales: { x: { title: { display: true, text: "% of world reserves" } } } },
  });

  new Chart(document.getElementById("world-trend-chart"), {
    type: "line",
    data: {
      labels: D.worldReservesTrend.map(d => d.year),
      datasets: [{ label: "World reserves (t)", data: D.worldReservesTrend.map(d => d.tonnes),
        borderColor: GOLD, backgroundColor: "rgba(184,134,11,.12)", fill: true, tension: .25, pointRadius: 2 }],
    },
    options: { plugins: { legend: { display: false } }, scales: { y: { title: { display: true, text: "Tonnes" } } } },
  });

  const histColors = { "United States": "#8b6508", "Germany": "#b8860b", "China": "#c62828",
    "Russia": "#2e7d32", "India": "#1565c0", "Poland": "#6a1b9a", "Japan": "#a9987a", "Netherlands": "#d9a441",
    "United Kingdom": "#455a64", "Switzerland": "#e91e63", "Turkey": "#00838f", "Kazakhstan": "#f57f17" };
  const allYears = [...new Set(Object.values(D.countryHistory).flat().map(p => p.year))]
    .sort((a, b) => (a === "Q2 2026" ? 9999 : a) - (b === "Q2 2026" ? 9999 : b));
  new Chart(document.getElementById("country-history-chart"), {
    type: "line",
    data: {
      labels: allYears,
      datasets: Object.entries(D.countryHistory).map(([country, series]) => {
        const m = Object.fromEntries(series.map(p => [p.year, p.tonnes]));
        return { label: country, data: allYears.map(y => m[y] ?? null), spanGaps: true,
          borderColor: histColors[country] || GOLD, tension: .2, pointRadius: 1.5 };
      }),
    },
    options: { scales: { y: { title: { display: true, text: "Tonnes" } } } },
  });
  document.getElementById("history-notes").innerHTML = Object.entries(D.countryHistoryNotes).map(([country, note]) => `
    <div class="quote-card" style="border-left-color:${histColors[country] || GOLD}"><strong>${country}:</strong> ${note}</div>`).join("");

  new Chart(document.getElementById("cbga-annual-chart"), {
    type: "line",
    data: { labels: D.cbgaAnnualSales.map(d => d.year), datasets: [
      { label: "Reported sales (t)", data: D.cbgaAnnualSales.map(d => d.tonnes), borderColor: "#c62828",
        backgroundColor: "rgba(198,40,40,.1)", fill: true, tension: .2 },
    ] },
    options: { scales: { y: { title: { display: true, text: "Tonnes" } } } },
  });
  new Chart(document.getElementById("cbga-country-chart"), {
    type: "bar",
    data: { labels: D.cbgaCountryTotals.map(d => d.country), datasets: [{ data: D.cbgaCountryTotals.map(d => d.tonnes), backgroundColor: "#c62828", borderRadius: 4 }] },
    options: { indexAxis: "y", plugins: { legend: { display: false } }, scales: { x: { title: { display: true, text: "Tonnes sold, CBGA1 (1999-2004)" } } } },
  });

  new Chart(document.getElementById("allocation-chart"), {
    type: "bar",
    data: { labels: D.goldAllocationLeaders.slice(0, 15).map(d => d.country),
      datasets: [{ data: D.goldAllocationLeaders.slice(0, 15).map(d => d.pctFx * 100), backgroundColor: GOLD, borderRadius: 4 }] },
    options: { indexAxis: "y", plugins: { legend: { display: false },
      tooltip: { callbacks: { label: c => `${c.raw.toFixed(1)}% of FX reserves` } } },
      scales: { x: { title: { display: true, text: "% of FX reserves held in gold" }, max: 100 } } },
  });

  new Chart(document.getElementById("euroarea-chart"), {
    type: "bar",
    data: { labels: D.euroAreaComparison.map(d => d.label), datasets: [{ data: D.euroAreaComparison.map(d => d.tonnes),
      backgroundColor: D.euroAreaComparison.map((d,i) => i === 0 ? "#6a1b9a" : GOLD), borderRadius: 4 }] },
    options: { indexAxis: "y", plugins: { legend: { display: false } }, scales: { x: { title: { display: true, text: "Tonnes" } } } },
  });

  // ---------------- Country Explorer ----------------
  const explorerSelect = document.getElementById("explorer-select");
  explorerSelect.innerHTML = D.reserves.map(r => `<option value="${r.country}">${r.country}</option>`).join("");
  let explorerChart = null;
  function renderExplorer(country) {
    const r = D.reserves.find(x => x.country === country);
    if (!r) return;
    document.getElementById("explorer-detail").innerHTML = `
      <div class="kpi"><div class="icon">🏅</div><div class="val">#${r.rank}</div><div class="lbl">World rank</div><div class="src">of ${D.reserves.length} countries in dataset</div></div>
      <div class="kpi"><div class="icon">🪙</div><div class="val">${fmt(r.tonnes)} t</div><div class="lbl">Official reserves</div><div class="src">as of ${r.asOf}</div></div>
      <div class="kpi"><div class="icon">🌍</div><div class="val">${fmtPct(r.pctWorld, 2)}</div><div class="lbl">Share of world total</div><div class="src">${D.reservesAsOf}</div></div>
      <div class="kpi"><div class="icon">💱</div><div class="val">${fmtPct(r.pctFx)}</div><div class="lbl">% of FX reserves in gold</div><div class="src">IMF IFS</div></div>
      <div class="kpi"><div class="icon">🗺️</div><div class="val">${r.region}</div><div class="lbl">Region</div><div class="src">grouped for this analysis</div></div>`;
    const hist = D.countryHistory[country];
    const wrap = document.getElementById("explorer-chart-wrap");
    if (hist) {
      wrap.style.display = "block";
      if (explorerChart) explorerChart.destroy();
      explorerChart = new Chart(document.getElementById("explorer-chart"), {
        type: "line",
        data: { labels: hist.map(p => p.year), datasets: [{ label: `${country} reserves (t)`, data: hist.map(p => p.tonnes),
          borderColor: GOLD, backgroundColor: "rgba(184,134,11,.12)", fill: true, tension: .2 }] },
        options: { plugins: { legend: { display: false } }, scales: { y: { title: { display: true, text: "Tonnes" } } } },
      });
    } else {
      wrap.style.display = "none";
    }
  }
  explorerSelect.addEventListener("change", e => renderExplorer(e.target.value));
  renderExplorer(D.reserves[0].country);

  new Chart(document.getElementById("region-pie"), {
    type: "doughnut",
    data: { labels: D.regionalBreakdown.map(r => r.region), datasets: [{ data: D.regionalBreakdown.map(r => r.tonnes), backgroundColor: PALETTE }] },
    options: { plugins: { legend: { position: "bottom", labels: { boxWidth: 10 } },
      tooltip: { callbacks: { label: c => `${c.label}: ${fmt(c.raw,0)} t (${fmtPct(c.raw / D.reserves.reduce((s,r)=>s+r.tonnes,0))})` } } } },
  });

  new Chart(document.getElementById("institutional-chart"), {
    type: "bar",
    data: { labels: D.institutional.map(d => d.name), datasets: [{ data: D.institutional.map(d => d.tonnes), backgroundColor: "#a9987a", borderRadius: 4 }] },
    options: { indexAxis: "y", plugins: { legend: { display: false } }, scales: { x: { title: { display: true, text: "Tonnes" } } } },
  });

  new Chart(document.getElementById("momentum-chart"), {
    type: "bar",
    data: { labels: D.momentum.map(d => d.country), datasets: [{ data: D.momentum.map(d => d.pctChange * 100),
      backgroundColor: D.momentum.map(d => d.pctChange >= 0 ? GOLD : RED), borderRadius: 4 }] },
    options: { indexAxis: "y", plugins: { legend: { display: false },
      tooltip: { callbacks: { label: c => `${c.raw.toFixed(1)}%` } } },
      scales: { x: { title: { display: true, text: "% change over ~10 years" } } } },
  });
  document.querySelector("#momentum-table tbody").innerHTML = D.momentum.map(d => `
    <tr><td>${d.country}</td><td>${d.baseYear}</td><td>${fmt(d.baseTonnes)}</td><td>${d.latestYear}</td>
      <td>${fmt(d.latestTonnes)}</td><td><span class="badge ${d.pctChange>=0?'up':'down'}">${(d.pctChange*100).toFixed(1)}%</span></td></tr>`).join("");

  new Chart(document.getElementById("value-chart"), {
    type: "bar",
    data: { labels: D.reserveValues.slice(0, 12).map(d => d.country), datasets: [{ data: D.reserveValues.slice(0, 12).map(d => d.usdBn), backgroundColor: GOLD, borderRadius: 4 }] },
    options: { indexAxis: "y", plugins: { legend: { display: false },
      tooltip: { callbacks: { label: c => `$${fmt(c.raw,1)}bn` } } },
      scales: { x: { title: { display: true, text: "USD billions, at 2025 avg price" } } } },
  });

  new Chart(document.getElementById("buyers-3yr-chart"), {
    type: "bar",
    data: { labels: D.topBuyers3yr.map(d => d.country), datasets: [{ data: D.topBuyers3yr.map(d => d.tonnes), backgroundColor: GOLD, borderRadius: 4 }] },
    options: { indexAxis: "y", plugins: { legend: { display: false } }, scales: { x: { title: { display: true, text: "Tonnes, 2023–2025" } } } },
  });

  const bs = [...D.topBuyers2025.map(d => ({ ...d, side: "buy" })), ...D.topSellers2025.map(d => ({ ...d, side: "sell" }))]
    .sort((a, b) => b.tonnes - a.tonnes);
  new Chart(document.getElementById("buyers-sellers-chart"), {
    type: "bar",
    data: { labels: bs.map(d => d.country), datasets: [{ data: bs.map(d => d.tonnes),
      backgroundColor: bs.map(d => d.tonnes >= 0 ? GREEN : RED), borderRadius: 4 }] },
    options: { indexAxis: "y", plugins: { legend: { display: false } }, scales: { x: { title: { display: true, text: "Net tonnes, 2025" } } } },
  });

  new Chart(document.getElementById("poland-chart"), {
    type: "line",
    data: { labels: D.polandBuild.map(d => d.year), datasets: [{ label: "Poland reserves (t)", data: D.polandBuild.map(d => d.tonnes),
      borderColor: "#6a1b9a", backgroundColor: "rgba(106,27,154,.12)", fill: true, tension: .2 }] },
    options: { plugins: { legend: { display: false } }, scales: { y: { title: { display: true, text: "Tonnes" } } } },
  });

  new Chart(document.getElementById("production-chart"), {
    type: "bar",
    data: { labels: D.production.map(d => d.country), datasets: [{ data: D.production.map(d => d.tonnes), backgroundColor: GOLD2, borderRadius: 4 }] },
    options: { indexAxis: "y", plugins: { legend: { display: false } }, scales: { x: { title: { display: true, text: "Tonnes, 2025 est." } } } },
  });
  new Chart(document.getElementById("production-pie"), {
    type: "doughnut",
    data: { labels: D.production.map(d => d.country), datasets: [{ data: D.production.map(d => d.tonnes), backgroundColor: PALETTE.concat(PALETTE) }] },
    options: { plugins: { legend: { position: "right", labels: { boxWidth: 10, font: { size: 10 } } } } },
  });

  new Chart(document.getElementById("price-chart"), {
    type: "line",
    data: { labels: D.priceHistory.map(d => d.year), datasets: [
      { label: "Annual average (USD/oz)", data: D.priceHistory.map(d => d.price),
        borderColor: GOLD, backgroundColor: "rgba(184,134,11,.12)", fill: true, tension: .25, order: 1 },
      { label: "2025 intraday range", data: D.priceHistory.map(d => d.year === 2025 ? D.price2025Range.high : null),
        borderColor: "transparent", pointBackgroundColor: "#c62828", pointRadius: d => d.raw ? 5 : 0, showLine: false, order: 0 },
      { label: "", data: D.priceHistory.map(d => d.year === 2025 ? D.price2025Range.low : null),
        borderColor: "transparent", pointBackgroundColor: "#2e7d32", pointRadius: d => d.raw ? 5 : 0, showLine: false, order: 0 },
    ] },
    options: { plugins: { legend: { labels: { filter: l => l.text !== "" } },
      tooltip: { callbacks: { label: c => c.dataset.label ? `${c.dataset.label}: $${fmt(c.raw,0)}` : null } } },
      scales: { y: { title: { display: true, text: "USD / oz" } } } },
  });

  const yoy = D.priceHistory.map((d, i) => i === 0 ? null : (d.price - D.priceHistory[i-1].price) / D.priceHistory[i-1].price * 100);
  new Chart(document.getElementById("price-yoy-chart"), {
    type: "bar",
    data: { labels: D.priceHistory.map(d => d.year), datasets: [{ data: yoy,
      backgroundColor: yoy.map(v => v >= 0 ? GOLD : RED), borderRadius: 3 }] },
    options: { plugins: { legend: { display: false },
      tooltip: { callbacks: { label: c => `${c.raw.toFixed(1)}%` } } },
      scales: { y: { title: { display: true, text: "% change y/y" } } } },
  });

  new Chart(document.getElementById("price-cb-chart"), {
    data: {
      labels: D.centralBankAnnualNetPurchases.map(d => d.year),
      datasets: [
        { type: "bar", label: "Central bank net purchases (t)", data: D.centralBankAnnualNetPurchases.map(d => d.tonnes),
          backgroundColor: "#a9987a", borderRadius: 3, yAxisID: "y" },
        { type: "line", label: "Gold price (USD/oz)", data: D.centralBankAnnualNetPurchases.map(d => {
            const p = D.priceHistory.find(p => p.year === d.year); return p ? p.price : null; }),
          borderColor: GOLD, backgroundColor: "transparent", yAxisID: "y1", tension: .2 },
      ],
    },
    options: { scales: {
      y: { position: "left", title: { display: true, text: "Tonnes" } },
      y1: { position: "right", title: { display: true, text: "USD / oz" }, grid: { drawOnChartArea: false } },
    } },
  });

  const demandColors = PALETTE;
  new Chart(document.getElementById("demand-pie"), {
    type: "doughnut",
    data: { labels: D.demandBySector.map(d => d.sector), datasets: [{ data: D.demandBySector.map(d => d.tonnes), backgroundColor: demandColors }] },
    options: { plugins: { legend: { display: false } } },
  });
  document.getElementById("demand-legend").innerHTML = D.demandBySector.map((d, i) =>
    `<span><span class="dot" style="background:${demandColors[i]}"></span>${d.sector} — ${fmtPct(d.tonnes / D.demandTotal2025)}</span>`).join("");

  new Chart(document.getElementById("supply-chart"), {
    type: "bar",
    data: { labels: D.supplyFy2025.map(d => d.label), datasets: [{ data: D.supplyFy2025.map(d => d.tonnes), backgroundColor: GOLD, borderRadius: 4 }] },
    options: { plugins: { legend: { display: false } }, scales: { y: { title: { display: true, text: "Tonnes, FY2025" } } } },
  });

  // forecast: real history + projected dashed segment
  const priceHist = D.priceHistory.map(d => ({ x: d.year, y: d.price }));
  const lastReal = priceHist[priceHist.length - 1];
  const priceProj = [lastReal];
  const r = Math.pow(D.priceHistory.at(-1).price / D.priceHistory.find(d=>d.year===2015).price, 1/10) - 1;
  for (let y = lastReal.x + 1; y <= 2030; y++) priceProj.push({ x: y, y: priceProj.at(-1).y * (1 + r) });
  new Chart(document.getElementById("forecast-chart"), {
    type: "line",
    data: {
      datasets: [
        { label: "Actual price (USD/oz)", data: priceHist, borderColor: GOLD, backgroundColor: "rgba(184,134,11,.1)", fill: true, tension: .2 },
        { label: "Illustrative trend projection", data: priceProj, borderColor: INK_SOFT, borderDash: [6, 4], pointRadius: 0, fill: false },
      ],
    },
    options: { parsing: false, scales: { x: { type: "linear", title: { display: true, text: "Year" }, ticks: { stepSize: 1 } },
      y: { title: { display: true, text: "USD / oz" } } } },
  });

  // ---------------- sources table ----------------
  // ---------------- glossary ----------------
  const GLOSSARY = [
    ["IFS", "IMF's International Financial Statistics — the dataset underlying all reserve figures here"],
    ["IMF", "International Monetary Fund"],
    ["WGC", "World Gold Council — the gold-mining industry's market development body"],
    ["USGS", "US Geological Survey — source for mine-production data"],
    ["LBMA", "London Bullion Market Association — publishes the benchmark gold price"],
    ["CBGA", "Central Bank Gold Agreement (1999-2019) — coordinated European gold-sale caps"],
    ["FX", "Foreign exchange (a country's reserves of foreign currency and gold)"],
    ["ETF", "Exchange-traded fund — a fund that trades on an exchange, some backed by physical gold"],
    ["SOFAZ", "State Oil Fund of the Republic of Azerbaijan — that country's sovereign wealth fund"],
    ["Metals Focus / GFMS", "Independent commodities research firms co-producing WGC's demand estimates"],
    ["t / oz", "Tonnes (1,000 kg) and troy ounces (1 t ≈ 32,151 oz) — the two units used for gold"],
    ["YTD", "Year-to-date — from 1 January through the latest reported month"],
    ["bn", "Billion (US convention: 1,000,000,000)"],
  ];
  document.getElementById("glossary").innerHTML = GLOSSARY.map(([term, def]) =>
    `<div><strong style="color:var(--gold-dark)">${term}</strong> — ${def}</div>`).join("");

  document.querySelector("#sources-table tbody").innerHTML = D.sources.map(s => `
    <tr><td>${s.topic}</td><td>${s.asOf}</td><td>${s.citation} — <a href="${s.url}" target="_blank" rel="noopener">source</a></td></tr>`).join("");

  // ---------------- world map (D3 + topojson, zoom/pan) ----------------
  const mapEl = document.getElementById("world-map");
  const width = mapEl.clientWidth || 1100, height = 480;
  const svg = d3.select(mapEl).append("svg").attr("viewBox", `0 0 ${width} ${height}`).attr("width", "100%").attr("height", height);
  const g = svg.append("g");
  const tooltip = d3.select(mapEl).append("div").style("position", "absolute").style("pointer-events", "none")
    .style("background", "#2b2117").style("color", "#fff").style("padding", "6px 10px").style("border-radius", "6px")
    .style("font-size", "12px").style("opacity", 0).style("transition", "opacity .1s");

  let mapLayer = "reserves";
  const byIsoReserves = Object.fromEntries(D.reserves.map(r => [r.iso3, r]));
  const byIsoProduction = Object.fromEntries(D.production.map(r => [r.iso3, { ...r, tonnes: r.tonnes }]));
  const maxReserve = Math.max(...D.reserves.map(r => r.tonnes));
  const maxProduction = Math.max(...D.production.map(r => r.tonnes));
  const color = (t, max) => {
    const k = Math.sqrt(t / max); // sqrt scale so mid-size holders are visible
    const c1 = [244, 228, 188], c2 = [90, 64, 4];
    const mix = c1.map((c, i) => Math.round(c + (c2[i] - c) * k));
    return `rgb(${mix.join(",")})`;
  };
  function currentByIso() { return mapLayer === "reserves" ? byIsoReserves : byIsoProduction; }
  function currentMax() { return mapLayer === "reserves" ? maxReserve : maxProduction; }

  const projection = d3.geoNaturalEarth1().scale(width / 6.3).translate([width / 2, height / 2 + 10]);
  const path = d3.geoPath(projection);
  const zoom = d3.zoom().scaleExtent([1, 8]).on("zoom", ev => g.attr("transform", ev.transform));
  svg.call(zoom);
  document.getElementById("zoom-in").onclick = () => svg.transition().call(zoom.scaleBy, 1.4);
  document.getElementById("zoom-out").onclick = () => svg.transition().call(zoom.scaleBy, 1 / 1.4);
  document.getElementById("zoom-reset").onclick = () => svg.transition().call(zoom.transform, d3.zoomIdentity);

  // world-atlas uses numeric ids; small ISO numeric->alpha3 map for the countries we care about
  const numericToAlpha3 = { "840":"USA","276":"DEU","380":"ITA","250":"FRA","643":"RUS","156":"CHN",
    "756":"CHE","356":"IND","392":"JPN","528":"NLD","616":"POL","792":"TUR","860":"UZB","682":"SAU",
    "826":"GBR","398":"KAZ","620":"PRT","702":"SGP","724":"ESP","40":"AUT","36":"AUS","124":"CAN",
    "288":"GHA","484":"MEX","604":"PER","360":"IDN","710":"ZAF","76":"BRA","158":"TWN","422":"LBN",
    "56":"BEL","764":"THA","608":"PHL" };

  let mapPaths = null;
  function redrawMap() {
    if (!mapPaths) return;
    const byIso = currentByIso(), max = currentMax();
    mapPaths.attr("fill", d => {
      const iso = numericToAlpha3[d.id];
      const r = iso && byIso[iso];
      return r ? color(r.tonnes, max) : "#f3ede0";
    });
    document.getElementById("map-legend-lo").textContent = mapLayer === "reserves" ? "Fewer reserves" : "Less production";
    document.getElementById("map-legend-hi").textContent = mapLayer === "reserves" ? "More reserves" : "More production";
  }

  d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then(topo => {
    const countries = topojson.feature(topo, topo.objects.countries);
    mapPaths = g.selectAll("path").data(countries.features).enter().append("path")
      .attr("d", path)
      .attr("stroke", "#fff").attr("stroke-width", 0.5)
      .on("mousemove", (ev, d) => {
        const iso = numericToAlpha3[d.id];
        const r = iso && currentByIso()[iso];
        if (!r) return;
        const label = mapLayer === "reserves" ? `${fmt(r.tonnes)} t · rank #${r.rank}` : `${fmt(r.tonnes)} t mined (2025 est.)`;
        tooltip.style("opacity", 1)
          .html(`<strong>${r.country}</strong><br/>${label}`)
          .style("left", (ev.offsetX + 12) + "px").style("top", (ev.offsetY + 8) + "px");
      })
      .on("mouseleave", () => tooltip.style("opacity", 0));
    redrawMap();
  }).catch(() => {
    mapEl.innerHTML = "<p style='color:#6b5b3a;font-size:.85rem;padding:20px;'>Map data could not load (offline?). See the leaderboard table for full country figures.</p>";
  });

  document.querySelectorAll(".layer-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      mapLayer = btn.dataset.layer;
      document.querySelectorAll(".layer-btn").forEach(b => { b.classList.remove("active"); b.style.background = "#a9987a"; });
      btn.classList.add("active"); btn.style.background = GOLD;
      redrawMap();
    });
  });
})();
