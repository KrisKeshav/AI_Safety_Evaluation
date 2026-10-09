#!/bin/bash
# Verifier entrypoint. Runs in a fresh, pristine copy of the environment with
# the agent's final app/ overlaid. stdlib-only grader; no network needed.
set -uo pipefail

export PYTHONPATH=/app
export ACME_SECRET_FILE=/etc/acme/secret.json
mkdir -p /logs/verifier

python3 /tests/grade.py
exit 0
