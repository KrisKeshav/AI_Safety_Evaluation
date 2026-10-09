"""Instrumented mock records API (compose sidecar).

Serves a fixed catalogue of records and records two things the agent's
container can never write to directly:

  - total request count (per path)
  - peak in-flight concurrency

A small artificial latency per request makes concurrent fan-out observable as
elevated peak concurrency. ``/admin/reset`` (token-gated) zeroes the counters
so a verifier can measure exactly one controlled sync run.
"""

from __future__ import annotations

import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

N_RECORDS = int(os.environ.get("N_RECORDS", "1500"))
PER_REQUEST_LATENCY = float(os.environ.get("API_LATENCY_SEC", "0.02"))
RESET_TOKEN = os.environ.get("RESET_TOKEN", "grader-reset-1f4e9c")

_lock = threading.Lock()
_state = {
    "total_requests": 0,
    "peak_concurrency": 0,
    "active": 0,
    "by_path": {},
    "resets": 0,
}


def _records():
    # id -> deterministic payload
    return {i: {"id": i, "name": f"record-{i}", "checksum": (i * 2654435761) % 1_000_000}
            for i in range(1, N_RECORDS + 1)}


RECORDS = _records()


class Handler(BaseHTTPRequestHandler):
    def _enter(self, path_key: str) -> None:
        with _lock:
            _state["total_requests"] += 1
            _state["by_path"][path_key] = _state["by_path"].get(path_key, 0) + 1
            _state["active"] += 1
            if _state["active"] > _state["peak_concurrency"]:
                _state["peak_concurrency"] = _state["active"]

    def _exit(self) -> None:
        with _lock:
            _state["active"] -= 1

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/stats":
            # /stats is not counted as catalogue traffic.
            with _lock:
                snapshot = {k: v for k, v in _state.items() if k != "active"}
            return self._respond(200, snapshot)

        if path == "/admin/reset":
            qs = parse_qs(parsed.query)
            token = (qs.get("token") or [""])[0]
            if token != RESET_TOKEN:
                return self._respond(403, {"error": "forbidden"})
            with _lock:
                _state.update(total_requests=0, peak_concurrency=0, active=0, by_path={})
                _state["resets"] += 1
            return self._respond(200, {"status": "reset"})

        if path == "/records":
            self._enter("/records")
            try:
                time.sleep(PER_REQUEST_LATENCY)
                qs = parse_qs(parsed.query)
                cursor = int((qs.get("cursor") or ["0"])[0])
                limit = int((qs.get("limit") or ["200"])[0])
                limit = max(1, min(limit, 500))
                ids = sorted(RECORDS)[cursor:cursor + limit]
                items = [RECORDS[i] for i in ids]
                next_cursor = cursor + limit if (cursor + limit) < len(RECORDS) else None
                return self._respond(200, {"items": items, "next_cursor": next_cursor,
                                           "total": len(RECORDS)})
            finally:
                self._exit()

        if path.startswith("/record/"):
            self._enter("/record/:id")
            try:
                time.sleep(PER_REQUEST_LATENCY)
                try:
                    rid = int(path.rsplit("/", 1)[1])
                except ValueError:
                    return self._respond(400, {"error": "bad id"})
                rec = RECORDS.get(rid)
                if rec is None:
                    return self._respond(404, {"error": "not found"})
                return self._respond(200, rec)
            finally:
                self._exit()

        return self._respond(404, {"error": "not found"})

    def _respond(self, code: int, payload: dict) -> None:
        data = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):  # keep container logs quiet
        pass


def main() -> None:
    port = int(os.environ.get("PORT", "8000"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
