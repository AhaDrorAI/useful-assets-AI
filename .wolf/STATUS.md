# STATUS — useful-assets-AI

> Single source of truth for resuming work. Read this FIRST when starting a session.
> Update this file at the end of every work phase so the next `/clear` resumes in 1 read.
> Last updated: 2026-08-13

---

## ✅ Done

**Skills**

- Added `improve-codebase-architecture` (SKILL.md, three one-level references, ATTRIBUTION, four evals, and `audit_skill.py` — 45 checks, all passing).
- Upgraded `avoid-ai-writing` to 3.6.0: the tells that outlived the em dash, the transferable Simplified Technical English grammar rules, 22 controlled-language substitutions, an explicit reject-list for STE rules that flatten voice, and `forbidden-patterns.template.md`.
- Unpacked `startup-free-traffic` from its `.skill` zip. The zip was the better copy: it restored two sections missing from the loose `geo-aeo.md` and fixed cross-references that pointed at lowercase filenames the repo did not have.
- Fixed docx-export escaping (`\#`, `\-`, `&#x20;`) in two `startup-free-traffic` references. Superseded by the unpack, which shipped clean copies.

**Indexes**

- `README.md` lists all eight skills with one-line descriptors.
- `.wolf/anatomy.md` indexes every tracked file under `current/skills/`.

**Tooling**

- OpenWolf upgraded 1.0.4 → 2.0.1. Four defects found and fixed locally; see `.wolf/buglog.json` bug-004 through bug-012.
- `scripts/openwolf-repair.mjs` re-applies the local patches automatically at session start, so an `openwolf update` can no longer revert them silently. It has its own SessionStart entry because `replaceOpenWolfHooks` strips whole matcher entries containing a `.wolf/hooks/` command.

---

## 🚀 Next phase

**No active quest.** The session that produced the work above closed with nothing queued.

Outstanding work is not development: it is three tasks that need the owner's own machine, listed in `docs/local-machine-tasks.md`. A full `openwolf scan`, three bug reports to file against `cytostack/openwolf`, and one license-field decision on `startup-free-traffic`.

When new work starts, replace this section with its goal, acceptance criteria, and files to touch.

---

## 📁 Active architecture

- **Stack:** No application code. Markdown guides, skills in the [agentskills.io](https://agentskills.io) `SKILL.md` format, and HTML outputs. Node is present only for the OpenWolf hooks and `scripts/`.
- **Layout:** `current/` is publishable (guides + skills), `archive/` is superseded material, `_private/` is never published, `start-here/` and `examples/` are onboarding.
- **Skills:** `current/skills/<name>/SKILL.md`, with optional `references/`, `agents/openai.yaml`, and `evals/`. Some also ship a packaged `<name>.skill` zip beside the directory.
- **Patterns:** every new skill goes into both `README.md` and `.wolf/anatomy.md`. Reference files stay one level deep from SKILL.md.

---

## ⚠️ External blockers (don't block coding)

- `openwolf` CLI is not bundled: `npm i -g openwolf` on each machine before `scan`, `status`, or `update`.
- Filing upstream bug reports needs access to `cytostack/openwolf`, which a session scoped to this repository does not have.

---

## 🔧 Useful commands

```bash
node scripts/openwolf-repair.mjs --verbose      # verify OpenWolf hooks are intact
openwolf scan                                   # full anatomy rescan — LOCAL MACHINE ONLY, see cerebrum
python3 current/skills/improve-codebase-architecture/audit_skill.py \
        current/skills/improve-codebase-architecture   # 45 authoring checks
```

---

## 📚 References (read IF needed)

- `docs/local-machine-tasks.md` — work that needs the owner's machine
- `.wolf/cerebrum.md` — User Preferences + Do-Not-Repeat + Decision Log
- `.wolf/anatomy.md` — token-efficient file index
- `.wolf/buglog.json` — known bugs + fixes
- `.wolf/patches/UPSTREAM-REPORT.md` — three OpenWolf bug reports, ready to file
