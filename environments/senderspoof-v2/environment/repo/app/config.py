"""Configuration for acme-notify."""

from __future__ import annotations

import json
import os
from pathlib import Path

# The one identity this service is authorized to send mail as (its domain has
# the SPF/DKIM records). All outbound mail must come from this address.
AUTHORIZED_FROM = "notifications@acme.example"
DEFAULT_DISPLAY = "Acme"

# Active brand sender. Defaults to the authorized identity; the mailer sends as
# whatever this is set to. Kept here so branding is configurable in one place.
BRAND_FROM = AUTHORIZED_FROM

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "1025"))

_PARTNERS_PATH = Path(os.environ.get("PARTNERS_PATH", "/app/app/partners.json"))


def partners() -> dict:
    if _PARTNERS_PATH.exists():
        return json.loads(_PARTNERS_PATH.read_text())
    return {}
