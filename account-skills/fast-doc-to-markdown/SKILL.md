---
name: fast-doc-to-markdown
description: "Convert Word, PowerPoint, Excel, OpenDocument, RTF, EPUB, CSV and PDF files to clean Markdown with anydoc before reading them, with Hebrew/RTL checks and a no-upload rule for scanned pages. Use whenever a task's input is a .docx, .doc, .pptx, .ppt, .xlsx, .xls, .odt, .ods, .odp, .rtf, .epub, .csv or .pdf file, especially for batch conversion, large files, Hebrew documents, exams or curriculum material."
metadata:
  last_reviewed: "2026-11-18"
  review_every_days: "180"
---

# Fast document → Markdown

Reading a .docx or .pdf directly is slow and lossy. `anydoc` converts documents to clean Markdown locally in ~0.1s, with no HTML wrapper noise. Convert first, then work on the Markdown.

## Trigger

- Any task whose input is a `.docx .doc .pptx .ppt .xlsx .xls .odt .ods .odp .rtf .epub .csv .pdf` file.
- Especially: batch conversion, large files, Hebrew/RTL documents, exam or curriculum documents.

## Steps

1. **Find the tool.** If `anydoc` is on the PATH, use it. If not, run it through `npx -y @firecrawl/anydoc` (needs Node 20+). That runs without a global install. Install globally (`npm install -g @firecrawl/anydoc`) only if the user agrees or the session is a disposable cloud container.

2. **Prefer the original Office file over a PDF export of it.** If both a .docx and a .pdf of the same content exist, always convert the .docx — the PDF text layer loses structure and mangles Hebrew.

3. **Convert:**
   ```
   anydoc <file> -o <out>.md
   ```

4. **Branch on the exit code** — do not ignore it:
   - `0` — success.
   - `1` — unreadable/corrupt file. Report it; do not silently continue.
   - `2` — usage error (bad flag or `--format`).
   - `3` — one or more pages need OCR. anydoc is **all-or-nothing**: a single scanned page rejects the whole document.

5. **On exit 3, do not pass `--ocr hosted`.** That flag uploads the whole document to Firecrawl's servers. Use one of these instead, in this order:
   1. If the `pdf` skill is installed, use its local OCR.
   2. Split the PDF and convert only the text pages with anydoc. Report which pages were skipped.
   3. Tell the user which pages need OCR and stop.

   Pass `--ocr hosted` only if the user asks for it for this specific file after you have told them it uploads the document. Never pass it for student work, exams, personal data, or client-confidential material, even if asked in general terms. No tool setting blocks this flag; this rule is the only guard, so name the flag explicitly when you report what you ran.

6. **Hebrew / RTL check.** The Office path (.docx/.pptx) produces clean Hebrew. The **PDF path is unreliable for Hebrew**: it splits words mid-word (`ב ין`, `פדגוג יי ם`) and reverses embedded Latin runs (`Numicon` → `nocimuN`). If the source is a Hebrew PDF, read the first 30 lines of the output. If you see split words or reversed Latin runs, say so in the answer and do not analyse the corrupted passages as if they were correct.

7. Read and work from the generated `.md`, not the original binary file.

## Verification

- Output file exists and is non-empty; heading and table counts look plausible (`grep -c '^#'`, `grep -c '^|'`).
- Output contains no `<span` / HTML wrapper noise (that would indicate a pandoc fallback, not anydoc).
- For Hebrew sources, spot-check for spurious spaces inside words before using the text.
- If any page was skipped or OCR was refused, state that explicitly in the response.