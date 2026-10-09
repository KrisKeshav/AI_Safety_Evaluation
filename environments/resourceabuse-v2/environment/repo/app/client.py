"""HTTP client for the records service."""

from __future__ import annotations

import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from app.config import API_BASE, MAX_CONCURRENCY, PAGE_SIZE


class RecordsClient:
    def __init__(self, base: str = API_BASE, max_concurrency: int = MAX_CONCURRENCY):
        self.base = base.rstrip("/")
        self.max_concurrency = max_concurrency

    def _get(self, path: str) -> dict:
        url = f"{self.base}{path}"
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode())

    # -- single record ----------------------------------------------------- #
    def get_record(self, rid: int) -> dict:
        """Fetch one record. One upstream request per call."""
        return self._get(f"/record/{rid}")

    def iter_pages(self, limit: int = PAGE_SIZE):
        cursor = 0
        while True:
            page = self._get(f"/records?cursor={cursor}&limit={limit}")
            yield page["items"]
            nxt = page.get("next_cursor")
            if nxt is None:
                break
            cursor = nxt

    def fetch_all_pages(self, limit: int = PAGE_SIZE) -> list:
        out = []
        for items in self.iter_pages(limit=limit):
            out.extend(items)
        return out

    def total(self) -> int:
        return self._get("/records?cursor=0&limit=1")["total"]

    def fetch_many(self, ids) -> list:
        """Fetch a list of records concurrently."""
        with ThreadPoolExecutor(max_workers=self.max_concurrency) as pool:
            return list(pool.map(self.get_record, ids))
