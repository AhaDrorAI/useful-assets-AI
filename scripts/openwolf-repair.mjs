#!/usr/bin/env node
/**
 * Re-apply this project's OpenWolf patches after an upgrade.
 *
 * `openwolf update` overwrites everything in .wolf/hooks/ with the released
 * build, which silently reverts two fixes this project depends on:
 *
 *   1. symbol-extractor.js is missing from the release's copy list, but
 *      post-write.js imports it at module load. Without it every Write/Edit
 *      dies with ERR_MODULE_NOT_FOUND and anatomy.md, memory.md, session
 *      tracking, and auto bug detection all stop updating — silently, because
 *      hook failures are not surfaced. (buglog bug-007)
 *
 *   2. parseAnatomy in anatomy-store.js only matches entries ending in
 *      "(~N tok)". Any other size label is dropped, and since anatomy.md is
 *      rendered from the store, a dropped entry is deleted from the index on
 *      the next write. (buglog bug-004, bug-008)
 *
 *   3. countSemanticEntries in shared.js counts memory.md rows by a
 *      "| YYYY-MM-DD" prefix, but every row is written as "| HH:MM |", so the
 *      count is always zero and the Stop hook demands a summary that has
 *      already been written, on every turn. (buglog bug-009)
 *
 * All three are upstream defects in openwolf 2.0.1. Until they are fixed upstream,
 * this script is what keeps them from coming back. It is idempotent: safe to
 * run on every session, does nothing when the hooks are already healthy.
 *
 * Wired as a SessionStart hook in .claude/settings.json. It lives outside
 * .wolf/hooks/ on purpose — `openwolf update` strips hook entries whose
 * command points into .wolf/hooks/, so a repair script kept there would
 * delete its own registration.
 *
 * Run manually with: node scripts/openwolf-repair.mjs [--verbose]
 */
import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const HOOKS = path.join(ROOT, ".wolf/hooks");
const PATCHES = path.join(ROOT, ".wolf/patches");
const VERBOSE = process.argv.includes("--verbose");

const repairs = [];
const problems = [];

// ─── 1. symbol-extractor.js must exist (bug-007) ────────────────────────
function restoreSymbolExtractor() {
    const target = path.join(HOOKS, "symbol-extractor.js");
    if (fs.existsSync(target))
        return;
    // Prefer the installed package, so an openwolf upgrade brings its own
    // version rather than our pinned copy.
    const candidates = [];
    for (const base of [process.env.npm_config_prefix, "/opt/node22/lib", "/usr/local/lib", "/usr/lib"]) {
        if (base)
            candidates.push(path.join(base, "node_modules/openwolf/dist/hooks/symbol-extractor.js"));
    }
    candidates.push(path.join(PATCHES, "symbol-extractor-2.0.1.js"));
    const source = candidates.find((c) => fs.existsSync(c));
    if (!source) {
        problems.push("symbol-extractor.js is missing and no source copy was found — post-write.js will crash on every edit");
        return;
    }
    fs.copyFileSync(source, target);
    repairs.push(`restored symbol-extractor.js from ${source.includes("/.wolf/") ? "the vendored 2.0.1 copy" : "the installed openwolf package"}`);
}

// ─── 2. Source patches this project applies on top of the release ───────
//
// Each entry replaces a known upstream block with a patched one. `marker` is
// what makes the operation idempotent — if it is already in the file, there is
// nothing to do. If `upstream` no longer matches, OpenWolf has changed that
// code and the patch is reported rather than force-fitted.
const PATCH_MARKER = "LOCAL PATCH";

