#!/bin/bash
# Run GPT-5.5 rollouts over all nine environments under Harbor.
# Prereqs: Docker running; Harbor installed; creds loaded:
#   set -a; . .env; set +a
# Then:  bash scripts/run_rollouts.sh
set -euo pipefail
export PYTHONUTF8=1   # Windows consoles: avoid cp1252 errors from Harbor spinners

: "${OPENAI_BASE_URL:?load .env first (set -a; . .env; set +a)}"
: "${OPENAI_API_KEY:?load .env first}"

S="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$S/jobs"

for rle in "$S"/environments/*/; do
  id="$(basename "$rle")"
  echo "=== rollout: $id ==="
  harbor run -p "$S/environments" -i "$id" -a terminus-2 -m openai/gpt-5.5 -k 6 \
       -o "$S/jobs/$id" --job-name rollouts -n 4 --yes
done

echo "Done. Per-trial reward.txt / result.json and logs are under $S/jobs/."
echo "Copy the evidence you keep into results/ (see README)."
