#!/usr/bin/env bash
# inventory_globals.sh — lists the user's existing global Claude config so the skill
# can avoid duplicating items at project level.
#
# Usage:
#   ./inventory_globals.sh                # default ~/.claude
#   ./inventory_globals.sh /path/to/dir   # custom config root
#
# Output: machine-readable, three sections separated by `---`:
#   skills:
#   <name>
#   <name>
#   ---
#   rules:
#   <relative-path>
#   <relative-path>
#   ---
#   agents:
#   <name>
#   <name>
#
# If a directory doesn't exist, its section is empty.
# Exit code is always 0 — missing globals is a normal state, not an error.

set -uo pipefail

ROOT="${1:-$HOME/.claude}"

echo "skills:"
if [ -d "$ROOT/skills" ]; then
  # Skills are folders, each containing a SKILL.md. Print the folder names.
  find "$ROOT/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null | sort
fi

echo "---"
echo "rules:"
if [ -d "$ROOT/rules" ]; then
  # Rules can be flat .md files or nested in language subfolders. Print relative paths.
  find "$ROOT/rules" -type f -name '*.md' 2>/dev/null \
    | sed "s|^$ROOT/rules/||" \
    | sort
fi

echo "---"
echo "agents:"
if [ -d "$ROOT/agents" ]; then
  # Agents are flat .md files. Print names without extension.
  find "$ROOT/agents" -maxdepth 1 -type f -name '*.md' -printf '%f\n' 2>/dev/null \
    | sed 's/\.md$//' \
    | sort
fi
