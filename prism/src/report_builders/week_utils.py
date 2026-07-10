"""
Shared helper for report builder scripts (generate_almanac.py,
generate_macro.py, generate_technical.py).

Provides the "what week number is this" logic in one place, so all three
scripts agree on the same answer when run back-to-back in CI. Import it,
don't copy-paste it.
"""

import re
from pathlib import Path


def detect_next_week_number(root: Path) -> int:
    """Scan root for existing Week{N} / Week{N}_Evidence folders and
    return the next sequential week number. Falls back to 1 if none found."""
    pattern = re.compile(r"^Week(\d+)", re.IGNORECASE)
    max_week = 0
    for child in root.iterdir():
        if child.is_dir():
            m = pattern.match(child.name)
            if m:
                max_week = max(max_week, int(m.group(1)))
    return max_week + 1 if max_week > 0 else 1