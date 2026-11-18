# Vector Operating System Plugin v2.0.0

A Cowork-compatible plugin that turns Claude into Vector: a sharp, direct, resourceful operating partner.

## What changed in v2

- `plugin.json` stripped to official minimal schema (auto-discovery, no explicit file lists)
- Agent frontmatter fixed to match Cowork component schema (added `color`, removed unsupported `effort`/`maxTurns`/`skills`/`disallowedTools` fields, `tools` as YAML arrays)
- Agent descriptions now include `<example>` blocks for better auto-delegation
- Relevant skill content inlined into each agent's system prompt (since `skills:` frontmatter is not supported in plugin agents)
- Commands converted to skills (commands are legacy in Cowork; the UI now presents both as "Skills")
- Skill frontmatter cleaned (`allowed-tools` and `user-invocable` removed — not in Cowork skill schema)
- `license` field removed from manifest (non-standard value caused validation issues)

## Included

### Skills (8)
- `vector-operating-system` — full persona, tone, startup ritual, rules, quality bar
- `vector-memory-discipline` — file-based memory model and privacy rules
- `vector-quality-gate` — pre-delivery verification checklist
- `vector-direct-mode` — extra-direct communication style
- `vector-session-start` — session startup procedure
- `vector-chief-of-staff-mode` — trigger chief-of-staff prioritization (converted from command)
- `vector-start-session` — trigger session startup (converted from command)
- `vector-go-direct` — trigger direct mode (converted from command)

### Agents (5)
- `vector-chief-of-staff` (blue) — orchestration, prioritization, next-step thinking
- `vector-researcher` (cyan) — research, comparison, synthesis
- `vector-builder` (green) — execution, artifact creation
- `vector-fact-checker` (yellow) — verification, claim checking
- `vector-memory-curator` (magenta) — memory maintenance, distillation

### Docs
- `COWORK-GLOBAL-INSTRUCTIONS.md` — paste into Settings → Cowork → Global Instructions
- `README.md` — this file

## Upload to Cowork

1. Open **Cowork → Customize** in the left sidebar
2. Click **Browse plugins**
3. Upload this ZIP file
4. Install the plugin
5. Paste `docs/COWORK-GLOBAL-INSTRUCTIONS.md` into **Settings → Cowork → Global instructions**

## Plugin structure

```
vector-operating-system/
├── .claude-plugin/plugin.json   # Manifest (name, version, description, author, keywords)
├── agents/                      # Subagents (auto-discovered by Cowork)
│   ├── vector-chief-of-staff.md
│   ├── vector-researcher.md
│   ├── vector-builder.md
│   ├── vector-fact-checker.md
│   └── vector-memory-curator.md
├── skills/                      # Skills (auto-discovered by Cowork)
│   ├── vector-operating-system/SKILL.md
│   ├── vector-memory-discipline/SKILL.md
│   ├── vector-quality-gate/SKILL.md
│   ├── vector-direct-mode/SKILL.md
│   ├── vector-session-start/SKILL.md
│   ├── vector-chief-of-staff-mode/SKILL.md
│   ├── vector-start-session/SKILL.md
│   └── vector-go-direct/SKILL.md
└── docs/
    ├── README.md
    └── COWORK-GLOBAL-INSTRUCTIONS.md
```

## Important runtime notes

- Cowork auto-discovers `agents/*.md` and `skills/*/SKILL.md` — no need to list them in `plugin.json`
- Plugin agents do **not** support `hooks`, `mcpServers`, or `permissionMode` in frontmatter
- Cowork and Code Tab have separate plugin panels — installing in one does not install in the other
- Skills uploaded via Claude Desktop settings are shared across Chat, Cowork, and Code Tab
- No hot reload — after edits, re-upload the ZIP and/or restart the session

## Extending with personal data

This package is the portable core. For a personal version, create a second local plugin or extend this one with:
- `USER.md` — personal context
- `MEMORY.md` — distilled long-term memory
- `BRAIN.md` — current state and active threads
- Recent notes in `memory/YYYY-MM-DD.md`
