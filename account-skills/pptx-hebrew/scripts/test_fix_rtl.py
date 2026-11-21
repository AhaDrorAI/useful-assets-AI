#!/usr/bin/env python3
"""Regression tests for fix_rtl.py. Standard library + lxml only.

    python test_fix_rtl.py        # prints one line per test, exits 1 on any failure
"""
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "fix_rtl.py")

SLIDE = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
         '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
         'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
         'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
         'xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" mc:Ignorable="p14">'
         '<p:cSld><p:spTree><p:sp><p:txBody>'
         '<a:p><a:r><a:rPr lang="en-US"/><a:t>שלום עולם</a:t></a:r></a:p>'
         '<a:p><a:r><a:rPr lang="en-US"/><a:t>An English line with one word עברית in it</a:t></a:r></a:p>'
         '<a:p><a:r><a:t>טקסט בלי rPr</a:t></a:r></a:p>'
         '</p:txBody></p:sp></p:spTree></p:cSld></p:sld>')


def make(path, extra=None):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("ppt/slides/slide1.xml", SLIDE)
        for name, data in (extra or {}).items():
            z.writestr(name, data)


def run(*args):
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)


def slide(path):
    return zipfile.ZipFile(path).read("ppt/slides/slide1.xml").decode()


def main():
    tmp = tempfile.mkdtemp()
    results = []
    try:
        deck = os.path.join(tmp, "deck.pptx")
        make(deck)
        results.append(("check finds work on unfixed deck", run(deck, "--check").returncode == 1))
        results.append(("fix exits 0", run(deck).returncode == 0))
        x = slide(deck)
        results.append(("mc:Ignorable-only prefix kept (xmlns:p14)", 'xmlns:p14=' in x and 'mc:Ignorable="p14"' in x))
        results.append(("p: prefix kept", "<p:sld" in x))
        paras = x.split("<a:p>")[1:]
        results.append(("Hebrew paragraph is RTL", 'rtl="1"' in paras[0] and 'lang="he-IL"' in paras[0]))
        results.append(("English-primary paragraph stays LTR", 'rtl="1"' not in paras[1] and 'lang="he-IL"' in paras[1]))
        results.append(("run without rPr gets lang", 'lang="he-IL"' in paras[2]))
        results.append(("second check finds nothing (idempotent)", run(deck, "--check").returncode == 0))

        for bad in ("../../etc/hostname", "/etc/hostname", "ppt/../../x.xml"):
            evil = os.path.join(tmp, "evil.pptx")
            make(evil, {bad: "x"})
            before = open(evil, "rb").read()
            r = run(evil)
            results.append((f"unsafe entry {bad!r} refused (exit 2, file unchanged)",
                            r.returncode == 2 and open(evil, "rb").read() == before))

        notzip = os.path.join(tmp, "not.pptx")
        open(notzip, "w").write("not a zip")
        results.append(("non-zip refused with exit 2", run(notzip).returncode == 2))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    failed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        failed += not ok
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
