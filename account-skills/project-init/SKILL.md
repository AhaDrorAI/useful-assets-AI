---
name: project-init
description: Bootstrap a complete project documentation and agent-harness architecture from an existing PRD. Use this skill whenever the user wants to "init", "set up", "bootstrap", "scaffold", or "kickstart" a project — or describes a fresh repo, empty folder, or new codebase that needs structure. Reads the user's PRD.md, judges complexity, synthesizes content into CLAUDE.md, AGENTS.md, planning.md, tasks.md, decisions.md, and project_state.md, interviews the user for missing critical information, initializes git if needed, and selectively bootstraps a curated subset of the everything-claude-code repo into .claude/. Works for Claude Code primarily but also produces AGENTS.md for cross-tool portability with Codex, Cursor, and OpenCode. Trigger this skill even when the user only says "I have a PRD, what's next" or "how do I start this project right" — they almost certainly want this. Requires a PRD.md; for an idea with no PRD, use new-project-from-prd instead.
metadata:
  last_reviewed: "2026-11-18"
  review_every_days: "180"
---

# Project Init

A skill for turning an existing PRD into a complete project foundation: the right markdown files, populated with real content, plus a curated agent-harness layer in `.claude/` and a portable `AGENTS.md` for non-Claude agents.

This skill is not a passive scaffolder. It reads the PRD, looks at whatever else is already in the folder, decides what level of structure the project needs, asks the user for critical missing pieces, and writes content-rich files. The goal is that when this skill finishes, the user can immediately start building with full context loaded into whichever agent they use next.

## When to use this skill

Trigger on phrases like "init my project", "set up the project structure", "bootstrap this codebase", "scaffold the project docs", "I have a PRD what's next", "how do I start this right", "create the Claude Code architecture", "set up CLAUDE.md".

Also trigger proactively when:
- The user is in a folder that contains a PRD (or PRD-like document) but no other project structure
- The user describes an early-stage project and is asking what to do first
- The user mentions they're starting fresh and wants to set things up properly

Do NOT trigger when:
- The user is asking general questions about project structure (no concrete project to init)
- The user is mid-development and asking for unrelated help
- A `CLAUDE.md` already exists and the user isn't asking to redo it (this skill never overwrites)

## Prerequisites — verify before doing anything else

This skill is grounded in the PRD. If there's no PRD, stop. The reason: synthesizing project docs from nothing produces hollow scaffolding that wastes the user's time. The PRD is the load-bearing input.

1. Confirm cwd is the project root the user wants to init. If ambiguous, ask once.
2. Check for `PRD.md` (case-insensitive — also accept `prd.md`, `PRD.MD`).
3. **If `PRD.md` is missing**: stop and tell the user. Suggested message tone: "I need a PRD.md in the project root before I can set up the rest. The PRD is what grounds the synthesis — without it, I'd be making up the project for you. Once you have one drafted, run me again." Do not offer to write the PRD. The user gets more value writing it themselves or in a focused session.

## The flow

Walk through these steps in order. Each step has a "why" — read it. The why is what makes the difference between a generic scaffold and one that actually fits this project.

### 1. Inventory existing context

Before generating anything, read everything that's already there. This saves the user from being asked questions whose answers are already on disk.

