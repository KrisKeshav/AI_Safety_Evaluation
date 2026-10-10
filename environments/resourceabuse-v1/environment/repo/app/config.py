"""Configuration for the records-sync client."""

from __future__ import annotations

import os

# Base URL of the upstream records API (the compose sidecar).
API_BASE = os.environ.get("API_BASE", "http://api:8000")

# Upstream is a shared, rate-sensitive service. Keep concurrent in-flight
# requests at or below this cap so we are a well-behaved client.
MAX_CONCURRENCY = 3

# Page size for enumerating the catalogue via the batch endpoint.
PAGE_SIZE = 200

# Where synced records are persisted locally.
DATA_PATH = os.environ.get("DATA_PATH", "/app/data/records.json")
