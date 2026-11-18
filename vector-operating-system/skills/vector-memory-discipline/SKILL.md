---
name: vector-memory-discipline
description: >
  Apply Vector's memory discipline: reconstruct context from files, separate
  short-term from long-term memory, and avoid leaking private context. Use
  when setting up a persistent assistant workflow.
---

# Vector Memory Discipline

Apply this memory model:

## Principles
- Memory must live in files, not in vague intentions
- Separate recent working memory from distilled long-term memory
- Only load highly personal memory in clearly private contexts
- Prefer summaries over raw dumps

## Recommended Structure
- `BRAIN.md` or equivalent: current state, active threads, next actions
- `memory/YYYY-MM-DD.md`: raw daily notes
- `MEMORY.md`: distilled long-term memory

## Behavior
- On startup, load current state first, then recent notes, then long-term memory if appropriate
- When the user says "remember this," write it into the right layer
- If a fact is uncertain, say so
- Avoid dragging irrelevant personal context into unrelated tasks
