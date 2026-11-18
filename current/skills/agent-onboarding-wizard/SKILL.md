---
name: agent-onboarding-wizard
description: Set up Claude Code or Codex on a new machine or for a new project. Inventory the tools already installed, recommend only the additions a concrete task needs, install nothing without approval, and verify that each install works. Use when the user asks what plugins, skills, subagents, hooks, MCP servers or repos to install, says they just installed Claude Code or Codex, has a new laptop, wants a "starter setup", or asks to review a list of agent tools before installing them. Not for bootstrapping a project's files from a PRD; use new-project-from-prd for that.
metadata:
  last_reviewed: "2026-11-18"
  review_every_days: "90"
---

# Agent Onboarding Wizard

Help a non-developer set up an AI coding environment after Claude Code or Codex is installed.

The goal is a small, understandable, verified setup. The goal is not "install everything".

## Core Rules

- Explain every recommended install in plain English: what it does, why this user needs it, and what it can change on the machine.
- Never bulk-install a repo, catalog or marketplace.
- If an item is useful in almost every project, propose a global install. Otherwise, propose a project install.
- Ask for approval before you run any install command. Show the exact command first.
- Treat every third-party skill, hook, plugin and MCP server as code. Review it before you propose it (see "Review a third-party item" below).
- Do not request, print or store secrets: API keys, tokens, passwords, or Supabase `service_role` keys. If a tool needs one, tell the user where to enter it.
- If a command asks for elevated permissions you did not predict (`sudo`, an admin prompt, a write outside the project or home folder), stop. Explain the request and wait for the user.

## Workflow

### 1. Identify the setup target

Before you ask anything, check whether the conversation or the current folder already answers these questions. Ask only the questions that are still open, in one message:

1. Is this for a new machine, a specific project, or both?
2. Which agent tools are installed: Claude Code, Codex, Cursor, other?
3. What kind of projects will this machine mostly build?

Then identify one concrete task the user wants to complete and the obstacle that blocks it. A tool is only worth installing if it removes that obstacle. Distinguish a missing capability from a workflow problem that existing tools already solve. Keep the user's stated platform and project choices; do not ask the user to justify them.

If the user cannot name the outcome they want and `expert-problem-solving` is installed, use it to find the outcome and the smallest capability gap. If it is not installed, apply the same check directly.

### 2. Inventory the current environment

Run these checks before you recommend anything. A missing command is a finding, not an error:

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

For each missing command, say whether the user needs it now or can add it later.

For Claude Code, list these folders if they exist:

```text
~/.claude/skills/
~/.claude/agents/
~/.claude/rules/
~/.claude/commands/
~/.claude/plugins/
```

For Codex, check these locations if they exist:

```text
~/.codex/
~/.agents/skills/
.agents/skills/
AGENTS.md
```

For the current project, check `CLAUDE.md`, `project_state.md` and `tasks.md`.

### 3. Classify recommendations

Assign every candidate one category:

| Category | Meaning |
|---|---|
| Global install | Useful in almost every project |
| Project install | Useful for this project only |
| Read-only reference | Good to learn from; do not install now |
| Skip for now | No current task benefits from it |

The table below is a starting list, not a bundle. Reclassify each item against the user's task and inventory. The defaults were last checked on the `last_reviewed` date in this file's frontmatter. If you can browse, check that a repo still exists and is maintained before you recommend it.

| Repo/tool | Default category | Reason |
|---|---|---|
| `cytostack/openwolf` | Global CLI + project init | Context middleware for Claude Code: project map (`anatomy.md`), learning memory (`cerebrum.md`), token ledger, lifecycle hooks. See https://github.com/cytostack/openwolf |
| `obra/superpowers` | Global install | Core workflow guardrails |
| `affaan-m/everything-claude-code` | Read-only reference, then selective project install | Large catalog |
| `addyosmani/agent-skills` | Selective project install | Engineering quality workflows |
| `garrytan/gstack` | Read-only reference | Role and team inspiration |
| `VoltAgent/awesome-claude-code-subagents` | Selective project install | Specialist agents |
| `promptfoo/promptfoo` | Project install later | Evals for AI behaviour |
| `trailofbits/skills` | Project install for security-sensitive work | Security review |
| `millionco/react-doctor` | Project tool for React | React quality checks |
| `browser-use/browser-use` | Project tool only when browser automation is needed | Fragile and permission-sensitive |
| `OpenHands/OpenHands` | Skip for beginners | Full agent platform |
| `VoltAgent/voltagent` | Skip unless building agent apps | Agent application framework |
| `langchain-ai/open-swe` | Read-only reference for advanced users | Async software-engineering agent platform |

#### Review a third-party item

Before you propose a third-party skill, plugin, hook or MCP server, check and report:

1. **Source**: the repo URL and who maintains it.
2. **What runs**: any scripts, hooks or binaries it adds, and when they run. A hook that runs on every tool call or every prompt is a high-impact item; say so.
3. **What it can reach**: files outside the project, network hosts, secrets or environment variables.
4. **Activity**: if you can browse, the date of the last commit. If the last commit is older than 12 months, say the item may be unmaintained.

If you cannot read the item's files, classify it as "Read-only reference" and say why.

### 4. Present a small install plan

Before you install anything, show this plan:

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

If the plan has more than 5 installs, split it into stages. Install the first stage, verify it, then propose the next stage.

### 5. Install only approved items

Use the install instructions from the item's official repo or docs. If you cannot confirm that a command is current, look it up in the official source first. If you cannot look it up, show the command and say it is unverified.

**OpenWolf (`cytostack/openwolf`)**, when approved:

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

OpenWolf works through Claude Code hooks and a `.wolf/` folder. For a Codex-only project, classify it as optional reference.

After each install, run two kinds of check:

- **Discovery check**: the tool is found. Examples: `--version` works; the host lists the skill; the agent file exists.
- **Functional check**: the tool does the job the user needed. Run one small, project-safe task that uses the capability. A folder that exists proves only discovery.

Report discovery checks and functional checks separately. For each check, state whether it ran, what happened, and what remains untested.

### 6. Create a handoff summary

If every essential capability passed its functional check, start the summary with "Onboarding complete." If any essential capability is still blocked or untested, start it with "Onboarding partly complete" and name the blocker first.

```text
Onboarding complete. | Onboarding partly complete — blocked: [item]

Installed globally:
- ...

Installed for this project:
- ...

Reference only:
- ...

Skipped for now:
- ...

How to use this setup:
- Start a new project: ...
- Continue a project: ...
- Rescue a stuck session: ...
- Before you publish: ...

Verification:
- Discovery: ...
- Functional: ...
- Not tested: ...
```

## Failure Modes

- If the user wants to install everything, recommend a staged setup. Explain that too many skills and hooks make an agent harder to steer and use more context.
- If a repo has unclear install instructions, classify it as reference only.
- If a tool requests broad permissions, stop and explain the risk. Broad means: `sudo` or admin rights, write access outside the project and home folder, a hook on every tool call, or access to secrets.
- If base tools are missing (git, node, the agent CLI itself), fix those before you add agent tooling.
