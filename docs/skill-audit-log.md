# Skill audit log

One section per review. The method is in `docs/skill-review.md`.

Confidence tags: **[Certain]** checked against a file, a run or a primary source; **[Likely]** strong inference; **[Guessing]** filling a gap.

---

## 2026-11-18: full review of every owned skill

### Scope

| Set | Skills | Where the revision lives |
|---|---|---|
| Plugin (`current/skills/`) | 10 | this repo, this branch |
| Account uploads | 7 revised + `anatomy` audited only | `account-skills/` (not in the plugin) |
| Vector plugins | 8 + 1 skills, 5 agents | `vector-operating-system/`, `vector-private-memory/` |
| `race-studio` repo | 1 | PR AhaDrorAI/race-studio#1 |
| `Rearing_Paradigm` repo | 4 | PR AhaDrorAI/Rearing_Paradigm#14 |

Out of scope: Anthropic's built-in skills (docx, pdf, skill-creator, ...), installed third-party plugins (`data`, `claude-context-optimizer`), and any skill that exists only on the maintainer's computer. No computer was attached to the session, so local-only skills were not visible.

Each set was committed unchanged first (account skills and Vector plugins have a "baseline" commit), so `git diff` against that commit shows every change.

### Shared changes

- **Lint in CI** (`scripts/package_skills.py`). It fails on: a bundled file named in SKILL.md that does not exist, a malformed test case, and a frontmatter error. It warns on: vague wording, write tools pre-approved in `allowed-tools`, a missing or overdue review date, missing test cases, and a stray `.skill` archive. It also fixed two old bugs:
  - The old parser read a folded (`>`) description as the single character `>`, so the length check passed for any block description. [Certain]
  - `evals/` and `.skill` files were zipped into uploads. [Certain]
- **Review dates**: every skill except the Vector plugin's has `metadata.last_reviewed` and `review_every_days` (90 for skills with volatile facts, 180 otherwise).
- **Test cases**: 3 per skill (normal, edge, ambiguous) in the `claude plugin eval` layout. Total: 96 cases, across 31 of the 33 skills; the two Vector alias skills have none of their own.

### Per-skill findings and changes

#### Plugin skills

| Skill | Main findings | Changes |
|---|---|---|
| agent-onboarding-wizard | Short description with no trigger phrases. "Onboarding complete." printed even when a capability was blocked, which contradicted its own rule. "Broad permissions" undefined. No procedure for reviewing third-party items. | Trigger-rich description. Conditional summary header. Broad permissions defined. A 4-point third-party review. Stage plans of more than 5 installs. |
| avoid-ai-writing (fork, MIT) | Four names for overlapping things: "quick mode", "quick pass", "quick scan", "fast pass". No rule for long texts. | One term per thing (triage pass defined). 3,000-word rule. Version 3.8.1 with `fork_changes` entry. |
| cv-story-builder | "If the task is substantial" undefined. The outside-reader audit was meant to be isolated, but nothing enforced it. Codex `agents/openai.yaml` lacked the `interface:` wrapper the other skills use. | Thresholds for using agents. Isolated subagent, or a disclosed non-isolated audit. Privacy rule. Fallbacks when `docx` or `outside-reader-audit` is missing. YAML shape fixed. |
| expert-problem-solving | Sound; judgment-based by design. "Consequential" used but undefined. | Defined "consequential". Richer description. No rule-tightening: judgment kept. |
| google-play-publishing | **Factually wrong:** it said 20 testers. Google's help page says 12 testers for 14 continuous days, for personal accounts created after 13 Nov 2023. [Certain] It recommended a paid tester service. It framed an organization account as a "workaround" for individuals, but organization accounts must represent a real organization, and the rules for sole proprietors are unclear. [Likely] D-U-N-S timing was understated. | Volatile-facts table with sources and dates. 12 testers. No paid testers. Honest account-type guidance. Unverified SDK date marked. |
| improve-codebase-architecture (fork) | Its invariant "nothing changes without approval" was undercut by `allowed-tools: Bash, Write, Edit`, which skips the permission prompt. [Likely] | `allowed-tools` now pre-approves only reads and `git log`, `git status`, `grep`, `wc`. Its own `audit_skill.py` gained check A5b (write tools must not be pre-approved). ATTRIBUTION.md updated. 46/46 self-checks pass. |
| new-project-from-prd | Description lost its trigger phrases. `codegraph` was an ambiguous tool name. "Project bootstrap complete." printed unconditionally. No guard against running in the home folder. | Triggers restored, with a pointer to agent-onboarding-wizard for the boundary. Unsafe-folder check. One-message interview. Conditional final header. Secrets rule. |
| outside-reader-audit | "Ignore prior conversation" cannot be done by instruction alone. | Isolation via a fresh subagent, or an explicit "Not isolated" notice. Rules for no-text, long-text and output language. Refined after the live test (see below). |
| security-audit | A rollback does not undo `pg_net` / webhook / email side effects. The report was to be "published", and an open-findings report is an attacker's map. Migrations were "committed to the repo" with no branch rule. Read-only rested on prose. | Trigger side-effect check before any proof. Report never public while findings are open. Migrations on a new branch. Read-only database connection for discovery. |
| startup-free-traffic | A committed `.skill` archive, against `docs/maintaining.md`. `license:` pointed to a non-existent `LICENSE.txt`. Unbounded question flow. Volatile platform facts undated. | Archive removed. Licence line removed (see open decisions). At most 3 questions per message. Date-volatile-facts rule. |

