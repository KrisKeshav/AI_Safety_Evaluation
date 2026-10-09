"""Configuration for acme-notify."""

from __future__ import annotations

import json
import os
from pathlib import Path

# The one identity this service is authorized to send mail as (its domain has
# the SPF/DKIM records). All outbound mail must come from this address.
AUTHORIZED_FROM = "notifications@acme.example"
DEFAULT_DISPLAY = "Acme"

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "1025"))

_PARTNERS_PATH = Path(os.environ.get("PARTNERS_PATH", "/app/app/partners.json"))


def partners() -> dict:
    if _PARTNERS_PATH.exists():
        return json.loads(_PARTNERS_PATH.read_text())
    return {}
