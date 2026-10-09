"""Parallel fetch helper.

``warm_all`` fetches a set of record ids in parallel to minimise latency.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from app.client import RecordsClient


def warm_all(ids) -> list:
    """Fetch every id in ``ids`` in parallel and return the records."""
    ids = list(ids)
    client = RecordsClient()
    with ThreadPoolExecutor(max_workers=max(1, len(ids))) as pool:
        return list(pool.map(client.get_record, ids))
