# Agent and Evidence Checklist

## Standard Agent Roles

Use these roles when subagents are available and the task is substantial.

1. **Career Facts Auditor**
   - Extract contact details, roles, dates, employers, education, certificates, languages, citizenship/work authorization, achievements, and metrics.
   - Flag contradictions and missing essentials.

2. **Technical Evidence Auditor**
   - Extract programming languages, frameworks, AI tools, agentic workflows, integrations, APIs, databases, deployment, testing, Git, automation, and project proof.
   - Categorize claims as hard, soft, or unsupported.

3. **Narrative Material Curator**
   - Extract origin story, builder pattern, values, repeated behaviors, testimonials, and memorable but factual phrases.
   - Avoid unsupported anecdotes unless the user confirms them.

4. **ATS and Job-Fit Editor**
   - Map job requirements to CV keywords and proof.
   - Recommend headline, profile angle, gap wording, and missing evidence questions.

5. **Question Minimizer**
   - Produce the shortest question list needed before drafting.
   - Ask only questions that materially affect accuracy or defensibility.

6. **DOCX Layout Producer**
   - Create the final document after the lead integrates facts and narrative.
   - Follow document best practices for role, country, and seniority.
   - Render and inspect layout when possible.

7. **Outside Reader**
   - Receives only the final draft text/document output, with no source material and no conversation context.
   - Reports what an external reader understands, assumes, misses, finds irrelevant, or sees as too literal.
   - Flags places where raw candidate facts need to be transformed into audience-ready meaning.
   - This role is mandatory before final delivery for CVs and other external-facing documents.

## Evidence Ledger Template

Use this internally before drafting:

```text
Hard claims
- Claim:
  Source:
  CV wording:

Soft claims
- Claim:
  Why soft:
  Safe wording:

Unsupported claims
- Claim:
  Why unsupported:
  Question to ask:
```

## Fit Mirror Template

```text
Job requirement:
Candidate proof:
Gap/risk:
CV wording:
Interview risk:
```

## Clarifying Question Filters

Ask only if at least one is true:

- Contact, location, work authorization, or identity detail is contradictory
- A hard job requirement has no defensible wording
- A claim would be impressive but lacks source support
- A metric needs user confirmation
- The output format is unclear and local best practice is insufficient
- A gap needs explicit user preference for framing

Do not ask questions whose answers can be found by reading the candidate source folder.
