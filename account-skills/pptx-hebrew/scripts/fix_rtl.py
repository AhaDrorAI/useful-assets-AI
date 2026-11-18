#!/usr/bin/env python3
"""
Post-process a PptxGenJS-generated PPTX to fix RTL/Hebrew issues.

PptxGenJS sets lang="en-US" on ALL text runs, even Hebrew text. This causes
PowerPoint to treat Hebrew text as LTR — wrong cursor direction, broken
spacing, misplaced punctuation, and incorrect paragraph flow.

This script fixes:
1. lang="he-IL" on text runs containing Hebrew characters
2. rtl="1" on paragraphs containing Hebrew text
3. Preserves lang="en-US" for purely-English text runs

Usage:
    python fix_rtl.py input.pptx [output.pptx]

If output is omitted, the input file is overwritten in place.
"""

import sys
import os
import re
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ET

# Hebrew Unicode range (includes Hebrew letters, points, and cantillation marks)
HEBREW_RE = re.compile(r'[\u0590-\u05FF]')

# Arabic Unicode range
ARABIC_RE = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')

# XML namespaces used in OOXML
NSMAP = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}

# Register namespaces to prevent ns0/ns1 prefix rewriting on save
ET.register_namespace('a', NSMAP['a'])
ET.register_namespace('r', NSMAP['r'])
ET.register_namespace('p', NSMAP['p'])
ET.register_namespace('', 'http://schemas.openxmlformats.org/presentationml/2006/main')
ET.register_namespace('mc', 'http://schemas.openxmlformats.org/markup-compatibility/2006')


def has_hebrew(text):
    """Check if a string contains Hebrew characters."""
    return bool(HEBREW_RE.search(text)) if text else False


def has_arabic(text):
    """Check if a string contains Arabic characters."""
    return bool(ARABIC_RE.search(text)) if text else False


def detect_rtl_lang(text):
    """Detect the appropriate RTL language tag for text content.
    Returns 'he-IL' for Hebrew, 'ar-SA' for Arabic, or None for LTR text."""
    if not text:
        return None
    if has_hebrew(text):
        return 'he-IL'
    if has_arabic(text):
        return 'ar-SA'
    return None


def paragraph_has_rtl(p_elem):
    """Check if any text run in a paragraph contains RTL characters."""
    ns_a = NSMAP['a']
    for r_elem in p_elem.findall(f'{{{ns_a}}}r'):
        t_elem = r_elem.find(f'{{{ns_a}}}t')
        if t_elem is not None and t_elem.text:
            if has_hebrew(t_elem.text) or has_arabic(t_elem.text):
                return True
    return False


def fix_slide_xml(xml_path):
    """Fix RTL attributes in a single slide XML file.
    Returns the number of changes made."""
    ns_a = NSMAP['a']

    tree = ET.parse(xml_path)
    root = tree.getroot()
    changes = 0

    for p_elem in root.iter(f'{{{ns_a}}}p'):
        p_is_rtl = paragraph_has_rtl(p_elem)

        # Get or create paragraph properties
        pPr = p_elem.find(f'{{{ns_a}}}pPr')

        if p_is_rtl:
            if pPr is None:
                pPr = ET.SubElement(p_elem, f'{{{ns_a}}}pPr')
                p_elem.remove(pPr)
                p_elem.insert(0, pPr)

            # Ensure rtl="1"
            if pPr.get('rtl') != '1':
                pPr.set('rtl', '1')
                changes += 1

            # Ensure right alignment if none set
            if not pPr.get('algn'):
                pPr.set('algn', 'r')
                changes += 1

        # Fix language on text runs
        for r_elem in p_elem.findall(f'{{{ns_a}}}r'):
            t_elem = r_elem.find(f'{{{ns_a}}}t')
            rPr = r_elem.find(f'{{{ns_a}}}rPr')

            if t_elem is not None and rPr is not None:
                text = t_elem.text or ''
                rtl_lang = detect_rtl_lang(text)

                if rtl_lang and rPr.get('lang') != rtl_lang:
                    rPr.set('lang', rtl_lang)
                    changes += 1

    if changes > 0:
        tree.write(xml_path, xml_declaration=True, encoding='UTF-8')

    return changes


def fix_pptx(input_path, output_path=None):
    """Fix RTL in a PPTX file by post-processing its XML."""
    if output_path is None:
        output_path = input_path

    tmp_dir = tempfile.mkdtemp(prefix='rtl_fix_')

    try:
        with zipfile.ZipFile(input_path, 'r') as zf:
            zf.extractall(tmp_dir)

        total_changes = 0

        # Process slides, slide layouts, and slide masters
        for subdir in ['slides', 'slideLayouts', 'slideMasters']:
            xml_dir = os.path.join(tmp_dir, 'ppt', subdir)
            if not os.path.isdir(xml_dir):
                continue
            for fname in sorted(os.listdir(xml_dir)):
                if fname.endswith('.xml'):
                    fpath = os.path.join(xml_dir, fname)
                    n = fix_slide_xml(fpath)
                    if n > 0:
                        print(f"  {subdir}/{fname}: {n} fixes")
                    total_changes += n

        print(f"\nTotal RTL fixes: {total_changes}")

        # Re-pack as PPTX
        actual_output = output_path + '.tmp' if os.path.abspath(output_path) == os.path.abspath(input_path) else output_path
        if os.path.exists(actual_output):
            os.remove(actual_output)

        with zipfile.ZipFile(actual_output, 'w', zipfile.ZIP_DEFLATED) as zf:
            for dirpath, _, filenames in os.walk(tmp_dir):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    arcname = os.path.relpath(file_path, tmp_dir)
                    zf.write(file_path, arcname)

        if actual_output != output_path:
            shutil.move(actual_output, output_path)

        print(f"Saved to: {output_path}")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_rtl.py input.pptx [output.pptx]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file

    print(f"Fixing RTL in: {input_file}")
    fix_pptx(input_file, output_file)
