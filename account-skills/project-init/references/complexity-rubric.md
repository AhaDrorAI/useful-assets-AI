# Complexity Rubric — Starter vs Full

The skill creates one of two structures. Use this rubric on the PRD to pick.

## Starter (3 docs + .claude/)

Generate `CLAUDE.md`, `tasks.md`, `project_state.md`, plus `AGENTS.md` and `.claude/`.

Skip `planning.md` and `decisions.md`.

### When to choose starter

The project hits **most** of these:

- Single-feature scope — there is one main thing being built, not a product with many surfaces
- One user/persona — no role-based access, no admin-vs-user split, no internal-vs-external distinction
- No backend, OR a stateless single-purpose backend (one endpoint, no DB)
- Five or fewer distinct user flows / screens / commands
- No regulated data (no PII handling beyond name/email, no payments, no health/financial regulation)
- One or zero third-party integrations
- Short timeline (days to a few weeks) or explicit throwaway/prototype framing
- The PRD itself is short — under ~500 words is a strong signal

### Why these criteria

`planning.md` and `decisions.md` only earn their place when there's enough complexity that you'd otherwise lose track of decisions or sequence. Forcing them on a one-screen tool just makes the user fill in ceremony files and erodes trust in the structure.

## Full (6 docs + .claude/)

Generate everything: `CLAUDE.md`, `PRD.md` (left as user wrote it), `planning.md`, `tasks.md`, `decisions.md`, `project_state.md`, plus `AGENTS.md` and `.claude/`.

### When to choose full

The project hits **any one** of these (any single one is enough — full set is cheap; missing it when needed is expensive):

- Multiple user roles or personas (admin vs user, buyer vs seller, teacher vs student, etc.)
- Multi-flow product — three or more distinct user journeys with their own screens
- Backend with non-trivial state — database schema, job queues, scheduled tasks, real-time channels
- Auth, payments, PII handling, or any regulated data (GDPR, HIPAA, PCI, COPPA, FERPA, etc.)
- Multiple third-party integrations that need ongoing management
- Production-bound or long-lived (months+ timeline, real users)
- The PRD itself is long and structured — sections like Goals, Non-goals, User Flows, etc. — signaling the user is treating it as a real product

### Why these criteria

`planning.md` is what keeps multi-flow products coherent. `decisions.md` is what stops the team from re-litigating the same architecture choices in month three. Both pay for themselves the first time the user has to remember "wait, why did we pick X?"

## Tiebreakers

- **PRD says one thing, file inventory says another.** If `package.json` reveals a Next.js app with Prisma and Auth.js, that's full-set even if the PRD is breezy. Trust the artifacts.
- **User explicitly asks for one or the other.** Always honor.
- **Genuinely ambiguous.** Default to **starter** and tell the user "I picked starter because [reason] — say the word and I'll add planning.md and decisions.md."

## What to tell the user

State the decision in one sentence with the reasoning, then proceed unless they push back. Examples:

- "PRD describes a single-screen browser tool with no backend → starter set."
- "PRD has admin and student roles, calls out Supabase + Inngest, and lists 8 flows → full set."
- "Borderline — defaulting to starter; tell me if you want planning.md and decisions.md too."
