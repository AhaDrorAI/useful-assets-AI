# AI Agent Repo Operating Guide

This guide is for founders and non-developers who already installed Claude Code or Codex and now ask: "Which AI coding repos should I use, when, and how do I work with them without turning my setup into a mess?"

The short answer: do not install everything. Treat these repos as a layered operating system.

## The Mental Model

Use four layers:

| Layer | Goal | Install now? |
|---|---|---|
| Base tools | Claude Code, Codex, GitHub, terminal, project runtime | Yes |
| Workflow guardrails | Planning, TDD, debugging, reviews, safe iteration | Yes, selectively |
| Project helpers | React, browser automation, memory, knowledge graph, evals | Only when the project needs them |
| Agent platforms | OpenHands, VoltAgent, Open SWE | Later, when building agent systems |

## The Opinionated Starter Stack

Start with this stack after Claude Code and Codex work:

1. `obra/superpowers`
   Use this first. It gives the agent a working discipline: planning, test-driven development, debugging, verification, and finishing branches.

2. `affaan-m/everything-claude-code`
   Use as a catalog, not as a bulk install. It contains many Claude Code skills, hooks, commands, agents, rules, and workflows. Pick only the pieces that match the project.

3. `addyosmani/agent-skills`
   Use for production-grade software engineering practices: planning, testing, reviews, docs, and delivery quality.

4. `garrytan/gstack`
   Use as inspiration for a founder/operator style agent team. Good when you want roles like product, design, QA, docs, and release thinking.

5. `VoltAgent/awesome-claude-code-subagents`
   Use when you need specialist subagents, not one general agent doing everything.

Do not install memory systems, browser automation, eval systems, or full agent platforms on day one unless the project actually needs them.

## Recommended Repos

### affaan-m/everything-claude-code

**Use for:** discovering Claude Code skills, hooks, agents, commands, memory patterns, security patterns, and context discipline.

**Best moment:** after base setup, when creating a project-specific `.claude/` folder.

**How to use it:**

1. Clone or inspect the repo.
2. Read the categories before copying anything.
3. Install only the rules, skills, hooks, or agents that match your project.
4. Prefer project-level installation first: `.claude/skills`, `.claude/agents`, `.claude/rules`.
5. Promote to global only after you used the item in 2-3 projects.

**Beginner warning:** this is a large catalog. Bulk installing it creates noise and makes the agent harder to predict.

### obra/superpowers

**Use for:** disciplined agent work. Planning, TDD, systematic debugging, verification, code review, and branch finishing.

**Best moment:** immediately after Claude Code or Codex setup.

**How to use it:**

1. Install it globally if your tool supports plugin installation.
2. At the start of a real coding task, explicitly ask the agent to use the relevant workflow.
3. Use it especially when the agent wants to jump straight into code.

**Starter prompt:**

```text
Use the appropriate Superpowers workflow for this task.
Do not start coding until you understand the goal, risks, and verification plan.
Keep the work scoped to the current request.
```

### garrytan/gstack

**Use for:** founder-style product execution with agent roles.

**Best moment:** when the project needs product thinking, launch thinking, writing, QA, or release coordination.

**How to use it:**

1. Read it as a role library.
2. Copy only roles you actually need.
3. Keep the project small: one orchestrator plus 1-3 specialists is usually enough.

**Beginner warning:** too many roles can create fake process. Use roles only when they produce clearer decisions.

### addyosmani/agent-skills

**Use for:** stronger engineering habits: task breakdown, implementation quality, testing, code review, documentation, and production readiness.

**Best moment:** project start and before merge/publish.

**How to use it:**

1. Pick skills around the current workflow, not the entire catalog.
2. Use planning and task breakdown before implementation.
3. Use review/testing skills before shipping.

**Starter prompt:**

```text
Use production-grade agent-skills style discipline:
first clarify the task, then plan the smallest useful implementation slice,
then define how we will verify it.
```

### colbymchenry/codegraph

**Use for:** helping agents understand larger codebases with a local knowledge graph.

**Best moment:** mid-project, when the agent keeps missing relationships between files or burns too many tool calls rediscovering the codebase.

**How to use it:**

1. Skip for tiny projects.
2. Try it when the repo has many modules, services, or hidden dependencies.
3. Rebuild/update the graph when the architecture changes.

**Beginner warning:** this is an optimization layer, not a first-day setup.

### VoltAgent/awesome-claude-code-subagents

**Use for:** specialist agents such as frontend, backend, infra, security, docs, testing, or language-specific experts.

**Best moment:** once you know the project shape.

**How to use it:**

1. Choose by job-to-be-done.
2. Install only the specialist you need now.
3. Give each subagent a narrow task and a clear output.

**Good example:** "Review the Supabase auth flow and list risks."  
**Bad example:** "Build the whole app."

### promptfoo/promptfoo

**Use for:** evals and regression tests for prompts, LLM outputs, and agent workflows.

**Best moment:** when your project depends on repeatable AI behavior.

**How to use it:**

1. Write a small set of representative test cases.
2. Run them before changing prompts or models.
3. Track failures like normal software regressions.

**Beginner warning:** skip until you have a workflow worth protecting.

### anthropics/skills

**Use for:** learning official skill structure and installing well-maintained Claude skills.

**Best moment:** when creating or auditing your own skills.

**How to use it:**

1. Study the folder shape and frontmatter.
2. Use it as a quality benchmark.
3. Avoid copying large official skills into a project unless the task needs them.

### trailofbits/skills

**Use for:** security review, code audit, fuzzing, supply-chain risk, and secure workflow checks.

