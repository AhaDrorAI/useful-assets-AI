# Tasks for a coding agent running on the local machine

Work that could not be done from the cloud session on 2026-08-13, either because
it needs the full working tree or because it needs access to a repository
outside this one. Written for an agent with a terminal on the owner's machine.

Do these in order. Each is independent, so a failure in one does not block the
next. Delete a section once it is done.

---

## 1. Run a full anatomy scan

**Why it could not be done remotely.** `openwolf scan` deletes index entries for
files it cannot see on disk. The cloud session runs from a fresh clone, where
`_private/` and every `desktop.ini` are absent because they are gitignored. A
scan there would have removed roughly 30 real entries from the committed
`.wolf/anatomy.md`.

**Preconditions.** A complete working tree, including `_private/`. Verify before
you start:

```bash
ls _private/supabase-sql/ | head        # must list .sql files
npm ls -g openwolf || npm i -g openwolf # CLI is not bundled with the repo
```

**Do:**

```bash
node scripts/openwolf-repair.mjs --verbose   # expect: hooks healthy
openwolf scan
git diff --stat .wolf/anatomy.md .wolf/anatomy-index.json
```

**Check before committing.** The diff should *add* symbol maps and correct token
counts. If it *removes* whole sections, especially `## _private/`, the working
tree was incomplete: discard with `git checkout -- .wolf/` and re-check the
preconditions. Commit only when the diff is additive.

---

## 2. File three bug reports against OpenWolf

**Why it could not be done remotely.** The cloud session is scoped to this
repository. It cannot read or post to `cytostack/openwolf`.

**Source.** `.wolf/patches/UPSTREAM-REPORT.md` holds all three, already written
with cause, file and line references, a runnable reproduction, and a suggested
fix. Paste each `## Issue N` section as its own issue at
https://github.com/cytostack/openwolf/issues.

Summary of what they are:

1. `init` and `update` never copy `symbol-extractor.js`, so `post-write.js`
   crashes on every edit after an install or upgrade, silently.
2. `parseAnatomy` drops anatomy entries whose size label is not `(~N tok)`.
   Under 2.0.x this deletes them from the store permanently.
3. Two Stop-hook reminders check state that can never show the work as done, so
   they fire on every turn forever.

**If you can open pull requests instead**, that is better: this repo already
carries working versions of all three fixes. `scripts/openwolf-repair.mjs`
contains the exact patched blocks for 2 and 3a, and the fix for 1 is one string
added to two arrays. The local patches were written against the compiled
`dist/` output, so port them to the TypeScript sources in `src/` before
submitting.

**When the fixes are released.** Upgrade, then delete `scripts/openwolf-repair.mjs`,
its SessionStart entry in `.claude/settings.json`, `.wolf/patches/`, and this
section. Until then the repair script is what keeps the patches alive across
upgrades, so do not remove it early.

---

## 3. Decide the `startup-free-traffic` license reference

Its `SKILL.md` frontmatter reads `license: Complete terms in LICENSE.txt`, and
no `LICENSE.txt` ships with the skill or the repository. The field points at a
file that does not exist.

This was left alone deliberately, because changing a license field is the
owner's call, not an agent's. Resolve it one of three ways: add the
`LICENSE.txt` the field refers to, change the field to name the actual license,
or, if the skill came from a third party, record where it came from so the
reference can be traced.

---

## Notes on this repository

- **Never run `openwolf scan` in CI or a container.** See task 1. This is
  recorded in `.wolf/cerebrum.md` under Do-Not-Repeat.
- **`.wolf/hooks/*.js` is vendored build output.** Local fixes there are real but
  an `openwolf update` overwrites them; `scripts/openwolf-repair.mjs` restores
  them at the next session start.
- **`.wolf/STATUS.md` is the handoff document.** Read it first, and update it
  when a piece of work finishes.
