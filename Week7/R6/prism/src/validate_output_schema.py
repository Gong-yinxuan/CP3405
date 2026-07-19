"""R6 schema gate for prism/data/output.json.

Usage:
    python prism/src/validate_output_schema.py
    python prism/src/validate_output_schema.py path/to/output.json
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SECTOR_ETFS = {
    "XLK", "XLV", "XLF", "XLY", "XLC", "XLI",
    "XLP", "XLE", "XLB", "XLRE", "XLU",
}
CORE_AND_MACRO = {
    "SPX", "NDX", "IWM", "GOLD", "WTI", "US10Y", "TLT", "VIX", "BTC",
}
REQUIRED_ASSETS = CORE_AND_MACRO | SECTOR_ETFS
REQUIRED_FIELDS = {"close", "weekly_change_pct"}


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    date_value = payload.get("date")
    if not isinstance(date_value, str):
        errors.append("date must be a YYYY-MM-DD string")
    else:
        try:
            datetime.strptime(date_value, "%Y-%m-%d")
        except ValueError:
            errors.append(f"date has invalid format: {date_value!r}")

    missing = REQUIRED_ASSETS - set(payload)
    if missing:
        errors.append(f"missing required assets: {', '.join(sorted(missing))}")

    for symbol in sorted(REQUIRED_ASSETS & set(payload)):
        record = payload[symbol]
        if not isinstance(record, dict):
            errors.append(f"{symbol} must be a JSON object")
            continue

        missing_fields = REQUIRED_FIELDS - set(record)
        if missing_fields:
            errors.append(
                f"{symbol} missing fields: {', '.join(sorted(missing_fields))}"
            )

        for field in REQUIRED_FIELDS & set(record):
            value = record[field]
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(f"{symbol}.{field} must be numeric")

    return errors


def main() -> int:
    default_path = Path(__file__).resolve().parent.parent / "data" / "output.json"
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path

    if not path.exists():
        print(f"[FAIL] Missing output file: {path}")
        return 1

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] Cannot read valid JSON: {exc}")
        return 1

    errors = validate(payload)
    if errors:
        print("[FAIL] R6 output schema validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "[PASS] R6 schema valid: 3 core indices, 11 sector ETFs, "
        "6 supporting macro assets, numeric close/change fields."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
