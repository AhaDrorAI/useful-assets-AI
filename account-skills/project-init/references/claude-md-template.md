<!--
TEMPLATE: CLAUDE.md
PURPOSE: Project conventions and operational layer for Claude Code.
HOW TO USE: Read every section. Fill placeholders from PRD + interview answers + existing files.
            Delete this comment block before writing the final file.
            Delete any optional sections that don't apply (better to omit than leave empty).
-->

# [FILL: Project name from PRD title]

[FILL: One-sentence description — what is this and who is it for. Pull from PRD opening or first paragraph.]

> This file is the operational layer for AI agents working on this project. For *what* the project is and *why* it exists, see `PRD.md`. For the current state of work, see `project_state.md`.

## Stack

<!-- Be specific. "TypeScript" is not enough; "Next.js 15 + Supabase + Vercel" is. -->

- **Language(s):** [FILL]
- **Framework / runtime:** [FILL]
- **Database / persistence:** [FILL or "none"]
- **Deployment target:** [FILL]
- **Key services:** [FILL: auth provider, payment, LLM, email, etc., or "none yet"]

## Commands

<!-- Pull from package.json scripts, Makefile, etc. if they exist; otherwise from interview. -->

```bash
[FILL: build command, e.g. npm run build]      # build
[FILL: test command, e.g. npm test]            # tests
[FILL: lint command, e.g. npm run lint]        # lint
[FILL: typecheck command if applicable]        # typecheck
[FILL: dev/run command, e.g. npm run dev]      # local dev
```

If any of these aren't defined yet, mark as `# TODO` rather than inventing a command. The agent should not run made-up commands.

## Architecture (high-level)

<!-- 3-5 sentences. Where do the major pieces live, how do they talk to each other.
     Keep this short and durable; deep detail goes in planning.md (full set) or stays in code. -->

[FILL: synthesized from PRD scope + stack. If the PRD doesn't say much about architecture, write what's reasonable for the stack and add a "TODO: confirm" marker.]

## Conventions

<!-- These should be enforceable, not aspirational. If the user has Prettier/ESLint/Black/Ruff configured, link to those rather than restating them. -->

- **File organization:** [FILL or "follows framework defaults"]
- **Naming:** [FILL or "follows framework defaults"]
- **Imports:** [FILL or "follows framework defaults"]
- **Comments:** [FILL or "minimal — code should be self-explanatory; comments explain *why*, not *what*"]
- **Tests:** [FILL: where they live, e.g. "co-located as `*.test.ts`" or "in `tests/`"]

## Guardrails — things the agent must never do

<!-- This is the highest-leverage section. Pull directly from the user's interview answer about hard guardrails. -->

[FILL: list hard rules. Examples below — replace with the user's actual answers.]

- Never modify the database schema without an explicit user request.
- Never commit directly to `main`. Always work on a branch.
- Never call external APIs in tests — use mocks or fixtures.
- Never log secrets, API keys, or PII to stdout or files.
- [FILL: project-specific guardrails from interview]

## Workflow expectations

- Read `PRD.md` and `project_state.md` at the start of every session.
- Update `project_state.md` when finishing a chunk of work or stopping for the day.
- Log non-trivial decisions in `decisions.md` <!-- only mention this if full set --> with the tradeoff that was weighed.
- Move tasks through `tasks.md` as they're picked up and completed.
- For non-trivial features, plan first (write or update `planning.md`) before implementing. <!-- full set only -->
- When uncertain about scope or approach, stop and ask rather than guessing.

## Out of scope (from PRD)

<!-- Pulling out-of-scope here, in addition to PRD, makes it visible during agent loop work. -->

[FILL: bullet list of explicit non-goals from the PRD's out-of-scope section. If the PRD doesn't have one, omit this section.]

## References

- `PRD.md` — what we're building and why
- `planning.md` — flows, screens, system design <!-- full set only -->
- `tasks.md` — execution layer
- `decisions.md` — decision log <!-- full set only -->
- `project_state.md` — load this first at the start of every session
- `AGENTS.md` — entry point for non-Claude agents (Codex, Cursor, OpenCode)
