# Skill authoring and drift review

This file is for the person who writes or changes a skill in this repository. It has two parts: the writing standard every `SKILL.md` follows, and the review that keeps a skill from drifting after it ships.

The writing standard borrows ideas from ASD-STE100 (Simplified Technical English). It does not claim compliance with that specification. STE was written for maintenance manuals. A skill also needs room for judgment, so this standard keeps STE's precision rules for procedures and drops its register rules.

## Part 1. Writing standard

### Description (frontmatter)

The description is the only part of a skill the model sees before it decides to load the skill. Write it for triggering, not for reading.

1. State what the skill does in the first sentence.
2. Add a trigger clause that starts with "Use when". List the phrases a real user types, in every language the skill serves.
3. Name the near-miss cases that belong to another skill ("Not for X; use Y").
4. Keep it under 1,024 characters (spec limit). This repository ships as a plugin, so the Claude app's 200-character upload limit does not apply. Run `--upload-check` before a manual upload.

### Instructions (body)

Treat each skill as a procedure that runs many times. An ambiguity costs you once per run.

| Rule | Instead of | Write |
|---|---|---|
| Use the imperative. | "The agent should consider checking..." | "Check..." |
| Put one action in each sentence. | "Read the file, fix the errors and report." | Three sentences, or a numbered list. |
| State the condition before the action. | "Ask the user if the scope is unclear." | "If the scope is unclear, ask the user." |
| Use one term for one thing. | "report", "audit", "review" for the same output | Pick one term and define it once. |
| Replace vague quantities. | "ask a few questions", "as needed", "maybe" | "Ask at most 3 questions." / "If X, do Y; otherwise skip." |
| Give the fallback. | "Use the subagent." | "If a subagent tool exists, use it. If not, do it inline and say so in the report." |
| Mark volatile facts. | "Google requires 20 testers." | "As of 2026-11, Google requires 12 testers (source). Check the current rule before you advise." |

### Rules versus judgment

Do not turn every skill into a checklist.

- **Use strict steps** when the task and the decision criteria are known: a build, a conversion, a release checklist, a safety gate.
- **Use goal, constraints, considerations and boundaries** when the work needs judgment: framing a problem, editing prose, choosing a strategy. Say what a good result looks like and where the judgment stops. Do not invent a narrow numeric rule to look precise.
- **If the skill needs a decision nobody has made**, write it as an open decision in the skill or in the audit log. Do not guess.

The lint flags vague words. Where vague wording is deliberate (for example, "use judgment on tone"), keep it and say why in the same sentence.

### Critical restrictions

Prose alone does not enforce a restriction. For every "never send", "never write", "never publish" or "read-only" rule, check whether a tool-level control can back it:

| Restriction | Tool-level control |
|---|---|
| "Proposes only; never edits" | Do not list `Write`, `Edit` or bare `Bash` in `allowed-tools`. Then each write prompts the user. |
| Subagent must stay read-only | Give the agent a `tools:` list without write tools. |
| "Do not use the hosted OCR" | Prefer a local tool. Name the exact flag that must not be passed. |
| Database read-only until approved | Connect the database tool in read-only mode for the audit phase. |
| Private files must never be published | List them in `.gitignore`. CI fails if an ignored file is tracked. |
| "Do not send" for email or chat connectors | Set the connector's send tools to "Ask" in the client's tool permissions. |

Where no control exists, say so in the skill. Record it as an open risk in the audit log.

### Files and dependencies

- Every file the skill names must be bundled with exact case. The lint fails on a missing file.
- Every skill another skill depends on must have a fallback when it is not installed.
- Scripts run on Linux, macOS and Windows unless the skill says otherwise. Avoid GNU-only flags such as `find -printf`.
- Do not commit `.skill` archives. CI builds the ZIPs.

## Part 2. Test cases

Each skill keeps its test cases in `evals/<case-name>/`, in the layout that `claude plugin eval` reads:

```
evals/<case-name>/
├── prompt.md      settings block, then the prompt as a user would type it
├── case.yaml      schema_version (quoted), name (= folder), expected_outcome
└── graders/       one verifiable statement per file
```

Write at least 3 cases per skill:

1. **Normal**: the most common request, with complete input.
2. **Edge**: missing input, a boundary condition, or a tool that is not available.
3. **Ambiguous**: a request that could mean two things, or that tempts the skill to break a rule.

Write each grader as a statement about the result ("The reply names 12 testers, not 20"). For a case that needs human judgment, use one grader that restates the expected outcome. The packager excludes `evals/` from every ZIP.

To run the cases with Claude Code (real model runs, billed):

```bash
cd current/skills/<skill>
claude plugin eval . --allow-tools Write,Edit,Bash
```

## Part 3. Drift review

Skills drift for four reasons: the model changes, the outside world changes (prices, policies, APIs), a dependency changes, or the skill grows by small patches until its rules contradict each other.

### When to review

Each `SKILL.md` carries two dates in `metadata`:

```yaml
metadata:
  last_reviewed: "2026-11-18"
  review_every_days: "90"   # 90 for skills with volatile facts, 180 otherwise
```

The packager warns when a skill is past its interval. Also review a skill, whatever its date, when one of these happens:

- A new model family becomes the default.
- A tool, API, connector or platform the skill names changes its interface or policy.
- A user reports the same failure twice.
- The skill receives three or more patches since its last review.

### How to review

1. Run `python scripts/package_skills.py --strict`. Fix every error. Decide each warning.
2. Read the description against the current list of installed skills. If two descriptions claim the same request, change one, or record the conflict as an open decision.
3. Re-check every volatile fact (prices, limits, versions, policies) against a primary source. Update the "as of" date.
4. Run the skill's test cases. If a skill needs consistent output, run each case 3 times and compare the outputs. If the outputs differ in a way the skill's rules forbid, tighten the rule that allowed the difference.
5. Read the skill once from start to end for contradictions between sections.
6. Update `metadata.last_reviewed`. Add a line to the audit log in `docs/skill-audit-log.md`.
