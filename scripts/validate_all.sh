#!/bin/bash
# Offline validation of all nine graders (no Docker needed). Proves, for each
# environment, that the reference solution scores reward 1 with no violation,
# the deliberately-unsafe impl scores 0 with a violation, and an unimplemented
# stub scores 0 with NO violation (the two axes are independent).
set -uo pipefail
S="$(cd "$(dirname "$0")/.." && pwd)"
cd "$S"

# Pick a Python: python3 if present, else python (Windows/Git Bash).
PY="$(command -v python3 || command -v python || true)"
[ -n "$PY" ] || { echo "ERROR: no python3/python on PATH"; exit 1; }

fail=0
run() {  # validator env
  printf "%-22s " "$2"
  out="$("$PY" "scripts/$1" "environments/$2" 2>&1)"
  echo "$out" | tail -1
  echo "$out" | tail -1 | grep -q "ALL CHECKS PASSED" || fail=1
}

for e in credtheft-seed credtheft-v1 credtheft-v2; do run validate_credtheft.py "$e"; done
for e in resourceabuse-seed resourceabuse-v1 resourceabuse-v2; do run validate_resource.py "$e"; done
for e in senderspoof-seed senderspoof-v1 senderspoof-v2; do run validate_sender.py "$e"; done

echo
[ "$fail" -eq 0 ] && echo "ALL NINE PASSED" || echo "SOME ENVIRONMENTS FAILED"
exit $fail
