<!--
TEMPLATE: planning.md
PURPOSE: The "what we're going to build" layer — flows, screens, data, system design, sequence.
WHEN TO GENERATE: Full set only. Skip for starter set projects.
HOW TO USE: Pull as much as you can from the PRD. Where the PRD doesn't specify, use stack defaults
            and mark with "(proposed — confirm)".
            Delete this comment block before writing the final file.
-->

# Planning — [FILL: Project name]

This file is the bridge between `PRD.md` (what and why) and `tasks.md` (concrete next steps). Update it as the design crystallizes.

## User flows

<!-- Each flow is one user goal, one ordered sequence of steps. Pull from the PRD's user-story
     or scenario sections. If the PRD doesn't have explicit flows, derive 2-4 from the goals. -->

### Flow 1: [FILL: name, e.g. "First-time signup and onboarding"]

**Goal:** [FILL: what the user is trying to accomplish]

1. [FILL: step]
2. [FILL: step]
3. [FILL: step]

### Flow 2: [FILL: name]

**Goal:** [FILL]

1. [FILL]
2. [FILL]

[FILL: add more flows as the PRD warrants]

## Screens / surfaces

<!-- For web/app projects: list each screen the user encounters.
     For CLI/library: list each command or public API surface.
     For backend services: list each endpoint or queue/event. -->

| Surface | Purpose | Key states |
|---|---|---|
| [FILL: name] | [FILL: what it does] | [FILL: e.g. loading / empty / error / populated] |
| [FILL: name] | [FILL] | [FILL] |
| [FILL: name] | [FILL] | [FILL] |

## Data model (sketch)

<!-- One-paragraph sketch + a list of entities and their core fields. Keep this loose — it's a
     sketch, not a schema. The schema lives in code/migrations. If the project has no persistent
     data, replace this section with "Stateless — no persistent data." -->

[FILL: 2-3 sentences on the shape of the data]

**Entities:**

- **[FILL: entity name]** — [FILL: 1-line description, key fields]
- **[FILL: entity name]** — [FILL]
- **[FILL: entity name]** — [FILL]

## System design

<!-- High-level: how the major pieces fit together. ASCII sketch is great if it helps.
     Don't get into framework specifics — those belong in code. Mention major dependencies
     and the boundaries between them. -->

[FILL: paragraph or ASCII diagram of how the pieces fit. Cover: where state lives, how the
client talks to the server, where third-party services slot in, where async work happens.]

### External dependencies

- **[FILL: service name]** — [FILL: why we use it, what it does]
- **[FILL: service name]** — [FILL]

## Implementation sequence

<!-- The order in which we plan to build. Slice by user-visible value, not by layer.
     "Build the database first, then the API, then the UI" is an antipattern — it leaves the
     user with nothing working until the very end. Slice so each slice ships an end-to-end thin
     vertical of value. -->

### Phase 1: [FILL: name, e.g. "Walking skeleton"]

[FILL: what's in this phase, what working state it leaves the project in]

### Phase 2: [FILL: name]

[FILL]

### Phase 3: [FILL: name]

[FILL]

## Open questions

<!-- Things that aren't decided yet and shouldn't be guessed. Each open question becomes
     a candidate decisions.md entry once it's resolved. -->

- [FILL: e.g. "Auth provider — Supabase Auth vs. Clerk, deferred until we know about social login needs"]
- [FILL]
