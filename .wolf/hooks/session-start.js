import * as fs from "node:fs";
import * as path from "node:path";
import { getWolfDir, ensureWolfDir, writeJSON, appendMarkdown, readJSON, timestamp, timeShort, readMarkdown, parseAnatomy, serializeAnatomy, walkProject, buildAnatomyEntry, normalizePath } from "./shared.js";
/**
 * Index files that exist on disk but are missing from anatomy.md.
 *
 * Nothing else ever did this: entries were only ever added by the post-write
 * hook, so files that arrived any other way (git clone, checkout, another
 * machine) stayed invisible to a protocol that tells every session to trust
 * anatomy.md before reading anything.
 *
 * Deliberately additive. Entries are never pruned for a missing file, because
 * anatomy legitimately indexes paths that are absent from this checkout —
 * gitignored directories such as _private/ exist on one machine and not another,
 * and pruning them would destroy the index they represent.
 */
function scanIntoAnatomy(wolfDir, projectRoot) {
    const MAX_NEW = 300;
    const anatomyPath = path.join(wolfDir, "anatomy.md");
    const content = readMarkdown(anatomyPath);
    if (!content)
        return;
    const sections = parseAnatomy(content);
    const known = new Set();
    for (const [key, entries] of sections)
        for (const e of entries)
            known.add(normalizePath(path.join(key === "./" ? "." : key, e.file)));
    let added = 0;
    for (const rel of walkProject(projectRoot)) {
        if (added >= MAX_NEW)
            break;
        if (known.has(rel))
            continue;
        const entry = buildAnatomyEntry(projectRoot, rel);
        if (!entry)
            continue;
        const dir = path.dirname(rel);
        const sectionKey = dir === "." ? "./" : normalizePath(dir) + "/";
        if (!sections.has(sectionKey))
            sections.set(sectionKey, []);
        sections.get(sectionKey).push(entry);
        added++;
    }
    let fileCount = 0;
    for (const [, list] of sections)
        fileCount += list.length;
    const serialized = serializeAnatomy(sections, {
        lastScanned: timestamp(),
        fileCount,
        hits: 0,
        misses: 0,
    });
    const tmp = anatomyPath + ".scan.tmp";
    try {
        fs.writeFileSync(tmp, serialized, "utf-8");
        fs.renameSync(tmp, anatomyPath);
    }
    catch {
        try {
            fs.unlinkSync(tmp);
        }
        catch { }
        return;
    }
    if (added > 0) {
        process.stderr.write(`🐺 OpenWolf: indexed ${added} file(s) missing from anatomy.md.\n`);
    }
}
async function main() {
    ensureWolfDir();
    const wolfDir = getWolfDir();
    // Clean up stale .tmp files left from failed atomic writes
    try {
        const files = fs.readdirSync(wolfDir);
        for (const f of files) {
            if (f.endsWith(".tmp")) {
                try {
                    fs.unlinkSync(path.join(wolfDir, f));
                }
                catch { }
            }
        }
    }
    catch { }
    const hooksDir = path.join(wolfDir, "hooks");
    const sessionFile = path.join(hooksDir, "_session.json");
    const now = new Date();
    const sessionId = `session-${now.toISOString().slice(0, 10)}-${String(now.getHours()).padStart(2, "0")}${String(now.getMinutes()).padStart(2, "0")}`;
    // Create fresh session state
    writeJSON(sessionFile, {
        session_id: sessionId,
        started: timestamp(),
        files_read: {},
        files_written: [],
        edit_counts: {},
        anatomy_hits: 0,
        anatomy_misses: 0,
        repeated_reads_warned: 0,
        cerebrum_warnings: 0,
        stop_count: 0,
    });
    // Bring anatomy.md up to date with what is actually on disk
    try {
        scanIntoAnatomy(wolfDir, process.env.CLAUDE_PROJECT_DIR || process.cwd());
    }
    catch { }
    // Append session header to memory.md
    const memoryPath = path.join(wolfDir, "memory.md");
    const header = `\n## Session: ${now.toISOString().slice(0, 10)} ${timeShort()}\n\n| Time | Action | File(s) | Outcome | ~Tokens |\n|------|--------|---------|---------|--------|\n`;
    appendMarkdown(memoryPath, header);
    // Check cerebrum freshness — remind Claude to learn
    try {
        const cerebrumPath = path.join(wolfDir, "cerebrum.md");
        const cerebrumContent = fs.readFileSync(cerebrumPath, "utf-8");
        const stat = fs.statSync(cerebrumPath);
        const daysSinceUpdate = (Date.now() - stat.mtimeMs) / (1000 * 60 * 60 * 24);
        // Count actual entries (non-comment, non-empty lines in content sections)
        const entryLines = cerebrumContent.split("\n").filter(l => {
            const t = l.trim();
            return t.startsWith("- ") || t.startsWith("* ") || (t.startsWith("[") && t.includes("]"));
        });
        if (entryLines.length < 3) {
            process.stderr.write(`💡 OpenWolf: cerebrum.md has only ${entryLines.length} entries. Learn from this session — record user preferences, project conventions, and mistakes to .wolf/cerebrum.md.\n`);
        }
        else if (daysSinceUpdate > 3) {
            process.stderr.write(`💡 OpenWolf: cerebrum.md hasn't been updated in ${Math.floor(daysSinceUpdate)} days. Look for opportunities to add learnings this session.\n`);
        }
    }
    catch { }
    // Check buglog — remind if empty
    try {
        const buglogPath = path.join(wolfDir, "buglog.json");
        const buglog = readJSON(buglogPath, { bugs: [] });
        if (buglog.bugs.length === 0) {
            process.stderr.write(`📋 OpenWolf: buglog.json is empty. If you encounter or fix any bugs, errors, or failed tests this session, log them to .wolf/buglog.json.\n`);
        }
    }
    catch { }
    // Increment total_sessions in token-ledger
    const ledgerPath = path.join(wolfDir, "token-ledger.json");
    const ledger = readJSON(ledgerPath, { version: 1, lifetime: { total_sessions: 0 } });
    ledger.lifetime.total_sessions++;
    writeJSON(ledgerPath, ledger);
    process.exit(0);
}
main().catch(() => process.exit(0));
//# sourceMappingURL=session-start.js.map