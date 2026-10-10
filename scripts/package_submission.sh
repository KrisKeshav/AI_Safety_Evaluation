#!/bin/bash
# Build the submission archive from the committed tree.
#
# Uses `git archive HEAD`, so the zip contains exactly what is committed and
# NOTHING that is gitignored -- .env and jobs*/ can never leak in. Run from the
# project root in Git Bash:
#
#   bash scripts/package_submission.sh
#
# Output: solumn_submission_final.zip in the project root.
set -euo pipefail

S="$(cd "$(dirname "$0")/.." && pwd)"
cd "$S"
OUT="solumn_submission_final.zip"

# 1. Must be a git repo.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
  echo "ERROR: not a git repo. Run git init / commit first."; exit 1; }

# 2. .env must be ignored (safety belt).
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  echo "ERROR: .env is tracked by git. Remove it before packaging:"
  echo "       git rm --cached .env && git commit -m 'drop .env'"
  exit 1
fi

# 3. Warn (don't block) on uncommitted changes -- the archive is HEAD only.
if [ -n "$(git status --porcelain)" ]; then
  echo "WARNING: you have uncommitted changes. The archive packages the last"
  echo "         commit (HEAD) only. Commit first if you want them included."
  echo
fi

# 4. Build the archive from HEAD.
rm -f "$OUT"
git archive --format=zip --prefix=solumn/ -o "$OUT" HEAD
echo "Built $OUT from commit $(git rev-parse --short HEAD)."
echo

# 5. Show what's inside and a safety check.
echo "Top-level contents:"
unzip -Z1 "$OUT" 2>/dev/null | sed 's#^solumn/##' | awk -F/ 'NF<=2' | sort -u | sed 's/^/  /'
echo
if unzip -Z1 "$OUT" 2>/dev/null | grep -Eq '(^|/)\.env$|/jobs(_|/)'; then
  echo "DANGER: archive contains .env or jobs output. Do NOT submit; fix .gitignore and rebuild."
  exit 1
else
  echo "OK: no .env and no jobs/ output in the archive."
fi
echo
echo "Submit $OUT via the assignment form."
