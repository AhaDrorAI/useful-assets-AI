---
name: improve-codebase-architecture
description: "Surveys a whole codebase or subsystem for deepening opportunities — shallow modules whose interface is nearly as complex as the implementation it hides — ranks them in a self-contained HTML report with before/after diagrams, then designs whichever one the user picks. Use when the user asks for an architecture review or audit, wants to find where a codebase should be refactored, asks what shape a legacy or vibe-coded repo is in, wants to find missing seams before writing tests, or asks how to make an upcoming change easy. This is a periodic survey run outside the build loop, not a refactoring tool: do not use it to restructure one module the user has already chosen, or to carry out a refactor already decided on. Proposes only; never edits code."
license: Inherits the license of the repository it ships in
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, Task
---

# Improve Codebase Architecture

Survey a codebase for **deepening opportunities**: changes that turn shallow modules into deep ones. The payoff is testability and navigability, for humans and agents alike.

This skill proposes. It does not refactor.

## Not this skill when

- **The module is already chosen.** Designing one known module is a design conversation, not a survey — skip to Step 6's questions without the scan or the report.
- **Mid-implementation.** A survey costs a large slice of the context window the current task needs. Finish, then run this separately.
- **The refactor is already decided.** Take the decision to the project's spec or ticket flow.

## Invariants

These four hold on every run. They exist because each one has a recorded failure mode.

1. **Nothing inside the repo changes without approval.** The report always lands outside it. Writes to tracked files (`CONTEXT.md`, ADRs) happen only after the user approves that specific write. A survey that silently edits files is not a survey.
2. **Report first, design second.** Do not design, propose interfaces, or interview the user about a candidate before the report exists and the user has named one. Scoping questions in Step 1 are fine and often necessary — the gate is on design discussion. The most common failure of this skill is latching onto the first idea and interviewing the user about it while eleven better candidates go unwritten.
3. **The scan is bounded.** Budgets are in Step 1. An unbounded exploration of a large repo exhausts the context window and produces a worse report than a scoped one, not a better one.
4. **"Nothing worth doing" is a valid result.** Say so plainly when it is true. Manufacturing candidates to look useful is the failure this invariant prevents.

## Vocabulary

Write every candidate in these terms. Do not drift into "component," "service," "API," or "boundary" — a report that mixes vocabularies reads as generic cleanup advice and gets ignored.

- **Module** — anything with an interface and an implementation: function, class, package, slice.
- **Interface** — everything a caller must know to use the module correctly. Types, yes, but also invariants, ordering, error modes, config, performance.
- **Depth** — behaviour behind interface. **Deep** = a lot behind a little. **Shallow** = interface nearly as complex as the implementation.
- **Seam** — where an interface lives; a place behaviour can change without editing in place.
- **Adapter** — a concrete thing satisfying an interface at a seam.
- **Leverage** — what callers gain from depth. **Locality** — what maintainers gain: change, bugs, and knowledge concentrated in one place.

Full definitions and the complete principle list: [LANGUAGE.md](LANGUAGE.md).

The three principles used constantly:

- **Deletion test** — imagine the module gone. Both outcomes are findings, but they are different findings and rank differently:
  - Complexity **reappears across callers** → the module earns its keep and can be deepened. This is a **deepening candidate**, and the only kind that can be ranked `Strong`.
  - Complexity **vanishes** → it was a pass-through hiding nothing. This is a **collapse candidate**: real, but small on its own. Never rank one `Strong`, and fold it into the deepening candidate that supersedes it where one exists, rather than listing it as separate work.
- **The interface is the test surface.**
- **One adapter is a hypothetical seam. Two adapters is a real one.**

## Workflow

Copy this checklist and tick items off as you go:

```
- [ ] Step 1: Scope and budget agreed
- [ ] Step 2: Explore within budget
- [ ] Step 3: Write the report
- [ ] Step 4: Verify the report renders
- [ ] Step 5: Hand over and STOP
- [ ] Step 6: Design the chosen candidate (only after the user picks)
```

### Step 1 — Scope and budget

Read `CONTEXT.md` and any ADRs under `docs/adr/` if they exist. The domain language gives good seams their names; the ADRs record decisions this skill should not relitigate.

Then decide where to look, in this order:

1. **The user named a direction** — a module, a subsystem, a pain point, an upcoming spec. Take it. Skip the inference below.
2. **The user named nothing** — read recent commit history (`git log --oneline -n 200`) and let the paths that keep recurring pull your attention. Deepening pays off through future edits, so code that changes often has the highest expected return and dormant code the lowest.
3. **No git history available** — a fresh repo, a tarball, or git not installed. Do not guess. Say the hot-spot signal is missing and ask which area to scan, offering the largest directories as a starting point.

Budgets, and why these numbers:

- **Read at most ~40 files in detail.** Past a few dozen, additional reading stops changing which candidate ranks first; it only costs context that Step 6 will need.
- **Stop scanning at whichever comes first: the file budget, or 8 candidates that pass the deletion test.** Eight is the point where a report starts getting skimmed rather than read, and a skimmed report defeats the ranking.
- **If more than 8 pass, report the 8 strongest** and say how many you set aside, so the user knows the list is a selection rather than everything you found.

If the repo is too large or too tangled to survey within these budgets, say so and propose a narrower scope — one package, one subsystem — rather than producing a shallow scan of everything. Going in circles across a whole legacy monolith is the known failure here, and a scoped answer beats an exhausted one.

### Step 2 — Explore

If the harness offers a subagent tool for parallel exploration, use it — in Claude Code that is the agent/`Task` tool with `subagent_type=Explore`; other harnesses name it differently, so match on capability rather than on the tool's name. If it does not, explore sequentially with the tools available and say in the report that the scan was sequential, so the user can judge how thorough it was. Never skip exploration because a particular tool is absent.

