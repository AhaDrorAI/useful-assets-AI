#!/usr/bin/env python3
"""Audit a skill package against Anthropic's authoring best practices
plus the findings from the review of this specific skill."""

import re
import sys
from pathlib import Path

RESULTS = []


def check(cid, name, ok, detail=""):
    RESULTS.append((cid, name, bool(ok), detail))


def split_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    raw = text[3:end].strip()
    fm = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[end + 4:]


def local_links(text):
    """Markdown links pointing at local files (not http, not anchors)."""
    out = []
    for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
        t = m.group(1)
        if t.startswith(("http://", "https://", "#", "mailto:")):
            continue
        out.append(t)
    return out


def audit(skill_dir: Path):
    sk = skill_dir / "SKILL.md"
    if not sk.exists():
        check("R0", "SKILL.md exists", False, "not found")
        return
    check("R0", "SKILL.md exists", True)

    text = sk.read_text()
    fm, body = split_frontmatter(text)

    # --- R1 frontmatter --------------------------------------------------
    check("R1a", "Frontmatter parses", fm is not None)
    if not fm:
        return
    name = fm.get("name", "")
    desc = fm.get("description", "")
    check("R1b", "name matches ^[a-z0-9-]{1,64}$",
          bool(re.fullmatch(r"[a-z0-9-]{1,64}", name)), name)
    check("R1c", "name avoids reserved words",
          not any(w in name.lower() for w in ("anthropic", "claude")), name)
    check("R1d", "description non-empty and <=1024 chars",
          0 < len(desc) <= 1024, f"{len(desc)} chars")
    check("R1e", "description has an explicit trigger clause",
          bool(re.search(r"\buse (when|whenever)\b", desc, re.I)))
    check("R1f", "description is third person",
          not re.search(r"\b(I can|I will|you can use this)\b", desc, re.I))
    check("R1g", "no XML tags in frontmatter",
          not re.search(r"<[a-zA-Z/][^>]*>", name + desc))

    # --- R6 declared surface ---------------------------------------------
    check("R6a", "allowed-tools declared", "allowed-tools" in fm)
    check("R6b", "license declared", "license" in fm)

    # --- R2 size, links, depth -------------------------------------------
    nlines = len(body.strip().splitlines())
    check("R2a", "SKILL.md body under 500 lines", nlines < 500, f"{nlines} lines")

    links = local_links(body)
    missing = [l for l in links if not (skill_dir / l).exists()]
    check("R2b", "no dead local references in SKILL.md",
          not missing, ", ".join(missing) or f"{len(links)} refs all resolve")

    # references one level deep: files linked from SKILL.md must not
    # introduce further local files of their own
    deeper = []
    for l in set(links):
        p = skill_dir / l
        if p.exists() and p.suffix == ".md":
            for sub in local_links(p.read_text()):
                if sub not in links and sub != "SKILL.md":
                    deeper.append(f"{l} -> {sub}")
    check("R2c", "references stay one level deep",
          not deeper, ", ".join(deeper) or "ok")

    # --- R5 hygiene -------------------------------------------------------
    all_md = sorted(skill_dir.rglob("*.md"))
    backslash = [str(p.name) for p in all_md
                 if re.search(r"\b\w+\\[\w/]+\.(md|py|ts|js)\b", p.read_text())]
    check("R5a", "no Windows-style paths", not backslash, ", ".join(backslash) or "ok")

    timey = []
    for p in all_md:
        for m in re.finditer(
                r"\b(as of|before|after|until)\s+(January|February|March|April|May|June|"
                r"July|August|September|October|November|December|20\d\d)\b",
                p.read_text(), re.I):
            timey.append(f"{p.name}: {m.group(0)}")
    check("R5b", "no time-sensitive statements", not timey, "; ".join(timey) or "ok")

    # terminology: banned words may appear only where flagged as banned
    bad_terms = []
    for p in all_md:
        for i, line in enumerate(p.read_text().splitlines(), 1):
            if re.search(r"\b(component|boundary)\b", line, re.I):
                if not re.search(r"avoid|don't|do not|not \"|instead|drift|banned|\|",
                                 line, re.I):
                    bad_terms.append(f"{p.name}:{i}")
    check("R5c", "banned vocabulary only appears in avoid-lists",
          not bad_terms, ", ".join(bad_terms) or "ok")

    # TOC in long reference files
    no_toc = []
    for p in all_md:
        if p.name == "SKILL.md":
            continue
        t = p.read_text()
        if len(t.splitlines()) > 100 and "## Contents" not in t:
            no_toc.append(p.name)
    check("R5d", "reference files >100 lines have a Contents list",
          not no_toc, ", ".join(no_toc) or "ok")

    # --- R7-R12 the findings from the review -----------------------------
    check("R7a", "explicit stop/gate before the design conversation",
          bool(re.search(r"stop there and wait|then stop", body, re.I)))
    check("R7b", "no-grill escape hatch documented",
          bool(re.search(r"no grill|just the report|don't interview", body, re.I)))
    check("R8", "repo writes are gated on user confirmation",
          bool(re.search(r"ask every time|only on yes|only after the user says",
                         body, re.I)))
    check("R9", "harness-neutral exploration with fallback",
          bool(re.search(r"if (the harness|it does not)", body, re.I))
          and "sequential" in body.lower())
    check("R10a", "scan budget is numeric",
          bool(re.search(r"at most ~?\d+ files", body, re.I)))
    check("R10b", "budgets are justified, not voodoo constants",
          bool(re.search(r"why these numbers|because", body, re.I)))
    check("R11", "explicit zero-findings exit",
          bool(re.search(r"if nothing passes the deletion test", body, re.I)))
    check("R12a", "output is self-contained by default",
          bool(re.search(r"loads no external resources|no external resources",
                         body, re.I)))
    check("R12b", "output is verified before hand-off",
          "grep" in body and bool(re.search(r"step 4|verify", body, re.I)))

    # --- R3/R4 structure --------------------------------------------------
    check("R3", "workflow presented as a trackable checklist",
          bool(re.search(r"- \[ \] Step 1", body)))
    check("R4", "a verification step exists in the workflow",
          bool(re.search(r"###? Step \d+ — Verify", body)))

    # --- A1-A8: regressions for the findings of the adversarial pass ------

    # A1: the scan cap and the report cap must not contradict each other
    stop_at = re.search(r"stop scanning[^.]*?(\d+) candidates", body, re.I)
    report_cap = re.findall(r"(?:more than|report the) (\d+)", body, re.I)
    coherent = bool(stop_at) and all(int(n) == int(stop_at.group(1))
                                     for n in report_cap)
    check("A1", "scan cap and report cap are numerically coherent",
          coherent, f"scan stops at {stop_at.group(1) if stop_at else '?'}, "
                    f"report caps {set(report_cap) or '?'}")

    # A2: no absolute claim that contradicts the consented repo writes
    check("A2", "read-only claim does not contradict consented writes",
          not re.search(r"every artifact[^.]*outside the repo", body, re.I))

    # A3: shell checks must not treat a zero-match grep as a failure
    check("A3", "verification command is exit-code safe",
          "grep -Eic" not in body and ("wc -l" in body or "|| true" in body))

    # A4: the hot-spot heuristic needs a no-git fallback
    check("A4", "handles a repo with no git history",
          bool(re.search(r"no git history", body, re.I)))

    # A5: tool names in the body must appear in allowed-tools
    tools = {t.strip() for t in fm.get("allowed-tools", "").split(",")}
    named = set(re.findall(r"`(Task|Agent|Bash|Write|Edit|Read|Grep|Glob)`", body))
    unlisted = {t for t in named if t not in tools}
    check("A5", "tools named in the body are declared in allowed-tools",
          not unlisted, ", ".join(sorted(unlisted)) or "ok")

    # A6: the report-first gate must exempt scoping
    check("A6", "report-first gate exempts scoping questions",
          bool(re.search(r"scoping questions[^.]*are fine", body, re.I)))

    # A7: output filename must be collision-safe
    check("A7", "report filename format is specified",
          "YYYYMMDD-HHMMSS" in body)

    # A8: evals shipped
    ev = skill_dir / "evals" / "evals.json"
    n_ev = 0
    if ev.exists():
        import json
        try:
            n_ev = len(json.loads(ev.read_text()).get("evals", []))
        except Exception:
            n_ev = -1
    check("A8", "at least 3 evals shipped with assertions",
          n_ev >= 3, f"{n_ev} evals")

    # --- B1-B5: regressions from the execution-simulation pass ------------

    # B1: every shell variable used must be assigned in the same block
    used = set(re.findall(r'"\$([A-Z_]+)"', body))
    assigned = set(re.findall(r"^([A-Z_]+)=", body, re.M))
    env_ok = {"TMPDIR", "TEMP", "HOME"}
    undefined = used - assigned - env_ok
    check("B1", "no undefined shell variables in commands",
          not undefined, ", ".join(sorted(undefined)) or "ok")

    # B2: the trigger must exclude single-module and mid-build work
    check("B2a", "description scopes out already-chosen refactors",
          bool(re.search(r"do not use it|not a refactoring tool", desc, re.I)))
    check("B2b", "body states when this is the wrong skill",
          bool(re.search(r"## Not this skill when", body)))

    # B3: a license naming a local file must ship that file
    lic = fm.get("license", "")
    lic_file = re.search(r"\b(LICENSE[\w.]*)\b", lic)
    check("B3", "license field does not point at a missing file",
          not lic_file or (skill_dir / lic_file.group(1)).exists(), lic)

    # B4: derivative work carries attribution, unreferenced to stay free
    att = skill_dir / "ATTRIBUTION.md"
    check("B4", "attribution present and not loaded at runtime",
          att.exists() and "ATTRIBUTION.md" not in body)

    # B5: the design conversation is capped
    check("B5", "design conversation has an explicit exit cadence",
          bool(re.search(r"offer an exit every \d+ questions", body, re.I)))

    # --- C1: cross-file semantic consistency (found by running the evals) --

    # The deletion test has two outcomes. No file may claim only one of them
    # counts, and every file that names the collapse case must rank it.
    exclusivity = []
    for p in all_md:
        t = p.read_text()
        if re.search(r"only .{0,30}(concentrates|the second case)", t, re.I):
            exclusivity.append(p.name)
    check("C1a", "no file claims only one deletion-test outcome counts",
          not exclusivity, ", ".join(exclusivity) or "ok")

    naming = [p.name for p in all_md
              if re.search(r"pass-through", p.read_text(), re.I)
              and not re.search(r"collapse candidate", p.read_text(), re.I)]
    check("C1b", "every file discussing pass-throughs names them collapse candidates",
          not naming, ", ".join(naming) or "ok")

    check("C1c", "collapse candidates are barred from the top rank",
          bool(re.search(r"collapse candidates never rank `Strong`", body, re.I)))


def main():
    d = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    audit(d)
    width = max(len(n) for _, n, _, _ in RESULTS)
    failed = 0
    for cid, name, ok, detail in RESULTS:
        mark = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"[{mark}] {cid:<5} {name:<{width}}  {detail}")
    print(f"\n{len(RESULTS) - failed}/{len(RESULTS)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
