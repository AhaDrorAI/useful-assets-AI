---
name: pptx-hebrew
description: "Hebrew and RTL language support for PowerPoint presentations created with PptxGenJS. MANDATORY when creating or editing .pptx files that contain Hebrew, Arabic, or any RTL text. Use this skill alongside the pptx skill whenever the presentation content includes Hebrew characters, the user communicates in Hebrew, or RTL text direction is needed. Also triggers for Arabic content. This skill fixes a critical PptxGenJS bug where all text is tagged as English (lang=\"en-US\"), causing PowerPoint to mishandle RTL text direction, cursor movement, spacing, and punctuation placement."
metadata:
  last_reviewed: "2026-11-18"
  review_every_days: "180"
---

# PPTX Hebrew / RTL Support

## The Problem

PptxGenJS has a critical limitation for RTL languages: it sets `lang="en-US"` on **every** text run, even when the text is Hebrew or Arabic. PowerPoint uses the `lang` attribute to determine text direction, cursor behavior, spacing rules, and punctuation placement. With `lang="en-US"`, Hebrew text appears right-aligned but **behaves** as English — causing broken editing, wrong punctuation placement, and incorrect spacing.

Additionally, PptxGenJS's `rtlMode: true` option doesn't consistently add `rtl="1"` to all paragraph properties, especially on bullet items and numbered lists.

## The Fix: Two-Step Process

### Step 1: PptxGenJS Code (during generation)

Set these on the presentation object:
```javascript
pres.rtlMode = true;
```

For every Hebrew text element, always include both `align` and `rtlMode`:
```javascript
slide.addText("טקסט בעברית", {
  align: "right",
  rtlMode: true,
  // ... other options
});
```

For rich text arrays, these go on the **container** options (not individual text items):
```javascript
slide.addText([
  { text: "שורה ראשונה", options: { bold: true, breakLine: true } },
  { text: "שורה שנייה", options: {} },
], {
  align: "right",
  rtlMode: true,  // applies to the whole text box
  x: 0.5, y: 0.5, w: 8, h: 2,
});
```

For bullets and numbered lists — use PptxGenJS bullet syntax, never manual characters:
```javascript
// ✅ Correct
{ text: "פריט ראשון", options: { bullet: true, breakLine: true } }
{ text: "פריט ממוספר", options: { bullet: { type: "number" }, breakLine: true } }

// ❌ Wrong — creates double bullets or misaligned numbers in RTL
{ text: "• פריט ראשון", options: { breakLine: true } }
{ text: "1. פריט ממוספר", options: { breakLine: true } }
```

### Step 2: Post-Processing (MANDATORY after PptxGenJS export)

After generating the PPTX with PptxGenJS, **always** run the RTL fix script:

```bash
python <skill-path>/scripts/fix_rtl.py output.pptx
```

This script opens the PPTX (which is a ZIP of XML files), and fixes:
- Sets `lang="he-IL"` on text runs containing Hebrew characters, and `lang="ar-SA"` on runs containing Arabic. A run without run properties gets them.
- Adds `rtl="1"` (and right alignment, if none is set) to RTL-primary paragraphs: paragraphs with at least as many Hebrew/Arabic letters as Latin letters.
- Leaves English-primary paragraphs left-to-right, even when they contain a Hebrew word. Pass `--any-rtl` to mark every paragraph that contains any RTL letter instead.
- Preserves `lang="en-US"` on purely English text runs, and keeps the file's XML namespace prefixes unchanged.

The script modifies the file in-place. You can also specify a separate output:
```bash
python <skill-path>/scripts/fix_rtl.py input.pptx output.pptx
```

## Complete Workflow

When creating a Hebrew/RTL presentation:

1. Write the PptxGenJS script with `rtlMode: true` and `align: "right"` on all Hebrew text
2. Generate the PPTX: `node create_presentation.js`
3. **Run the RTL post-processor**: `python <skill-path>/scripts/fix_rtl.py output.pptx`
4. **Verify the fix**: `python <skill-path>/scripts/fix_rtl.py output.pptx --check`. Exit code 0 and "0 changes needed" means every RTL run and paragraph is tagged. Exit code 1 means the fix did not run on this file; run step 3 again.
5. Convert to PDF or images for layout QA: `python <pptx-skill>/scripts/office/soffice.py --headless --convert-to pdf output.pptx`. Inspect the slides visually.

A visual check alone cannot confirm the RTL fix: LibreOffice renders Hebrew correctly even when the tags are wrong (see "Why This Matters"). Step 4 is the check for the fix; step 5 is the check for layout.

## Mixed Language Content

For slides with both Hebrew and English:
- The script handles mixed content automatically: Hebrew runs get `he-IL`, English runs stay `en-US`.
- If the **primary** language of a text box is Hebrew, set `rtlMode: true` and `align: "right"`.
- If a text box is English-primary with occasional Hebrew words, omit `rtlMode`. The script keeps those paragraphs left-to-right.

## Hyperlinks in Hebrew Presentations

YouTube URLs and other links should use PptxGenJS's hyperlink syntax:
```javascript
slide.addText([
  { text: "צפו בסרטון: ", options: { rtlMode: true } },
  { text: "youtube.com/watch?v=ABC123", options: {
    hyperlink: { url: "https://youtube.com/watch?v=ABC123" },
    fontSize: 11, color: "0A5B73"
  }},
], { align: "right", rtlMode: true, x: 0.5, y: 1, w: 8, h: 0.5 });
```

## Why This Matters

Without the post-processing fix, a Hebrew presentation will:
- Look correct in the PDF preview (LibreOffice renders based on character detection)
- **Break in PowerPoint** — cursor moves backwards, spaces appear in wrong places, parentheses and punctuation are misplaced, editing is painful
- Confuse PowerPoint's spell-checker (tries to spell-check Hebrew as English)

The fix ensures PowerPoint treats Hebrew text as Hebrew at the XML level — the same result you'd get typing Hebrew directly in PowerPoint.
