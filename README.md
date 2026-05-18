# Dror AI Agent Launchpad

Reusable guides, skills, and examples for helping non-developers work with Claude Code, Codex, and AI coding agents.

## Start Here

Open [start-here/README.md](start-here/README.md) for the recommended path.

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

- [Agent onboarding wizard](current/skills/agent-onboarding-wizard/SKILL.md)
- [New project from PRD](current/skills/new-project-from-prd/SKILL.md)
- Packaged `.skill` files are in [current/skills](current/skills).

## Safety

Before publishing, scan for:

- API keys
- `.env` files
- Supabase service-role keys
- private URLs
- student data
- internal database details

