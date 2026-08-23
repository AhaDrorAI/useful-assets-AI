# useful-assets-AI

Writing gates and working skills for Claude Code, Claude Desktop, Cowork, Codex, and ChatGPT. Hebrew and English. Built so a skill stays small, loads only the rules the current language needs, and refuses to give a fake pass on text it cannot judge.

Course path: [start-here/](start-here/).

## Install

The skills install as one plugin. The marketplace catalog lives in this repository, so an install stays connected to the source and can be updated later.

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

`Customize` → `Plugins` → under **Personal plugins**, `+` → `Add marketplace` → `Add from a repository` → enter `AhaDrorAI/useful-assets-AI`. Then install `useful-assets-ai` from the marketplace that appears.

Same catalog as Claude Code. One source, three surfaces.

### Codex and ChatGPT desktop

These read skills from a local folder rather than a marketplace. Clone the repo once and point the skills directory at it:

```bash
git clone https://github.com/AhaDrorAI/useful-assets-AI.git
```

Then link `~/.agents/skills` to `current/skills` inside the clone. After that, `git pull` updates every skill at once.

## Update

```
/plugin marketplace update
/plugin update
```

In Claude Desktop and Cowork, refresh the marketplace from the same Plugins screen. For Codex, `git pull` in the clone.

## Skills

| Skill | What it does |
|---|---|
| [avoid-ai-writing](current/skills/avoid-ai-writing/SKILL.md) | Audits and rewrites text to remove AI writing patterns. English and Hebrew. |
| [outside-reader-audit](current/skills/outside-reader-audit/SKILL.md) | Reads external-facing text as an outsider with no hidden context. Has an Israeli-reader module. |
| [improve-codebase-architecture](current/skills/improve-codebase-architecture/SKILL.md) | Surveys a codebase for shallow modules and ranks deepening candidates. Proposes only, never edits. |
| [cv-story-builder](current/skills/cv-story-builder/SKILL.md) | Builds a tailored CV from a job post and candidate source files. |
| [agent-onboarding-wizard](current/skills/agent-onboarding-wizard/SKILL.md) | Sets up a safe AI coding environment after installing Claude Code or Codex. |
| [new-project-from-prd](current/skills/new-project-from-prd/SKILL.md) | Turns a PRD or product idea into a project an agent can build. |
| [startup-free-traffic](current/skills/startup-free-traffic/SKILL.md) | Organic, zero-budget traffic and launch strategy for early-stage startups. |
| [google-play-publishing](current/skills/google-play-publishing/SKILL.md) | Walks through publishing an Android app on Google Play. |

Claude Code, Desktop, and Cowork load these through the plugin. Codex and ChatGPT use the same folders from `current/skills`. Packaged `.zip` files are built by CI and attached to [GitHub Releases](https://github.com/AhaDrorAI/useful-assets-AI/releases) when a version is tagged.

## How the skills are structured

Each `SKILL.md` stays small, because that file is read in full every time the skill loads. Detailed rule sets live in `references/` and load only when the task needs them.

`avoid-ai-writing` is the clearest example. `SKILL.md` holds the method and the highest-signal checks. Vocabulary tiers, the pattern catalogue, Simplified Technical English, context profiles, and the Hebrew module are separate reference files. Auditing Hebrew text loads the Hebrew module and skips the English tables.

An English pattern list does not fire on Hebrew, so running it on Hebrew would return a clean bill of health that means nothing. Skills that can face more than one language name their reference file per language and are told to say "I have no module for this language" rather than report a false pass.

## Guides

- [New machine setup, English](guides/new-machine-claude-code-setup.en.html)
- [New machine setup, Hebrew](guides/new-machine-claude-code-setup.he.html)
- [AI agent repo advisor, English](guides/ai-agent-repo-advisor.en.html)
- [AI agent repo advisor, Hebrew](guides/ai-agent-repo-advisor.he.html)
- [AI agent repo operating guide](guides/ai-agent-repo-operating-guide.md)

Maintainers: [docs/maintaining.md](docs/maintaining.md).
