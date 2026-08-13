# Upstream bug reports for openwolf 2.0.1

Three defects found while upgrading this project from 1.0.4 to 2.0.1. All are
reproducible from a clean install of the published package. Ready to file at
https://github.com/cytostack/openwolf/issues — paste each section as its own
issue.

Local mitigation lives in `scripts/openwolf-repair.mjs`; delete it once these
are fixed upstream and released.

---

## Issue 1 — `init` and `update` do not copy `symbol-extractor.js`, breaking every write hook

**Version:** 2.0.1 (also affects any 2.0.x install path)

**Impact:** After `openwolf init` or `openwolf update`, every `Write`/`Edit`
crashes the post-write hook. Because hook failures are not surfaced to the
user, `anatomy.md`, `memory.md`, session tracking, and auto bug detection all
stop updating silently. The project looks healthy and is not.

**Cause:** `dist/hooks/post-write.js` imports the module at load time:

```js
import { extractSymbols, symbolsSupported, SYMBOL_MIN_TOKENS } from "./symbol-extractor.js";
```

but both copy routines use a hardcoded ten-entry list that omits it:

- `dist/src/cli/update.js`, `hookFiles` (~line 413)
- `dist/src/cli/init.js`, `hookFiles` (~line 550)

Both list `session-start.js`, `pre-read.js`, `pre-write.js`, `post-read.js`,
`post-write.js`, `precompact.js`, `stop.js`, `shared.js`, `anatomy-store.js`,
`anatomy-lock.js` — and stop there. `symbol-extractor.js` ships in the package
(`dist/hooks/`) but never reaches `.wolf/hooks/`.

**Reproduce:**

```bash
npm i -g openwolf@2.0.1
cd /tmp && mkdir demo && cd demo && openwolf init
ls .wolf/hooks/symbol-extractor.js          # missing
echo '{"tool_name":"Write","tool_input":{"file_path":"a.md","content":"# a"}}' \
  | CLAUDE_PROJECT_DIR=$PWD node .wolf/hooks/post-write.js
# Error [ERR_MODULE_NOT_FOUND]: Cannot find module '.../.wolf/hooks/symbol-extractor.js'
```

**Suggested fix:** add `"symbol-extractor.js"` to both lists. Deriving the list
from `fs.readdirSync(sourceHooksDir)` would stop this recurring whenever a hook
module is added — `update.js` already does exactly that at ~line 347 for the
backup path.

---

## Issue 2 — `parseAnatomy` silently drops entries whose size label is not `(~N tok)`

**Version:** 2.0.1 (present since at least 1.0.0; more damaging since the store
landed)

**Impact:** Anatomy entries disappear. Under 1.0.x the loss happened on the next
write; under 2.0.x it happens at store-migration time and is then permanent,
because `anatomy.md` is rendered *from* the store. Upgrading this project
imported 87 of 89 entries — the two lost ones were hand-written entries for
packaged `.skill` files, labelled `(~5.1K zip)` and `(~15K zip)` rather than
`(~N tok)`.

**Cause:** `dist/hooks/anatomy-store.js`, `parseAnatomy` (~line 69) matches only
the token form, and a line that fails the regex is skipped entirely:

```js
const em = line.match(/^- `([^`]+)`(?:\s+—\s+(.+?))?\s*\(~(\d+)\s+tok\)$/);
if (em) { sections.get(currentSection).push({ ... }); }
// no else — unmatched entry lines vanish
```

Since `importFromMarkdown` feeds `parseAnatomy`, and `loadStoreReconciled`
re-imports whenever `anatomy.md`'s hash changes, a hand-edited entry in any
other shape is discarded rather than preserved or reported.

**Reproduce:**

```bash
# in a project with an anatomy.md, add one hand-written entry:
#   - `bundle.skill` — Packaged bundle (~5.1K zip)
# then trigger any write hook and re-read anatomy.md — the line is gone.
```

**Suggested fix:** fall back to a permissive pattern for entry lines that do not
carry a token count, importing them with `tokens: 0` so a later scan can fill in
the real value. A patch of this shape is running locally against 2.0.1:

```js
const alt = line.match(/^- `([^`]+)`(?:\s+—\s+(.+?))?\s*(?:\((.+)\))?$/);
if (alt && alt[1]) {
    sections.get(currentSection).push({ file: alt[1], description: alt[2] || "", tokens: 0 });
}
```

It must be placed after the `(~N tok)` branch, with a `continue` added to that
branch, and it correctly ignores indented symbol sub-entries because it anchors
on `^- `.

---

## Issue 3 — two Stop-hook reminders are unsatisfiable by construction

**Version:** 2.0.1

**Impact:** Both reminders fire on every turn regardless of what the session
does, because the state they check can never show the work as done. Agents
either comply repeatedly with work already finished, or learn to ignore Stop
reminders generally — which defeats the ones that are real.

**3a. `countSemanticEntries` (dist/hooks/shared.js)** counts memory.md rows by a
`| YYYY-MM-DD` prefix, but every row — in `OPENWOLF.md`'s documented format and
in what the hooks themselves append — is `| HH:MM | ... |`. The count is always
zero, so "no semantic summary was written to memory.md" fires forever.

Scoping to the session rather than the date also matters: a session that runs
past midnight, or is resumed the next day, appends no new `## Session:` header,
so a date-based check is wrong even once the row format is handled.

**3b. `checkForMissingBugLogs` (dist/hooks/stop.js)** looks for `buglog.json` in
`session.files_written`:

```js
const buglogWritten = session.files_written.some(w => w.file.includes("buglog.json"));
```

but `post-write.js` exits early for every path under `.wolf/`, so writes to
`.wolf/buglog.json` are never recorded there. The reminder cannot be satisfied
by logging a bug.

**Suggested fix:** for 3b, compare `buglog.json`'s mtime against
`session.started` — exactly what `checkStatusFreshness` does a few lines below
in the same file. For 3a, count non-mechanical rows after the last
`## Session:` header.

---

## Note on a fourth finding (not a bug, worth documenting)

`openwolf scan` prunes entries whose files are absent from disk. That is correct
for a working copy but destructive in a fresh clone or CI checkout, where
gitignored directories do not exist — running a scan there and committing the
result deletes those entries from a committed `anatomy.md`. A note in the docs,
or a `--no-prune` flag, would help projects that commit their anatomy.
