---
name: vector-private-memory
description: Load and use the private Vector memory pack safely. Use in private one-to-one contexts when user history, preferences, current state, or long-term continuity matter.
allowed-tools: Read, Grep, Glob
---

# Vector Private Memory

This skill governs use of the local private memory pack bundled with this plugin.

## Files in this plugin
- `USER.md` — private profile of the human you are helping
- `MEMORY.md` — distilled long-term memory
- `BRAIN.md` — live working memory / current state
- `memory/` — selected recent notes

## Strict privacy gate
Use these files **only** when all of the following are true:
1. The conversation is private: exactly one human, the user, and not a shared project, team channel, Slack thread or shared Cowork space. If you cannot tell, treat it as shared.
2. The information is relevant to the current task
3. Using it helps the user rather than merely being available

If any of these is false:
- do not load or cite private memory
- do not volunteer personal details
- continue with general behavior only

## Usage rules
- Prefer `BRAIN.md` for current state
- Prefer `MEMORY.md` for durable context
- Prefer `USER.md` for preferences, style, and personal operating model
- Use recent `memory/` notes only when recency matters
- Summarize instead of quoting raw personal text unless the user asks
- Never expose secrets, tokens, private URLs, or sensitive family details
- If a file listed above is missing, say which one and continue without it; do not search elsewhere on the machine for personal data
- In shared/group/org contexts, private memory is off-limits by default

## When to use
Use this memory pack when the task depends on:
- prior decisions
- established preferences
- known relationships or client context
- ongoing projects and current status
- reminders, follow-ups, or continuity across sessions

## Output behavior
- Use memory quietly as background context when appropriate
- Surface only the minimum needed detail
- If memory is uncertain or stale, say so plainly
