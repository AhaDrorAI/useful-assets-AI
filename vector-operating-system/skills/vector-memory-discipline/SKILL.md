---
name: vector-memory-discipline
description: >
  Apply Vector's memory discipline: keep memory in files, separate recent notes
  from distilled long-term memory, write "remember this" items to the right
  layer, and keep private context out of shared spaces. Use when setting up a
  persistent assistant workflow, when the user says "remember this", or when
  deciding what to load at the start of a session.
---

# Vector Memory Discipline

## Principles
- Memory lives in files, not in intentions.
- Recent working notes and distilled long-term memory are separate files.
- Load personal memory only in a private context: exactly one human, the user, and not a shared project, channel or space. If you cannot tell, treat the context as shared.
- Prefer summaries over raw dumps.

## Structure
- `BRAIN.md` (or `project_state.md`): current state, active threads, next actions.
- `memory/YYYY-MM-DD.md`: raw daily notes.
- `MEMORY.md`: distilled long-term memory.

## Behaviour
- At startup, follow `vector-session-start`.
- When the user says "remember this":
  - If it is about current work or a next step, write it to `BRAIN.md`.
  - If it is a durable fact, preference or decision, write it to `MEMORY.md` with the date.
  - Otherwise, write it to today's `memory/` note.
  - Tell the user which file you used.
- If a remembered fact may be out of date, say so and give its date.
- Do not bring personal context into a task it is not relevant to.
- Never write secrets (keys, tokens, passwords) into memory files, even if asked; say where the user should store them instead.
