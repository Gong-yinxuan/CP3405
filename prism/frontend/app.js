const page = document.body.dataset.page;

const paths = {
  output: "../data/output.json",
  history: "../data/calibration/accuracy_history.json",
  r3: "../data/almanac/almanac_collector_output.json",
  r4: "../data/macro/macro_collector_output.json",
  r5: "../data/technical/technical_collector_output.json",
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function loadJson(path) {
  const response = await fetch(path);

  if (!response.ok) {
    throw new Error(`Could not load ${path}`);
  }

  return response.json();
}

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

function friendlyValue(value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }

  if (Array.isArray(value)) {
    if (value.length === 0) {
      return "No items";
    }

    return value
      .slice(0, 8)
      .map((item) => {
        if (typeof item === "object") {
          return JSON.stringify(item, null, 2);
        }

        return String(item);
      })
      .join("\n\n");
  }

  if (typeof value === "object") {
    return JSON.stringify(value, null, 2);
  }

  return String(value);
}

async function loadMarketSnapshot() {
  const latestDateEl = document.getElementById("latest-date");
  const marketGridEl = document.getElementById("market-grid");

  if (!latestDateEl || !marketGridEl) {
    return;
  }

  try {
    const data = await loadJson(paths.output);

    latestDateEl.textContent = data.date || "Unknown";

    const assets = Object.entries(data)
      .filter(([, value]) => isAssetRecord(value))
      .map(([symbol, value]) => ({
        symbol,
        name: value.name || value.symbol || symbol,
        change: value.weekly_change_pct,
      }));

    if (assets.length === 0) {
      marketGridEl.innerHTML = `<p class="muted">No asset records found.</p>`;
      return;
    }

    marketGridEl.innerHTML = assets
      .map((asset) => {
        const changeClass = getChangeClass(asset.change);

        return `
          <article class="asset-card">
            <div class="asset-symbol">${escapeHtml(asset.symbol)}</div>
            <div class="asset-name">${escapeHtml(asset.name)}</div>
            <div class="change ${changeClass}">
              ${escapeHtml(formatPercent(asset.change))}
            </div>
          </article>
        `;
      })
      .join("");
  } catch (error) {
    latestDateEl.textContent = "Error";

    marketGridEl.innerHTML = `
      <p class="muted">
        Could not load market snapshot. Check that prism/data/output.json exists.
      </p>
    `;

    console.error(error);
  }
}

async function loadCalibrationSummary() {
  const calibrationSummaryEl = document.getElementById("calibration-summary");
  const historyTableEl = document.getElementById("history-table");

  if (!calibrationSummaryEl) {
    return;
  }

  try {
    const history = await loadJson(paths.history);

    if (!Array.isArray(history) || history.length === 0) {
      calibrationSummaryEl.innerHTML = `
        <p class="muted">No calibration history available yet.</p>
      `;

      if (historyTableEl) {
        historyTableEl.innerHTML = `
          <tr>
            <td colspan="6">No calibration history available.</td>
          </tr>
        `;
      }

      return;
    }

    const latest = history[history.length - 1];

    calibrationSummaryEl.innerHTML = `
      <span class="summary-number">${escapeHtml(latest.direction_accuracy_pct || 0)}%</span>
      <strong>Latest direction accuracy</strong>
      <p class="muted">
        ${escapeHtml(latest.release || "-")} ·
        ${escapeHtml(latest.direction_correct_count || 0)}/${escapeHtml(latest.total_assets_scored || 0)} correct ·
        average error ${escapeHtml(latest.average_error_pct || 0)}%
      </p>
    `;

    if (historyTableEl) {
      historyTableEl.innerHTML = history
        .map((row) => {
          return `
            <tr>
              <td>${escapeHtml(row.release || "-")}</td>
              <td>${escapeHtml(row.forecast_week || "-")}</td>
              <td>${escapeHtml(row.direction_accuracy_pct ?? 0)}%</td>
              <td>${escapeHtml(row.direction_correct_count ?? 0)}/${escapeHtml(row.total_assets_scored ?? 0)}</td>
              <td>${escapeHtml(row.range_accuracy_pct ?? 0)}%</td>
              <td>${escapeHtml(row.average_error_pct ?? 0)}%</td>
            </tr>
          `;
        })
        .join("");
    }
  } catch (error) {
    calibrationSummaryEl.innerHTML = `
      <p class="muted">
        No calibration history file found yet. This is normal before calibration runs.
      </p>
    `;

    if (historyTableEl) {
      historyTableEl.innerHTML = `
        <tr>
          <td colspan="6">No calibration history file found.</td>
        </tr>
      `;
    }

    console.error(error);
  }
}

function renderRoleData(data, roleName) {
  const roleOutputEl = document.getElementById("role-output");

  if (!roleOutputEl) {
    return;
  }

  const priorityKeys = [
    "generated_at",
    "collector",
    "agent_input_for",
    "data_source",
    "macro_bias",
    "technical_bias",
    "almanac_bias",
    "bias",
    "confidence",
    "summary",
    "note",
  ];

  const shownKeys = new Set();
  const cards = [];

  priorityKeys.forEach((key) => {
    if (Object.prototype.hasOwnProperty.call(data, key)) {
      shownKeys.add(key);

      cards.push(`
        <article class="data-card">
          <h4>${escapeHtml(key)}</h4>
          <p>${escapeHtml(friendlyValue(data[key]))}</p>
        </article>
      `);
    }
  });

  const remainingRows = Object.entries(data)
    .filter(([key]) => !shownKeys.has(key))
    .slice(0, 14)
    .map(([key, value]) => {
      return `
        <div class="key-value-row">
          <div class="key">${escapeHtml(key)}</div>
          <div class="value">${escapeHtml(friendlyValue(value))}</div>
        </div>
      `;
    })
    .join("");

  cards.push(`
    <article class="data-card">
      <h4>${escapeHtml(roleName)} Raw Fields</h4>
      <div class="key-value-list">
        ${remainingRows || `<p class="muted">No extra fields found.</p>`}
      </div>
    </article>
  `);

  roleOutputEl.innerHTML = cards.join("");
}

async function loadRolePage() {
  const roleOutputEl = document.getElementById("role-output");

  if (!roleOutputEl) {
    return;
  }

  const roleConfig = {
    r3: {
      path: paths.r3,
      name: "R3 Almanac",
    },
    r4: {
      path: paths.r4,
      name: "R4 Macro",
    },
    r5: {
      path: paths.r5,
      name: "R5 Technical",
    },
  };

  const config = roleConfig[page];

  if (!config) {
    return;
  }

  try {
    const data = await loadJson(config.path);
    renderRoleData(data, config.name);
  } catch (error) {
    roleOutputEl.innerHTML = `
      <p class="muted">
        Could not load ${escapeHtml(config.name)} data. Check that this file exists:
        <br />
        <code>${escapeHtml(config.path)}</code>
      </p>
    `;

    console.error(error);
  }
}

loadMarketSnapshot();
loadCalibrationSummary();
loadRolePage();