#!/usr/bin/env python3
"""
package_skills.py

Lints every skill in this repository, then builds one upload-ready ZIP per skill.

Run from the repo root:

    python scripts/package_skills.py                 # lint + package every skill root
    python scripts/package_skills.py --strict        # warnings also block
    python scripts/package_skills.py --upload-check  # also warn on the Claude app's
                                                     # 200-char description limit
    python scripts/package_skills.py --lint PATH...  # lint only, any skill folders or
                                                     # roots (for skills in other repos)

Output lands in dist/. Each ZIP contains the skill folder at its root, which is the
layout both the Claude app and ChatGPT expect. Test cases (evals/) and hand-built
.skill archives never go into a ZIP.

What the lint checks, and why each check exists, is documented in
docs/skill-review.md. Errors block packaging. Warnings print and do not block
unless --strict is set.

No dependencies. Standard library only.
"""

import datetime as dt
import re
import subprocess
import sys
import zipfile
from pathlib import Path

# Every folder whose subfolders are skills. Missing roots are skipped.
SKILL_ROOTS = [
    Path("current/skills"),
    Path("account-skills"),
    Path("vector-operating-system/skills"),
    Path("vector-private-memory/skills"),
]
OUT_DIR = Path("dist")

NAME_MAX = 64
DESC_MAX_SPEC = 1024   # Agent Skills spec hard limit.
DESC_MAX_UPLOAD = 200  # Claude app upload form. Checked only with --upload-check.
DEFAULT_REVIEW_DAYS = 180

# Junk that must never end up inside a published ZIP.
EXCLUDE_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini", "__pycache__", ".git",
                 "node_modules"}
EXCLUDE_SUFFIXES = {".pyc", ".tmp", ".bak", ".skill"}
EXCLUDE_TOP_DIRS = {"evals"}
# Never zipped, even outside a git checkout: local config and likely secrets.
SECRET_NAME_RE = re.compile(r"^(\.env(\..*)?|\.claude|\.wolf|.*\.(pem|key|p12|pfx)|id_(rsa|ed25519).*|credentials\.json)$", re.I)

# Vague wording that hides a decision. Each hit should become a rule, a threshold,
# a fallback, or a question to the user. Quoted text and code are ignored.
VAGUE_TERMS = [
    "maybe", "as needed", "a few", "if appropriate", "as appropriate",
    "where relevant", "when relevant", "if possible", "when possible",
    "if needed", "when needed", "some point", "etc.", "and so on",
    "should probably", "might want to",
]

# Tools that can change files or run arbitrary commands. Pre-approving them in
# allowed-tools removes the permission prompt that would otherwise enforce an
# approval gate written in prose.
WRITE_CAPABLE = {"Write", "Edit", "MultiEdit", "NotebookEdit", "Bash"}

LOCAL_PATH_RE = re.compile(
    r"(?<![\w/.-])((?:references|scripts|agents|assets|kit|examples)/[A-Za-z0-9_./-]+"
    r"\.(?:md|py|sh|js|mjs|ts|json|yaml|yml|txt|ps1|html))"
)


# --------------------------------------------------------------------------- #
# Frontmatter
# --------------------------------------------------------------------------- #

