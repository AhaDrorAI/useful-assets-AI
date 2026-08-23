#!/usr/bin/env python3
"""
package_skills.py

Builds one upload-ready ZIP per skill, checks each skill against the limits the
Claude app enforces on upload, and verifies that every references/*.md path named
inside a SKILL.md actually exists with matching case.

Run from the repo root:

    python scripts/package_skills.py

Output lands in dist/. Each ZIP contains the skill folder at its root, which is
the layout both the Claude app and ChatGPT expect.

No dependencies. Standard library only.
"""

import re
import sys
import zipfile
from pathlib import Path

SKILLS_DIR = Path("current/skills")
OUT_DIR = Path("dist")

# Limits documented for skill upload in the Claude app.
NAME_MAX = 64
DESC_MAX = 200

# Junk that must never end up inside a published ZIP.
EXCLUDE_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini", "__pycache__", ".git"}
EXCLUDE_SUFFIXES = {".pyc", ".tmp", ".bak"}


def read_frontmatter(skill_md: Path):
    """Return (name, description) from the YAML frontmatter, or (None, None)."""
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return None, None
    block = match.group(1)

    def field(key):
        # Handles both plain and quoted values on a single line.
        m = re.search(rf"^{key}\s*:\s*(.+?)\s*$", block, re.MULTILINE)
        if not m:
            return None
        return m.group(1).strip().strip("'\"")

    return field("name"), field("description")


def check_reference_links(skill_dir: Path, skill_md: Path):
    """Every references/x.md named in SKILL.md must exist with EXACT case.

    Windows and macOS are case-insensitive, so a wrong-case link works locally and
    fails on Linux and inside the plugin cache. The skill then silently runs without
    half its rules and reports the text clean, which is worse than not running at all.
    """
    problems, warnings = [], []
    text = skill_md.read_text(encoding="utf-8")
    named = sorted(set(re.findall(r"references/[A-Za-z0-9_.-]+\.md", text)))
    if not named:
        return problems, warnings

    ref_dir = skill_dir / "references"
    on_disk = {p.name for p in ref_dir.iterdir()} if ref_dir.is_dir() else set()

    for link in named:
        fname = link.split("/", 1)[1]
        if fname in on_disk:
            continue
        same_lower = [a for a in on_disk if a.lower() == fname.lower()]
        if same_lower:
            problems.append(
                f"SKILL.md links `{link}` but the file is `references/{same_lower[0]}`. "
                f"Case mismatch. Works on Windows, breaks everywhere else."
            )
        else:
            problems.append(f"SKILL.md links `{link}` but no such file exists")

    unlinked = on_disk - {l.split("/", 1)[1] for l in named}
    for o in sorted(unlinked):
        warnings.append(f"`references/{o}` exists but SKILL.md never routes to it. It will never load.")

    return problems, warnings


def should_skip(path: Path) -> bool:
    if any(part in EXCLUDE_NAMES for part in path.parts):
        return True
    return path.suffix in EXCLUDE_SUFFIXES


def check(skill_dir: Path):
    """Validate one skill. Returns (errors, warnings)."""
    problems = []
    warnings = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        # Case-insensitive filesystems hide this. Check explicitly.
        alt = [p for p in skill_dir.iterdir() if p.name.lower() == "skill.md"]
        if alt:
            skill_md = alt[0]
        else:
            return ["no SKILL.md"], []

    name, desc = read_frontmatter(skill_md)

    if name is None:
        problems.append("frontmatter has no `name`")
    else:
        if name != skill_dir.name:
            problems.append(f"`name` is '{name}' but the folder is '{skill_dir.name}'. They must match.")
        if len(name) > NAME_MAX:
            problems.append(f"`name` is {len(name)} chars, limit is {NAME_MAX}")

    if desc is None:
        problems.append("frontmatter has no `description`")
    elif len(desc) > DESC_MAX:
        warnings.append(
            f"`description` is {len(desc)} chars. The Claude app documents a {DESC_MAX} "
            f"char limit for uploaded skills. Over by {len(desc) - DESC_MAX}. "
            f"Fine in Claude Code and as a plugin."
        )

    if "\n" in (desc or ""):
        problems.append("`description` spans more than one line. It must be a single line.")

    ref_problems, ref_warnings = check_reference_links(skill_dir, skill_md)
    problems += ref_problems
    warnings += ref_warnings

    return problems, warnings


def build_zip(skill_dir: Path) -> Path:
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / f"{skill_dir.name}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(skill_dir.rglob("*")):
            if path.is_dir() or should_skip(path):
                continue
            # arcname keeps the skill folder as the top level inside the ZIP.
            z.write(path, path.relative_to(skill_dir.parent).as_posix())
    return out


def main():
    if not SKILLS_DIR.is_dir():
        print(f"Not found: {SKILLS_DIR}. Run this from the repo root.", file=sys.stderr)
        return 1

    skills = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skills:
        print(f"No skill folders in {SKILLS_DIR}.", file=sys.stderr)
        return 1

    strict = "--strict" in sys.argv
    failed = 0
    warned = 0

    for skill_dir in skills:
        problems, warnings = check(skill_dir)
        if problems:
            failed += 1
            print(f"[FAIL] {skill_dir.name}")
            for p in problems:
                print(f"        {p}")
            continue
        if warnings and strict:
            failed += 1
            print(f"[FAIL] {skill_dir.name}   (--strict)")
            for w in warnings:
                print(f"        {w}")
            continue
        out = build_zip(skill_dir)
        size_kb = out.stat().st_size / 1024
        label = "warn" if warnings else "ok"
        if warnings:
            warned += 1
        print(f"[{label:<4}] {skill_dir.name}  ->  {out}  ({size_kb:.0f} KB)")
        for w in warnings:
            print(f"        {w}")

    print()
    print(f"{len(skills) - failed} packaged ({warned} with warnings), {failed} blocked. "
          f"ZIPs are in {OUT_DIR}/")
    if warned:
        print("Warnings do not affect Claude Code or the plugin path. They only")
        print("matter if you upload the ZIP by hand into the Claude app.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
