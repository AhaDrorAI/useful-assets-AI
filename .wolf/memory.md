# Memory

> Chronological action log. Hooks and AI append to this file automatically.
> Old sessions are consolidated by the daemon weekly.

## Session: 2026-06-23 16:40

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|
| 16:42 | Created current/skills/google-play-publishing/SKILL.md | — | ~2930 |
| 16:44 | Created current/guides/google-play-publishing.he.md | — | ~2522 |
| 16:44 | Created google-play-publishing skill and guide from uploaded source file | current/skills/google-play-publishing/SKILL.md, current/skills/google-play-publishing.skill, current/guides/google-play-publishing.he.md | created | ~6000 |
| 16:45 | Session end: 2 writes across 2 files (SKILL.md, google-play-publishing.he.md) | 4 reads | ~12096 tok |
| 16:50 | Edited current/skills/google-play-publishing/SKILL.md | 10→12 lines | ~155 |
| 16:50 | Edited current/skills/google-play-publishing/SKILL.md | modified requirement() | ~155 |
| 16:51 | Edited current/skills/google-play-publishing/SKILL.md | inline fix | ~27 |
| 16:51 | Edited current/skills/google-play-publishing/SKILL.md | 3→5 lines | ~114 |
| 16:51 | Edited current/skills/google-play-publishing/SKILL.md | 1→3 lines | ~66 |
| 16:51 | Edited current/skills/google-play-publishing/SKILL.md | 2→3 lines | ~91 |
| 16:51 | Edited current/guides/google-play-publishing.he.md | 6→8 lines | ~105 |
| 16:51 | Edited current/guides/google-play-publishing.he.md | 10→13 lines | ~120 |
| 16:51 | Edited current/guides/google-play-publishing.he.md | 5→7 lines | ~56 |
| 16:51 | Edited current/guides/google-play-publishing.he.md | 14→18 lines | ~126 |
| 16:52 | Edited current/guides/google-play-publishing.he.md | 4→4 lines | ~50 |
| 16:52 | Edited current/guides/google-play-publishing.he.md | 4→8 lines | ~76 |
| 16:52 | Edited current/guides/google-play-publishing.he.md | 4→6 lines | ~96 |
| 16:52 | Edited current/guides/google-play-publishing.he.md | expanded (+6 lines) | ~87 |
| 16:53 | Session end: 16 writes across 2 files (SKILL.md, google-play-publishing.he.md) | 6 reads | ~16261 tok |

## Session: 2026-06-23 17:14

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|

## Session: 2026-08-12 06:00

