#!/usr/bin/env bash
# fetch_ecc.sh — clones the everything-claude-code repo (sparse) to a temp cache
# and prints the cache path on stdout. Designed to be called from the project-init skill.
#
# Usage:
#   ./fetch_ecc.sh                    # clone to a fresh temp dir, print path
#   ./fetch_ecc.sh /path/to/cache     # clone to a specific path, print path
#
# Exit codes:
#   0  — success, cache path printed on stdout
#   1  — git not available
#   2  — network/clone failure
#   3  — sparse checkout failure
#
# Notes:
#   - Uses --depth 1 --filter=blob:none for speed.
#   - Sparse-checks out only rules/, skills/, and agents/ — the directories project-init pulls from.
#   - Re-running with the same target path will refresh (git pull) instead of re-cloning.

set -euo pipefail

ECC_REPO="https://github.com/affaan-m/everything-claude-code.git"
CACHE_DIR="${1:-/tmp/ecc-cache-$(date +%s)}"

# Pre-flight
if ! command -v git >/dev/null 2>&1; then
  echo "fetch_ecc: git is not installed" >&2
  exit 1
fi

# Refresh path if it already exists; otherwise fresh clone
if [ -d "$CACHE_DIR/.git" ]; then
  echo "fetch_ecc: refreshing existing cache at $CACHE_DIR" >&2
  git -C "$CACHE_DIR" fetch --depth 1 origin >/dev/null 2>&1 || {
    echo "fetch_ecc: git fetch failed" >&2
    exit 2
  }
  git -C "$CACHE_DIR" reset --hard origin/HEAD >/dev/null 2>&1 || {
    echo "fetch_ecc: git reset failed" >&2
    exit 2
  }
else
  mkdir -p "$CACHE_DIR"
  echo "fetch_ecc: cloning $ECC_REPO to $CACHE_DIR" >&2
  git clone \
    --depth 1 \
    --filter=blob:none \
    --sparse \
    "$ECC_REPO" \
    "$CACHE_DIR" >/dev/null 2>&1 || {
    echo "fetch_ecc: clone failed (network? rate limit?)" >&2
    exit 2
  }
  git -C "$CACHE_DIR" sparse-checkout set rules skills agents >/dev/null 2>&1 || {
    echo "fetch_ecc: sparse-checkout failed" >&2
    exit 3
  }
fi

# Sanity check — at least rules/ should exist
if [ ! -d "$CACHE_DIR/rules" ]; then
  echo "fetch_ecc: cache is missing rules/ directory after checkout" >&2
  exit 3
fi

# Print cache path on stdout (the only thing on stdout — all logs go to stderr)
echo "$CACHE_DIR"
