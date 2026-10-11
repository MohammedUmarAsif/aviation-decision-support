"use strict";

const byId = (id) => document.getElementById(id);
const format = (value, digits = 0) => value == null ? "Unknown" : Number(value).toLocaleString("en-US", { maximumFractionDigits: digits, minimumFractionDigits: digits });
const percent = (value) => value == null ? "Unknown" : `${format(value * 100, 2)}%`;
const escapeText = (value) => String(value).replace(/[&<>"']/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[character]);
const models = { train_median: "Median baseline", random_forest: "Random forest" };
const ranks = {
  delay_minutes: { label: "Total delay time", title: "Highest reported delay burden", unit: "Total reported minutes", value: (v) => `${format(v)} min` },
  delay_rate: { label: "Share delayed", title: "Highest share of delayed arrivals", unit: "Delayed arrivals / matched reported flights", value: percent },
  flights: { label: "Number of flights", title: "Busiest reported segments", unit: "Reported flights", value: (v) => `${format(v)} flights` },
};
let evidence;
let state;
const segmentKey = (s) => `${s.carrier}-${s.airport}`;
const carrierLabel = (s) => (s.carrier_name || s.carrier).replace(/\s+(Inc\.|Inc|LLC|Co\.).*$/, "").replace(/ d\/b\/a.*$/, "");
const airportLabel = (s) => (s.airport_name || s.airport).split(":")[0];
const segmentLabel = (s) => `${carrierLabel(s)} · ${airportLabel(s)}`;

function sortedSegments(metric) {
  return evidence.monthly.segments.filter((s) => s.eligible && s[metric] != null).sort((a, b) => b[metric] - a[metric] || a.carrier.localeCompare(b.carrier) || a.airport.localeCompare(b.airport));
}

function readState() {
  const params = new URLSearchParams(location.search);
  const rank = Object.hasOwn(ranks, params.get("rank")) ? params.get("rank") : "delay_minutes";
  const model = Object.hasOwn(models, params.get("model")) ? params.get("model") : "random_forest";
  const capacity = [10, 20, 40, 80].includes(Number(params.get("capacity"))) ? Number(params.get("capacity")) : 20;
  const eligible = evidence.monthly.segments.filter((s) => s.eligible);
  const segment = eligible.some((s) => segmentKey(s) === params.get("segment")) ? params.get("segment") : segmentKey(sortedSegments(rank)[0]);
  return { rank, model, capacity, segment };
}

function shareState() {
  const url = new URL(location.href);
  url.search = new URLSearchParams({ rank: state.rank, model: state.model, capacity: state.capacity, segment: state.segment }).toString();
  history.pushState(null, "", url);
}

function changeState(update) {
  state = { ...state, ...update };
  if (update.rank) state.segment = segmentKey(sortedSegments(state.rank)[0]);
  shareState();
  renderInteractive();
}

function renderRanking() {
  const metric = ranks[state.rank];
  const entries = sortedSegments(state.rank);
  byId("rank").value = state.rank;
  byId("ranking-title").textContent = metric.title;
  byId("ranking-units").textContent = `${metric.unit} · July 2026 · US arrivals · ≥100-flight screen`;
  byId("rank-chart").replaceChildren();
  for (const row of entries.slice(0, 8)) {
    const button = document.createElement("button");
    button.className = "rank-row";
    button.setAttribute("aria-pressed", String(segmentKey(row) === state.segment));
    button.innerHTML = `<span class="rank-label"><span><strong>${escapeText(segmentLabel(row))}</strong><small>${escapeText(row.carrier)}–${escapeText(row.airport)}</small></span><span class="rank-value">${escapeText(metric.value(row[state.rank]))}</span></span><span class="track" aria-hidden="true"><span class="bar" style="display:block;width:${100 * row[state.rank] / entries[0][state.rank]}%"></span></span>`;
    button.addEventListener("click", () => changeState({ segment: segmentKey(row) }));
    byId("rank-chart").append(button);
  }
  const selected = evidence.monthly.segments.find((s) => segmentKey(s) === state.segment);
  byId("segment").value = state.segment;
  byId("segment-title").textContent = segmentLabel(selected);
  byId("segment-values").innerHTML = `<dl><div><dt>Carrier / airport</dt><dd>${escapeText(selected.carrier)}–${escapeText(selected.airport)}</dd></div><div><dt>Reported flights</dt><dd>${format(selected.flights)}</dd></div><div><dt>15+ min delayed</dt><dd>${format(selected.delayed)}</dd></div><div><dt>Rate denominator</dt><dd>${format(selected.rate_flights)}</dd></div><div><dt>Share delayed</dt><dd>${percent(selected.delay_rate)}</dd></div><div><dt>Total delay time</dt><dd>${format(selected.delay_minutes)} min</dd></div></dl>`;
  const focus = state.rank === "delay_rate" ? `Frequency: ${format(selected.delayed)} known delayed arrivals out of ${format(selected.rate_flights)} matched reported flights. Compare burden and sample size before assigning priority.` : state.rank === "flights" ? `Exposure: ${format(selected.flights)} reported flights. Traffic alone does not show how often or how severely arrivals were delayed.` : `Burden: ${format(selected.delay_minutes)} reported delay minutes. This total reflects both traffic and disruption; it does not identify a cause or the effect of an intervention.`;
  byId("segment-note").textContent = `${focus} ${format(selected.reconciliation_flag_records)} cause reconciliation flags; ${format(selected.missing_count_records)} records with unknown delay counts; ${format(selected.missing_burden_records)} with unknown burden.`;
  byId("segment-request").textContent = selected.reconciliation_flag_records ? "Resolve flagged cause totals with the provider; then check repeated months and request flight-level schedules and rotations." : "Check repeated months; request flight-level schedules, turnaround/rotation history and decision-time weather forecasts.";
  byId("rank-table").querySelector("tbody").innerHTML = entries.slice(0, 10).map((s) => `<tr><th scope="row">${escapeText(segmentLabel(s))} (${escapeText(segmentKey(s))})</th><td>${format(s.flights)}</td><td>${format(s.rate_flights)}</td><td>${format(s.delayed)}</td><td>${percent(s.delay_rate)}</td><td>${format(s.delay_minutes)}</td></tr>`).join("");
}

function renderQueue() {
  const capacities = evidence.forecast.capacities;
  const row = capacities.models[state.model][String(state.capacity)];
  byId("queue-scope").textContent = `Retrospective · ${capacities.test_days} test days · Identical known-outcome eligibility`;
  byId("model").value = state.model;
  byId("capacity").value = String(state.capacity);
  byId("queue-caption").textContent = `${models[state.model]} · ${state.capacity} reviews per day`;
  byId("queue-denominator").textContent = `${format(row.alerts)} total reviews over ${capacities.test_days} test days · known outcomes only`;
  byId("queue-bar").innerHTML = `<div class="queue-hit" style="width:${100 * row.hits / row.alerts}%"></div><div class="queue-other"></div>`;
  byId("queue-key").innerHTML = `<span><i class="swatch" aria-hidden="true"></i><strong>${format(row.hits)}</strong> severe delays found</span><span><i class="swatch other" aria-hidden="true"></i><strong>${format(row.false_alerts)}</strong> other reviews (false alerts)</span>`;
  byId("outcome-denominator").textContent = `${format(capacities.severe_outcomes)} eligible severe delays · same test period`;
  byId("outcome-bar").innerHTML = `<div class="queue-hit" style="width:${100 * row.hits / capacities.severe_outcomes}%"></div><div class="queue-other"></div>`;
  byId("outcome-key").textContent = `${format(row.hits)} found · ${format(row.missed_disruptions)} missed. Most severe delays remain outside the queue.`;
  byId("queue-summary").innerHTML = `<p><strong>${format(row.missed_disruptions)}</strong>of ${format(capacities.severe_outcomes)} severe outcomes missed</p><p><strong>${percent(row.precision)}</strong>of reviews found a severe delay</p><p><strong>${percent(row.recall)}</strong>of all severe outcomes found</p>`;
}

function renderInteractive() {
  renderRanking();
  renderQueue();
}

function renderStaticEvidence() {
  const audit = evidence.monthly.audit;
  const result = evidence.forecast.results;
  const leaders = sortedSegments("delay_minutes").slice(0, 3);
  byId("landing-chart").innerHTML = leaders.map((s) => `<div class="landing-row"><div class="metric-label"><span>${escapeText(segmentLabel(s))}<small>${escapeText(s.carrier)}–${escapeText(s.airport)}</small></span><strong>${format(s.delay_minutes)}<small>minutes</small></strong></div><div class="track" aria-hidden="true"><div class="bar" style="width:${100 * s.delay_minutes / leaders[0].delay_minutes}%"></div></div></div>`).join("");
  byId("monthly-scope").textContent = `Study A · July 2026 · US arrivals · ${format(audit.raw_rows)} carrier-airport records · ${format(audit.raw_reported_flights)} reported flights`;
  byId("monthly-limit").textContent = `Rate denominator: ${format(audit.rate_denominator_flights)} flights with known delay counts (${format(audit.missing_delay_count_rows)} record excluded). ${format(audit.reconciliation_flag_keys.length)} records have cause reconciliation flags. Missing burden stays unknown. This is an investigation screen, not an airline-quality ranking.`;
  byId("monthly-method").textContent = `Complete export: ${format(evidence.monthly.segments.length)} segments, including those below the screen. Overall share delayed: ${percent(audit.weighted_delay_rate)} (${format(audit.delayed_flights)} / ${format(audit.rate_denominator_flights)}).`;
  byId("forecast-scope").textContent = `Study B · NYC departures, 2013 · ${format(result.quality.raw_flights)} raw flights · ${format(result.quality.missing_departure_delay)} unknown outcomes excluded · ${format(result.partitions.test.flights)} test flights`;
  byId("mae-chart").innerHTML = Object.keys(models).map((name) => `<div class="metric-row"><div class="metric-label"><span>${models[name]}</span><strong>${format(result.test[name].mae_minutes, 2)} min</strong></div><div class="track" aria-hidden="true"><div class="bar" style="width:${100 * result.test[name].mae_minutes / 25}%"></div></div></div>`).join("");
  byId("median-note").textContent = `Baseline prediction: training median (${format(result.train_median_minutes)} minute). Both models use the same ${format(result.partitions.test.flights)} test outcomes.`;
  byId("mae-table").querySelector("tbody").innerHTML = Object.keys(models).map((name) => `<tr><th scope="row">${models[name]}</th><td>${format(result.validation_mae_minutes[name], 2)}</td><td>${format(result.test[name].mae_minutes, 2)}</td><td>${name === result.selected_by_validation_mae ? "Yes" : "No"}</td></tr>`).join("");
  byId("queue-table").querySelector("tbody").innerHTML = Object.entries(evidence.forecast.capacities.models).flatMap(([name, grid]) => Object.values(grid).map((row) => `<tr><th scope="row">${models[name]}</th><td>${row.capacity_per_day}</td><td>${format(row.alerts)}</td><td>${format(row.hits)}</td><td>${format(row.false_alerts)}</td><td>${format(row.missed_disruptions)}</td><td>${percent(row.precision)}</td><td>${percent(row.recall)}</td></tr>`)).join("");
  const coverage = result.split_conformal;
  const periods = [{ name: "All test flights", flights: result.partitions.test.flights, coverage: coverage.test_coverage }, ...Object.entries(coverage.monthly).map(([month, entry]) => ({ name: month === "11" ? "November" : "December", ...entry }))];
  byId("coverage-chart").innerHTML = `<p class="target-label">Dashed marker: ${percent(coverage.nominal_coverage)} target</p>${periods.map((entry) => `<div class="metric-row"><div class="metric-label"><span>${entry.name}</span><strong>${percent(entry.coverage)}</strong></div><div class="track" aria-hidden="true"><div class="bar" style="width:${entry.coverage * 100}%"></div><span class="target-marker"></span></div></div>`).join("")}`;
  byId("coverage-table").querySelector("tbody").innerHTML = periods.map((entry) => `<tr><th scope="row">${entry.name}</th><td>${format(entry.flights)}</td><td>${percent(entry.coverage)}</td></tr>`).join("");
  byId("coverage-width").textContent = `Fixed interval width: ${format(coverage.width_minutes)} minutes · median baseline only · ${format(result.partitions.test.flights)} eligible test flights`;
  byId("coverage-note").textContent = `Overall coverage was ${percent(coverage.test_coverage)}, compared with ${percent(coverage.monthly["11"].coverage)} in November and ${percent(coverage.monthly["12"].coverage)} in December. A nominal target is useful only when checked against held-out outcomes.`;
  byId("source-hashes").textContent = `BTS raw-file SHA256: ${audit.source_sha256}. NYC converted CSV SHA256: ${result.source_sha256}.`;
  const select = byId("segment");
  for (const s of evidence.monthly.segments.filter((s) => s.eligible)) {
    const option = document.createElement("option");
    option.value = segmentKey(s);
    option.textContent = `${segmentLabel(s)} (${segmentKey(s)})`;
    select.append(option);
  }
}

function findingsBrief() {
  const s = evidence.monthly.segments.find((entry) => segmentKey(entry) === state.segment);
  const queue = evidence.forecast.capacities.models[state.model][String(state.capacity)];
  const results = evidence.forecast.results;
  return `# Flight Review  ·  findings brief\n\nIndependent study by Mohammed Umar Asif Sayed; AI-assisted development. Agent checks are not personal review or peer review.\n\n## Investigation\n\nStudy A: July 2026, US monthly reported arrivals; carrier plus arrival airport, not a route.\nSelected ranking: ${ranks[state.rank].label}.\nSelected segment: ${segmentLabel(s)} (${segmentKey(s)}).\nReported flights: ${format(s.flights)}; known delayed 15+ minutes: ${format(s.delayed)}; matched rate denominator: ${format(s.rate_flights)}; share delayed: ${percent(s.delay_rate)}; reported delay minutes: ${format(s.delay_minutes)}.\nCause flags: ${s.reconciliation_flag_records}; missing count records: ${s.missing_count_records}; missing burden records: ${s.missing_burden_records}.\nScreen: at least 100 reported flights, not a confidence guarantee.\n\n## Forecast review experiment\n\nStudy B: 2013 NYC departures; November–December test, ${format(results.partitions.test.flights)} known outcomes. Separate from Study A.\nSelected queue: ${models[state.model]}, ${state.capacity} reviews/day across ${evidence.forecast.capacities.test_days} days.\n${format(queue.alerts)} reviews = ${format(queue.hits)} severe delays found + ${format(queue.false_alerts)} false alerts.\n${format(queue.missed_disruptions)} severe delays missed; ${format(evidence.forecast.capacities.severe_outcomes)} total eligible severe outcomes (departure at least 60 minutes late).\nPrecision (reviews denominator): ${percent(queue.precision)}; recall (all severe outcomes denominator): ${percent(queue.recall)}.\nTest MAE: median ${format(results.test.train_median.mae_minutes, 2)} minutes; forest ${format(results.test.random_forest.mae_minutes, 2)}. Median won validation; forest was not selected by MAE.\nSelected median interval: ${percent(results.split_conformal.nominal_coverage)} target, ${percent(results.split_conformal.test_coverage)} measured coverage; width ${results.split_conformal.width_minutes} minutes. November ${percent(results.split_conformal.monthly["11"].coverage)}; December ${percent(results.split_conformal.monthly["12"].coverage)}. These intervals are not assigned to the forest.\n\n## Recommendation\n\nUse diagnostics to investigate high burden. Schedule-only forecast evidence does not justify operational adoption. Verify repeated patterns and source discrepancies; obtain current decision-time schedules, rotations and weather forecasts; agree review capacity and error costs before prospective evaluation.\n\n## Limits\n\n${evidence.limitations.map((limit) => `- ${limit}`).join("\n")}\n\n## Sources and reproducibility\n\n${Object.entries(evidence.sources).map(([name, url]) => `- ${name}: ${url}`).join("\n")}\n- Public page: https://mohammedumarasif.github.io/aviation-decision-support/\n- Evidence and hashes: https://mohammedumarasif.github.io/aviation-decision-support/manifest.json\n- Code: https://github.com/MohammedUmarAsif/aviation-decision-support\n- BTS source SHA256: ${evidence.monthly.audit.source_sha256}\n- NYC CSV SHA256: ${results.source_sha256}\n\nSelected state: ${location.href}\n`;
}

async function load() {
  try {
    const response = await fetch("evidence.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    evidence = await response.json();
    if (evidence.schema_version !== 1 || !evidence.monthly.segments.length || !evidence.forecast.capacities.models.random_forest["20"]) throw new Error("Unsupported evidence format");
    renderStaticEvidence();
    state = readState();
    renderInteractive();
    for (const id of ["rank", "segment", "model", "capacity", "export", "reset"]) byId(id).disabled = false;
    byId("rank").addEventListener("change", (event) => changeState({ rank: event.target.value }));
    byId("segment").addEventListener("change", (event) => changeState({ segment: event.target.value }));
    byId("model").addEventListener("change", (event) => changeState({ model: event.target.value }));
    byId("capacity").addEventListener("change", (event) => changeState({ capacity: Number(event.target.value) }));
    byId("reset").addEventListener("click", () => {
      const url = new URL(location.href); url.search = ""; history.pushState(null, "", url);
      state = readState(); renderInteractive();
      byId("export-status").textContent = "Exploration reset to total delay time, random forest and 20 reviews per day.";
    });
    byId("export").addEventListener("click", () => {
      const blob = new Blob([findingsBrief()], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a"); anchor.href = url; anchor.download = "flight-review-findings.md";
      document.body.append(anchor); anchor.click(); anchor.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      byId("export-status").textContent = "Findings brief downloaded with your selected evidence and its limitations.";
    });
    window.addEventListener("popstate", () => { state = readState(); renderInteractive(); });
    byId("load-status").hidden = true;
    // Evidence changes section heights. Restore a linked chapter after rendering.
    const chapter = document.getElementById(location.hash.slice(1));
    if (chapter) requestAnimationFrame(() => chapter.scrollIntoView());
  } catch (error) {
    byId("load-status").classList.add("error");
    byId("load-status").textContent = `The evidence could not load (${error.message}). Reload this page, or read the linked findings report and evidence files. Controls remain unavailable until the evidence loads.`;
    const report = document.createElement("a");
    report.href = "https://github.com/MohammedUmarAsif/aviation-decision-support/blob/main/reports/stakeholder.md";
    report.textContent = " Read the findings report.";
    byId("load-status").append(report);
  }
}
load();