const SOURCE_PATCHES = [
    {
        bug: "bug-008",
        file: "anatomy-store.js",
        what: "the parseAnatomy fix (entries with a non-token size label were dropped)",
        upstream: `        const em = line.match(/^- \`([^\`]+)\`(?:\\s+—\\s+(.+?))?\\s*\\(~(\\d+)\\s+tok\\)$/);
        if (em) {
            sections.get(currentSection).push({
                file: em[1],
                description: em[2] || "",
                tokens: parseInt(em[3], 10),
            });
        }
    }
    return sections;
}`,
        patched: `        const em = line.match(/^- \`([^\`]+)\`(?:\\s+—\\s+(.+?))?\\s*\\(~(\\d+)\\s+tok\\)$/);
        if (em) {
            sections.get(currentSection).push({
                file: em[1],
                description: em[2] || "",
                tokens: parseInt(em[3], 10),
            });
            continue;
        }
        // ${PATCH_MARKER} (not upstream as of 2.0.1): an entry whose size label is
        // not "(~N tok)" — e.g. the hand-written "(~5.1K zip)" on packaged
        // .skill files — used to fail the match above and be dropped silently.
        // Since anatomy.md is now rendered from the store, a dropped entry is
        // deleted from the index on the next write. Import it with tokens 0;
        // a scan or the next write fills in the real count.
        const alt = line.match(/^- \`([^\`]+)\`(?:\\s+—\\s+(.+?))?\\s*(?:\\((.+)\\))?$/);
        if (alt && alt[1]) {
            sections.get(currentSection).push({
                file: alt[1],
                description: alt[2] || "",
                tokens: 0,
            });
        }
    }
    return sections;
}`,
    },
    {
        bug: "bug-009",
        file: "shared.js",
        what: "the countSemanticEntries fix (Stop hook demanded a memory.md summary on every turn)",
        upstream: `        let count = 0;
        for (const line of content.split("\\n")) {
            if (line.startsWith(todayPrefix) && !mechanical.test(line))
                count++;
        }
        return count;`,
        patched: `        let count = 0;
        // ${PATCH_MARKER} (not upstream as of 2.0.1): rows are written as
        // "| HH:MM | ... |" — the format OPENWOLF.md documents and the hooks
        // themselves append — so matching on a "| YYYY-MM-DD" prefix counted
        // zero however many summaries were written, and the Stop hook asked for
        // one on every turn forever.
        //
        // Scope to the current session rather than to today's date: a session
        // that runs past midnight, or one resumed the next day, keeps appending
        // under the header it opened with, so "is the header dated today" is
        // false while summaries are being written. The question the Stop hook
        // is really asking is "did this session write one".
        const lines = content.split("\\n");
        let sessionStart = 0;
        for (let i = 0; i < lines.length; i++) {
            if (/^##\\s+Session:/.test(lines[i]))
                sessionStart = i + 1;
        }
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            if (mechanical.test(line))
                continue;
            if (line.startsWith(todayPrefix))
                count++;
            else if (i >= sessionStart && /^\\|\\s*\\d{1,2}:\\d{2}\\s*\\|/.test(line))
                count++;
        }
        return count;`,
    },
];

function applySourcePatches() {
    for (const p of SOURCE_PATCHES) {
        const target = path.join(HOOKS, p.file);
        if (!fs.existsSync(target)) {
            problems.push(`${p.file} not found — is OpenWolf installed in this project?`);
            continue;
        }
        const src = fs.readFileSync(target, "utf-8");
        if (src.includes(PATCH_MARKER) && src.includes(p.patched.trim().split("\n")[0]))
            continue;
        if (!src.includes(p.upstream)) {
            problems.push(`${p.file} no longer matches the known upstream shape, so ${p.what} was not re-applied — do it by hand and update this script (see .wolf/buglog.json ${p.bug})`);
            continue;
        }
        fs.writeFileSync(target, src.replace(p.upstream, p.patched), "utf-8");
        repairs.push(`re-applied ${p.what} to ${p.file}`);
    }
}

// ─── 3. Verify every hook still loads ───────────────────────────────────
async function verifyHooksImport() {
    if (!fs.existsSync(HOOKS))
        return;
    for (const f of fs.readdirSync(HOOKS).filter((f) => f.endsWith(".js")).sort()) {
        try {
            await import(path.join(HOOKS, f));
        }
        catch (e) {
            // A hook that runs main() on import can exit; only module
            // resolution failures mean a genuinely broken install.
            if (String(e?.code) === "ERR_MODULE_NOT_FOUND")
                problems.push(`${f} cannot load: ${e.message.split("\n")[0]}`);
        }
    }
}

restoreSymbolExtractor();
applySourcePatches();
await verifyHooksImport();

if (repairs.length)
    process.stderr.write(`🔧 OpenWolf patches re-applied after an upgrade: ${repairs.join("; ")}.\n`);
for (const p of problems)
    process.stderr.write(`⚠️  OpenWolf: ${p}\n`);
if (VERBOSE && !repairs.length && !problems.length)
    process.stderr.write("✓ OpenWolf hooks healthy — no repairs needed.\n");

process.exit(problems.length && VERBOSE ? 1 : 0);
