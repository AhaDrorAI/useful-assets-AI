---
name: fast-doc-to-markdown
description: "Convert Word/PPT/Excel/PDF/EPUB documents to clean Markdown with anydoc before reading them — with Hebrew/RTL and OCR-privacy guardrails."
---

# Fast document → Markdown

Reading a .docx or .pdf directly is slow and lossy. `anydoc` converts documents to clean Markdown locally in ~0.1s, with no HTML wrapper noise. Convert first, then work on the Markdown.

## Trigger

- Any task whose input is a `.docx .doc .pptx .ppt .xlsx .xls .odt .ods .odp .rtf .epub .csv .pdf` file.
- Especially: batch conversion, large files, Hebrew/RTL documents, exam or curriculum documents.

## Steps

1. **Ensure the binary exists** (cloud sessions start clean, so this is normal):
   ```
   which anydoc || npm install -g @firecrawl/anydoc
   ```

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

5. **On exit 3, do NOT reach for `--ocr hosted` by default.** That flag uploads the document to Firecrawl's API. Never use it for student work, exams, personal or client-confidential material. Instead fall back to the local `pdf` skill for OCR, or split the PDF and convert only the text pages with anydoc.

6. **Hebrew / RTL check.** The Office path (.docx/.pptx) produces clean Hebrew. The **PDF path is unreliable for Hebrew**: it splits words mid-word (`ב ין`, `פדגוג יי ם`) and reverses embedded Latin runs (`Numicon` → `nocimuN`). If the source is a Hebrew PDF, sample the output before trusting it, and say so in the answer rather than analyzing corrupted text.

7. Read and work from the generated `.md`, not the original binary file.

## Verification

- Output file exists and is non-empty; heading and table counts look plausible (`grep -c '^#'`, `grep -c '^|'`).
- Output contains no `<span` / HTML wrapper noise (that would indicate a pandoc fallback, not anydoc).
- For Hebrew sources, spot-check for spurious spaces inside words before using the text.
- If any page was skipped or OCR was refused, state that explicitly in the response.