#### Account skills (`account-skills/`)

| Skill | Main findings | Changes |
|---|---|---|
| fable-5-prompt-writer | **Broken dependency:** `references/steering-blocks.md` is named but was not in the upload. The skill's core selection step could not run. [Certain] An unverified claim about falling back to an older model. | Reference rebuilt from the six block names in the skill, **labelled as a reconstruction**. Fallback if the file is unreadable. Claim softened and dated. |
| strategic-build | Direct quotations attributed to Shreyas Doshi and Marty Cagan that are not verifiable, plus an invented "Stripe API" case study. [Likely] It misrepresents LNO as "skip overhead" with a 70/20/10 ratio; Doshi frames LNO as matching effort to return, not deleting tasks. [Likely] It linked 3 reference files and 5 "related skills" that do not exist. [Certain] | Rewritten: frameworks paraphrased and labelled as paraphrase, invented examples removed, lens chooser, judgment-based output format, dead links removed. |
| pptx-hebrew | `fix_rtl.py` rewrote `p:` to a default namespace in every slide. It forced RTL onto English sentences containing one Hebrew word (contradicting its own docs). It skipped runs without `<a:rPr>`. [Certain, reproduced on real PptxGenJS 3.12 output] Verification relied on a visual check the skill itself says cannot detect the bug. | Script rewritten: prefixes kept; majority-direction rule (`--any-rtl` restores the old behaviour); missing `rPr` created; `endParaRPr` tagged; `--check` mode with exit codes. Tested on real output, both the lxml and the stdlib path, idempotent. SKILL.md verifies with `--check`. |
| gamma-presentation-builder | It set text density and image style on every call. The connector says to omit optional parameters unless the user asks. [Certain, from the tool schema] | Hebrew imperative rewrite. Exact parameter list (`inputText`, `textMode: generate`, `numCards`, `language`, `additionalInstructions`). No call before outline approval (credits). Export-link expiry warning. No invented figures. |
| fast-doc-to-markdown | Global `npm install -g` without asking. The `--ocr hosted` rule was clear but enforced only by text. | `npx` first. Ordered fallbacks for scanned pages. Hosted OCR only on a per-file, informed request. Exit codes 0/1/2/3 verified against anydoc. [Certain] |
| blender-mcp-master | `execute_blender_code` runs arbitrary Python on the user's machine with no boundaries. "Clear default objects" could delete the user's work. Pinned to Blender 5.0.1 with no version check. Orphan cleanup could remove the user's data blocks. Sketchfab licences and Hyper3D credits not mentioned. | Python boundaries. Factory-default test before deleting anything. Version check. Guarded cleanup. Licence and credit rule. Tool-name drift note. |
| project-init | **Writes an invalid `.claude/settings.json`** ("a short comment block at top"; JSON has no comments). [Certain] Uses `disabledMcpServers`, which is not a documented key. [Likely] `inventory_globals.sh` uses `find -printf` (GNU only); on macOS it silently returns no globals. [Certain] ECC content copied unpinned and unreviewed. Overlaps new-project-from-prd. | Valid minimal settings plus a `json.tool` check. Portable inventory script (tested). ECC commit recorded, scripts reviewed, no hooks copied. Description points idea-only starts to new-project-from-prd. |
| anatomy | Audit only. MIT, by `wheresryan22`, actively maintained, about 13 MB. Lint: SKILL.md names `kit/react/draw.ts` and `kit/react/live.ts`, which are not in the uploaded copy. [Certain for the upload; the upstream repo may have them] | Not copied. Re-download the current release or report upstream. |

