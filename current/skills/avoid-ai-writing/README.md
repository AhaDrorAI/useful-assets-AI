# avoid-ai-writing

Audit and rewrite content to strip AI writing tells ("AI-isms"). Flags a tiered
vocabulary list, formatting habits, and structural patterns; runs in `rewrite`
(default), `quick` (clean text only) or `detect` (flag, do not rewrite) mode.

This is a fork of Conor Bronsdon's MIT-licensed skill, with added rules for
overgeneralized "Most people..." openers, adverb crutches, fake profundity, and
the "after careful consideration" / "here's the thing" stalls.

Version 3.8.0 adds analogy and metaphor control (`references/metaphor.md`): banned
setups, the exhausted image families, the metaphor-verb list that survives every
other sweep, a length-based frequency budget, and a five-point permission test.
It also generalises the old single "it's not X, it's Y" bullet into a full Reframes
section covering the soft variants that never use the word "not", the pivot-word
watchlist, reframe headings, and the rhetorical-question form. Smaller additions: a
rule-priority ladder for when two rules disagree, a `quick` output mode, targeting
the assistant's own last draft on "audit your text", and fake-depth participles,
meta commentary, engagement bait and a digits rule. The project-local
`forbidden-patterns.md` now loads on the audit path, not only when drafting.

Version 3.6.0 absorbs the transferable rules from ASD-STE100 Simplified Technical
English: nominalisations, actorless passive, tense bloat, empty-subject openers,
noun stacks, and 22 controlled-language word substitutions. It also states which
STE rules to reject, since a standard written for aircraft manuals bans
contractions and phrasal verbs that ordinary prose needs to sound human.

Version 3.5.0 adds the tells that outlived the em dash — paired fragments, two-image
contrasts, self-applause tags, X-of-Y analogies, and hedged numeric ranges — plus a
section on preventing the patterns at generation time with ASD-STE100, Zinsser's
fourth principle, and a project-local forbidden-patterns file. Adapted from Ruben
Hassid's nine tells ([ste.rubenhassid.ai](http://ste.rubenhassid.ai)).

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
