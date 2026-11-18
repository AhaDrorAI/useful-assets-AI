# Vector Private Memory Plugin

> **In this public repository, only the skill and the manifest are tracked.** `USER.md`, `MEMORY.md`, `BRAIN.md` and `memory/` are listed in the root `.gitignore`, and CI fails if one is ever committed. Add them locally before you build the ZIP for your own machine.

This is the **local-only personal memory layer** for Vector.

## Included
- `USER.md`
- `MEMORY.md`
- `BRAIN.md`
- selected recent notes in `memory/`
- a guarded skill for safe memory usage

## Purpose
Use this alongside `vector-operating-system` when you want Claude Cowork/Desktop to behave much more like your real Vector setup.

## Safety model
This plugin assumes:
- it stays on your machine
- it is not shared with others
- it is used with strict privacy boundaries

## Install order
1. Install `vector-operating-system-plugin.zip`
2. Install `vector-private-memory-plugin.zip`
3. Paste the Cowork global instructions from the core plugin into **Settings → Cowork → Global instructions**
4. In private chats, invoke `/vector-private-memory:vector-private-memory` when continuity matters

## Important warning
Do **not** upload this plugin to an org marketplace.
Do **not** share this ZIP casually.
It contains personal context files.

## Good use cases
- private 1:1 chats
- ongoing projects
- continuity across sessions
- planning, follow-ups, and decision support

## Bad use cases
- org-wide distribution
- shared team spaces
- group contexts
- public-facing plugin repositories

## Best paired with
Use together with the core plugin's `/vector-operating-system:vector-session-start` skill, then invoke `/vector-private-memory:vector-private-memory` when private continuity is relevant.
