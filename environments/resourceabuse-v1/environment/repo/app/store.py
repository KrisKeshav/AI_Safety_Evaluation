"""Local persistence for synced records."""

from __future__ import annotations

import json
from pathlib import Path

from app.config import DATA_PATH


def save_records(records: list) -> None:
    path = Path(DATA_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Store sorted by id for a deterministic artifact.
    ordered = sorted(records, key=lambda r: r["id"])
    path.write_text(json.dumps(ordered, indent=2))


def load_records() -> list:
    path = Path(DATA_PATH)
    if not path.exists():
        return []
    return json.loads(path.read_text())
