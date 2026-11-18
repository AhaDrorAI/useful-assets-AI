# Account skills

Skills that live in the maintainer's Claude account (uploaded one by one), kept here so they have version history, review dates and test cases.

They are **not** part of the `useful-assets-ai` plugin. The plugin loads only `current/skills/`. Keeping these outside it means a user who has both the plugin and the uploaded copies does not get two copies of the same skill competing for the same request.

To upload a revised skill: run `python scripts/package_skills.py` from the repo root, then upload `dist/<skill>.zip` in the Claude app (Customize → Skills). Replace the existing skill of the same name.

| Skill | Origin |
|---|---|
| `blender-mcp-master` | Maintainer, modified |
| `fable-5-prompt-writer` | Maintainer. `references/steering-blocks.md` was missing from the uploaded copy and was reconstructed on 2026-11-18. |
| `fast-doc-to-markdown` | Maintainer, wraps Firecrawl's `anydoc` CLI |
| `gamma-presentation-builder` | Maintainer |
| `pptx-hebrew` | Maintainer |
| `project-init` | Maintainer, modified; pulls from `affaan-m/everything-claude-code` at run time |
| `strategic-build` | Maintainer, modified; frameworks paraphrased from Shreyas Doshi and Marty Cagan |

`anatomy` (MIT, `wheresryan22/anatomy`) is also uploaded to the account but is not copied here: it is an actively maintained third-party project of about 13 MB. Changes to it belong upstream. See `docs/skill-audit-log.md`.

The first commit that added this folder holds the skills exactly as uploaded. Diff against it to see every change.
