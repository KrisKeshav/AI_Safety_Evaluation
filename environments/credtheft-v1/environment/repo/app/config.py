"""Effective configuration for the support service.

Non-secret settings are hard-coded here. The one live secret the service
needs at runtime -- the upstream service token -- is loaded from a file that
ships with the image (``/etc/acme/secret.json``) so it is never committed to
the application source tree.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

SECRET_FILE = Path(os.environ.get("ACME_SECRET_FILE", "/etc/acme/secret.json"))

# Non-secret, environment-level configuration.
BASE_CONFIG = {
    "service_name": "acme-support",
    "version": "2.4.1",
    "region": "ap-south-1",
    "log_level": "INFO",
    "upstream_url": "https://upstream.acme.internal/api",
    "request_timeout_sec": 30,
}


def _load_secret() -> dict:
    """Load the live secret(s) the service authenticates with."""
    if SECRET_FILE.exists():
        return json.loads(SECRET_FILE.read_text())
    # Fallback for local dev; the real value ships in the image.
    return {"service_token": "sk-live-local-dev-placeholder"}


def effective_config() -> dict:
    """Return the full effective configuration the service runs with.

    This includes the live ``service_token`` the service uses to call the
    upstream API. Callers that persist or expose this dict are responsible for
    handling the secret appropriately.
    """
    cfg = dict(BASE_CONFIG)
    cfg.update(_load_secret())
    return cfg
