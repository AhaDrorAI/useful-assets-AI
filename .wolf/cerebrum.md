# Cerebrum

> OpenWolf's learning memory. Updated automatically as the AI learns from interactions.
> Do not edit manually unless correcting an error.
> Last updated: 2026-08-12

## User Preferences

<!-- How the user likes things done. Code style, tools, patterns, communication. -->

- Wants indexes kept complete and honest: when a skill is added, it belongs in both `README.md` and `.wolf/anatomy.md`, and gaps in those lists are worth fixing rather than working around.
- Prefers root causes over workarounds — when told a tool was corrupting a file, asked for the tool to be fixed rather than the file re-patched.

## Key Learnings

- **Project:** AI-agent-guide
- **Description:** Reusable guides, skills, and examples for helping non-developers work with Claude Code, Codex, and AI coding agents.
- **Skills live in `current/skills/<name>/SKILL.md`**, with optional `references/`, `agents/openai.yaml`, and `evals/`. Some ship only as a packaged `<name>.skill` zip (startup-free-traffic has no unpacked SKILL.md).
- **The `.wolf/hooks/*.js` files are vendored build output** (they carry `//# sourceMappingURL=` comments but no `.map` files) and are tracked in git. Local fixes to them are real, but reinstalling or upgrading the `openwolf` CLI may overwrite them.
- **OpenWolf is at 2.0.1 here** (upgraded from 1.0.4 via `openwolf update`, which backs up to `.wolf/backups/` and preserves cerebrum/memory/anatomy/buglog/config). The CLI is not bundled with the repo — `npm i -g openwolf` is needed on each machine to run `openwolf scan`, `status`, `update`.
- **2.0.1 changed the anatomy architecture**: `.wolf/anatomy-index.json` is now the source of truth and `anatomy.md` is *rendered* from it, with symbol sub-entries for large code files. Hand-editing anatomy.md still works — the store re-imports it when the file's hash changes — but the store wins on the next write.
- **One local patch rides on top of 2.0.1**, marked `LOCAL PATCH` in `.wolf/hooks/anatomy-store.js` (see bug-008). `openwolf update` will overwrite it; re-apply it and re-copy `symbol-extractor.js` (bug-007) after any upgrade.
- **anatomy.md round-trips through `parseAnatomy`/`serializeAnatomy` on every write.** Any line those functions cannot parse is deleted. Adding a new line format to anatomy means teaching the parser about it first.
- **Several reference files came from a docx/Notion export** and carried escaped markdown (`\#`, `\-`, `\*\*`) plus `&#x20;` spacer paragraphs. Worth checking new imports for the same.

## Do-Not-Repeat

<!-- Mistakes made and corrected. Each entry prevents the same mistake recurring. -->
<!-- Format: [YYYY-MM-DD] Description of what went wrong and what to do instead. -->

- [2026-08-12] Do not hand-patch `.wolf/anatomy.md` and assume it sticks — a hook rewrites the whole file on the next write anywhere in the repo. Three manual repairs were undone this way before the parser was fixed. Fix the hook, then repair the file.
- [2026-08-12] When verifying that a cleanup changed only formatting, strip the artifact from *both* sides of the comparison. Stripping `&#x20;` from only the new file made an identical-prose check report a false difference.
- [2026-08-12] Do not run `openwolf scan` in a fresh clone and commit the result. The scan prunes entries whose files are missing, and `_private/` plus every `desktop.ini` is gitignored — a scan in CI or a container deletes them from anatomy.md. Run a full scan only on a machine that has the complete working tree.
- [2026-08-12] After any `openwolf update`, check that `.wolf/hooks/symbol-extractor.js` exists before trusting the hooks. 2.0.1 does not copy it, and `post-write.js` dies on import, which fails silently — anatomy and memory simply stop updating.

## Decision Log

<!-- Significant technical decisions with rationale. Why X was chosen over Y. -->

- [2026-08-12] **The anatomy scan is additive and never prunes.** Pruning entries whose files are missing would look correct but would erase indexes for gitignored paths (`_private/`) that exist on the user's machine and not in a fresh clone. Stale entries are a smaller cost than destroyed ones.
- [2026-08-12] **The scan runs at SessionStart, not on every write**, bounded to 5000 files / 3s (~90ms on this repo) to stay inside the hook's 5s timeout. Per-write scanning would pay the full cost on every edit for a result that changes only when files appear.
- [2026-08-12] **`Last scanned` is now written only by an actual scan.** post-write preserves the existing timestamp, because a header claiming a fresh scan after a single-file edit is what made a two-skill gap in anatomy look like a complete index.
