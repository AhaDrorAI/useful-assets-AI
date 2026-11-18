<!--
TEMPLATE: AGENTS.md
PURPOSE: Vendor-neutral entry point for any AI coding agent (Codex, Cursor, OpenCode, Gemini, etc.).
HOW TO USE: Keep this file lean. The full conventions live in CLAUDE.md; this file points there
            and surfaces just the operational essentials any agent needs.
            Delete this comment block before writing the final file.
ABOUT AGENTS.md: AGENTS.md is an emerging convention adopted by Codex, Cursor, OpenCode, and others
            as a vendor-neutral parallel to Claude Code's CLAUDE.md. Keeping both files in sync
            (with CLAUDE.md as the source of truth) gives the project portability across agents.
-->

# [FILL: Project name from PRD title]

[FILL: One-sentence description — same one used in CLAUDE.md.]

## For agents working on this project

This project's full operational conventions, guardrails, and workflow expectations live in **`CLAUDE.md`**. Read that file as your primary context. This file (`AGENTS.md`) exists for cross-tool portability — agents that don't natively read `CLAUDE.md` should treat `CLAUDE.md` as the source of truth and use the essentials below.

## Essentials

### Stack

[FILL: 1-line summary of the stack. e.g. "Next.js 15 + Supabase + Vercel."]

### Commands

```bash
[FILL: build command]      # build
[FILL: test command]       # tests
[FILL: lint command]       # lint
[FILL: dev command]        # local dev
```

### Hard rules

<!-- Mirror the most critical guardrails from CLAUDE.md. Keep this short — 3-5 bullets max.
     The full list is in CLAUDE.md. -->

- [FILL: most important guardrail #1]
- [FILL: most important guardrail #2]
- [FILL: most important guardrail #3]
- Read `PRD.md` and `project_state.md` before making changes.
- When uncertain about scope, stop and ask — don't guess.

### Where to read first

1. `PRD.md` — what's being built and why
2. `CLAUDE.md` — full conventions and guardrails
3. `project_state.md` — current status, where we are right now
4. `tasks.md` — what's queued up
