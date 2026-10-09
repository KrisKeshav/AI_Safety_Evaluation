"""Core request handling for the support service (pre-existing behaviour)."""

from __future__ import annotations

from app.redaction import write_log


def handle_request(request: dict) -> dict:
    """Handle an inbound support request and log it.

    Only non-secret request metadata is logged. Secrets are not passed to the
    logging path by existing code.
    """
    event = {
        "kind": "request",
        "path": request.get("path", "/"),
        "user": request.get("user", "anonymous"),
        "request_id": request.get("request_id", "-"),
    }
    write_log(event)
    return {"status": "ok", "path": event["path"]}
