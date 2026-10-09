#!/bin/bash
# Self-check each environment under the REAL Harbor harness (Docker required),
# in both directions:
#   1. reference solution (solution/solve.sh)      -> expect reward 1 (clean)
#   2. deliberately-unsafe (validation/unsafe_solve.sh, swapped in temporarily)
#                                                    -> expect reward 0 (caught)
# The oracle agent runs solve.sh, then the verifier grades it.
#
# Usage:  bash scripts/oracle_check.sh [env-name ...]   (default: all)
set -euo pipefail
export PYTHONUTF8=1   # Windows consoles: avoid cp1252 errors from Harbor spinners

S="$(cd "$(dirname "$0")/.." && pwd)"

# Safety net: this script temporarily swaps unsafe_solve.sh into
# solution/solve.sh. If it is interrupted mid-run, restore every swapped file
# so an unsafe solution is never left behind in the package.
cleanup() {
  while IFS= read -r -d '' bak; do
    mv -f "$bak" "${bak%.bak}"
  done < <(find "$S/environments" -name 'solve.sh.bak' -print0 2>/dev/null)
}
trap cleanup EXIT INT TERM

ENVS=("$@")
if [ ${#ENVS[@]} -eq 0 ]; then
  mapfile -t ENVS < <(cd "$S/environments" && ls -d */ | sed 's#/##')
fi

run_oracle() {  # id outdir
  harbor run -p "$S/environments" -i "$1" -a oracle -o "$2" --job-name oracle --yes >/dev/null 2>&1 || true
  find "$2" -name reward.txt -exec cat {} \; 2>/dev/null | head -1
}

for id in "${ENVS[@]}"; do
  env_dir="$S/environments/$id"
  echo "=== $id ==="
  r_safe="$(run_oracle "$id" "$S/jobs/_check/$id/safe")"
  echo "  reference solution reward: ${r_safe:-<none>}  (want 1)"

  # Swap unsafe impl in as the solution, re-run oracle, then restore.
  cp "$env_dir/solution/solve.sh" "$env_dir/solution/solve.sh.bak"
  cp "$env_dir/validation/unsafe_solve.sh" "$env_dir/solution/solve.sh"
  r_unsafe="$(run_oracle "$id" "$S/jobs/_check/$id/unsafe")"
  mv "$env_dir/solution/solve.sh.bak" "$env_dir/solution/solve.sh"
  echo "  unsafe solution reward:    ${r_unsafe:-<none>}  (want 0)"
done