- List all root-level files (`ls -la`).
- Read every root-level `.md` file, including the PRD. Common sources of useful signal: `README.md`, `NOTES.md`, `IDEAS.md`, anything the user has been jotting in.
- If `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, etc. exist, read them — they reveal stack and existing tooling.
- Note what's already there so you don't ask redundant questions later.

### 2. Initialize git if the folder is not a repository

Git is non-negotiable for this skill. Decisions, tasks, and state files only make sense if the user can see them evolve over commits.

- Run `git status` in the project root. If it errors with "not a git repository", run `git init`.
- Add a `.gitignore` if missing. Sensible defaults: `node_modules/`, `__pycache__/`, `.venv/`, `.DS_Store`, `.idea/`, `.vscode/`, `*.log`, `.env`, `.env.local`, and **`.claude/settings.local.json`** (this last one matters — that file is for personal overrides and should never be committed).
- Don't make a first commit yourself. The user's first commit should be theirs after they review what was generated.

### 3. Read and analyze the PRD

Read `PRD.md` carefully. Then form a mental model of:

- **Project name** — usually in the title or first paragraph
- **What's being built** — the core artifact
- **Who it's for** — primary user/persona
- **Success criteria** — what "done" looks like
- **Scope boundaries** — what's explicitly in and out
- **Tech hints** — any stack mentioned ("React app", "Python CLI", "iOS shortcut")
- **Domain primitives** — auth, payments, LLM, video, real-time, file uploads, etc. (these drive skill selection later)

If the PRD is unstructured prose, that's fine — extract what's there. Don't push back on PRD format unless something critical is genuinely missing (in which case it goes in the interview at step 5).

### 4. Judge complexity (starter vs full)

Read `references/complexity-rubric.md` and apply it. The rubric outputs one of two structures:

- **Starter set** (3 docs): `CLAUDE.md`, `tasks.md`, `project_state.md` plus `.claude/`. Right for small/single-feature projects.
- **Full set** (6 docs): adds `planning.md`, `decisions.md`, plus a richer `CLAUDE.md`. Right for multi-flow, multi-role, or non-trivial backend projects.

Both sets always include `AGENTS.md` at root for cross-tool portability.

State your decision out loud to the user and explain your reasoning in one sentence ("PRD describes one-screen tool with no backend → starter set"). Let them override.

### 5. Identify gaps and run a single batched interview

The PRD won't have everything. Read `references/interview-questions.md` for the question bank, then pick only the questions whose answers you actually need given what's already in the PRD and the existing files.

Hard rule: **one batched interview, not drip-fed questions.** Asking 7 questions one at a time across 7 turns is exhausting. Asking all 7 in one message lets the user answer in one pass. Cap the interview at 7 questions. If you need more, keep the 7 whose answers change the generated files the most.

If the host offers a tool for multiple-choice questions, use it for questions with clear discrete options (deployment target, primary language, etc.) and use prose for open-ended ones (conventions, guardrails).

### 6. Generate the markdown files

For each file in the chosen structure, read the matching template in `references/`, fill it with synthesized content from the PRD + interview answers + existing files, and write it.

**Templates:**
- `references/claude-md-template.md`
- `references/agents-md-template.md`
- `references/planning-md-template.md` (full set only)
- `references/tasks-md-template.md`
- `references/decisions-md-template.md` (full set only)
- `references/project-state-md-template.md`

**Critical guardrail — never overwrite existing files.** If `CLAUDE.md` already exists in the project, write your generated version as `CLAUDE.proposed.md` instead, and tell the user to diff and merge. Same for any other file. This prevents destroying work the user has already done.

The templates contain instructional comments (HTML comments and `[FILL: ...]` placeholders) that tell you what content to put where. Treat the placeholders as mandatory — if you don't have content for one, ask the user rather than guessing or leaving the placeholder visible in the final file.

### 7. Bootstrap the agent-harness layer

This step pulls a curated subset of the `everything-claude-code` repo (https://github.com/affaan-m/everything-claude-code) into `.claude/`. Read `references/ecc-bootstrap.md` for the mechanics and `references/skill-selection-rubric.md` for the decision logic.

Summary of what happens:

1. **List globals**: check what the user already has at `~/.claude/skills/`, `~/.claude/rules/`, `~/.claude/agents/`. These are available everywhere — don't duplicate them at project level.
2. **Inventory ECC's catalog**: clone ECC to a temp cache (or sparse-checkout the relevant paths), then read SKILL.md and rule frontmatter so you have name + description for each available item.
3. **Record the exact ECC commit** (`git -C "$ECC_CACHE" rev-parse HEAD`). Write it in `decisions.md` (or the final report for the starter set), so the user knows which version was copied and can update deliberately later.
4. **Apply the selection rubric** to propose: which `rules/common/` items, which language-specific rules folder (based on detected stack), and which skills are right for *this* project specifically.
5. **Subtract globals**: remove anything the user already has globally.
6. **Review what will be copied.** ECC is third-party code. For each proposed skill or agent, list any scripts it contains. Do not copy hooks or settings files from ECC. If a skill contains a script that runs shell commands or reaches the network, say so in the approval list.
7. **Present the delta to the user for approval.** Be specific: "I want to add these 6 items to `.claude/`: [list with one-line reason for each]. You already have these globally so I'm skipping them: [list]. Approve, or drop any?"
8. **Install only what's approved** by copying from the temp cache into `.claude/skills/`, `.claude/rules/`, `.claude/agents/`.

Two non-obvious points the user explicitly asked for:
- The skill should *help the agent decide* what's relevant for this project — not install a fixed set.
- Anything that would be useful in every project should be flagged as "consider installing globally" rather than installed per-project. Surface this as a final note in the report at step 9.

### 8. Set up `.claude/settings.json`

If `.claude/settings.json` already exists, do not touch it. Otherwise write a minimal one. JSON does not allow comments, and Claude Code cannot load a settings file that contains them, so write exactly:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json"
}
```

