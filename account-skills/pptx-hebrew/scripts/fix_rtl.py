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

Namespace prefixes are preserved (p:, a:, r:, mc: ...). With lxml installed the
XML is rewritten byte-for-byte except for the changed attributes; without lxml
the standard library is used with every prefix in the file re-registered.

Usage:
    python fix_rtl.py input.pptx [output.pptx] [--any-rtl] [--check]

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
    import xml.etree.ElementTree as ET
    HAVE_LXML = False

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


def register_prefixes(xml_bytes):
    """stdlib only: re-register every prefix declared in the file, so ET writes
    the same prefixes back instead of ns0:/default namespaces."""
    for prefix, uri in re.findall(rb'xmlns:([A-Za-z0-9_]+)="([^"]+)"', xml_bytes):
        ET.register_namespace(prefix.decode(), uri.decode())


def fix_xml(path, any_rtl=False, write=True):
    with open(path, "rb") as f:
        raw = f.read()
    if not HAVE_LXML:
        register_prefixes(raw)
    tree = ET.ElementTree(ET.fromstring(raw))
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
        if HAVE_LXML:
            tree.write(path, xml_declaration=True, encoding="UTF-8", standalone=True)
        else:
            tree.write(path, xml_declaration=True, encoding="UTF-8")
    return changes


def fix_pptx(input_path, output_path=None, any_rtl=False, check=False):
    output_path = output_path or input_path
    tmp_dir = tempfile.mkdtemp(prefix="rtl_fix_")
    try:
        with zipfile.ZipFile(input_path) as zf:
            names = zf.namelist()  # keep the original entry order
            zf.extractall(tmp_dir)

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
                if os.path.isfile(full):
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
    print(f"{'Checking' if '--check' in flags else 'Fixing'} RTL in: {args[0]}")
    n = fix_pptx(args[0], args[1] if len(args) > 1 else None,
                 any_rtl="--any-rtl" in flags, check="--check" in flags)
    sys.exit(1 if ("--check" in flags and n) else 0)