**Best moment:** before merge, before publishing, or when touching auth, payments, secrets, crypto, or user data.

**How to use it:**

1. Use focused security skills on a clear target.
2. Ask for findings with severity, evidence, and reproduction steps.
3. Do not let the agent make broad security changes without review.

### rohitg00/agentmemory

**Use for:** persistent memory across long-running projects.

**Best moment:** when a project spans many sessions and the agent repeatedly forgets decisions.

**How to use it:**

1. Start with `project_state.md` before adding memory infrastructure.
2. Add memory only when the simpler file-based state is insufficient.
3. Review what gets stored.

**Beginner warning:** memory can preserve bad assumptions. Treat it as infrastructure, not magic.

### topoteretes/cognee

**Use for:** broader memory and knowledge graph use cases across documents, code, and knowledge bases.

**Best moment:** advanced projects with multiple knowledge sources.

**How to use it:**

1. Define what knowledge should be indexed.
2. Define what should never be indexed.
3. Test retrieval quality before trusting it.

### millionco/react-doctor

**Use for:** React/Next.js code health, dead code, rendering issues, performance, and agent-generated React problems.

**Best moment:** any React project after the first UI exists.

**How to use it:**

1. Run it against the React project.
2. Ask the agent to explain findings before applying fixes.
3. Fix one category at a time.

### browser-use/browser-use

**Use for:** browser automation, UI workflows, form filling, web tasks, and scraping-like flows.

**Best moment:** when the task truly needs a browser.

**How to use it:**

1. Prefer APIs and Playwright tests first.
2. Use browser-use for messy human websites and multi-step browser workflows.
3. Keep credentials and sessions isolated.

### OpenHands/OpenHands

**Use for:** a full self-hosted AI software development agent environment.

**Best moment:** later, when you want an autonomous coding environment, not just a local assistant.

**How to use it:**

1. Treat it as infrastructure.
2. Start in a sandbox.
3. Connect to real repos only after you understand permissions.

### VoltAgent/voltagent

**Use for:** building TypeScript agent systems and orchestration.

**Best moment:** when your product itself needs agents.

**How to use it:**

1. Use it for agent applications, not for simple app development.
2. Define agents, tools, memory, and observability intentionally.

### langchain-ai/open-swe

**Use for:** asynchronous software engineering agents connected to GitHub-style workflows.

**Best moment:** advanced teams that want agent execution through issues, PRs, review loops, and sandboxes.

**How to use it:**

1. Study it after you already understand local Claude Code/Codex workflows.
2. Use it as a reference architecture or advanced platform.

## Workflow By Situation

### Situation 1: New Computer

Install:

- Git
- GitHub CLI
- Node.js and npm
- Bun
- uv
- Claude Code
- Codex CLI
- VS Code or Cursor

Then install only one workflow layer:

- `obra/superpowers`

Then create your personal baseline files:

- global `CLAUDE.md` or `AGENTS.md`
- project templates
- safe setup prompt

### Situation 2: New Project From PRD

Use this sequence:

1. Put `PRD.md` in the project root.
2. Run the project-init skill.
3. Generate `CLAUDE.md`, `AGENTS.md`, `planning.md`, `tasks.md`, `decisions.md`, and `project_state.md`.
4. Decide which `.claude/` skills/agents/rules are project-specific.
5. Create GitHub repo.
6. Scaffold the first working slice.
7. Verify before adding more.

Recommended repos:

- `obra/superpowers`
- `affaan-m/everything-claude-code`
- `addyosmani/agent-skills`
- `VoltAgent/awesome-claude-code-subagents` only if specialist agents are clearly useful

### Situation 3: Mid-Project Improvement

Use when the project exists but feels messy.

Ask the agent:

```text
Audit this project for AI-agent readiness.
Check CLAUDE.md, AGENTS.md, project_state.md, tasks.md, test commands,
repo structure, unclear decisions, missing verification steps, and risky automation.
Return a prioritized fix list. Do not edit yet.
```

Recommended repos:

- `colbymchenry/codegraph` for larger codebases
- `millionco/react-doctor` for React
- `promptfoo/promptfoo` for AI behavior regression
- `trailofbits/skills` for security review
- `rohitg00/agentmemory` only after file-based state stops being enough

### Situation 4: Stuck

Use a rescue workflow:

```text
I am stuck.
Do not add features.
First summarize the current state from files and git status.
Then identify the smallest blocker.
Then propose three safe next steps.
Execute only the first step after I approve it.
```

Recommended repos:

- `obra/superpowers` for systematic debugging
- `addyosmani/agent-skills` for task breakdown
- `trailofbits/skills` if the issue may be security-sensitive

### Situation 5: Before Publish Or Merge

Run:

1. Tests
2. Lint/typecheck
3. UI verification if relevant
4. Security review if user data/auth/payments/secrets are involved
5. PR summary
6. Known risks list

Recommended repos:

- `trailofbits/skills`
- `promptfoo/promptfoo` if AI outputs matter
- `millionco/react-doctor` for React apps
- `addyosmani/agent-skills` for review and release discipline

## The Rule That Prevents Setup Chaos

Use this decision rule:

```text
Global install only if I expect to use it in almost every project.
Project install if it helps this specific project.
Read-only reference if I only need ideas.
Skip if I cannot name the next task it improves.
```

## Suggested Course Path

For course participants:

1. Finish the new-machine setup page.
2. Install Claude Code and Codex.
3. Install one workflow guardrail: Superpowers.
4. Create or bring a PRD.
5. Run the project-init skill.
6. Build one working slice.
7. Only then explore the repo catalog.

The goal is not to become a developer. The goal is to use a coding agent like a careful technical partner.

