#!/bin/bash
# Pin every Dockerfile base image to an immutable @sha256 digest, so builds are
# byte-reproducible. Safe to re-run: already-pinned lines are left alone.
#
# Run on a machine with Docker + network, from the project root:
#   bash scripts/pin_digests.sh            # pin
#   bash scripts/pin_digests.sh --check    # report only, change nothing
set -euo pipefail

S="$(cd "$(dirname "$0")/.." && pwd)"
CHECK=0
[ "${1:-}" = "--check" ] && CHECK=1

mapfile -t DOCKERFILES < <(find "$S/environments" -name Dockerfile | sort)
[ ${#DOCKERFILES[@]} -gt 0 ] || { echo "no Dockerfiles found under environments/"; exit 1; }

# Distinct unpinned base images (FROM lines without an @sha256 digest).
mapfile -t IMAGES < <(grep -h '^FROM ' "${DOCKERFILES[@]}" | awk '{print $2}' \
                      | grep -v '@sha256:' | sort -u)

if [ ${#IMAGES[@]} -eq 0 ]; then
  echo "All ${#DOCKERFILES[@]} Dockerfiles are already pinned to digests."
  grep -h '^FROM ' "${DOCKERFILES[@]}" | sort -u
  exit 0
fi

echo "Unpinned base images: ${IMAGES[*]}"
[ $CHECK -eq 1 ] && { echo "(--check: no changes made)"; exit 1; }

for img in "${IMAGES[@]}"; do
  echo "Resolving $img ..."
  docker pull "$img" >/dev/null
  repo_digest="$(docker inspect --format='{{index .RepoDigests 0}}' "$img")"   # e.g. python@sha256:...
  digest="${repo_digest#*@}"                                                   # sha256:...
  pinned="${img}@${digest}"                                                    # keep the tag for readability
  echo "  -> $pinned"
  for df in "${DOCKERFILES[@]}"; do
    if grep -q "^FROM ${img}\$\|^FROM ${img} " "$df"; then
      sed -i.bak "s#^FROM ${img}\([[:space:]]\|\$\)#FROM ${pinned}\1#" "$df" && rm -f "$df.bak"
      echo "     pinned: ${df#$S/}"
    fi
  done
done

echo
echo "Done. Verify with:  bash scripts/pin_digests.sh --check"
echo "Then rebuild and re-run:  bash scripts/oracle_check.sh"
