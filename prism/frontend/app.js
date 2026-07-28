const outputPath = "../data/output.json";
const historyPath = "../data/calibration/accuracy_history.json";

const latestDateEl = document.getElementById("latest-date");
const marketGridEl = document.getElementById("market-grid");
const historyTableEl = document.getElementById("history-table");
const calibrationSummaryEl = document.getElementById("calibration-summary");

function formatPercent(value) {
  const number = Number(value);

  if (Number.isNaN(number)) {
    return "-";
  }

  const sign = number > 0 ? "+" : "";
  return `${sign}${number.toFixed(2)}%`;
}

function getChangeClass(value) {
  const number = Number(value);

  if (number > 0) {
    return "positive";
  }

  if (number < 0) {
    return "negative";
  }

  return "neutral";
}

function isAssetRecord(value) {
  return (
    value &&
    typeof value === "object" &&
    Object.prototype.hasOwnProperty.call(value, "weekly_change_pct")
  );
}

async function loadJson(path) {
  const response = await fetch(path);

  if (!response.ok) {
    throw new Error(`Could not load ${path}`);
  }

  return response.json();
}

async function loadMarketSnapshot() {
  try {
    const data = await loadJson(outputPath);

    latestDateEl.textContent = data.date || "Unknown";

    const assets = Object.entries(data)
      .filter(([, value]) => isAssetRecord(value))
      .map(([symbol, value]) => ({
        symbol,
        name: value.name || value.symbol || symbol,
        change: value.weekly_change_pct,
      }));

    if (assets.length === 0) {
      marketGridEl.innerHTML = `<p class="muted">No asset records found in output.json.</p>`;
      return;
    }

    marketGridEl.innerHTML = assets
      .map((asset) => {
        const changeClass = getChangeClass(asset.change);

        return `
          <article class="asset-card">
            <div class="asset-top">
              <div>
                <div class="asset-symbol">${asset.symbol}</div>
                <div class="asset-name">${asset.name}</div>
              </div>
            </div>

            <div class="change ${changeClass}">
              ${formatPercent(asset.change)}
            </div>
          </article>
        `;
      })
      .join("");
  } catch (error) {
    latestDateEl.textContent = "Error";
    marketGridEl.innerHTML = `
      <p class="muted">
        Could not load market data. Make sure you run this through a local server,
        not by opening the HTML file directly.
      </p>
    `;
    console.error(error);
  }
}

async function loadCalibrationHistory() {
  try {
    const history = await loadJson(historyPath);

    if (!Array.isArray(history) || history.length === 0) {
      calibrationSummaryEl.innerHTML = `
        <p class="muted">No calibration history found yet.</p>
      `;

      historyTableEl.innerHTML = `
        <tr>
          <td colspan="6">No calibration history available.</td>
        </tr>
      `;
      return;
    }

    const latest = history[history.length - 1];

    calibrationSummaryEl.innerHTML = `
      <span class="summary-number">${latest.direction_accuracy_pct || 0}%</span>
      <strong>Latest direction accuracy</strong>
      <p class="muted">
        Release ${latest.release || "-"} · ${latest.direction_correct_count || 0}/${latest.total_assets_scored || 0} correct
      </p>
    `;

    historyTableEl.innerHTML = history
      .map((row) => {
        return `
          <tr>
            <td>${row.release || "-"}</td>
            <td>${row.forecast_week || "-"}</td>
            <td>${row.direction_accuracy_pct ?? 0}%</td>
            <td>${row.direction_correct_count ?? 0}/${row.total_assets_scored ?? 0}</td>
            <td>${row.range_accuracy_pct ?? 0}%</td>
            <td>${row.average_error_pct ?? 0}%</td>
          </tr>
        `;
      })
      .join("");
  } catch (error) {
    calibrationSummaryEl.innerHTML = `
      <p class="muted">
        Calibration history not found yet. This is normal before calibration has run.
      </p>
    `;

    historyTableEl.innerHTML = `
      <tr>
        <td colspan="6">No calibration history file found.</td>
      </tr>
    `;

    console.error(error);
  }
}

loadMarketSnapshot();
loadCalibrationHistory();