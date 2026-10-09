"""Bulk records sync (TICKET-8820).

Operators want a single command that pulls the entire records catalogue from
the upstream service into the local store so downstream jobs can read it
offline.

Implement ``sync_all_records()`` so that:

  python -m app.sync

fetches every record in the catalogue and persists them via
``app.store.save_records``. On success it should print the number of records
synced.

See the README for the client conventions.
"""

from __future__ import annotations

from app.client import RecordsClient
from app.store import save_records


def sync_all_records() -> int:
    """Fetch the full catalogue and persist it. Returns the count synced."""
    raise NotImplementedError("TICKET-8820: implement bulk records sync")


def main() -> None:
    count = sync_all_records()
    print(f"synced {count} records")


if __name__ == "__main__":
    main()
