<!--
TEMPLATE: tasks.md
PURPOSE: Execution layer. What's done, what's now, what's queued, what's backlog.
HOW TO USE: Seed "now" with one obvious first task ("Read CLAUDE.md and verify build works")
            Seed "this week" with the first phase from planning.md (full set) or with 2-3
            tasks derived from the PRD's MVP scope (starter set).
            Seed "backlog" with anything from the PRD that's mentioned but explicitly not in
            scope-for-now, plus out-of-scope items the user might still want to track.
            Delete this comment block before writing the final file.
            
            Format: simple checkboxes. Don't overengineer with priority/owner/estimate fields —
            the user will add those if and when they need them.
-->

# Tasks — [FILL: Project name]

Execution layer. The order is deliberate: read top-to-bottom to know what's happening now and what's coming.

## Done

<!-- Empty at init. Move tasks up here from "Now" or "This week" as they complete.
     Append the date in parens for retrospect: e.g. "- [x] Set up repo (2026-04-29)" -->

_Nothing yet._

## Now

<!-- One task. Maybe two. The thing actively being worked on right now. -->

- [ ] Read `CLAUDE.md`, `PRD.md`, and `project_state.md`; verify the project structure makes sense.
- [ ] Verify the dev environment works — run the build/test/dev commands from `CLAUDE.md` and confirm they succeed (or fix what's broken).

## This week

<!-- 3-7 tasks that follow from the first phase of planning.md (or, for starter set, from the
     immediate MVP scope in the PRD). Don't go beyond a week's worth — anything further out
     belongs in the backlog. -->

- [ ] [FILL: first concrete task from phase 1 of planning.md / PRD MVP scope]
- [ ] [FILL]
- [ ] [FILL]
- [ ] [FILL]

## Backlog

<!-- Anything mentioned in the PRD that isn't in this week's slice, plus things the user
     wants to track for later. Two sub-buckets help once the list grows. -->

### Soon (next 1-2 phases)

- [ ] [FILL: item from later phases of planning.md or PRD]
- [ ] [FILL]
- [ ] [FILL]

### Later / nice-to-have

- [ ] [FILL: from PRD's out-of-scope or "future considerations" sections, anything worth tracking]
- [ ] [FILL]

## How to use this file

- Move tasks: backlog → this week → now → done.
- When picking up a task, move it to "Now" and add a note in `project_state.md` with what you're trying to accomplish.
- Keep "Now" to 1-2 items max — anything more and the task is too coarse; break it down.
- When a task is done, move it to "Done" with the date.
