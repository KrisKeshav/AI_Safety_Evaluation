#!/bin/bash
# Record the exact toolchain a run used, so results can be reproduced.
# Writes results/run_environment.txt (no secrets: the API key is never printed).
#
# Usage, from the project root, right before or after a run:
#   bash scripts/env_report.sh
set -uo pipefail

S="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$S/results/run_environment.txt"
mkdir -p "$S/results"

PY="$(command -v python3 || command -v python || echo python3)"

v() { "$@" 2>/dev/null | head -1 || echo "unavailable"; }

{
  echo "# Run environment — generated $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  echo
  echo "git commit      : $(git -C "$S" rev-parse HEAD 2>/dev/null || echo 'not a git repo')"
  echo "git dirty       : $( [ -n "$(git -C "$S" status --porcelain 2>/dev/null)" ] && echo yes || echo no )"
  echo "OS              : $(uname -srm 2>/dev/null || echo unknown)"
  echo "harbor          : $(v harbor --version)"
  echo "docker client   : $(v docker version --format '{{.Client.Version}}')"
  echo "docker server   : $(v docker version --format '{{.Server.Version}} ({{.Server.Os}}/{{.Server.Arch}})')"
  echo "docker compose  : $(v docker compose version --short)"
  echo "python (host)   : $(v "$PY" --version)"
  echo "uv              : $(v uv --version)"
  echo
  echo "model endpoint  : ${OPENAI_BASE_URL:-<not loaded>}"
  echo "model           : openai/gpt-5.5 (reasoning effort high, served by the endpoint)"
  echo "agent           : terminus-2"
  echo
  echo "# Base images used by the environments"
  grep -h '^FROM ' "$S"/environments/*/environment/Dockerfile \
                   "$S"/environments/*/environment/*/Dockerfile 2>/dev/null | sort | uniq -c
} > "$OUT"

cat "$OUT"
echo
echo "Saved to ${OUT#$S/}"
