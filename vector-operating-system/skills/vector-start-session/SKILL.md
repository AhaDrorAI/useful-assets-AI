---
name: vector-start-session
description: >
  Start a session in Vector mode, reconstruct context, and ask what matters
  now. Use when the user says "start session", "good morning", "let's go",
  or begins a new working session.
---

# Start Session

Invoke the Vector session-start behavior.

1. Reconstruct context from available plugin/workspace files.
2. Load current-state context first.
3. Load recent notes if recency matters.
4. In private one-to-one contexts, use private memory when relevant.
5. Greet naturally in 1-3 sentences.
6. Ask what matters now.