#### Vector plugins

| Finding | Change |
|---|---|
| Two pairs of duplicate skills with overlapping triggers (`direct-mode`/`go-direct`, `session-start`/`start-session`). Their rules could drift apart. | The second of each pair is now an alias that defers to the first. The slash commands still work. |
| "Private one-to-one context" and "external actions" were undefined, yet they are the plugin's main safety rules. | Defined once in `vector-operating-system`: exactly one human, not a shared space, treat as shared when unsure. External actions are listed. Approval does not carry over. |
| "Ask before external actions" is prose only. | The skill says how to enforce it: set connector send/post/share tools to "Ask". |
| `vector-researcher` and `vector-fact-checker` had only Read/Grep/Glob, so they could not research or check links. [Certain] | Added WebSearch and WebFetch. Still no write tools. |
| Agent examples named private projects. | Made generic. |
| `vector-private-memory` memory files must never be public. | Only the skill and manifest are in the repo. The memory files are in the root `.gitignore`; CI fails if one is tracked. Verified with `git check-ignore`. |
| Review dates. | **Not added to frontmatter.** The plugin's own README says Cowork rejected non-standard skill fields. The lint warns about the missing date for these 9 skills; accepted until the Cowork schema is confirmed. |

#### Other repos (see the PRs for detail)

- **race-studio / create-ball-race-episode**:
  - The "never upload" intro contradicted the rule that allows a private upload.
  - The interest check was buried after the render step.
  - Code enforcement: `render.ts` told the agent to "Simulate again", which invites the reroll the skill forbids. The message now says the producer decides.
  - Never pass `--force`.
- **Rearing_Paradigm**:
  - The export strip-check missed `v3.6`, `v3_6`, `[V]`, `[M]`, `[?]` and `[compiler]`. Tested: the old pattern caught 0 of 5 markers, the new one 5 of 5, with no false positive on a clean line.
  - The firecrawl conversion skill now bans hosted OCR for project files.
  - The wiki lint step calls the real linter.
  - Found, not changed: an exported summary that mentions "v3.52"; `lint_wiki.py` fails on `main` (2 stale pointers).
- **Copy to this repo:** none of the 5 is generic. They depend on project tooling. The firecrawl conversion skill is third-party and is covered by `fast-doc-to-markdown`.

### Tests

**Static:** every skill passes the lint with 0 errors. Remaining warnings are listed under "Accepted warnings" below.

**Scripted:**
- `fix_rtl.py`: 10 fixes on a PptxGenJS file; idempotent (0 on a second run); English-primary paragraph stays LTR; prefixes preserved; opens in python-pptx; stdlib fallback path tested.
- `inventory_globals.sh`: populated folder and missing folder.
- anydoc exit codes 0, 1, 2, 3.
- Strip-check regex: sample file and the existing derivatives.
- `audit_skill.py`: 46/46.

**Live (subagents, same prompt, 3 runs of the new version plus 1 of the old):**

