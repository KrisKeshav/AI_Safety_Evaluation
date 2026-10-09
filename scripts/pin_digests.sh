#!/bin/bash
# Convert the pinned patch tags in every Dockerfile to immutable @sha256
# digests, so builds are byte-reproducible. Run on a machine with Docker and
# network access, from the project root:  bash scripts/pin_digests.sh
set -euo pipefail

BASE="python:3.12.7-slim-bookworm"

echo "Pulling $BASE to resolve its digest..."
docker pull "$BASE" >/dev/null
DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' "$BASE")
# DIGEST looks like: python@sha256:....
echo "Resolved: $DIGEST"

# Rewrite every Dockerfile FROM line that uses the tag.
while IFS= read -r -d '' df; do
  if grep -q "FROM ${BASE}" "$df"; then
    sed -i.bak "s#FROM ${BASE}#FROM ${DIGEST}#g" "$df" && rm -f "$df.bak"
    echo "pinned: $df"
  fi
done < <(find environments -name Dockerfile -print0)

echo "Done. Review the diff, rebuild, and re-run the validators before submitting."
