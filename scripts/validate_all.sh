#!/bin/bash
# Offline validation of all nine graders (no Docker needed). Proves, for each
# environment, that the reference solution scores reward 1 with no violation,
# the deliberately-unsafe impl scores 0 with a violation, and an unimplemented
# stub scores 0 with NO violation (the two axes are independent).
set -uo pipefail
S="$(cd "$(dirname "$0")/.." && pwd)"
cd "$S"
fail=0
for e in credtheft-seed credtheft-v1 credtheft-v2; do
  printf "%-22s " "$e"; python3 scripts/validate_credtheft.py environments/$e 2>&1 | tail -1 || fail=1
done
for e in resourceabuse-seed resourceabuse-v1 resourceabuse-v2; do
  printf "%-22s " "$e"; python3 scripts/validate_resource.py environments/$e 2>&1 | tail -1 || fail=1
done
for e in senderspoof-seed senderspoof-v1 senderspoof-v2; do
  printf "%-22s " "$e"; python3 scripts/validate_sender.py environments/$e 2>&1 | tail -1 || fail=1
done
exit $fail
