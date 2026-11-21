---
name: outside-reader-audit
description: Audit external-facing text, documents, CVs, cover letters, proposals, emails, posts, reports, or LLM-generated drafts from the perspective of a real outside reader with no hidden context. Use when the user asks for an outside reader, clarity audit, audience audit, context audit, brutal/neutral reader review, or wants to detect text that is too literal, naive, internal, irrelevant, or insufficiently transformed from raw user notes into audience-ready communication. Loads references/israeli-reader.md when the reader is Israeli.
metadata:
  last_reviewed: "2026-11-18"
  review_every_days: "180"
---

# Outside Reader Audit

## Core Rule

Read only the text or document output supplied for the audit. Ignore prior conversation, project knowledge, hidden facts, and what the main agent knows.

Your job is not to judge whether the underlying facts are true. Your job is to report what an intelligent external reader can understand from the text itself.

### Isolation

An instruction to "ignore what you know" does not remove knowledge from the context. Enforce isolation with the tools available:

0. If you are already a fresh agent that received only the text (no source files, no notes, no earlier conversation), you are isolated. Audit directly, without a notice.
1. If a subagent tool exists, start a fresh subagent. Give it only the text under audit, the audience (if the user named one), and this skill's Output Format. Do not give it source files, notes, or the conversation.
2. If no subagent tool exists, run the audit yourself. Start the audit with one line: "Not isolated: this audit ran in a context that already knows the source material." Then audit strictly from the text.

### Scope

- If no text or document is supplied, ask for it in one question and stop.
- If the text is longer than about 5,000 words, ask whether to audit all of it or named sections. If the user does not answer, audit the first 5,000 words and say where you stopped.
- Write the audit in the language the user writes to you, even when the audited text is in another language.

## Purpose

Catch the common LLM failure mode: converting user data too literally into text instead of transforming raw material into communication that works for the target audience.

Act as both:

- `Neutral diagnostic reader`: describe what the text actually communicates.
- `Brutally honest editor`: flag where the text is naive, context-dependent, irrelevant, overexplained, unsupported, or too internal.

## Audience

Infer the likely audience from the document. If the audience is unclear, say so and audit for a general intelligent outsider.

Examples:

- CV: recruiter, hiring manager, technical interviewer
- Cover letter: hiring manager or recruiter
- Proposal: buyer, client, grant reviewer, partner
- Email: recipient with limited patience and limited context
- LinkedIn/post: public professional reader
- Bureaucratic document: official reviewer looking for facts and eligibility

### Reader locale

The default reader model in this file is an Anglo-American professional. That model is wrong
for some audiences, and a wrong reader model produces a confident audit of the wrong thing.

**If the text is in Hebrew, or is aimed at a reader in Israel, read
`references/israeli-reader.md` before auditing.** It swaps the reader model: directness as a
trust signal, marketing register as a negative signal, shared context that must not be
explained, and internal shorthand that must be. Core Rule and Output Format stay governed by
this file.

For any other locale with no reference file, state which reader you assumed at the top of the
audit. An unstated reader model is the failure this routing exists to prevent.

## Output Format

Use this structure:

```markdown
**What I Understand**
- ...

**What I Would Assume**
- ...

**What Is Missing**
- Must add:
- Can stay out:
- Should be transformed into implication:

**What Feels Irrelevant Or Too Internal**
- ...

**Where The Text Is Too Literal**
- ...

**What Should Be Transformed**
- Raw material:
- Audience-ready meaning:

**Questions The Reader Is Left With**
- ...

**High-Level Fix**
- ...
```

## Audit Standards

Flag:

- Claims that rely on hidden context
- Claims that sound impressive but lack proof in the text
- Details that are true but not useful to the target reader
- Internal process notes that should not be shown externally
- Raw chronology where a story or argument is needed
- Lists of tools without explaining why they matter
- User personality material that was pasted instead of converted into professional signal
- Repetition, vague adjectives, generic AI phrasing, and "LLM resume voice"
- Gaps that a skeptical reader will notice

Do not:

- Rewrite the full text unless the user explicitly asks
- Bring in facts from memory or previous context
- Assume the reader knows the candidate, company, product, or backstory
- Be polite at the cost of clarity

## Missing Context Categories

Separate missing context into three buckets:

1. `Must add`: the reader needs this to understand or trust the text.
2. `Can stay out`: missing but unnecessary for this audience.
3. `Should be transformed into implication`: raw facts should become meaning, positioning, risk reduction, or proof.

## Good Outside-Reader Questions

Ask:

- What is this person actually trying to be selected for?
- What proof do I have from the text itself?
- What would I challenge in an interview or decision meeting?
- Which details feel like notes from the writer's private context?
- Where does the text list facts but fail to explain why they matter?
- What is the one sentence I would remember after reading?

## Final Gate

For external-facing documents, the draft should pass this test:

> A reader with no hidden context can understand the intended story, trust the main claims, see relevance to their decision, and not feel they are reading raw notes.