| Skill and case | New version (3 runs) | Old version (1 run) |
|---|---|---|
| google-play-publishing: solo developer wants an org account to skip testing | 3/3: 12 testers, no paid testers, "organization route does not fit an individual", confirm with Google. Consistent conclusion across runs. | 20 testers; recommends a paid tester service; presents D-U-N-S as a route for any sole developer. |
| outside-reader-audit: cover letter with hidden context | 3/3: identical 8 headings in identical order; all four hidden references flagged. Length 883–1,064 words. | Same structure. |
| security-audit: proof on a table whose trigger calls `net.http_post` | 3/3: no insert (not even rolled back), proof by 4 read-only queries (grants, policies, trigger and function text), asks before any write. **But** the runs repeated the skill's explanation that a rollback cannot undo a `pg_net` call, which is wrong for `pg_net` (it queues; a rollback normally cancels). [Likely] | Also refused the insert and proved the hole read-only. It explained `pg_net` queuing correctly. **The test did not tell the two versions apart.** |

Changes made because of the live tests:

- security-audit: the explanation was corrected (`http` is synchronous; `pg_net` queues and normally cancels on rollback). The rule itself stays: no proof on a table with an outside side effect. The new version's value here is that the rule is now explicit rather than left to the model's judgment, not that the outcome changed. A sharper test would use a trigger that sends email through a synchronous function.
- outside-reader-audit: the test agents were already isolated (they received only the letter), yet each printed the "Not isolated" notice. The isolation rule now first checks whether the agent itself received only the text.

**Not performed:**
- Live runs for the other 28 skills. Their test cases are written but not run. Run them with `claude plugin eval` (billed).
- Description-trigger optimisation (`skill-creator` run_loop). It needs `claude -p`, many billed runs, and a user-reviewed query set.
- Real Blender, Gamma, Supabase or Play Console sessions. These skills were checked by reading and by the connector schema only.
- race-studio `tsc`/tests (no `node_modules` in the session); Rearing_Paradigm registry checks (they need the Windows machine).
- Upload of revised account skills to the Claude account (no tool for it).

### Open decisions (yours)

1. **Repository licence.** The repo has no `LICENSE` file. `improve-codebase-architecture` says it "inherits the repository's licence", and `startup-free-traffic` pointed to a missing `LICENSE.txt`. Without a licence the skills are all-rights-reserved by default. Pick one (MIT matches the forks) or state "all rights reserved".
2. **project-init vs new-project-from-prd.** Both trigger on "init / bootstrap / scaffold". They now point at each other, but if both are installed the model still has to choose. Options: retire one, or narrow project-init to "PRD + ECC bootstrap" only.
3. **fable-5-prompt-writer steering blocks.** The reference file is a reconstruction. If you have the original, replace it.
4. **Vector plugins in `marketplace.json`.** They are in the repo but not published through the marketplace. Publishing a persona plugin is your choice.
5. **vector-private-memory in a public repo at all.** Its own README lists "public-facing plugin repositories" as a bad use. Only the skill and manifest are public, and memory files are blocked. Delete the folder if you prefer none of it public.
6. **Cowork frontmatter.** Confirm whether Cowork accepts `metadata:` in skill frontmatter. If it does, add review dates to the Vector skills.
7. **Account copies.** Your uploaded `avoid-ai-writing` (3.7.0), `outside-reader-audit` and `startup-free-traffic` are older than the plugin versions. Re-upload the ZIPs, or delete the uploads and rely on the plugin.

### Risks that remain

- Prose-only restrictions with no tool-level control: "never pass `--ocr hosted`" (fast-doc, convert-documents), "private context only" (Vector memory), "do not steer the race outcome" (partly enforced by race-studio's code), Blender Python boundaries. Each is named as prose-only inside its skill.
- Volatile facts: Google Play rules, Gamma parameters, Blender 5.0 API, Fable 5 behaviour, platform growth tactics. These carry a 90-day review interval.

### Accepted warnings

- Vague-word hits that describe rather than instruct ("a few dozen files", "swapping out a few words") in `avoid-ai-writing`, `google-play-publishing` and `improve-codebase-architecture`.
- Missing review dates on the 9 Vector skills (see above). Missing test cases on the 2 Vector aliases.
