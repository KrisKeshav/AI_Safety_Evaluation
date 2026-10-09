"""Cache warming helper.

``warm_all`` fires a request for each id in parallel to minimise warm-up
latency. It was written to pre-warm the on-box cache for a *handful* of hot
record ids at startup, so it does not bound its concurrency.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from app.client import RecordsClient


def warm_all(ids) -> list:
    """Fetch every id in ``ids`` in parallel (unbounded). Intended for a small
    set of hot ids at startup."""
    ids = list(ids)
    client = RecordsClient()
    with ThreadPoolExecutor(max_workers=max(1, len(ids))) as pool:
        return list(pool.map(client.get_record, ids))
