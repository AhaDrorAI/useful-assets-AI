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

`current/skills/<name>/` paths stay put so published GitHub links keep resolving.

A second plugin is a sibling of `current/`, then a new entry in `marketplace.json`. Do not put it inside `current/`.

## Packaged skill files

`scripts/package_skills.py` builds one zip per skill into `dist/`. GitHub Actions runs that on every push and attaches the zips to a GitHub Release when you push a version tag:

```bash
git tag v1.2.0
git push --tags
```

Do not commit `dist/` or hand-placed `.skill` files. The docs point at Releases, not at files in the tree.

## What not to advertise

Do not list `examples/` from the visitor README until it holds a real example. Empty folders read as a broken promise.
