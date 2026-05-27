---
name: cv-story-builder
description: Create or improve a tailored CV/resume from a job post and candidate source files using evidence-first storytelling, job-fit mirroring, multi-agent auditing, clarifying questions, and professional output formatting. Use when the user asks to write, rewrite, tailor, optimize, or generate a CV/resume for a specific role, especially from folders like "about me/" or "about [name]/", job screenshots/photos, PDFs, DOCX files, LinkedIn exports, portfolios, or mixed source material.
---

# CV Story Builder

## Principle

Build the strongest true CV. Treat the candidate's files and answers as raw material, the job post as the mirror, and the CV as a proof story.

The default voice is accurate, high-signal, builder-story, quietly confident, no hype. Let readers infer "this is the candidate I pictured" through fit, proof, and narrative inevitability.

## Source Contract

Use only accurate information from:

- Candidate folders named `about me/`, `about [candidate name]/`, or user-specified source folders
- Existing CVs, LinkedIn exports, portfolios, certificates, project files, screenshots, and user answers
- The job post, job photo, or role description supplied by the user

Do not invent. Separate every claim into:

- `Hard claim`: directly supported by files or user answers
- `Soft claim`: reasonable but requires careful wording
- `Unsupported claim`: do not use; ask a clarifying question if important

When evidence conflicts, ask or use conservative wording. Prefer "academic Java foundation" over "strong Java background" unless professional Java evidence exists.

## Workflow

1. **Read the job first**
   - Extract title, location, work model, format expectations, technical requirements, hidden requirements, and screening keywords.
   - If the job is a photo, read the image carefully and transcribe the relevant requirements.
   - Build a `Fit Mirror`: each requirement mapped to candidate proof, gap, and wording strategy.

2. **Find and parse candidate material**
   - Search likely folders with `rg --files`, prioritizing `about me/`, `about [name]/`, and user-provided paths.
   - Read DOCX/PDF/Markdown/spreadsheet sources using available document tooling.
   - Gather: contact details, role history, dates, education, certificates, technical skills, projects, metrics, citizenship/work authorization, language ability, and portfolio links.

3. **Use subagents when available**
   - Use parallel agents if the user asks for agents or if the task is substantial.
   - Assign fixed roles from [agent-and-evidence-checklist.md](references/agent-and-evidence-checklist.md).
   - Do not let agents draft the final CV independently. Use them to audit facts, surface proof, and reduce questions.

4. **Ask only high-leverage clarifying questions**
   - Ask about contradictions, missing contact/work-authorization facts, unverified technical claims, and metrics that materially affect the CV.
   - Avoid asking for facts already found in files.
   - If a gap is likely to be screened hard, ask how truthful framing should handle it.

5. **Craft the narrative spine**
   - Use the Top 1% prompt in [top-1-superprompt.md](references/top-1-superprompt.md) as the internal standard.
   - The narrative should explain why the candidate's path makes sense for this job.
   - Tie origin, craft, tools, technical proof, and job requirements into one coherent arc.

6. **Choose format by role and location**
   - Do not assume a fixed CV length or format.
   - Ask the user when needed, or use best practices for the relevant country, seniority, and job type.
   - For DOCX, use the Documents skill when available: create, render, visually inspect, and iterate.
   - Save generated files under `generated-cvs/` unless the user requests another location.

7. **Run the Outside Reader audit**
   - Before final delivery, perform an outside-reader audit on the final CV text/document output.
   - The outside reader must receive only the CV draft/output, with no prior context, no source files, and no explanation of intent.
   - Use the `outside-reader-audit` skill when available.
   - Apply the audit findings that improve clarity, audience fit, relevance, and truthful proof.

8. **Finalize with verification**
   - Check every claim against evidence or user answers.
   - Confirm page count, readability, links, contact details, work authorization, and gap wording.
   - For `.docx`, render to PDF/PNG when possible and inspect for layout defects before delivery.

## Gap Handling

Handle gaps honestly. The goal is not to hide weakness; it is to reframe the risk around stronger proof.

Pattern:

1. State the accurate level.
2. Show adjacent proof.
3. Explain the ramp mechanism.
4. Bring it back to the job.

Example:

> Java: academic foundation and practical code-reading/writing capability; recent delivery is mainly Python, JavaScript, Next.js, Google Apps Script, SQL, bots, automations, and integrations. I ramp quickly across languages using AI-assisted workflows because the core asset is logical thinking, architecture, problem solving, and orchestration of code agents toward a high-quality product.

Use the user's wording when it is sharp and accurate, but convert it into professional CV language.

## Output Rules

- Prefer a tailored CV over a generic biography.
- Lead with the role-fit story, not with a chronological dump.
- Include enough keywords for screening without making the CV robotic.
- Use metrics only when sourced or explicitly confirmed by the user.
- Avoid inflated claims like "expert", "strong Java", "production agent architect", or "senior software engineer" unless the evidence supports them.
- Do not deliver a final CV until an outside reader could understand it without hidden context.
- Keep final answers concise and link to the generated file.

## Trigger Examples

- "Write a CV for this job from the files in about me/"
- "Tailor my resume to this role and make it a story"
- "Use all my source files but only accurate info"
- "Handle the Java gap honestly"
- "Create a 2-page DOCX CV for this job photo"
- "Use agents to audit my CV fit before writing"
