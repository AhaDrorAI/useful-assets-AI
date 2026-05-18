# Publishing Recommendation

## Recommendation

Use both your site and a public GitHub repo, but give each one a different job.

## 1. Public GitHub repo

Create a public repo for the reusable assets:

```text
dror-ai-agent-launchpad
```

Recommended contents:

```text
/guides
  new-machine-claude-code-setup.en.html
  new-machine-claude-code-setup.he.html
  ai-agent-repo-advisor.en.html
  ai-agent-repo-advisor.he.html

/skills
  agent-onboarding-wizard.skill
  new-project-from-prd.skill
  agent-onboarding-wizard/SKILL.md
  new-project-from-prd/SKILL.md
```

Why public GitHub:

- Easy for course participants to download skills.
- Easy to version and update.
- Easy to link from your site.
- Good place for technical users to inspect what a skill contains before installing it.

What should not go there:

- Supabase SQL used only to update your private tables.
- Supabase keys.
- Private course data.
- Internal drafts.
- Anything that assumes your production database schema is private.

## 2. Your site

Use your site as the polished learning experience.

Recommended structure:

```text
/toolbox/guides/new-machine-claude-code-codex-setup
/toolbox/guides/ai-agent-repo-operating-guide
/toolbox/ai-agent-repo-advisor
/toolbox/skills
```

Recommended content source:

- Store canonical guide metadata and markdown in Supabase.
- Hardcode or statically host the interactive HTML pages unless you are ready to convert them into native React components.
- Keep repo records in Supabase so they can appear in the existing GitHub repo catalog.
- Link skill downloads from the public GitHub releases or raw files.

## 3. What to hardcode vs Supabase

Use Supabase for:

- Guides list.
- Repo catalog.
- Tags, categories, search, filters.
- Guide markdown content.

Hardcode or static-host for now:

- Interactive advisor HTML.
- New-machine setup HTML.
- Skill download cards.

Reason: the HTML pages are interactive experiences, not just database content. They will be easier to maintain as files until you convert them into proper site components.

## 4. Skill distribution

Best path:

1. Keep editable skill folders in GitHub.
2. Publish zipped `.skill` bundles in the same repo.
3. Add a `/toolbox/skills` page on your site with:
   - what the skill does
   - who should use it
   - install/download link
   - safety note
   - version/date

Do not hide skills only inside Supabase. Skills are executable instructions; users should be able to inspect them as files.

## 5. Recommended publishing order

1. Add the two HTML pages to your site as static pages.
2. Insert/update Supabase guide and repo records.
3. Create public GitHub repo for skills and source files.
4. Add a site page linking to the skills.
5. Later, convert the HTML advisor into a native site component connected to Supabase repo data.

## Final architecture

```text
Public GitHub repo = source of truth for reusable artifacts
Your site = friendly course experience
Supabase = searchable guide/repo data
Static HTML or React components = interactive guided workflows
```
