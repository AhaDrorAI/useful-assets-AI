# Maintaining this repository

Visitor entry is [README.md](../README.md). This file is for the person who changes the tree.

## Publish boundary

`.gitignore` is the boundary. Tracked files are public. Local working state (`.wolf/`, `.claude/`, machine notes, OpenWolf repair) is ignored and must not be added back.

CI fails the build if a tracked file matches `.gitignore`.

## Layout

| Path | Role |
|---|---|
| `current/` | Plugin files (`skills/`). LinkedIn URLs stay here. |
| `.claude-plugin/marketplace.json` | Marketplace catalog. Desktop sync needs a `github` object source, not a relative string or `git-subdir`. |
| `.claude-plugin/plugin.json` | Plugin manifest at the repo root. Skills path is `./current/skills`. |
| `guides/` | Human-readable guides. Invisible to the plugin loader. |
| `start-here/` | Course sequence. |
| `docs/` | Maintainer notes. |
| `account-skills/` | Skills uploaded to the maintainer's Claude account, kept here for history, review dates and tests. Not part of the plugin. |
| `vector-operating-system/`, `vector-private-memory/` | Personal plugins, kept as sibling folders. Not in `marketplace.json`. Memory files of `vector-private-memory` are gitignored. |

`current/skills/<name>/` paths stay put so published GitHub links keep resolving.

A second plugin is a sibling of `current/`, then a new entry in `marketplace.json`. Do not put it inside `current/`.

## Skill review

`docs/skill-review.md` is the writing standard, the test-case layout, and the drift review. `docs/skill-audit-log.md` records each review. Every skill carries `metadata.last_reviewed`; the packager warns when one is overdue.

## Packaged skill files

`scripts/package_skills.py` lints every skill root and builds one zip per skill into `dist/`. Test cases (`evals/`) and `.skill` files never go into a zip. GitHub Actions runs that on every push and attaches the zips to a GitHub Release when you push a version tag:

```bash
git tag v1.2.0
git push --tags
```

Do not commit `dist/` or hand-placed `.skill` files. The docs point at Releases, not at files in the tree.

## What not to advertise

Do not list `examples/` from the visitor README until it holds a real example. Empty folders read as a broken promise.
