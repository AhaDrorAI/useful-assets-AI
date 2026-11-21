#!/usr/bin/env python3
"""
Post-process a PptxGenJS-generated PPTX to fix RTL (Hebrew / Arabic) text.

PptxGenJS writes lang="en-US" on every text run, and its rtlMode does not reach
every paragraph (bullets and numbered items are often missed). PowerPoint then
treats Hebrew as English: wrong cursor movement, spacing and punctuation.

What this script changes, per slide, layout and master XML file:
1. Every text run that contains Hebrew gets lang="he-IL"; Arabic gets lang="ar-SA".
   A run with no <a:rPr> gets one. Runs with no RTL letters keep their lang.
2. A paragraph gets rtl="1" (and algn="r" if it has no alignment) when it is
   RTL-primary: it has at least as many Hebrew/Arabic letters as Latin letters.
   An English sentence with one Hebrew word stays left-to-right.
   Use --any-rtl to mark every paragraph that contains any RTL letter instead.
3. In an RTL-primary paragraph, <a:endParaRPr> gets the RTL lang too, so text
   typed at the end of the line continues in Hebrew/Arabic.

Requires lxml (`pip install lxml`; python-pptx already depends on it). lxml keeps
every namespace declaration, including prefixes used only inside mc:Ignorable.
The standard-library XML writer drops those, which corrupts the slide, so there
is no fallback: without lxml the script stops before changing anything.

Untrusted input: the deck is treated as untrusted. An archive whose entry names
are absolute or climb out of the archive (`../`) is refused, and XML is parsed
with entity resolution and network access turned off.

Usage:
    python fix_rtl.py input.pptx [output.pptx] [--any-rtl] [--check]

Exit codes: 0 done (or --check found nothing to change); 1 --check found changes
needed; 2 bad input (missing file, not a zip, unsafe archive); 3 lxml missing.

    --check   Do not write. Print what would change and exit 1 if anything would.
              Use it after a fix to verify: a fixed file reports 0 changes.

If output is omitted, the input file is overwritten in place (via a temp file).
"""

import os
import re
import shutil
import sys
import tempfile
import zipfile

try:
    from lxml import etree as ET  # preserves prefixes and declarations exactly
    HAVE_LXML = True
except ImportError:  # pragma: no cover
    ET = None
    HAVE_LXML = False

SAFE_PARSER = ET.XMLParser(resolve_entities=False, no_network=True, huge_tree=False) if HAVE_LXML else None

HEBREW_RE = re.compile(r"[֐-׿יִ-ﭏ]")
ARABIC_RE = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
LATIN_RE = re.compile(r"[A-Za-zÀ-ɏ]")

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
Q = lambda tag: f"{{{A}}}{tag}"


def rtl_lang(text):
    if HEBREW_RE.search(text or ""):
        return "he-IL"
    if ARABIC_RE.search(text or ""):
        return "ar-SA"
    return None


def paragraph_text(p):
    return "".join((t.text or "") for t in p.iter(Q("t")))


def is_rtl_primary(text, any_rtl):
    rtl = len(HEBREW_RE.findall(text)) + len(ARABIC_RE.findall(text))
    if rtl == 0:
        return False
    if any_rtl:
        return True
    return rtl >= len(LATIN_RE.findall(text))


class UnsafeArchive(Exception):
    pass


def safe_member_names(zf):
    """Return the archive's file entries, or raise if any name could escape the
    extraction folder. A real .pptx never has such names."""
    names = []
    for info in zf.infolist():
        n = info.filename
        if info.is_dir():
            continue
        parts = n.replace("\\", "/").split("/")
        if n.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", n) or ".." in parts or "" in parts[:-1]:
            raise UnsafeArchive(f"unsafe entry name in archive: {n!r}")
        names.append(n)
    return names


def inside(base, path):
    base = os.path.realpath(base)
    return os.path.commonpath([base, os.path.realpath(path)]) == base


def fix_xml(path, any_rtl=False, write=True):
    with open(path, "rb") as f:
        raw = f.read()
    tree = ET.ElementTree(ET.fromstring(raw, SAFE_PARSER))
    root = tree.getroot()
    changes = 0

    for p in root.iter(Q("p")):
        text = paragraph_text(p)
        primary = is_rtl_primary(text, any_rtl)
        para_lang = rtl_lang(text)

        if primary:
            ppr = p.find(Q("pPr"))
            if ppr is None:
                ppr = ET.Element(Q("pPr"))
                p.insert(0, ppr)
            if ppr.get("rtl") != "1":
                ppr.set("rtl", "1")
                changes += 1
            if not ppr.get("algn"):
                ppr.set("algn", "r")
                changes += 1
            end = p.find(Q("endParaRPr"))
            if end is not None and para_lang and end.get("lang") != para_lang:
                end.set("lang", para_lang)
                changes += 1

        for r in p.findall(Q("r")):
            t = r.find(Q("t"))
            lang = rtl_lang(t.text if t is not None else "")
            if not lang:
                continue
            rpr = r.find(Q("rPr"))
            if rpr is None:
                rpr = ET.Element(Q("rPr"))
                r.insert(0, rpr)  # rPr must be the first child of a:r
            if rpr.get("lang") != lang:
                rpr.set("lang", lang)
                changes += 1

    if changes and write:
        tree.write(path, xml_declaration=True, encoding="UTF-8", standalone=True)
    return changes


def fix_pptx(input_path, output_path=None, any_rtl=False, check=False):
    output_path = output_path or input_path
    tmp_dir = tempfile.mkdtemp(prefix="rtl_fix_")
    try:
        with zipfile.ZipFile(input_path) as zf:
            names = safe_member_names(zf)  # keeps the original entry order
            for name in names:
                dest = os.path.join(tmp_dir, name)
                if not inside(tmp_dir, dest):
                    raise UnsafeArchive(f"entry escapes the archive: {name!r}")
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with zf.open(name) as src, open(dest, "wb") as out:
                    shutil.copyfileobj(src, out)

        total = 0
        for name in names:
            if re.match(r"ppt/(slides|slideLayouts|slideMasters)/[^/]+\.xml$", name):
                n = fix_xml(os.path.join(tmp_dir, name), any_rtl, write=not check)
                if n:
                    print(f"  {name}: {n} {'needed' if check else 'fixes'}")
                total += n
        print(f"\nTotal RTL {'changes needed' if check else 'fixes'}: {total}")
        if check:
            return total

        tmp_out = output_path + ".tmp"
        with zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zf:
            for name in names:
                full = os.path.join(tmp_dir, name)
                if inside(tmp_dir, full) and os.path.isfile(full):
                    zf.write(full, name)
        shutil.move(tmp_out, output_path)
        print(f"Saved to: {output_path}")
        return total
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        print(__doc__)
        sys.exit(2)
    if not os.path.isfile(args[0]):
        print(f"Not found: {args[0]}", file=sys.stderr)
        sys.exit(2)
    if not HAVE_LXML:
        print("fix_rtl.py needs lxml: pip install lxml. Nothing was changed.", file=sys.stderr)
        sys.exit(3)
    print(f"{'Checking' if '--check' in flags else 'Fixing'} RTL in: {args[0]}")
    try:
        n = fix_pptx(args[0], args[1] if len(args) > 1 else None,
                     any_rtl="--any-rtl" in flags, check="--check" in flags)
    except (UnsafeArchive, zipfile.BadZipFile) as e:
        print(f"Refused: {e}. Nothing was changed.", file=sys.stderr)
        sys.exit(2)
    sys.exit(1 if ("--check" in flags and n) else 0)