Explore organically rather than by checklist, and note where you feel friction:

- Understanding one concept requires bouncing between many small modules.
- A module is shallow — its interface is nearly as complex as its implementation.
- Pure functions were extracted for testability while the real bugs live in how they are called (no locality).
- Tightly-coupled modules leak across their seams.
- Code is untested or untestable through its current interface.

Apply the deletion test to every suspect, and record which kind of candidate it became — deepening or collapse.

**If nothing passes the deletion test**, stop here. Tell the user the scan found no deepening worth doing, name the areas you looked at so they can judge the coverage, and offer to rescan with a narrower or different scope. Do not pad the report with speculative candidates to justify the run. A handful of collapse candidates and no deepening is also this outcome: say so plainly rather than promoting them to fill the report.

### Step 3 — Write the report

Write one self-contained HTML file outside the repo. Resolve the temp directory from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-YYYYMMDD-HHMMSS.html`. Second-level precision so two runs in the same session never overwrite each other.

**The report loads no external resources.** All CSS is inline; all diagrams are hand-built SVG or styled divs. This is not a style preference: you cannot see the rendered page, so a CDN that is blocked by an offline machine, a corporate proxy, or a subresource-integrity hook fails silently and you will report success on a blank page. Only use CDN-hosted Tailwind or Mermaid if the user explicitly asks for it, having been told it needs network access at open time.

Scaffold, diagram patterns, and styling: [HTML-REPORT.md](HTML-REPORT.md).

Each candidate is a card with exactly these fields:

- **Files** — which files and modules are involved.
- **Problem** — the friction the current shape causes.
- **Solution** — plain English, no code.
- **Benefits** — stated as locality and leverage, plus which tests get simpler or disappear.
- **Before / After** — side-by-side diagram showing the shallowness and the deepening.
- **Strength** — `Strong` (a deepening candidate whose friction is real and present), `Worth exploring` (payoff depends on where the code is heading), or `Speculative` (surfaced for completeness). Collapse candidates never rank `Strong`.

Close with a **Top recommendation**: which one you would do first, and why that one.

Use `CONTEXT.md` vocabulary for the domain and the vocabulary above for the architecture. If `CONTEXT.md` defines "Order," write "the Order intake module" — not "the FooBarHandler," and not "the Order service."

**ADR conflicts:** surface a candidate that contradicts an ADR only when the friction is real enough to justify reopening the decision. Mark it in the card: *"contradicts ADR-0007 — worth reopening because…"*. Do not enumerate every refactor an ADR forbids.

Do not propose interfaces yet. That is Step 6, and only for the one candidate the user picks.

### Step 4 — Verify

Before telling the user the report is ready, confirm it:

```bash
REPORT_PATH="<the absolute path you just wrote>"
grep -Eio 'src="https?:|href="https?:|cdn\.[a-z]' "$REPORT_PATH" | wc -l   # expect 0
```

Piping to `wc -l` matters: bare `grep -c` exits non-zero when it finds nothing, so the success case would look like a failed command.

Anything other than 0 means an external dependency crept in — usually a font link or an icon URL. Inline it or remove it, then re-check. Then confirm the file is a plausible size for its content, and that every candidate card carries all six fields. Fix and re-verify before moving on; a report you have not checked is a report you cannot vouch for.

### Step 5 — Hand over, then stop

Open the report — `xdg-open` on Linux, `open` on macOS, `start` on Windows — and give the user the absolute path in case it does not open.

Then ask: **"Which of these would you like to explore?"**

**Stop there and wait.** Do not begin designing, do not start asking design questions, do not volunteer your own pick beyond the Top recommendation already written in the report. The user chooses.

If the user has said anything like "just the report", "no grilling", or "don't interview me", the run ends here. Confirm the path and stop. This is a supported way to use the skill, not a degraded one.

### Step 6 — Design the chosen candidate

Once the user names a candidate, work through the design with them **one question at a time**: constraints, what sits behind the seam, what the deepened interface should look like, which tests survive. Alternative interface shapes are worth exploring — see [INTERFACE-DESIGN.md](INTERFACE-DESIGN.md).

**Offer an exit every 5 questions.** Say what you have settled so far and ask whether that is enough to write up. Long unbroken interrogation is this skill's most complained-about behaviour, and the cause is always the same: continuing to ask past the point where the user already has what they came for. Ask each question because the answer changes the design, never to be thorough. If the user asks you to wrap up, stop immediately and write up what you have — an incomplete decision they can act on beats a complete one they abandoned.

**One candidate per session.** Working several in one conversation fills the context window with the report, the design discussion, and the vocabulary edits all at once, and the quality of the last one suffers for it. Send the rest to the issue tracker as tickets.

The output of this step is a **decision, not a diff**. Hand the decision to the project's spec or ticket flow. Do not start implementing.

**Repo writes — ask every time.** These are useful, and none of them happen unprompted:

- **The deepened module needs a name that is not in `CONTEXT.md`?** Ask: *"Want me to add <term> to CONTEXT.md?"* Only on yes. Same for sharpening a term that is already there.
- **The user rejects a candidate for a durable reason?** Ask: *"Want me to record this as an ADR so future reviews don't re-suggest it?"* Only offer when a future reader would actually need the reason. Skip ephemeral ones ("not this quarter") and self-evident ones.

Follow the project's existing `CONTEXT.md` and ADR conventions if it has them — the `grill-with-docs` skill's `CONTEXT-FORMAT.md` and `ADR-FORMAT.md` if that skill is installed. If neither exists, keep it minimal: for a term, one line of definition plus what it is not; for an ADR, a numbered file with context, decision, and consequences.
