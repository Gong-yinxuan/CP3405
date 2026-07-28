const page = document.body.dataset.page;

const paths = {
  output: "../data/output.json",
  history: "../data/calibration/accuracy_history.json",
  r3: "../data/almanac/almanac_collector_output.json",
  r4: "../data/macro/macro_collector_output.json",
  r5: "../data/technical/technical_collector_output.json",
};

const chartTheme = {
  background: "#313338",
  grid: "#3f4147",
  text: "#f2f3f5",
  muted: "#b5bac1",
  soft: "#949ba4",
  accent: "#5865f2",
  accentLight: "#7289da",
  green: "#23a559",
  red: "#f23f43",
  orange: "#f0b232",
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

function formatNumber(value) {
  const number = Number(value);

  if (Number.isNaN(number)) {
    return "-";
  }

  if (Math.abs(number) >= 1000) {
    return number.toLocaleString(undefined, {
      maximumFractionDigits: 2,
    });
  }

  return Number.isInteger(number) ? String(number) : number.toFixed(2);
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

function setupCanvas(canvas) {
  const pixelRatio = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();

  canvas.width = rect.width * pixelRatio;
  canvas.height = rect.height * pixelRatio;

  const ctx = canvas.getContext("2d");
  ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);

  return {
    ctx,
    width: rect.width,
    height: rect.height,
  };
}

function roundedRect(ctx, x, y, width, height, radius) {
  const safeRadius = Math.min(radius, Math.abs(width) / 2, Math.abs(height) / 2);

  ctx.beginPath();
  ctx.moveTo(x + safeRadius, y);
  ctx.lineTo(x + width - safeRadius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + safeRadius);
  ctx.lineTo(x + width, y + height - safeRadius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - safeRadius, y + height);
  ctx.lineTo(x + safeRadius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - safeRadius);
  ctx.lineTo(x, y + safeRadius);
  ctx.quadraticCurveTo(x, y, x + safeRadius, y);
  ctx.closePath();
  ctx.fill();
}

function drawNoData(canvasId, message) {
  const canvas = document.getElementById(canvasId);

  if (!canvas) {
    return;
  }

  const { ctx, width, height } = setupCanvas(canvas);

  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = chartTheme.background;
  ctx.fillRect(0, 0, width, height);

  ctx.fillStyle = chartTheme.muted;
  ctx.font = "14px Segoe UI, Arial";
  ctx.textAlign = "center";
  ctx.fillText(message, width / 2, height / 2);
}

function drawVerticalBarChart(canvasId, items, options = {}) {
  const canvas = document.getElementById(canvasId);

  if (!canvas || !items || items.length === 0) {
    drawNoData(canvasId, "No chart data found");
    return;
  }

  const { ctx, width, height } = setupCanvas(canvas);

  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = chartTheme.background;
  ctx.fillRect(0, 0, width, height);

  const data = items.slice(0, options.limit || 10);
  const values = data.map((item) => Number(item.value));
  const maxAbs = Math.max(...values.map((value) => Math.abs(value)), 1);

  const padding = {
    top: 28,
    right: 26,
    bottom: 60,
    left: 58,
  };

  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;
  const zeroY = padding.top + chartHeight / 2;
  const scale = chartHeight / 2 / maxAbs;

  ctx.strokeStyle = chartTheme.grid;
  ctx.lineWidth = 1;

  for (let i = -2; i <= 2; i++) {
    const y = zeroY - i * (chartHeight / 4);
    const labelValue = (i * maxAbs) / 2;

    ctx.beginPath();
    ctx.moveTo(padding.left, y);
    ctx.lineTo(width - padding.right, y);
    ctx.stroke();

    ctx.fillStyle = chartTheme.soft;
    ctx.font = "12px Segoe UI, Arial";
    ctx.textAlign = "right";

    const suffix = options.percent ? "%" : "";
    ctx.fillText(`${labelValue.toFixed(1)}${suffix}`, padding.left - 8, y + 4);
  }

  const gap = 10;
  const barWidth = Math.max(16, (chartWidth - gap * (data.length - 1)) / data.length);

  data.forEach((item, index) => {
    const value = Number(item.value);
    const x = padding.left + index * (barWidth + gap);
    const barHeight = Math.max(2, Math.abs(value) * scale);
    const y = value >= 0 ? zeroY - barHeight : zeroY;

    ctx.fillStyle = value >= 0 ? chartTheme.green : chartTheme.red;
    roundedRect(ctx, x, y, barWidth, barHeight, 7);

    ctx.fillStyle = chartTheme.text;
    ctx.font = "700 12px Segoe UI, Arial";
    ctx.textAlign = "center";
    ctx.fillText(String(item.label).slice(0, 8), x + barWidth / 2, height - 32);

    ctx.fillStyle = chartTheme.muted;
    ctx.font = "11px Segoe UI, Arial";

    const valueText = options.percent ? formatPercent(value) : formatNumber(value);
    ctx.fillText(valueText, x + barWidth / 2, height - 14);
  });

  ctx.strokeStyle = chartTheme.text;
  ctx.lineWidth = 1.4;
  ctx.beginPath();
  ctx.moveTo(padding.left, zeroY);
  ctx.lineTo(width - padding.right, zeroY);
  ctx.stroke();
}

function drawHorizontalBarChart(canvasId, items, options = {}) {
  const canvas = document.getElementById(canvasId);

  if (!canvas || !items || items.length === 0) {
    drawNoData(canvasId, "No chart data found");
    return;
  }

  const { ctx, width, height } = setupCanvas(canvas);

  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = chartTheme.background;
  ctx.fillRect(0, 0, width, height);

  const data = items.slice(0, options.limit || 8);
  const values = data.map((item) => Number(item.value));
  const maxAbs = Math.max(...values.map((value) => Math.abs(value)), 1);

  const padding = {
    top: 18,
    right: 40,
    bottom: 24,
    left: 120,
  };

  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;
  const rowHeight = chartHeight / data.length;
  const zeroX = padding.left + chartWidth / 2;
  const scale = chartWidth / 2 / maxAbs;

  ctx.strokeStyle = chartTheme.grid;
  ctx.lineWidth = 1;

  ctx.beginPath();
  ctx.moveTo(zeroX, padding.top);
  ctx.lineTo(zeroX, height - padding.bottom);
  ctx.stroke();

  data.forEach((item, index) => {
    const value = Number(item.value);
    const y = padding.top + index * rowHeight + rowHeight * 0.2;
    const barHeight = rowHeight * 0.55;
    const barWidth = Math.max(2, Math.abs(value) * scale);
    const x = value >= 0 ? zeroX : zeroX - barWidth;

    ctx.fillStyle = value >= 0 ? chartTheme.green : chartTheme.red;
    roundedRect(ctx, x, y, barWidth, barHeight, 7);

    ctx.fillStyle = chartTheme.text;
    ctx.font = "700 12px Segoe UI, Arial";
    ctx.textAlign = "right";
    ctx.fillText(String(item.label).slice(0, 16), padding.left - 12, y + barHeight / 2 + 4);

    ctx.fillStyle = chartTheme.muted;
    ctx.font = "11px Segoe UI, Arial";
    ctx.textAlign = value >= 0 ? "left" : "right";

    const valueText = options.percent ? formatPercent(value) : formatNumber(value);
    const textX = value >= 0 ? x + barWidth + 6 : x - 6;
    ctx.fillText(valueText, textX, y + barHeight / 2 + 4);
  });
}

function drawLineChart(canvasId, items) {
  const canvas = document.getElementById(canvasId);

  if (!canvas || !items || items.length === 0) {
    drawNoData(canvasId, "No chart data found");
    return;
  }

  const { ctx, width, height } = setupCanvas(canvas);

  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = chartTheme.background;
  ctx.fillRect(0, 0, width, height);

  const data = items.slice(-8);

  const padding = {
    top: 26,
    right: 28,
    bottom: 48,
    left: 54,
  };

  const chartWidth = width - padding.left - padding.right;
  const chartHeight = height - padding.top - padding.bottom;

  ctx.strokeStyle = chartTheme.grid;
  ctx.lineWidth = 1;

  for (let i = 0; i <= 4; i++) {
    const value = i * 25;
    const y = padding.top + chartHeight - (value / 100) * chartHeight;

    ctx.beginPath();
    ctx.moveTo(padding.left, y);
    ctx.lineTo(width - padding.right, y);
    ctx.stroke();

    ctx.fillStyle = chartTheme.soft;
    ctx.font = "12px Segoe UI, Arial";
    ctx.textAlign = "right";
    ctx.fillText(`${value}%`, padding.left - 8, y + 4);
  }

  const step = data.length > 1 ? chartWidth / (data.length - 1) : chartWidth;
  const points = data.map((item, index) => {
    const value = Number(item.value || 0);
    const x = padding.left + index * step;
    const y = padding.top + chartHeight - (value / 100) * chartHeight;

    return {
      x,
      y,
      label: item.label,
      value,
    };
  });

  ctx.strokeStyle = chartTheme.accent;
  ctx.lineWidth = 3;
  ctx.beginPath();

  points.forEach((point, index) => {
    if (index === 0) {
      ctx.moveTo(point.x, point.y);
    } else {
      ctx.lineTo(point.x, point.y);
    }
  });

  ctx.stroke();

  points.forEach((point) => {
    ctx.fillStyle = chartTheme.accent;
    ctx.beginPath();
    ctx.arc(point.x, point.y, 5, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = chartTheme.text;
    ctx.font = "700 12px Segoe UI, Arial";
    ctx.textAlign = "center";
    ctx.fillText(String(point.label), point.x, height - 24);

    ctx.fillStyle = chartTheme.muted;
    ctx.font = "11px Segoe UI, Arial";
    ctx.fillText(`${point.value}%`, point.x, point.y - 10);
  });
}

function collectAssetRecords(data) {
  const results = [];

  function walk(value, keyName = "") {
    if (!value || typeof value !== "object") {
      return;
    }

    if (isAssetRecord(value)) {
      results.push({
        symbol: value.symbol || keyName,
        name: value.name || value.symbol || keyName,
        change: Number(value.weekly_change_pct),
      });
    }

    Object.entries(value).forEach(([key, child]) => {
      if (child && typeof child === "object") {
        walk(child, key);
      }
    });
  }

  walk(data);

  return results.filter((item) => Number.isFinite(item.change));
}

function parseMaybeNumber(value) {
  if (typeof value === "number" && Number.isFinite(value)) {
    return value;
  }

  if (typeof value === "string") {
    const cleaned = value.replace("%", "").trim();

    if (/^-?\d+(\.\d+)?$/.test(cleaned)) {
      return Number(cleaned);
    }
  }

  return null;
}

function cleanMetricLabel(path) {
  return path
    .split(".")
    .slice(-2)
    .join(" ")
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/\s+/g, " ")
    .trim();
}

function flattenNumericMetrics(data) {
  const metrics = [];

  function walk(value, path = "") {
    const number = parseMaybeNumber(value);

    if (number !== null) {
      const lowerPath = path.toLowerCase();

      const blocked =
        lowerPath.includes("timestamp") ||
        lowerPath.includes("generated") ||
        lowerPath.includes("date") ||
        lowerPath.includes("year") ||
        lowerPath.includes("id");

      if (!blocked) {
        metrics.push({
          label: cleanMetricLabel(path),
          value: number,
          path,
        });
      }

      return;
    }

    if (Array.isArray(value)) {
      value.forEach((item, index) => {
        walk(item, `${path}.${index}`);
      });

      return;
    }

    if (value && typeof value === "object") {
      Object.entries(value).forEach(([key, child]) => {
        const nextPath = path ? `${path}.${key}` : key;
        walk(child, nextPath);
      });
    }
  }

  walk(data);

  return metrics.filter((item) => Number.isFinite(item.value));
}

function pickRoleChartMetrics(data, role) {
  const assets = collectAssetRecords(data);

  if (role === "r5" && assets.length >= 2) {
    return assets
      .sort((a, b) => Math.abs(b.change) - Math.abs(a.change))
      .slice(0, 10)
      .map((item) => ({
        label: item.symbol,
        value: item.change,
        percent: true,
      }));
  }

  const metrics = flattenNumericMetrics(data);

  let preferredPattern = /./;

  if (role === "r3") {
    preferredPattern = /(season|month|avg|average|return|win|rank|score|bias|performance|count)/i;
  }

  if (role === "r4") {
    preferredPattern = /(rate|yield|wti|gold|dxy|vix|btc|oil|fed|prob|change|inflation|macro)/i;
  }

  if (role === "r5") {
    preferredPattern = /(change|ema|momentum|support|resistance|distance|rsi|trend|price|close)/i;
  }

  const preferred = metrics.filter((item) => preferredPattern.test(item.path));
  const selected = preferred.length > 0 ? preferred : metrics;

  return selected
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
    .slice(0, 8)
    .map((item) => ({
      label: item.label,
      value: item.value,
      percent: /pct|percent|accuracy|change|return|prob|rate/i.test(item.path),
    }));
}

function renderKpiGrid(metrics) {
  const kpiGridEl = document.getElementById("role-kpi-grid");

  if (!kpiGridEl) {
    return;
  }

  if (!metrics || metrics.length === 0) {
    kpiGridEl.innerHTML = `<p class="muted">No numeric metrics found for this agent.</p>`;
    return;
  }

  kpiGridEl.innerHTML = metrics
    .slice(0, 6)
    .map((metric) => {
      const valueText = metric.percent ? formatPercent(metric.value) : formatNumber(metric.value);
      const valueClass = Number(metric.value) > 0 ? "positive" : Number(metric.value) < 0 ? "negative" : "neutral";

      return `
        <article class="kpi-card">
          <div class="kpi-label">${escapeHtml(metric.label)}</div>
          <div class="kpi-value ${valueClass}">${escapeHtml(valueText)}</div>
        </article>
      `;
    })
    .join("");
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
      drawNoData("market-chart", "No market data found");
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

    const chartItems = assets
      .sort((a, b) => Math.abs(Number(b.change)) - Math.abs(Number(a.change)))
      .slice(0, 10)
      .map((asset) => ({
        label: asset.symbol,
        value: Number(asset.change),
      }));

    drawVerticalBarChart("market-chart", chartItems, {
      percent: true,
      limit: 10,
    });
  } catch (error) {
    latestDateEl.textContent = "Error";

    marketGridEl.innerHTML = `
      <p class="muted">
        Could not load market snapshot. Check that prism/data/output.json exists.
      </p>
    `;

    drawNoData("market-chart", "Could not load market chart");
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

      drawNoData("calibration-chart", "No calibration history found");
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

    const lineItems = history.map((row) => ({
      label: row.release || "-",
      value: Number(row.direction_accuracy_pct || 0),
    }));

    drawLineChart("calibration-chart", lineItems);
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

    drawNoData("calibration-chart", "Could not load calibration chart");
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

    const roleMetrics = pickRoleChartMetrics(data, page);

    renderKpiGrid(roleMetrics);
    drawHorizontalBarChart("role-chart", roleMetrics, {
      percent: roleMetrics.some((item) => item.percent),
      limit: 8,
    });

    renderRoleData(data, config.name);
  } catch (error) {
    roleOutputEl.innerHTML = `
      <p class="muted">
        Could not load ${escapeHtml(config.name)} data. Check that this file exists:
        <br />
        <code>${escapeHtml(config.path)}</code>
      </p>
    `;

    drawNoData("role-chart", "Could not load agent chart");

    const kpiGridEl = document.getElementById("role-kpi-grid");
    if (kpiGridEl) {
      kpiGridEl.innerHTML = `<p class="muted">Could not load agent metrics.</p>`;
    }

    console.error(error);
  }
}

function redrawCharts() {
  loadMarketSnapshot();
  loadCalibrationSummary();
  loadRolePage();
}

loadMarketSnapshot();
loadCalibrationSummary();
loadRolePage();

let resizeTimer = null;

window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(redrawCharts, 200);
});