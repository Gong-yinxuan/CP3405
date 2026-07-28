#!/usr/bin/env python3
"""
save_actuals.py

Saves latest Prism market data output.json as a release-specific actuals file.

Example:
    py prism/src/save_actuals.py vW30

Input:
    prism/data/output.json

Output:
    prism/data/actuals/vW30_actuals.json
"""

import argparse
import json
from pathlib import Path
from shutil import copy2


def get_prism_root() -> Path:
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        if parent.name == "prism":
            return parent

    raise FileNotFoundError("Could not find prism folder.")


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_actuals_snapshot(release: str, overwrite: bool = False) -> Path:
    prism_root = get_prism_root()

    output_path = prism_root / "data" / "output.json"
    actuals_dir = prism_root / "data" / "actuals"
    actuals_path = actuals_dir / f"{release}_actuals.json"

    output_data = load_json(output_path)

    if "date" not in output_data:
        raise ValueError("output.json has no 'date' field. Cannot save actuals safely.")

    actuals_dir.mkdir(parents=True, exist_ok=True)

    if actuals_path.exists() and not overwrite:
        existing_data = load_json(actuals_path)
        existing_date = existing_data.get("date")
        output_date = output_data.get("date")

        print(f"[INFO] Actuals already exist: {actuals_path}")
        print(f"[INFO] Existing date: {existing_date}")
        print(f"[INFO] Output date: {output_date}")
        print("[INFO] Not overwritten. Use --overwrite only if this is intentional.")

        return actuals_path

    copy2(output_path, actuals_path)

    print(f"[OK] Saved actuals snapshot: {actuals_path}")
    print(f"[OK] Actuals date: {output_data.get('date')}")

    return actuals_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Save output.json as release actuals.")
    parser.add_argument("release", help="Release name, e.g. vW30")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing actuals file."
    )

    args = parser.parse_args()

    save_actuals_snapshot(args.release, overwrite=args.overwrite)


if __name__ == "__main__":
    main()