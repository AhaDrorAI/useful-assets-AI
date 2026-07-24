# avoid-ai-writing

Audit and rewrite content to strip AI writing tells ("AI-isms"). Flags a tiered
vocabulary list, formatting habits, and structural patterns; runs in `rewrite`
(default) or `detect` mode.

This is a fork of Conor Bronsdon's MIT-licensed skill, with added rules for
overgeneralized "Most people..." openers, adverb crutches, fake profundity, and
the "after careful consideration" / "here's the thing" stalls.

## Install

The skill is one `SKILL.md` following the [agentskills.io](https://agentskills.io)
open standard. Every supported agent reads the same file; only the directory
differs. Drop the `avoid-ai-writing/` folder into the matching path.

| Agent | Global (all projects) | Project-local |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.codex/skills/` | `.codex/skills/` |
| Grok Build | `~/.grok/skills/` | `.grok/skills/` |

Grok Build also auto-discovers the Claude Code copy, so a single
`~/.claude/skills/avoid-ai-writing/` install covers both Claude and Grok.

### Copy install (one agent)

```bash
git clone https://github.com/<you>/<repo>.git
cp -r <repo>/avoid-ai-writing ~/.claude/skills/
```

### Symlink install (edit once, all three follow)

Keep the repo as the single source of truth and link each agent to it:

```bash
REPO=~/path/to/<repo>
ln -s "$REPO/avoid-ai-writing" ~/.claude/skills/avoid-ai-writing
ln -s "$REPO/avoid-ai-writing" ~/.codex/skills/avoid-ai-writing
ln -s "$REPO/avoid-ai-writing" ~/.grok/skills/avoid-ai-writing
```

On Windows, run the clone/symlink from Git Bash, or use
`New-Item -ItemType SymbolicLink` in an elevated PowerShell.

## Use

Ask the agent to "remove AI-isms," "clean up this draft," or "detect AI patterns
only." Pass a context hint (`linkedin`, `blog`, `investor-email`, `docs`,
`casual`) to adjust strictness; it auto-detects if you don't.

## License

MIT. Original author: Conor Bronsdon. Attribution retained per the license.
