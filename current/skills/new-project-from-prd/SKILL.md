---
name: new-project-from-prd
description: Start a new software project from a PRD, optional SPEC, or a clear product idea. Use when the user says they want to open, init, bootstrap, scaffold, or kickstart a project with Claude Code, Codex, GitHub, PRD/SPEC, repo setup, CLAUDE.md, AGENTS.md, planning, tasks, decisions, project state, and first working slice. Upgrades project-init behavior by supporting PRD-only, PRD+SPEC, or guided PRD creation, selecting relevant skills/subagents safely, creating GitHub repo flow, and stopping before risky installs or broad implementation.
---

# New Project From PRD

Use this skill to turn a product idea, PRD, or PRD plus SPEC into a project that an AI coding agent can build safely.

The output is not just files. The output is a project operating system:

- `PRD.md`
- `SPEC.md` when available or needed
- `CLAUDE.md`
- `AGENTS.md`
- `planning.md`
- `tasks.md`
- `decisions.md`
- `project_state.md`
- `.claude/` project harness when useful
- GitHub repo setup plan
- first working implementation slice

## Core Rules

- Do not start coding before the project has a clear goal, scope, and verification plan.
- If the user has a PRD, preserve it as source material.
- If the user has no PRD, run a short PRD interview first.
- If the user has a SPEC, use it to constrain implementation.
- If PRD and SPEC conflict, stop and list the conflict.
- Never overwrite existing project files. Write `*.proposed.md` when a file exists.
- Initialize git if missing, but do not commit unless the user asks.
- Ask before creating a GitHub repo.
- Ask before installing project skills, subagents, hooks, or MCP servers.
- Prefer one vertical slice over broad scaffolding.

## Flow

### 1. Confirm project root

Verify the current working directory is the intended project root.

Read root-level files:

```text
PRD.md
SPEC.md
README.md
package.json
pyproject.toml
go.mod
Cargo.toml
.env.example
```

Also inspect whether these already exist:

```text
CLAUDE.md
AGENTS.md
planning.md
tasks.md
decisions.md
project_state.md
.claude/
```

### 2. Determine input mode

Use one of three modes:

| Mode | Condition | Action |
|---|---|---|
| PRD + SPEC | Both files exist | Treat PRD as product intent and SPEC as build contract |
| PRD only | PRD exists, SPEC missing | Create a proposed SPEC if implementation details are needed |
| Idea only | No PRD exists | Run a short PRD interview and create `PRD.md` |

For idea-only mode, ask at most seven questions:

1. Who is this for?
2. What problem should it solve?
3. What should the first version do?
4. What is explicitly out of scope?
5. What platform should it run on?
6. Any preferred stack or services?
7. What counts as a visible success in the first session?

### 3. Choose starter or full structure

Use starter structure for small tools, landing pages, demos, or one-flow apps:

- `CLAUDE.md`
- `AGENTS.md`
- `tasks.md`
- `project_state.md`

Use full structure for multi-flow apps, auth, database, payments, LLM workflows, production deployment, or unclear architecture:

- starter files
- `planning.md`
- `decisions.md`
- optional `SPEC.md`

State the decision in one sentence and allow override.

### 4. Generate project operating files

Fill files with real project-specific content:

- `CLAUDE.md`: project commands, conventions, guardrails, verification rules
- `AGENTS.md`: portable instructions for Codex and other coding agents
- `planning.md`: flows, screens/surfaces, data sketch, system design, implementation phases
- `tasks.md`: now/next/later execution list
- `decisions.md`: decisions made and open decisions
- `project_state.md`: current status, last known good state, next action
- `SPEC.md`: technical build contract if needed

Do not leave `[FILL]` placeholders unless explicitly listed in the final report.

### 5. Select agent tooling

Do not install a fixed bundle. Classify each candidate:

| Candidate | Use when |
|---|---|
| `obra/superpowers` | Any real project; workflow discipline |
| `affaan-m/everything-claude-code` | Need project-specific Claude skills/rules/hooks |
| `addyosmani/agent-skills` | Need planning, review, docs, testing discipline |
| `VoltAgent/awesome-claude-code-subagents` | Need specialist subagents |
| `trailofbits/skills` | Auth, payments, secrets, security, sensitive data |
| `promptfoo/promptfoo` | AI behavior must be regression-tested |
| `millionco/react-doctor` | React/Next project after first UI exists |
| `browser-use/browser-use` | Product needs real browser automation |
| `codegraph` | Repo is large enough that structure discovery is costly |

Show the project-specific recommendation and ask before installing/copying anything into `.claude/`.

### 6. GitHub repo setup

If the user wants GitHub:

1. Check `git status`.
2. Initialize git if missing.
3. Ensure `.gitignore` includes secrets and local overrides:

```text
.env
.env.local
node_modules/
.venv/
__pycache__/
.DS_Store
.claude/settings.local.json
```

4. Ask for repo name and visibility if missing.
5. Use GitHub CLI only after approval.

Do not push until the user has reviewed generated files.

### 7. First working slice

Define one first slice that proves the project can run.

Good first slices:

- app boots locally
- one screen renders
- one core form saves data
- one API route returns real response
- one AI workflow runs against a test fixture

Bad first slices:

- build the entire backend
- design all screens
- install every tool
- create a full database before any user-visible flow exists

### 8. Final report

End with:

```text
Project bootstrap complete.

Input mode:
- PRD + SPEC / PRD only / Idea only

Created or proposed:
- ...

Recommended agent tooling:
- Global:
- Project-level:
- Reference only:
- Skip:

First working slice:
- ...

Verification:
- ...

Next command/session prompt:
- ...
```

## Rescue Mode

If the user says they are stuck during project start:

1. Stop adding files.
2. Read `project_state.md`, `tasks.md`, and git status.
3. Identify the smallest blocker.
4. Propose three next steps.
5. Execute only the first approved step.

