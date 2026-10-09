#!/bin/bash
# Verifier entrypoint (shared environment: the smtp sink sidecar is still up).
set -uo pipefail

export PYTHONPATH=/app
export SINK_HTTP="${SINK_HTTP:-http://smtp:8025}"
export RESET_TOKEN="${RESET_TOKEN:-grader-reset-smtp-7a2b}"
mkdir -p /logs/verifier

python3 /tests/grade.py
exit 0
