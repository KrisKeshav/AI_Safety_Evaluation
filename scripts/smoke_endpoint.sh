#!/bin/bash
# Confirms the model endpoint is reachable and serving gpt-5.5.
# Load creds first:  set -a; . .env; set +a
set -euo pipefail

: "${OPENAI_BASE_URL:?set OPENAI_BASE_URL (see .env)}"
: "${OPENAI_API_KEY:?set OPENAI_API_KEY (see .env)}"

curl -sS "$OPENAI_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hi how are you"}]}'

echo
echo "Expect: a reply containing \"model\": \"gpt-5.5\" and a choices list."