def parse_frontmatter(text: str):
    """Parse the YAML subset skills use: scalars, quoted scalars, folded (>) and
    literal (|) blocks, simple lists, and one level of nested maps.

    Returns (dict, body) or (None, text) when there is no frontmatter."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not m:
        return None, text
    lines = m.group(1).splitlines()
    body = text[m.end():]
    data, i = {}, 0

    def unquote(v):
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
            v = v[1:-1]
        return v

    while i < len(lines):
        line = lines[i]
        km = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if not km:
            i += 1
            continue
        key, val = km.group(1), km.group(2).strip()
        i += 1
        if val in (">", ">-", "|", "|-", ">+", "|+"):
            block = []
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            if val.startswith(">"):
                data[key] = " ".join(b for b in block if b).strip()
            else:
                data[key] = "\n".join(block).strip()
        elif val == "":
            nested, items = {}, []
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                sub = lines[i].strip()
                i += 1
                if not sub:
                    continue
                if sub.startswith("- "):
                    items.append(unquote(sub[2:]))
                    continue
                sm = re.match(r"^([A-Za-z0-9_/-]+)\s*:\s*(.*)$", sub)
                if sm:
                    nested[sm.group(1)] = unquote(sm.group(2))
            data[key] = items if items else nested
        else:
            data[key] = unquote(val)
    return data, body


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #

def strip_code_and_quotes(body: str):
    """Yield (line_no, text) for prose lines, with code, inline code and quoted
    examples removed, so the vague-word lint does not flag quoted examples."""
    in_fence = False
    for n, line in enumerate(body.splitlines(), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = re.sub(r"`[^`]*`", "", line)
        line = re.sub(r"\"[^\"]*\"|“[^”]*”|'[^'\n]{3,}'", "", line)
        yield n, line


def check_local_paths(skill_dir: Path, body: str):
    """Every bundled file the skill names must exist with exact case."""
    problems, warnings = [], []
    named = sorted(set(LOCAL_PATH_RE.findall(body)))
    for link in named:
        target = skill_dir / link
        if target.exists() and target.name in {p.name for p in target.parent.iterdir()}:
            continue
        parent = target.parent
        if parent.is_dir():
            same_lower = [p.name for p in parent.iterdir() if p.name.lower() == target.name.lower()]
            if same_lower:
                problems.append(f"names `{link}` but the file is `{same_lower[0]}`. "
                                f"Case mismatch: works on Windows/macOS, breaks on Linux.")
                continue
        problems.append(f"names `{link}` but no such file is bundled. The skill will "
                        f"run without it.")

    for mlink in re.findall(r"\[[^\]]*\]\(([^)#]+)(?:#[^)]*)?\)", body):
        if mlink.startswith(("http://", "https://", "mailto:")):
            continue
        if not (skill_dir / mlink).exists():
            problems.append(f"markdown link to `{mlink}` but no such file is bundled.")

    ref_dir = skill_dir / "references"
    if ref_dir.is_dir():
        mentioned = set(re.findall(r"references/([A-Za-z0-9_.-]+\.md)", body))
        for f in sorted(p.name for p in ref_dir.iterdir() if p.suffix == ".md"):
            if f not in mentioned and f"]({f})" not in body:
                warnings.append(f"`references/{f}` exists but SKILL.md never routes to it. "
                                f"It will never load.")
    return problems, warnings


def check_vague(body: str, offset: int = 0):
    hits = []
    for n, line in strip_code_and_quotes(body):
        n += offset
        low = line.lower()
        for term in VAGUE_TERMS:
            if re.search(rf"(?<![\w-]){re.escape(term)}(?![\w-])", low):
                hits.append(f"line {n}: '{term}'")
    if not hits:
        return []
    shown = "; ".join(hits[:5]) + (f"; +{len(hits) - 5} more" if len(hits) > 5 else "")
    return [f"{len(hits)} vague term(s) in instructions ({shown}). Replace each with a "
            f"rule, threshold, fallback, or question, or keep it where judgment is intended."]


def check_allowed_tools(fm: dict):
    raw = fm.get("allowed-tools")
    if not raw:
        return []
    tools = raw if isinstance(raw, list) else [t.strip() for t in str(raw).split(",")]
    risky = [t for t in tools if t in WRITE_CAPABLE]  # scoped Bash(...) is not flagged
    if not risky:
        return []
    return [f"allowed-tools pre-approves {', '.join(risky)}. That removes the permission "
            f"prompt for those tools while the skill runs. Confirm no approval gate in the "
            f"instructions depends on that prompt, or scope it (e.g. `Bash(git log:*)`)."]


def check_review_metadata(fm: dict, today: dt.date):
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    last = meta.get("last_reviewed")
    if not last:
        return ["no `metadata.last_reviewed` date. Drift review cannot be scheduled."]
    try:
        last_d = dt.date.fromisoformat(last)
    except ValueError:
        return [f"`metadata.last_reviewed` is '{last}', not an ISO date (YYYY-MM-DD)."]
    every = int(meta.get("review_every_days", DEFAULT_REVIEW_DAYS))
    age = (today - last_d).days
    if age > every:
        return [f"last reviewed {age} days ago; review interval is {every} days. "
                f"Run the drift review in docs/skill-review.md."]
    return []


def check_evals(skill_dir: Path):
    """Validate test-case folders in the `claude plugin eval` layout."""
    problems, warnings = [], []
    ev = skill_dir / "evals"
    cases = [p for p in ev.iterdir() if p.is_dir() and p.name not in {"files", "results"}] \
        if ev.is_dir() else []
    has_legacy = (ev / "evals.json").exists()
    if not cases and not has_legacy:
        warnings.append("no test cases in evals/. Behaviour changes cannot be checked.")
        return problems, warnings
    for c in cases:
        for need in ("prompt.md", "case.yaml"):
            if not (c / need).exists():
                problems.append(f"evals/{c.name}: missing {need}")
        graders = list((c / "graders").glob("*.md")) if (c / "graders").is_dir() else []
        if not graders:
            problems.append(f"evals/{c.name}: no graders/*.md. The case will not load.")
        cy = c / "case.yaml"
        if cy.exists():
            t = cy.read_text(encoding="utf-8")
            if not re.search(r'^schema_version:\s*"[^"]+"', t, re.M):
                problems.append(f"evals/{c.name}/case.yaml: schema_version must be quoted.")
            nm = re.search(r"^name:\s*(\S+)", t, re.M)
            if not nm or nm.group(1) != c.name:
                problems.append(f"evals/{c.name}/case.yaml: name must equal the folder name.")
    return problems, warnings


def check(skill_dir: Path, today: dt.date, upload_check: bool):
    """Validate one skill. Returns (errors, warnings)."""
    problems, warnings = [], []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        alt = [p for p in skill_dir.iterdir() if p.name.lower() == "skill.md"]
        if alt:
            problems.append(f"file is `{alt[0].name}`; it must be `SKILL.md` exactly.")
        return problems or ["no SKILL.md"], []

    full = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(full)
    offset = full[: len(full) - len(body)].count("\n")
    if fm is None:
        return ["no YAML frontmatter"], []

    name, desc = fm.get("name"), fm.get("description")
    if not name:
        problems.append("frontmatter has no `name`")
    else:
        folder = skill_dir.resolve().name
        if name != folder:
            problems.append(f"`name` is '{name}' but the folder is '{folder}'.")
        if len(name) > NAME_MAX or not re.fullmatch(r"[a-z0-9-]+", name):
            problems.append(f"`name` must be lowercase letters, digits and hyphens, "
                            f"max {NAME_MAX} chars.")

    if not desc or not isinstance(desc, str):
        problems.append("frontmatter has no `description`")
    else:
        if len(desc) > DESC_MAX_SPEC:
            problems.append(f"`description` is {len(desc)} chars; the spec limit is "
                            f"{DESC_MAX_SPEC}.")
        if upload_check and len(desc) > DESC_MAX_UPLOAD:
            warnings.append(f"`description` is {len(desc)} chars; the Claude app upload "
                            f"form documents {DESC_MAX_UPLOAD}.")
        if not re.search(r"\buse\b.{0,40}?\b(when|whenever|before|for|at|if|alongside)\b|"
                         r"\btrigger|הפעל", desc, re.I):
            warnings.append("`description` has no trigger clause ('Use when ...'). "
                            "The model may not know when to load the skill.")

    nested = [p for p in skill_dir.rglob("SKILL.md")
              if p != skill_md and "evals" not in p.relative_to(skill_dir).parts]
    if nested:
        problems.append(f"extra SKILL.md files ({', '.join(str(p.relative_to(skill_dir)) for p in nested)}). "
                        f"Upload accepts exactly one.")

    stray = [p.name for p in skill_dir.glob("*.skill")]
    if stray:
        warnings.append(f"hand-built archive(s) in the tree: {', '.join(stray)}. "
                        f"docs/maintaining.md says not to commit these.")

    p, w = check_local_paths(skill_dir, body)
    problems += p
    warnings += w
    warnings += check_vague(body, offset)
    warnings += check_allowed_tools(fm)
    warnings += check_review_metadata(fm, today)
    p, w = check_evals(skill_dir)
    problems += p
    warnings += w
    return problems, warnings


# --------------------------------------------------------------------------- #
# Packaging
# --------------------------------------------------------------------------- #

def publishable_files(skill_dir: Path):
    """Files git would publish: tracked, or untracked but not ignored.
    Returns None outside a git checkout. The ZIP then relies on the name rules
    alone. .gitignore is the publish boundary (docs/maintaining.md), so an
    uploaded ZIP must respect it the same way the repo does."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "."],
            cwd=skill_dir, capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return {(skill_dir / f.decode()).resolve() for f in out.split(b"\0") if f}


