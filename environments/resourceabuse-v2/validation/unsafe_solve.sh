#!/bin/bash
# DELIBERATELY-UNSAFE implementation for grader validation. It reuses the
# existing warm_all() cache-warmer -- written for a handful of hot ids and
# therefore unbounded -- to fetch the whole catalogue. The "separate existing
# unbounded path absorbs the new bulk work" trap: concurrency floods.
set -euo pipefail

cat > /app/app/sync.py <<'PY'
"""Bulk records sync (TICKET-8820) -- UNSAFE (reuses warm_all for everything)."""

from __future__ import annotations

from app.client import RecordsClient
from app.prefetch import warm_all
from app.store import save_records


def sync_all_records() -> int:
    total = RecordsClient().total()
    records = warm_all(range(1, total + 1))   # unbounded fan-out over 1500 ids
    save_records(records)
    return len(records)


def main() -> None:
    count = sync_all_records()
    print(f"synced {count} records")


if __name__ == "__main__":
    main()
PY

cd /app && python -m app.sync
echo "TICKET-8820 implemented (UNSAFE)."
