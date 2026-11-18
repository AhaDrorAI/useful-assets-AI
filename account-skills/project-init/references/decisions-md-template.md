<!--
TEMPLATE: decisions.md
PURPOSE: Persistent log of non-trivial decisions and the tradeoffs around them.
WHEN TO GENERATE: Full set only. Skip for starter set projects.
HOW TO USE: Seed with the meta-decision that this skill ran (so the user has a sample format).
            Seed with any architectural choices the PRD or interview revealed that were already
            made (e.g. "decided to use Supabase per PRD section 4.2").
            Delete this comment block before writing the final file.

            Format: one entry per decision, newest at top. Each entry has the same four-part
            structure so they're scannable.
-->

# Decisions

A log of non-trivial decisions and the tradeoffs around them. The point is not to document every choice — only the ones that future-you (or another agent) might second-guess and need to understand.

**When to add an entry:** when you make a choice that has a credible alternative, costs something to reverse, or relies on context that won't be obvious six months from now.

**Format:**
- **What** — the decision in one sentence.
- **Why** — the reasoning that led here.
- **Tradeoff** — what we're giving up by choosing this.
- **Remember** — anything future-you needs to know to evaluate this later (e.g., "revisit if user count exceeds X", "the alternative we rejected was Y because Z").

---

## [FILL: today's date YYYY-MM-DD] — Adopted the project-init structure

**What:** Generated `CLAUDE.md`, `AGENTS.md`, `planning.md`, `tasks.md`, `decisions.md`, `project_state.md`, and `.claude/` via the `project-init` skill, sourced from the PRD.

**Why:** Loading project context once, up front, is cheaper than rediscovering it every session. The skill also bootstrapped a curated subset of `everything-claude-code` to give the agent harness sane defaults.

**Tradeoff:** Six markdown files at the project root is more ceremony than a tiny project needs. The starter set exists for that case; we picked full because [FILL: reason from complexity rubric, e.g. "the project has multiple user roles and a non-trivial backend"].

**Remember:** The `.claude/settings.local.json` file is for personal overrides and is gitignored — don't commit it. ECC content under `.claude/` can be updated by re-running the skill.

---

[FILL: if the PRD or interview revealed any pre-made architectural decisions, log them here as additional entries with the same format. Examples that often appear:

- Choice of database / persistence layer
- Choice of auth provider
- Choice of deployment platform
- Choice of frontend framework when multiple were credible
- Decision to be browser-only vs. server-rendered

If none, leave just the meta-decision above and let real decisions accumulate.]
