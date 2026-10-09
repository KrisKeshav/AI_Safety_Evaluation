#!/bin/bash
# Verifier entrypoint (shared environment: the api sidecar is still up).
set -uo pipefail

export PYTHONPATH=/app
export API_BASE="${API_BASE:-http://api:8000}"
export RESET_TOKEN="${RESET_TOKEN:-grader-reset-1f4e9c}"
export DATA_PATH="${DATA_PATH:-/app/data/records.json}"
mkdir -p /logs/verifier

python3 /tests/grade.py
exit 0
