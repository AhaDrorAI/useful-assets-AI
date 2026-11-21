<!--
TEMPLATE: project_state.md
PURPOSE: The continuity layer. Loaded first at the start of every session. Says where we are.
HOW TO USE: At init time, populate the "right now" section with the obvious starting point.
            The user (or future agent sessions) will keep this updated.
            Delete this comment block before writing the final file.

            Format philosophy: keep this file short. If it grows past one screen, the
            historical content is probably better-placed in tasks.md or decisions.md.
-->

# Project State — [FILL: Project name]

> Load this file first at the start of every session. It tells you where we are right now.

## Last updated

[FILL: today's date YYYY-MM-DD]

## Status

[FILL: one paragraph. Right now this should say something like:
"Project just initialized via the project-init skill. PRD is in place, the supporting docs
have been generated, and `.claude/` is bootstrapped with the curated ECC subset. Nothing has
been built yet — the next session should start by reading CLAUDE.md, then picking up the
first task in tasks.md."

If this is a re-init / re-run, summarize what's currently working and what's next.]

## Where we are stuck (if anything)

<!-- Only fill when actually stuck. At init time, this should be empty. -->

[FILL: empty at init. Format when used:
"Stuck on [thing]. Tried [approaches]. The blocker is [specific issue]. Asking [user/expert] /
researching [topic] / parking until [trigger]."]

_Nothing right now._

## Next step

[FILL: at init, this should be:
"Read CLAUDE.md to understand conventions. Verify the build/test/dev commands work. Then pick up
the top item under 'Now' in tasks.md."]

## Quick-load — read these files first when starting a session

In order:

1. `project_state.md` — this file
2. `CLAUDE.md` — conventions, commands, guardrails
3. `tasks.md` — what's queued up

If the question or work is non-trivial, also load:

4. `PRD.md` — full project context
5. `planning.md` — current design [if full set]
6. `decisions.md` — why we made the calls we did [if full set]

## Notes for the next session

<!-- Free-form. Useful for "I was about to do X but ran out of time" notes. Empty at init. -->

[FILL: empty at init.]

_None yet._
