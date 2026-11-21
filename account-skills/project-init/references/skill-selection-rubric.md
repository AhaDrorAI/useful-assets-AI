# Skill Selection Rubric

This is the *what to install* decision logic. The *how* is in `ecc-bootstrap.md`.

The goal: install only what's relevant to *this* project, not a fixed default set. Two reasons:

1. **Token cost.** Each rule and skill in `.claude/` consumes context window when the agent loads it. Unused content = wasted tokens.
2. **Signal-to-noise.** A `.claude/` cluttered with irrelevant skills makes the relevant ones harder for the agent to find and use.

## Inputs

Before applying the rubric, gather:

- Stack signal: from PRD, `package.json`, `pyproject.toml`, etc.
- Domain primitives: from PRD ("uses Stripe", "calls OpenAI", "Supabase realtime", etc.)
- Quality signals: from PRD or interview ("production", "regulated data", "throwaway", etc.)
- Global inventory: `~/.claude/skills/`, `~/.claude/rules/`, `~/.claude/agents/`
- ECC catalog: live, parsed from `$ECC_CACHE/skills/`, `rules/`, `agents/`

## The rubric — work through it in order

### A. Rules from `rules/common/`

These are universal and almost always worth installing. Default install all of `common/`. Skip individual ones only if the user signals strongly against them.

- `coding-style.md` — install
- `git-workflow.md` — install
- `testing.md` — install **unless** the project is "no tests" by design (rare, ask if unsure)
- `performance.md` — install
- `patterns.md` — install
- `hooks.md` — install
- `agents.md` — install
- `security.md` — install. If the PRD mentions PII/payments/regulated data, this becomes critical.

### B. Stack-specific rules from `rules/<lang>/`

Install the folder matching the detected primary stack. Skip all others.

| Detected signal | Install folder |
|---|---|
| `package.json`, `tsconfig.json`, "Next.js", "React", "Vue", "Node" | `rules/typescript/` |
| `pyproject.toml`, `requirements.txt`, "Django", "FastAPI", "Flask" | `rules/python/` |
| `go.mod`, "Go" | `rules/golang/` |
| `Cargo.toml`, "Rust" | `rules/rust/` (if exists) |
| `*.swift`, Xcode project, "iOS", "macOS" | `rules/swift/` |
| `composer.json`, "Laravel", "PHP" | `rules/php/` |

If the project is multi-stack (frontend TS + backend Python, common case), install both.

If the stack isn't in ECC's available rules folders, skip — don't substitute the wrong language's rules.

### C. Skills — apply branches

For each branch below, check whether it applies to *this project*. If yes, propose the listed skills. The exact skill names may shift as ECC evolves — read the live catalog and pick the closest match by description.

#### Quality / methodology — almost always

- `tdd-workflow` — propose unless project is "no tests" by design
- `verification-loop` — propose unless project is one-off / throwaway
- `search-first` — propose for any project of substance (research before code beats reinventing)
- `strategic-compact` — propose only if project will involve long sessions

#### Stack-specific patterns

If detected stack matches one of these, propose the corresponding skill (and any sibling like `<stack>-testing`):

- TypeScript / React / Next.js → `frontend-patterns`, `nextjs-turbopack` (if Next 16+)
- Python (Django) → `django-patterns`, `django-tdd`, `django-security`, `django-verification`
- Python (general) → `python-patterns`, `python-testing`
- Go → `golang-patterns`, `golang-testing`
- Java/Spring Boot → `springboot-patterns`, `springboot-tdd`, `springboot-security`
- Laravel → `laravel-patterns`, `laravel-tdd`, `laravel-security`
- C++ → `cpp-coding-standards`, `cpp-testing`
- Swift → `swift-actor-persistence`, `swift-protocol-di-testing`
- Rust → `rust-patterns` (if exists)
- Perl → `perl-patterns`, `perl-testing`, `perl-security`

#### Domain primitives — install only when used

| If the project involves... | Propose |
|---|---|
| External API design / REST endpoints | `api-design`, `backend-patterns` |
| Database schema or migrations | `database-migrations`, `postgres-patterns` (if Postgres) |
| LLM calls (OpenAI, Anthropic, etc.) | `cost-aware-llm-pipeline`, `claude-api` if relevant |
| Text parsing / extraction | `regex-vs-llm-structured-text` |
| File processing with caching | `content-hash-cache-pattern` |
| Docker / deployment | `docker-patterns`, `deployment-patterns` |
| E2E browser testing | `e2e-testing` |
| MCP server development | `mcp-server-patterns` |
| Documentation / API reference work | `documentation-lookup` |
| iOS 26+ / on-device AI | `liquid-glass-design`, `foundation-models-on-device` |
| Multi-platform content / writing | `article-writing`, `content-engine` |
| Investor / fundraising work | `investor-materials`, `investor-outreach` |
| Market research | `market-research` |
| Video / media generation | `fal-ai-media`, `video-editing`, `videodb` |

If a category isn't on this list but seems relevant, scan the live ECC catalog and propose anything whose description fits.

#### Security-critical projects

If PRD signals security sensitivity (PII, payments, auth-as-a-feature, regulated data):

- `security-review` — propose, weight as high priority
- `security-scan` — propose

#### Project-only filter

Before finalizing, ask: **would this skill be useful in every project I work on, or specifically in this one?**

- If "every project": flag for *recommended global install*, not project install. The user gets it once at `~/.claude/skills/` and benefits everywhere.
- If "specifically this one": project install at `.claude/skills/`.

Examples of typically-global skills: `tdd-workflow`, `verification-loop`, `search-first`, `continuous-learning-v2`, `strategic-compact`. The user may already have these globally — check the inventory.

### D. Agents

Be more conservative with agents — each one is a separate context window when invoked, so cluttering `.claude/agents/` is more costly than cluttering skills.

Default proposals:

- `code-reviewer` — propose for almost any project
- `planner` — propose for full-set projects (multi-flow products benefit)
- `<stack>-reviewer` — propose if a matching one exists (e.g., `python-reviewer`, `go-reviewer`, `typescript-reviewer`)
- `security-reviewer` — propose only for security-critical projects
- `e2e-runner` — propose only if project will have Playwright/E2E tests
- `build-error-resolver` — propose for any project with a real build pipeline

Skip everything else by default. The user can add more later as needs emerge.

## Subtract globals (always last step)

After the rubric proposes a list, walk it once more and remove anything already at `~/.claude/skills/`, `~/.claude/rules/`, or `~/.claude/agents/`. Mention these in the final report ("you already have these globally") so the user knows they're covered.

## Present and wait

Show the user the final delta — proposed installs + globals being skipped + recommended globals — and wait for approval before copying anything. Don't proceed silently.

## Calibrating depth

A reasonable project install ends up around:

- **8 rules** (most of `common/` + one stack folder with ~3 files)
- **3-6 skills** (1-2 quality skills if not already global, 1-2 stack patterns, 1-3 domain skills)
- **2-4 agents** (`code-reviewer`, stack reviewer, maybe planner, maybe build-error-resolver)

If the rubric is producing 15+ skills, you're over-installing. Cut. The user can always add more.
