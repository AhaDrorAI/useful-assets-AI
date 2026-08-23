# Dror AI Agent Launchpad

Reusable guides, skills, and examples for helping non-developers work with Claude Code, Codex, and AI coding agents.

## Start Here

Open [start-here/README.md](start-here/README.md) for the recommended path.

---
 
## Install
 
The skills in this repo install as one plugin. The marketplace catalog lives in this
repository, so an install stays connected to the source and can be updated later.
 
### Claude Code
 
```
/plugin marketplace add AhaDrorAI/useful-assets-AI
```
 
Run that on its own and wait for it to finish. Then, as a separate command:
 
```
/plugin install useful-assets-ai@aha-dror-ai
```
 
If the install reports `Run /reload-plugins to activate.`, run that too.
 
### Claude Desktop and Cowork
 
`Customize` → `Plugins` → under **Personal plugins**, `+` → `Add marketplace` →
`Add from a repository` → enter `AhaDrorAI/useful-assets-AI`. Then install
`useful-assets-ai` from the marketplace that appears.
 
Same catalog as Claude Code. One source, three surfaces.
 
### Codex and ChatGPT desktop
 
These read skills from a local folder rather than a marketplace. Clone the repo once and
point the skills directory at it:
 
```bash
git clone https://github.com/AhaDrorAI/useful-assets-AI.git
```
 
Then link `~/.agents/skills` to `current/skills` inside the clone. After that, `git pull`
updates every skill at once.
 
## Update
 
```
/plugin marketplace update
/plugin update
```
 
In Claude Desktop and Cowork, refresh the marketplace from the same Plugins screen.
For Codex, `git pull` in the clone.
 
## Skills in this plugin
 
| Skill | What it does |
|---|---|
| `avoid-ai-writing` | Audits and rewrites text to remove AI writing patterns. English and Hebrew. |
| `outside-reader-audit` | Reads external-facing text as an outsider with no hidden context. Has an Israeli-reader module. |
| `improve-codebase-architecture` | Surveys a codebase for shallow modules and ranks deepening candidates. Proposes only, never edits. |
| `cv-story-builder` | Builds a tailored CV from a job post and candidate source files. |
| `agent-onboarding-wizard` | Sets up a safe AI coding environment after installing Claude Code or Codex. |
| `new-project-from-prd` | Turns a PRD or product idea into a project an agent can build. |
| `startup-free-traffic` | Organic, zero-budget traffic and launch strategy for early-stage startups. |
| `google-play-publishing` | Walks through publishing an Android app on Google Play. |
 
## How the skills are structured
 
Each skill keeps `SKILL.md` small, because that file is read in full every time the skill
loads. The detailed rule sets live in `references/` and load only when the task needs them.
 
`avoid-ai-writing` is the clearest example. `SKILL.md` holds the method and the
highest-signal checks. The vocabulary tiers, the pattern catalogue, the Simplified Technical
English rules, the context profiles and the Hebrew module are six separate reference files.
Auditing a Hebrew text loads the Hebrew module and skips 27KB of English tables it has no
use for.
 
Language routing follows the same idea. An English pattern list does not fire on Hebrew, so
running it on Hebrew text returns a clean bill of health that means nothing. Each skill that
can face more than one language names its reference file per language and is told to say
"I have no module for this language" rather than report a false pass.

## Folder Structure

```text
start-here/       Entry point for course participants and new users
current/          Current publishable guides and skills
examples/         Small demos, mini-sites, lecture demos, and practical examples
media/            Links to recordings and external media
docs/             Maintainer notes and publishing recommendations
archive/          Older drafts, context notes, and legacy outputs
_private/         Local-only files, including Supabase SQL; do not publish
```

## What To Publish

Publish these folders:

- `start-here/`
- `current/`
- `examples/`
- `media/`
- `docs/`
- `archive/` only if you want transparent old material

Do not publish `_private/`.

## Current Assets

Guides:

- [New machine setup, English](current/guides/new-machine-claude-code-setup.en.html)
- [New machine setup, Hebrew](current/guides/new-machine-claude-code-setup.he.html)
- [AI agent repo advisor, English](current/guides/ai-agent-repo-advisor.en.html)
- [AI agent repo advisor, Hebrew](current/guides/ai-agent-repo-advisor.he.html)
- [AI agent repo operating guide](current/guides/ai-agent-repo-operating-guide.md)

Skills:

- [Agent onboarding wizard](current/skills/agent-onboarding-wizard/SKILL.md) — set up a safe AI coding environment after installing Claude Code or Codex
- [Avoid AI writing](current/skills/avoid-ai-writing/SKILL.md) — audit and rewrite text to remove AI writing patterns
- [CV story builder](current/skills/cv-story-builder/SKILL.md) — build a tailored CV from a job post and candidate source files
- [Google Play publishing](current/skills/google-play-publishing/SKILL.md) — walk through publishing an Android app on Google Play
- [Improve codebase architecture](current/skills/improve-codebase-architecture/SKILL.md) — survey a codebase for shallow modules and rank deepening candidates
- [New project from PRD](current/skills/new-project-from-prd/SKILL.md) — turn a PRD or product idea into a project an agent can build
- [Outside reader audit](current/skills/outside-reader-audit/SKILL.md) — read external-facing text as an outsider with no hidden context
- [Startup free traffic](current/skills/startup-free-traffic/SKILL.md) — organic, zero-budget traffic and launch strategy for early-stage startups
- Packaged `.skill` files are in [current/skills](current/skills).

## Safety

Before publishing, scan for:

- API keys
- `.env` files
- Supabase service-role keys
- private URLs
- student data
- internal database details

