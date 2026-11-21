# ECC Bootstrap — Mechanics

This file covers *how* to pull content from `everything-claude-code`. The decision logic for *what* to pull is in `skill-selection-rubric.md`.

ECC repo: https://github.com/affaan-m/everything-claude-code

## Strategy

ECC is a large repo (140k+ stars worth of content). Don't full-clone it into the project — clone to a temporary cache, copy out only what's needed, then optionally clean up.

## Step-by-step

### 1. Clone to a temp cache

Use a sparse checkout to only fetch the directories we care about. This is much faster than a full clone.

```bash
ECC_CACHE="/tmp/ecc-cache-$(date +%s)"
git clone --depth 1 --filter=blob:none --sparse https://github.com/affaan-m/everything-claude-code "$ECC_CACHE"
cd "$ECC_CACHE"
git sparse-checkout set rules skills agents
```

If the user has a slow connection or no network, fall back to fetching individual raw files via `https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/<path>`. If even that fails, skip the bootstrap and note it in the final report — the user can run the skill again later when they have connectivity.

The `scripts/fetch_ecc.sh` bundled with this skill wraps this logic. Prefer running it over reinventing the clone command inline.

### 2. Inventory what's available

Walk three directories:

- `$ECC_CACHE/rules/` — has subdirs: `common/`, `typescript/`, `python/`, `golang/`, `swift/`, `php/`, plus possibly more added since this skill was written
- `$ECC_CACHE/skills/` — each subdir has a `SKILL.md` with YAML frontmatter (name + description)
- `$ECC_CACHE/agents/` — flat folder of `*.md` files, each with frontmatter (name + description)

For skills, parse the YAML frontmatter to get the description. The description is what tells you whether the skill fits this project. Don't infer from folder names alone — names are aspirational; descriptions are concrete.

```bash
# Quick way to see all skill descriptions:
for f in "$ECC_CACHE"/skills/*/SKILL.md; do
  awk '/^---$/{if(++c==2)exit;next} c==1' "$f"
  echo "  ── from $f"
  echo
done
```

### 3. Inventory the user's globals

Before deciding what to install at project level, see what the user already has globally — those are available in every project and don't need to be duplicated.

```bash
ls -1 ~/.claude/skills/ 2>/dev/null  # global skills
ls -1 ~/.claude/rules/  2>/dev/null  # global rules (may be a flat list or subdirs)
ls -1 ~/.claude/agents/ 2>/dev/null  # global agents
```

The bundled `scripts/inventory_globals.sh` does this and prints a clean list.

If `~/.claude/` doesn't exist, the user has no globals — install everything proposed at project level.

### 4. Apply the selection rubric

See `skill-selection-rubric.md` for the decision logic. Output is a proposed list of items to install, organized as:

- Rules to install: `rules/common/<files>`, `rules/<stack>/<files>`
- Skills to install: `skills/<skill-1>/`, `skills/<skill-2>/`, ...
- Agents to install: `agents/<agent-1>.md`, ...
- Items to *recommend installing globally* (would help across all projects, not just this one)

### 5. Subtract globals

For each item in the proposed list, check if it's already in the user's globals. If yes, drop it from the project-level install list — but mention it in the final report so the user knows it's covered.

### 6. Present the delta to the user

This is the user's checkpoint. Show them:

```
Proposing to install in .claude/:

Rules:
- common/coding-style.md — universal coding-style rules
- common/git-workflow.md — commit format, PR process
- common/testing.md — TDD, coverage requirements
- common/security.md — mandatory security checks
- typescript/style.md — TS/JS specific (matches your stack)

Skills:
- tdd-workflow — write-tests-first methodology
- verification-loop — build/test/lint verification before claiming done
- search-first — research before coding (cuts wasted implementation)

Agents:
- code-reviewer — review my work for quality and security

Already in your globals (skipping):
- strategic-compact (you have this globally)
- search-first (also already global — overriding above to skip)

Recommended for global install (would help across all your projects):
- continuous-learning-v2 — auto-extracts patterns from sessions

Approve, or drop any from the list?
```

Wait for confirmation. Don't auto-install.

### 7. Install approved items

Never overwrite anything that already exists in the project's `.claude/`. A project copy may hold local customisations, and the approval list did not tell the user it would be replaced.

Before you present the approval list (step 6), check each proposed item against the project as well as the globals:

```bash
# A rule, skill or agent that already exists in the project is "skipped (exists)"
for p in rules/common/coding-style.md skills/tdd-workflow agents/code-reviewer.md; do
  [ -e ".claude/$p" ] && echo "skipped (exists in project): $p"
done
```

List those items as "skipped (already in project)" in the approval message.

Copy only items that do not exist yet. Copy a skill as a whole folder, and only when the destination folder does not exist; never merge into an existing skill folder:

```bash
copy_new_file() {  # $1 = source, $2 = destination file
  if [ -e "$2" ]; then echo "skipped (exists): $2"; else mkdir -p "$(dirname "$2")" && cp "$1" "$2"; fi
}
copy_new_dir() {   # $1 = source folder, $2 = destination folder
  if [ -e "$2" ]; then echo "skipped (exists): $2"; else mkdir -p "$(dirname "$2")" && cp -R "$1" "$2"; fi
}

copy_new_file "$ECC_CACHE/rules/common/coding-style.md" .claude/rules/common/coding-style.md
copy_new_file "$ECC_CACHE/rules/common/git-workflow.md" .claude/rules/common/git-workflow.md
copy_new_dir  "$ECC_CACHE/skills/tdd-workflow"          .claude/skills/tdd-workflow
copy_new_file "$ECC_CACHE/agents/code-reviewer.md"      .claude/agents/code-reviewer.md
```

Report every "skipped (exists)" line in the final report.

### 8. Clean up the cache

```bash
rm -rf "$ECC_CACHE"
```

Or leave it — it's small after sparse-checkout, and a future re-run of this skill can reuse it.

## Notes on ECC drift

ECC is actively maintained — new skills, rules, and agents land regularly. Don't bake a fixed list of "good ECC content" into this skill. Always inventory the live `$ECC_CACHE/skills/` and `rules/` and `agents/` directories at runtime so you're working with the current catalog.

If a specific item the rubric expected (e.g., `tdd-workflow`) isn't there, just skip it and note the absence — don't fail the whole step.

## When ECC is unreachable

If the clone fails (no network, GitHub down, rate-limited):

1. Don't fail the skill. Generate everything else (markdown files, settings.json, etc.).
2. In the final report, include: "ECC bootstrap was skipped because [reason]. To run it later, re-invoke this skill or manually clone ECC and copy the items you want into `.claude/`."
3. Still create empty `.claude/skills/`, `.claude/rules/`, `.claude/agents/` so the structure exists.