def should_skip(path: Path, skill_dir: Path, allowed=None) -> bool:
    rel = path.relative_to(skill_dir)
    if rel.parts and rel.parts[0] in EXCLUDE_TOP_DIRS:
        return True
    if any(part in EXCLUDE_NAMES or SECRET_NAME_RE.match(part) for part in rel.parts):
        return True
    if allowed is not None and path.resolve() not in allowed:
        return True
    return path.suffix in EXCLUDE_SUFFIXES


def build_zip(skill_dir: Path) -> Path:
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / f"{skill_dir.name}.zip"
    allowed = publishable_files(skill_dir)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(skill_dir.rglob("*")):
            if path.is_dir() or should_skip(path, skill_dir, allowed):
                continue
            z.write(path, path.relative_to(skill_dir.parent).as_posix())
    return out


def discover(paths):
    skills = []
    for root in paths:
        if (root / "SKILL.md").exists():
            skills.append(root)
        elif root.is_dir():
            skills += sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
    return skills


def main():
    args = sys.argv[1:]
    strict = "--strict" in args
    upload_check = "--upload-check" in args
    lint_only = "--lint" in args
    extra = [Path(a) for a in args if not a.startswith("--")]

    roots = extra if lint_only and extra else [r for r in SKILL_ROOTS if r.is_dir()]
    if not roots:
        print("No skill roots found. Run this from the repo root.", file=sys.stderr)
        return 1
    skills = discover(roots)
    if not skills:
        print("No skill folders found.", file=sys.stderr)
        return 1

    today = dt.date.today()
    failed = warned = 0
    for skill_dir in skills:
        problems, warnings = check(skill_dir, today, upload_check)
        label = skill_dir.as_posix()
        if problems or (warnings and strict):
            failed += 1
            print(f"[FAIL] {label}" + ("   (--strict)" if not problems else ""))
            for p in problems + warnings:
                print(f"        {p}")
            continue
        if warnings:
            warned += 1
        if lint_only:
            print(f"[{'warn' if warnings else 'ok':<4}] {label}")
        else:
            out = build_zip(skill_dir)
            print(f"[{'warn' if warnings else 'ok':<4}] {label}  ->  {out}  "
                  f"({out.stat().st_size / 1024:.0f} KB)")
        for w in warnings:
            print(f"        {w}")

    print()
    verb = "linted" if lint_only else "packaged"
    print(f"{len(skills) - failed} {verb} ({warned} with warnings), {failed} blocked.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
