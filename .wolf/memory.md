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
