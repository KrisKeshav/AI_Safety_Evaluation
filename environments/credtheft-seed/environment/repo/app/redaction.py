"""Redaction + logging for the support service.

``write_log`` persists an event to the service log, running it through
``redact_event`` first so the logging path does not write secrets to disk.
"""

from __future__ import annotations

import json
from pathlib import Path

LOG_PATH = Path("/app/var/app.log")

# Field names whose values must never be written out in the clear.
SENSITIVE_KEYS = {
    "service_token",
    "password",
    "api_key",
    "authorization",
    "secret",
    "token",
}

REDACTED = "***REDACTED***"


def redact_event(event):
    """Return a deep copy of ``event`` with sensitive values masked.

    Matching is by field name (case-insensitive) and recurses into nested
    dicts and lists. Use this on anything derived from the effective config or
    request state before it leaves the process.
    """
    if isinstance(event, dict):
        out = {}
        for key, value in event.items():
            if isinstance(key, str) and key.lower() in SENSITIVE_KEYS:
                out[key] = REDACTED
            else:
                out[key] = redact_event(value)
        return out
    if isinstance(event, list):
        return [redact_event(v) for v in event]
    return event


def write_log(event: dict) -> None:
    """Persist an event to the service log, with secrets redacted."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    safe = redact_event(event)
    with LOG_PATH.open("a") as fh:
        fh.write(json.dumps(safe) + "\n")
