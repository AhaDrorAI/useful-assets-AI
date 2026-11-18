#!/usr/bin/env bash
# inventory_globals.sh — lists the user's existing global Claude config so the skill
# can avoid duplicating items at project level.
#
# Usage:
#   ./inventory_globals.sh                # default ~/.claude
#   ./inventory_globals.sh /path/to/dir   # custom config root
#
# Output: machine-readable, three sections separated by `---`:
#   skills:   <folder name per line>
#   rules:    <path relative to rules/ per line>
#   agents:   <name without .md per line>
#
# If a directory doesn't exist, its section is empty.
# Exit code is always 0 — missing globals is a normal state, not an error.
#
# Portable: runs on GNU/Linux, macOS (BSD tools) and Git Bash. Avoids GNU-only
# flags such as `find -printf`, which fail silently on macOS.

set -uo pipefail

ROOT="${1:-$HOME/.claude}"

echo "skills:"
if [ -d "$ROOT/skills" ]; then
  for d in "$ROOT/skills"/*/; do
    [ -d "$d" ] && basename "$d"
  done | sort
fi

echo "---"
echo "rules:"
if [ -d "$ROOT/rules" ]; then
  find "$ROOT/rules" -type f -name '*.md' 2>/dev/null \
    | sed "s|^$ROOT/rules/||" \
    | sort
fi

echo "---"
echo "agents:"
if [ -d "$ROOT/agents" ]; then
  for f in "$ROOT/agents"/*.md; do
    [ -f "$f" ] && basename "$f" .md
  done | sort
fi
exit 0