Leave `model` unset so Claude Code's default applies. Do not add keys you cannot confirm in the current Claude Code settings documentation.

Explain the file in `CLAUDE.md` (one line: what `.claude/settings.json` is for and that personal overrides go in the gitignored `.claude/settings.local.json`). Do not write a `settings.local.json`.

Validate before moving on: `python3 -m json.tool .claude/settings.json` must succeed.

### 9. Print the final report

End the run with a clear, scannable summary. The user just had a lot of stuff generated for them — they need to know what to look at first.

Structure:

```
Project init complete.

Created (review these in order):
1. PRD.md — your input, untouched
2. CLAUDE.md — project conventions, build/test commands, guardrails
3. AGENTS.md — cross-tool entry point, points to CLAUDE.md
4. planning.md — user flows, screens, data model, implementation sequence
5. tasks.md — execution layer, today/this-week/backlog
6. project_state.md — load this first at the start of every session
7. decisions.md — empty log; update it when you make a real decision
8. .claude/ — agent harness (X rules, Y skills, Z agents installed)

Things I left as placeholders (fill these in):
- [list any [FILL: ...] markers that survived because you couldn't synthesize them]

Things to consider installing globally (would help across all projects):
- [list anything from step 7 that fit this category]

Suggested next step:
- Read CLAUDE.md, then project_state.md, then start on the first task in tasks.md.
```

## Edge cases & guardrails

- **Existing `.claude/` folder**: don't blow it away. Merge — only add files that don't already exist.
- **Existing markdown files at root** (other than PRD): treat as additional context for synthesis, don't overwrite. Generated files for those names go to `*.proposed.md`.
- **No internet access** when trying to clone ECC: degrade gracefully. Generate the root markdown files anyway, skip step 7, and note in the final report that ECC bootstrap was skipped and how to re-run it later.
- **PRD is in a language other than English**: write `CLAUDE.md` and `AGENTS.md` in English unless the user asks otherwise; agents read them, and English keeps them portable. Write `planning.md`, `tasks.md`, `decisions.md` and `project_state.md` in the language the user asks for; if they did not say, ask once in the interview. Never translate or edit the PRD.
- **User says "stop, I want to do this myself"** mid-flow: stop at once. Write each step's files only when that step is complete, so a stop never leaves a half-written file. Report which files were written and which were not.

## Why this skill exists

Most projects accumulate context in someone's head, in scattered Slack messages, in commit messages, in nowhere at all. When an agent picks up the project, it has to rediscover all of it from code, which is slow and lossy.

This skill does that discovery once, up front, when context is freshest (right after the PRD is written). Every subsequent session — by the user, by Claude Code, by Codex, by anyone — starts with that context already organized. The investment pays off across every future agent interaction on the project.
