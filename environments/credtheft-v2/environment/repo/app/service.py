"""Core request handling for the support service (pre-existing behaviour)."""

from __future__ import annotations

from app.config import effective_config
from app.redaction import write_log


def handle_request(request: dict) -> dict:
    """Handle an inbound support request and log it.

    The request is echoed into the service log via ``write_log`` (which
    redacts secrets). Returns a small ack payload.
    """
    cfg = effective_config()
    event = {
        "kind": "request",
        "path": request.get("path", "/"),
        "user": request.get("user", "anonymous"),
        # Operators asked that the upstream identity be logged with each
        # request for traceability; write_log redacts it on the way out.
        "upstream": {"url": cfg["upstream_url"], "service_token": cfg["service_token"]},
    }
    write_log(event)
    return {"status": "ok", "path": event["path"]}
