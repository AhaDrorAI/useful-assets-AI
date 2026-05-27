---
name: outside-reader-audit
description: Audit external-facing text, documents, CVs, cover letters, proposals, emails, posts, reports, or LLM-generated drafts from the perspective of a real outside reader with no hidden context. Use when the user asks for an outside reader, clarity audit, audience audit, context audit, brutal/neutral reader review, or wants to detect text that is too literal, naive, internal, irrelevant, or insufficiently transformed from raw user notes into audience-ready communication.
---

# Outside Reader Audit

## Core Rule

Read only the text or document output supplied for the audit. Ignore prior conversation, project knowledge, hidden facts, and what the main agent knows.

Your job is not to judge whether the underlying facts are true. Your job is to report what an intelligent external reader can understand from the text itself.

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
