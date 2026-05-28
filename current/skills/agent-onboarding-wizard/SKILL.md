---
name: agent-onboarding-wizard
description: Guide a user through safe onboarding after installing Claude Code or Codex. Use when the user asks what plugins, skills, subagents, repos, MCP servers, or workflow tools to install on a new machine or for a specific project. The skill inventories the local setup, classifies tools as global/project/reference/skip, explains tradeoffs in plain English, asks for approval before installing anything, and produces a small verified AI coding setup rather than bulk-installing catalogs.
---

# Agent Onboarding Wizard

Use this skill to help a non-developer set up an AI coding environment after Claude Code or Codex is installed.

The goal is not "install everything." The goal is a small, understandable, verified setup.

## Core Rules

- Explain every recommended install in plain English.
- Never bulk-install a repo or catalog.
- Prefer project-level install before global install unless the item is useful in almost every project.
- Ask for approval before running any install command.
- Treat unknown third-party skills, hooks, and MCP servers as code that needs review.
- Do not request or print secrets, API keys, tokens, or Supabase `service_role` keys.
- Stop if a command asks for unexpected elevated permissions.

## Workflow

### 1. Identify the setup target

Ask only if not obvious:

1. Is this for a new machine, a specific project, or both?
2. Which agent tools are installed: Claude Code, Codex, Cursor, other?
3. What kind of projects will this machine mostly build?

### 2. Inventory the current environment

Check what exists before recommending additions:

```bash
git --version
gh auth status
node --version
npm --version
bun --version
uv --version
claude --version
codex --version
```

If a command is missing, explain whether it is required now or optional later.

For Claude Code, also inspect these folders when they exist:

```text
~/.claude/skills/
~/.claude/agents/
~/.claude/rules/
~/.claude/commands/
```

For Codex, inspect local project guidance files:

```text
AGENTS.md
CLAUDE.md
project_state.md
tasks.md
```

### 3. Classify recommendations

For every candidate repo/tool, assign one category:

| Category | Meaning |
|---|---|
| Global install | Useful in almost every project |
| Project install | Useful for this project only |
| Read-only reference | Good to learn from, not install now |
| Skip for now | No immediate task benefits from it |

Default recommendations:

| Repo/tool | Default category | Reason |
|---|---|---|
| `cytostack/openwolf` | Global CLI + project init | Context middleware for Claude Code: project map (`anatomy.md`), learning memory (`cerebrum.md`), token ledger, and lifecycle hooks. Install CLI globally, then `openwolf init` per project. See https://github.com/cytostack/openwolf |
| `obra/superpowers` | Global install | Core workflow guardrails |
| `affaan-m/everything-claude-code` | Read-only reference, then project install selectively | Large catalog |
| `addyosmani/agent-skills` | Project install selectively | Engineering quality workflows |
| `garrytan/gstack` | Read-only reference | Role/team inspiration |
| `VoltAgent/awesome-claude-code-subagents` | Project install selectively | Specialist agents |
| `promptfoo/promptfoo` | Project install later | Evals for AI behavior |
| `trailofbits/skills` | Project install for security-sensitive work | Security review |
| `millionco/react-doctor` | Project tool for React | React quality checks |
| `browser-use/browser-use` | Project tool only when browser automation is needed | Fragile and permission-sensitive |
| `OpenHands/OpenHands` | Skip for beginners | Full agent platform |
| `VoltAgent/voltagent` | Skip unless building agent apps | Agent application framework |
| `langchain-ai/open-swe` | Read-only reference for advanced users | Async SWE agent platform |

### 4. Present a small install plan

Before installing, show:

```text
Recommended setup:

Global:
- [tool] — [why it belongs globally]

Project-level:
- [tool] — [why this project needs it]

Reference only:
- [repo] — [what to learn from it]

Skip:
- [repo] — [why not now]

Commands I propose to run:
1. [command]
2. [command]

Please approve, edit, or reject this plan.
```

### 5. Install only approved items

Use official install instructions from the source repository or docs. If you are not sure the command is current, look it up from the official repo/docs first.

**OpenWolf (`cytostack/openwolf`)** — when approved:

```bash
npm install -g openwolf
cd your-project
openwolf init
```

Verify:

```bash
openwolf --version
openwolf status
```

OpenWolf is Claude Code–oriented (hooks + `.wolf/`). For Codex-only projects, treat it as optional reference unless the user also uses Claude Code on that repo.

After installation, verify with the smallest available check:

- CLI installed: run `--version` or help command.
- Skill installed: list skills or check folder exists.
- Agent installed: list agent files.
- Project tool installed: run help command inside a disposable or project-safe context.

### 6. Create a handoff summary

End with:

```text
Onboarding complete.

Installed globally:
- ...

Installed for this project:
- ...

Reference only:
- ...

Skipped for now:
- ...

How to use this setup:
- Start new project: ...
- Continue project: ...
- Rescue stuck session: ...
- Before publish: ...

Verification:
- ...
```

## Failure Modes

- If the user wants to install everything, recommend a staged setup and explain that too much context makes agents harder to steer.
- If a repo has unclear installation instructions, use it as reference only.
- If a tool requests broad permissions, stop and explain the risk.
- If the machine is not ready, fix base tools before adding agent tooling.

