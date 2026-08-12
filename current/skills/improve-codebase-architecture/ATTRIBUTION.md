# Attribution

This is a revised version of the `improve-codebase-architecture` skill by Matt Pocock
(https://github.com/mattpocock/skills). The core ideas — module depth, the deletion test,
seams and adapters, the HTML candidate report, and the vocabulary discipline — are his.
The depth/interface framing derives from John Ousterhout's *A Philosophy of Software Design*.

This revision changes process control rather than substance:

- The design conversation is gated behind an explicit user choice, with a documented
  no-design exit and a check-in every 5 questions.
- The scan is bounded by a file budget and a candidate cap.
- Repo writes (`CONTEXT.md`, ADRs) require per-write confirmation.
- Exploration is described by capability rather than by a specific harness's tool name.
- The report is self-contained by default, with a verification step, replacing the
  CDN-dependent scaffold that failed silently offline.
- "No candidate worth pursuing" is an explicit, supported outcome.
- The trigger is scoped to survey-shaped requests, so it does not fire mid-implementation.

Set the `license` field in SKILL.md to match the license of the repository this ships in
before distributing.

This file is intentionally not referenced from SKILL.md, so it costs no context at runtime.
