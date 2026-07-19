"""
Prism Calibration Runner — R6/R10

Reads:
- prism/data/predictions/vW25_prediction.json
- prism/data/predictions/vW28_prediction.json
- etc.

Actuals:
- prism/data/output.json

Automatically creates actuals snapshot:
- prism/data/actuals/vW25_actuals.json
- prism/data/actuals/vW28_actuals.json
- etc.

Generates:
- delta_W25.md / delta_W28.md
- prism/data/calibration/delta_W25.json / delta_W28.json
- prism/data/calibration/accuracy_history.json
- prism/data/calibration/accuracy_history.md
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from shutil import copy2


def get_prism_root() -> Path:
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        if parent.name == "prism":
            return parent

    raise FileNotFoundError("Could not find prism folder.")


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"[OK] Saved {path}")


def save_text(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        file.write(text)

    print(f"[OK] Saved {path}")


def detect_latest_release(prism_root: Path) -> str:
    prediction_dir = prism_root / "data" / "predictions"

    prediction_files = list(prediction_dir.glob("vW*_prediction.json"))

    if not prediction_files:
        raise FileNotFoundError(
            f"No prediction JSON files found in {prediction_dir}"
        )

    releases = []

    for path in prediction_files:
        release = path.name.replace("_prediction.json", "")

        try:
            week_number = int(release.replace("vW", ""))
            releases.append((week_number, release))
        except ValueError:
            continue

    if not releases:
        raise ValueError(
            "No valid prediction files found. Expected format: vW28_prediction.json"
        )

    releases.sort()
    return releases[-1][1]


def get_prediction_path(prism_root: Path, release: str) -> Path:
    prediction_path = (
        prism_root
        / "data"
        / "predictions"
        / f"{release}_prediction.json"
    )

    if not prediction_path.exists():
        raise FileNotFoundError(f"Missing prediction file: {prediction_path}")

    return prediction_path


def forecast_end_date(prediction_data: dict) -> str | None:
    """Extract the final YYYY-MM-DD date from forecast_week metadata."""
    text = str(prediction_data.get("forecast_week", ""))
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    return dates[-1] if dates else None


def get_actuals_path_for_release(
    prism_root: Path,
    release: str,
    output_path: Path,
    prediction_data: dict,
) -> Path:
    """
    Return a release-specific actuals snapshot with date-integrity protection.

    For the latest release, an existing snapshot is refreshed only when:
    1. its date does not match the prediction forecast end date, and
    2. output.json has the exact expected date.

    Old releases are never silently rebuilt from the latest output.
    """
    actuals_dir = prism_root / "data" / "actuals"
    actuals_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = actuals_dir / f"{release}_actuals.json"

    expected_date = forecast_end_date(prediction_data)
    latest_release = detect_latest_release(prism_root)

    if not output_path.exists():
        raise FileNotFoundError(f"Missing actuals output file: {output_path}")

    output_data = load_json(output_path)
    output_date = str(output_data.get("date", ""))

    if snapshot_path.exists():
        snapshot_data = load_json(snapshot_path)
        snapshot_date = str(snapshot_data.get("date", ""))

        if expected_date and snapshot_date != expected_date:
            if release != latest_release:
                raise ValueError(
                    f"Stale actuals for old release {release}: "
                    f"snapshot={snapshot_date}, expected={expected_date}. "
                    "Do not rebuild old releases from current output.json."
                )

            if output_date != expected_date:
                raise ValueError(
                    f"Actuals date mismatch for {release}: "
                    f"snapshot={snapshot_date}, output={output_date}, "
                    f"expected={expected_date}. Calibration stopped."
                )

            archive_path = actuals_dir / (
                f"{release}_actuals_{snapshot_date}_stale.json"
            )
            if snapshot_date and not archive_path.exists():
                copy2(snapshot_path, archive_path)
                print(f"[WARN] Archived stale snapshot: {archive_path}")

            copy2(output_path, snapshot_path)
            print(
                f"[OK] Refreshed {release} actuals from "
                f"{snapshot_date} to {output_date}"
            )
            return snapshot_path

        print(
            f"[INFO] Using validated actuals snapshot: "
            f"{snapshot_path} ({snapshot_date})"
        )
        return snapshot_path

    if release != latest_release:
        raise FileNotFoundError(
            f"Missing actuals file for old release: {snapshot_path}. "
            "Cannot create old actuals from the latest output.json."
        )

    if expected_date and output_date != expected_date:
        raise ValueError(
            f"Cannot create {release} snapshot: output date {output_date} "
            f"does not match forecast end date {expected_date}."
        )

    copy2(output_path, snapshot_path)
    print(f"[OK] Created actuals snapshot: {snapshot_path}")
    return snapshot_path

def normalise_direction(direction: str) -> str:
    direction = str(direction).strip().lower()

    if direction in ["up", "bullish", "positive"]:
        return "Up"

    if direction in ["down", "bearish", "negative"]:
        return "Down"

    if direction in ["flat", "neutral", "sideways"]:
        return "Neutral"

    return "Neutral"


def actual_direction_from_change(change_pct: float) -> str:
    if change_pct > 0:
        return "Up"

    if change_pct < 0:
        return "Down"

    return "Neutral"


def is_direction_correct(
    predicted_direction: str,
    actual_change: float,
    range_low,
    range_high
) -> bool:
    predicted_direction = normalise_direction(predicted_direction)
    actual_direction = actual_direction_from_change(actual_change)

    if predicted_direction == "Up":
        return actual_direction == "Up"

    if predicted_direction == "Down":
        return actual_direction == "Down"

    # For Flat/Neutral predictions, use the predicted range.
    if range_low is not None and range_high is not None:
        return float(range_low) <= actual_change <= float(range_high)

    # Fallback if no range is provided.
    return -0.5 <= actual_change <= 0.5


def classify_bias(expected_change: float, actual_change: float) -> str:
    difference = expected_change - actual_change

    if difference > 0.5:
        return "Too bullish"

    if difference < -0.5:
        return "Too bearish"

    return "Well calibrated"


def compare_prediction_to_actuals(
    release: str,
    prediction_data: dict,
    actual_data: dict
) -> dict:
    asset_results = []
    predicted_assets = prediction_data.get("assets", {})

    for symbol, prediction in predicted_assets.items():
        actual = actual_data.get(symbol)

        if actual is None:
            asset_results.append({
                "symbol": symbol,
                "status": "missing_actual_data"
            })
            continue

        actual_change = actual.get("weekly_change_pct")

        if actual_change is None:
            asset_results.append({
                "symbol": symbol,
                "status": "missing_actual_weekly_change_pct"
            })
            continue

        actual_change = float(actual_change)

        predicted_direction = normalise_direction(
            prediction.get("predicted_direction", "Neutral")
        )

        expected_change = float(prediction.get("expected_change_pct", 0.0))

        range_low = prediction.get("range_low_pct")
        range_high = prediction.get("range_high_pct")

        range_hit = False

        if range_low is not None and range_high is not None:
            range_hit = float(range_low) <= actual_change <= float(range_high)

        direction_correct = is_direction_correct(
            predicted_direction,
            actual_change,
            range_low,
            range_high
        )

        error_size = round(abs(expected_change - actual_change), 2)

        asset_results.append({
            "symbol": symbol,
            "name": prediction.get("name", symbol),
            "predicted_direction": predicted_direction,
            "expected_change_pct": expected_change,
            "range_low_pct": range_low,
            "range_high_pct": range_high,
            "confidence": prediction.get("confidence"),
            "actual_direction": actual_direction_from_change(actual_change),
            "actual_weekly_change_pct": actual_change,
            "direction_correct": direction_correct,
            "range_hit": range_hit,
            "error_size_pct": error_size,
            "bias": classify_bias(expected_change, actual_change),
            "status": "ok"
        })

    valid_results = [
        row for row in asset_results
        if row.get("status") == "ok"
    ]

    total_scored = len(valid_results)
    correct_count = sum(1 for row in valid_results if row["direction_correct"])
    range_hit_count = sum(1 for row in valid_results if row["range_hit"])

    if total_scored > 0:
        direction_accuracy_pct = round((correct_count / total_scored) * 100, 1)
        range_accuracy_pct = round((range_hit_count / total_scored) * 100, 1)
        error_total = sum(
            Decimal(str(row["error_size_pct"])) for row in valid_results
        )
        average_error_pct = float(
            (error_total / Decimal(total_scored)).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        )
    else:
        direction_accuracy_pct = 0
        range_accuracy_pct = 0
        average_error_pct = 0

    return {
        "release": release,
        "week": release.replace("v", ""),
        "forecast_week": prediction_data.get("forecast_week", ""),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prediction_source_type": prediction_data.get(
            "source_type",
            "official_prediction_json"
        ),
        "actuals_source": f"prism/data/actuals/{release}_actuals.json",
        "total_assets_scored": total_scored,
        "direction_correct_count": correct_count,
        "direction_accuracy_pct": direction_accuracy_pct,
        "range_hit_count": range_hit_count,
        "range_accuracy_pct": range_accuracy_pct,
        "average_error_pct": average_error_pct,
        "asset_results": asset_results
    }


def update_accuracy_history(history_path: Path, weekly_result: dict) -> list:
    if history_path.exists():
        history = load_json(history_path)
    else:
        history = []

    # Replace old result for same release if script is re-run.
    history = [
        row for row in history
        if row.get("release") != weekly_result.get("release")
    ]

    history.append({
        "release": weekly_result["release"],
        "week": weekly_result["week"],
        "forecast_week": weekly_result.get("forecast_week", ""),
        "direction_accuracy_pct": weekly_result["direction_accuracy_pct"],
        "direction_correct_count": weekly_result["direction_correct_count"],
        "total_assets_scored": weekly_result["total_assets_scored"],
        "range_accuracy_pct": weekly_result["range_accuracy_pct"],
        "range_hit_count": weekly_result["range_hit_count"],
        "average_error_pct": weekly_result["average_error_pct"]
    })

    def sort_key(row):
        week_text = str(row.get("week", "")).replace("W", "")

        try:
            return int(week_text)
        except ValueError:
            return 999

    history.sort(key=sort_key)

    return history


def build_delta_markdown(result: dict) -> str:
    lines = []

    lines.append(f"# Delta Report — {result['release']}")
    lines.append("")
    lines.append(f"**Week:** {result.get('week', '')}")
    lines.append(f"**Forecast week:** {result.get('forecast_week', '')}")
    lines.append(f"**Generated at:** {result.get('generated_at', '')}")
    lines.append(f"**Actuals source:** `{result.get('actuals_source', '')}`")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Direction accuracy: {result['direction_accuracy_pct']}%")
    lines.append(
        f"- Correct directions: {result['direction_correct_count']} "
        f"out of {result['total_assets_scored']}"
    )
    lines.append(f"- Range accuracy: {result['range_accuracy_pct']}%")
    lines.append(
        f"- Range hits: {result['range_hit_count']} "
        f"out of {result['total_assets_scored']}"
    )
    lines.append(f"- Average error size: {result['average_error_pct']}%")
    lines.append("")

    lines.append("## Asset Results")
    lines.append("")
    lines.append(
        "| Asset | Prediction | Expected % | Range % | Actual direction | Actual % | Direction correct? | Range hit? | Error % | Bias |"
    )
    lines.append(
        "|---|---|---:|---:|---|---:|---|---|---:|---|"
    )

    for row in result["asset_results"]:
        if row.get("status") != "ok":
            lines.append(
                f"| {row.get('symbol', '')} | - | - | - | - | - | - | - | - | {row.get('status', '')} |"
            )
            continue

        direction_correct = "Yes" if row["direction_correct"] else "No"
        range_hit = "Yes" if row["range_hit"] else "No"

        range_text = "-"

        if row.get("range_low_pct") is not None and row.get("range_high_pct") is not None:
            range_text = f"{row['range_low_pct']} to {row['range_high_pct']}"

        lines.append(
            f"| {row['symbol']} "
            f"| {row['predicted_direction']} "
            f"| {row['expected_change_pct']} "
            f"| {range_text} "
            f"| {row['actual_direction']} "
            f"| {row['actual_weekly_change_pct']} "
            f"| {direction_correct} "
            f"| {range_hit} "
            f"| {row['error_size_pct']} "
            f"| {row['bias']} |"
        )

    lines.append("")
    lines.append("## R6/R10 Notes")
    lines.append("")
    valid_rows = [
        row for row in result["asset_results"]
        if row.get("status") == "ok"
    ]
    if valid_rows:
        largest = max(valid_rows, key=lambda row: row["error_size_pct"])
        too_bullish = sum(1 for row in valid_rows if row["bias"] == "Too bullish")
        too_bearish = sum(1 for row in valid_rows if row["bias"] == "Too bearish")
        if too_bullish > too_bearish:
            main_bias = "Too bullish"
        elif too_bearish > too_bullish:
            main_bias = "Too bearish"
        else:
            main_bias = "Balanced by count"
        lines.append(
            f"- Largest error: {largest['symbol']} "
            f"({largest['error_size_pct']} percentage points)"
        )
        lines.append(
            f"- Main bias: {main_bias} "
            f"({too_bullish} too bullish vs {too_bearish} too bearish)"
        )
        lines.append(
            "- Improvement: validate actuals date, reduce correlated "
            "confidence, and widen ranges for high-volatility assets."
        )
    else:
        lines.append("- No valid assets were available for calibration.")
    lines.append("")

    return "\n".join(lines)


def build_accuracy_history_markdown(history: list) -> str:
    lines = []

    if history:
        week_numbers = []

        for row in history:
            week_text = str(row.get("week", "")).replace("W", "")

            try:
                week_numbers.append(int(week_text))
            except ValueError:
                pass

        if week_numbers:
            title = f"# Accuracy History — W{min(week_numbers)} to W{max(week_numbers)}"
        else:
            title = "# Accuracy History"
    else:
        title = "# Accuracy History"

    lines.append(title)
    lines.append("")
    lines.append(
        "| Release | Week | Forecast week | Direction accuracy | Correct / Total | Range accuracy | Range hits | Average error % |"
    )
    lines.append(
        "|---|---|---|---:|---:|---:|---:|---:|"
    )

    for row in history:
        lines.append(
            f"| {row.get('release', '')} "
            f"| {row.get('week', '')} "
            f"| {row.get('forecast_week', '')} "
            f"| {row.get('direction_accuracy_pct', 0)}% "
            f"| {row.get('direction_correct_count', 0)}/{row.get('total_assets_scored', 0)} "
            f"| {row.get('range_accuracy_pct', 0)}% "
            f"| {row.get('range_hit_count', 0)}/{row.get('total_assets_scored', 0)} "
            f"| {row.get('average_error_pct', 0)}% |"
        )

    if history:
        average_direction_accuracy = round(
            sum(row.get("direction_accuracy_pct", 0) for row in history) / len(history),
            1
        )

        average_range_accuracy = round(
            sum(row.get("range_accuracy_pct", 0) for row in history) / len(history),
            1
        )

        average_error = round(
            sum(row.get("average_error_pct", 0) for row in history) / len(history),
            2
        )
    else:
        average_direction_accuracy = 0
        average_range_accuracy = 0
        average_error = 0

    lines.append("")
    lines.append("## Cumulative Summary")
    lines.append("")
    lines.append(f"- Average direction accuracy: {average_direction_accuracy}%")
    lines.append(f"- Average range accuracy: {average_range_accuracy}%")
    lines.append(f"- Average error size: {average_error}%")
    total_assets = sum(row.get("total_assets_scored", 0) for row in history)
    total_correct = sum(row.get("direction_correct_count", 0) for row in history)
    total_range_hits = sum(row.get("range_hit_count", 0) for row in history)
    weighted_direction = round((total_correct / total_assets) * 100, 1) if total_assets else 0
    weighted_range = round((total_range_hits / total_assets) * 100, 1) if total_assets else 0
    lines.append(f"- Asset-weighted direction accuracy: {weighted_direction}%")
    lines.append(f"- Asset-weighted range accuracy: {weighted_range}%")
    lines.append(
        "- Improvement: seal predictions before outcomes and require "
        "actuals-date validation before updating history."
    )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    prism_root = get_prism_root()
    repo_root = prism_root.parent

    if len(sys.argv) >= 2:
        release = sys.argv[1]
    else:
        release = detect_latest_release(prism_root)

    prediction_path = get_prediction_path(prism_root, release)
    output_path = prism_root / "data" / "output.json"

    print(f"[INFO] Release: {release}")
    print(f"[INFO] Prediction file: {prediction_path}")
    print(f"[INFO] Latest output file: {output_path}")

    prediction_data = load_json(prediction_path)

    actuals_snapshot_path = get_actuals_path_for_release(
        prism_root=prism_root,
        release=release,
        output_path=output_path,
        prediction_data=prediction_data,
    )

    print(f"[INFO] Actuals snapshot file: {actuals_snapshot_path}")

    actual_data = load_json(actuals_snapshot_path)

    result = compare_prediction_to_actuals(
        release=release,
        prediction_data=prediction_data,
        actual_data=actual_data
    )

    calibration_dir = prism_root / "data" / "calibration"

    delta_json_path = calibration_dir / f"delta_{release.replace('v', '')}.json"
    delta_md_path = repo_root / f"delta_{release.replace('v', '')}.md"

    history_json_path = calibration_dir / "accuracy_history.json"
    history_md_path = calibration_dir / "accuracy_history.md"

    save_json(result, delta_json_path)

    delta_markdown = build_delta_markdown(result)
    save_text(delta_markdown, delta_md_path)

    history = update_accuracy_history(history_json_path, result)
    save_json(history, history_json_path)

    history_markdown = build_accuracy_history_markdown(history)
    save_text(history_markdown, history_md_path)

    print("[OK] Calibration complete.")


if __name__ == "__main__":
    main()