| Time | Action | File(s) | Outcome | ~Tokens |
|------|--------|---------|---------|--------|
| 06:02 | Edited README.md | 1→2 lines | ~43 |
| 06:05 | Added improve-codebase-architecture skill (SKILL.md + 3 references + ATTRIBUTION + audit script + evals) | current/skills/improve-codebase-architecture/* | created, audit 45/45 pass | ~9000 |
| 06:06 | Indexed the new skill | .wolf/anatomy.md, README.md | updated | ~600 |
| 06:03 | Session end: 1 writes across 1 files (README.md) | 1 reads | ~485 tok |
| 06:03 | Session end: 1 writes across 1 files (README.md) | 1 reads | ~485 tok |
| 06:04 | Edited README.md | 4→9 lines | ~311 |
| 06:12 | Backfilled all 8 skills into the README skills list with one-line descriptors | README.md | updated, all links verified | ~700 |
| 06:04 | Session end: 2 writes across 1 files (README.md) | 1 reads | ~840 tok |
| 06:20 | Added avoid-ai-writing and startup-free-traffic sections to anatomy; restored dropped google-play-publishing.skill entry | .wolf/anatomy.md | all tracked skill files now indexed | ~900 |
| 06:06 | Session end: 2 writes across 1 files (README.md) | 1 reads | ~840 tok |
| 06:07 | Created ../../../tmp/claude-0/-home-user-useful-assets-AI/60cd6acf-b74f-5f4c-9918-6ca7703929b4/scratchpad/unescape.py | — | ~268 |
| 06:30 | Removed docx-export escaping (\# \- \*\* and &#x20; fillers) from two reference files | current/skills/startup-free-traffic/references/{geo-aeo,pre-launch}.md | headings/lists/bold now render; prose verified byte-identical | ~1500 |
| 06:31 | Repaired anatomy after scanner rescan (dropped 2 .skill entries, indexed a /tmp scratchpad path) | .wolf/anatomy.md | restored | ~400 |
| 06:09 | Session end: 3 writes across 2 files (README.md, unescape.py) | 3 reads | ~3118 tok |
| 06:40 | Fixed 3 anatomy scanner bugs: lossy parse dropping non-token entries, /tmp paths indexed as sections, no scanner existed | .wolf/hooks/{shared,post-write,session-start}.js | 16 regression tests pass; scan runs in ~90ms | ~7000 |
| 06:41 | Logged bug-004/005/006 and recorded learnings | .wolf/buglog.json, .wolf/cerebrum.md | updated | ~1200 |
| 06:15 | Session end: 3 writes across 2 files (README.md, unescape.py) | 3 reads | ~3118 tok |
| 06:45 | Upgraded OpenWolf 1.0.4 -> 2.0.1 via `openwolf update` (backup in .wolf/backups/, user data preserved) | .wolf/hooks/*, .claude/settings.json, OPENWOLF.md | hooks replaced; PreCompact hook added; anatomy migrated to anatomy-index.json | ~9000 |
| 06:46 | Fixed 2.0.1 shipping bug: symbol-extractor.js not copied by update, post-write crashed on every write | .wolf/hooks/symbol-extractor.js | copied from package; post-write verified working | ~800 |
| 06:47 | Re-applied the lossy-parse fix (still unfixed upstream) and recovered 2 entries lost in migration | .wolf/hooks/anatomy-store.js, .wolf/anatomy-index.json | A/B tested patched vs upstream parser | ~2500 |
| 06:23 | Session end: 3 writes across 2 files (README.md, unescape.py) | 3 reads | ~3118 tok |
| 06:50 | Session summary: added improve-codebase-architecture skill; completed README + anatomy skill indexes; de-escaped 2 docx-export reference files; fixed 3 anatomy scanner defects then upgraded OpenWolf 1.0.4→2.0.1, re-applying the one fix still unfixed upstream and repairing the broken 2.0.1 hook install | current/skills/improve-codebase-architecture/*, README.md, .wolf/* | 6 commits pushed to claude/add-new-skill-kwapod; skill audit 45/45, hook tests 16/16 | ~95000 |
| 06:23 | Session end: 3 writes across 2 files (README.md, unescape.py) | 3 reads | ~3118 tok |
| 06:56 | Fixed unsatisfiable Stop-hook nag: countSemanticEntries matched a date prefix against time-prefixed rows, so it always counted 0 | .wolf/hooks/shared.js | patched + verified (12 counted vs 0 upstream); logged bug-009 | ~2000 |
| 06:25 | Session end: 3 writes across 2 files (README.md, unescape.py) | 3 reads | ~3118 tok |
| 06:27 | Session end: 3 writes across 2 files (README.md, unescape.py) | 3 reads | ~3118 tok |
| 06:49 | Created scripts/openwolf-repair.mjs | — | ~1691 |
| 11:17 | Edited .claude/settings.json | 12→17 lines | ~122 |
| 11:47 | Edited .claude/settings.json | 17→22 lines | ~141 |
| 11:50 | Added self-healing repair hook so openwolf upgrades cannot silently revert the two local patches | scripts/openwolf-repair.mjs, .claude/settings.json, .wolf/patches/ | tested against simulated upgrade: both patches auto-restored | ~6000 |
| 11:52 | Wrote filing-ready upstream bug reports for both openwolf 2.0.1 defects | .wolf/patches/UPSTREAM-REPORT.md | ready to submit; session cannot reach cytostack/openwolf | ~2000 |
| 11:49 | Edited scripts/openwolf-repair.mjs | added 4 condition(s) | ~1168 |
| 11:49 | Edited scripts/openwolf-repair.mjs | patchAnatomyParser() → applySourcePatches() | ~20 |
| 11:49 | Edited scripts/openwolf-repair.mjs | 6→11 lines | ~174 |
| 11:55 | Added scripts/openwolf-repair.mjs + own SessionStart entry so openwolf upgrades cannot silently revert the 3 local patches | scripts/openwolf-repair.mjs, .claude/settings.json, .wolf/patches/ | all 3 auto-restore; idempotent; tested vs simulated upgrade | ~8000 |
| 11:57 | Found and fixed a real defect in the earlier bug-009 fix: date-scoped counting failed across midnight | .wolf/hooks/shared.js | now session-scoped; count 15 vs 0 before | ~2000 |
| 11:58 | Wrote filing-ready upstream reports for the two openwolf 2.0.1 defects | .wolf/patches/UPSTREAM-REPORT.md | ready to submit; this session cannot reach cytostack/openwolf | ~2000 |
| 11:52 | Session end: 9 writes across 4 files (README.md, unescape.py, openwolf-repair.mjs, settings.json) | 4 reads | ~7093 tok |
| 12:05 | Fixed a third unsatisfiable Stop-hook reminder: buglog check read session.files_written, which never contains .wolf/ paths | .wolf/hooks/stop.js, scripts/openwolf-repair.mjs | now mtime-based; added to repair table; all 4 patches auto-restore | ~3000 |
| 11:54 | Session end: 9 writes across 4 files (README.md, unescape.py, openwolf-repair.mjs, settings.json) | 4 reads | ~7093 tok |
| 11:58 | Edited current/skills/avoid-ai-writing/SKILL.md | 7→8 lines | ~243 |
| 11:58 | Edited current/skills/avoid-ai-writing/SKILL.md | expanded (+9 lines) | ~271 |
| 11:58 | Edited current/skills/avoid-ai-writing/SKILL.md | inline fix | ~131 |
| 11:58 | Edited current/skills/avoid-ai-writing/SKILL.md | modified at() | ~699 |
| 11:58 | Edited current/skills/avoid-ai-writing/SKILL.md | 1→4 lines | ~80 |
| 11:59 | Edited current/skills/avoid-ai-writing/SKILL.md | expanded (+36 lines) | ~798 |
| 11:59 | Edited current/skills/avoid-ai-writing/SKILL.md | 4→8 lines | ~104 |
| 11:59 | Edited current/skills/avoid-ai-writing/SKILL.md | 3→5 lines | ~66 |
| 11:59 | Edited current/skills/avoid-ai-writing/SKILL.md | expanded (+8 lines) | ~163 |
| 11:59 | Edited current/skills/avoid-ai-writing/README.md | expanded (+6 lines) | ~166 |
| 12:00 | Edited current/skills/avoid-ai-writing/SKILL.md | 7→11 lines | ~556 |
| 12:01 | Created current/skills/avoid-ai-writing/forbidden-patterns.template.md | — | ~407 |
| 12:01 | Edited current/skills/avoid-ai-writing/SKILL.md | 1→3 lines | ~142 |
| 12:20 | Upgraded avoid-ai-writing to 3.5.0: 5 post-em-dash tells, generation-time prevention (ASD-STE100 + Zinsser humanity), forbidden-list workflow, credits | current/skills/avoid-ai-writing/{SKILL.md,README.md,forbidden-patterns.template.md} | self-audited against its own rules | ~7000 |
| 12:02 | Session end: 22 writes across 6 files (README.md, unescape.py, openwolf-repair.mjs, settings.json, SKILL.md) | 4 reads | ~11192 tok |
| 12:10 | Edited current/skills/avoid-ai-writing/SKILL.md | expanded (+32 lines) | ~1085 |
| 12:10 | Edited current/skills/avoid-ai-writing/SKILL.md | 4→6 lines | ~78 |
| 12:10 | Edited current/skills/avoid-ai-writing/SKILL.md | 2→5 lines | ~61 |
| 12:11 | Edited current/skills/avoid-ai-writing/SKILL.md | 1→3 lines | ~172 |
| 12:35 | Absorbed STE skill rules into avoid-ai-writing 3.6.0: 4 grammar patterns, 22 substitutions, and an explicit reject-list for STE rules that flatten voice | current/skills/avoid-ai-writing/{SKILL.md,README.md} | 3 duplicate table rows caught and resolved | ~9000 |
| 12:12 | Session end: 26 writes across 6 files (README.md, unescape.py, openwolf-repair.mjs, settings.json, SKILL.md) | 4 reads | ~12687 tok |
| 13:36 | Session end: 26 writes across 6 files (README.md, unescape.py, openwolf-repair.mjs, settings.json, SKILL.md) | 4 reads | ~12687 tok |
| 13:37 | Session end: 26 writes across 6 files (README.md, unescape.py, openwolf-repair.mjs, settings.json, SKILL.md) | 4 reads | ~12687 tok |
| 16:35 | Edited README.md | inline fix | ~39 |
| 16:36 | Created docs/local-machine-tasks.md | — | ~1083 |
| 16:40 | Unpacked startup-free-traffic.skill as canonical; zip was the better copy (restored 2 lost geo-aeo sections, fixed broken lowercase cross-references) | current/skills/startup-free-traffic/ | 5 refs renamed, SKILL.md added | ~3000 |
| 16:42 | Wrote local-machine handoff instructions and filled STATUS.md (no active quest) | docs/local-machine-tasks.md, .wolf/STATUS.md | ready for the local agent | ~3500 |
