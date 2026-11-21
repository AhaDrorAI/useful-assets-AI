# Interview Questions — Filling PRD Gaps

Use this as a question bank, not a checklist. The PRD plus existing files (`package.json`, `pyproject.toml`, README, etc.) usually answer half of these. Only ask what isn't already on disk.

**Hard rule: one batched interview, max ~7 questions.** Asking 7 questions one at a time is exhausting; asking them in one message lets the user answer in one pass. If you have a way to ask discrete-choice questions in a UI (like `ask_user_input_v0`), use it for the categorical ones below and use prose for the open-ended ones.

## Tier 1 — Almost always needed

These shape generated content directly. Ask whichever the PRD didn't answer.

1. **Primary language / runtime.**
   - Multiple choice: `TypeScript / JavaScript`, `Python`, `Go`, `Rust`, `Swift`, `Java/Kotlin`, `Other (specify)`, `Mixed (specify)`
   - Skip if `package.json`, `pyproject.toml`, etc. already on disk.

2. **Framework / stack** (only if Tier 1 #1 didn't fully answer).
   - Open-ended: "What framework or libraries do you expect to use? (e.g., Next.js + Supabase, FastAPI + Postgres, Vite + React)"
   - Skip if obvious from existing files.

3. **Build / test / lint commands.**
   - Open-ended: "What commands do you run for: build, test, lint, typecheck? (Leave any blank if not applicable.)"
   - Skip if `package.json` scripts or a Makefile already define them.

4. **Deployment target.**
   - Multiple choice: `Vercel`, `Netlify`, `Cloudflare`, `AWS`, `Self-hosted / VPS`, `Mobile app store`, `Desktop / local-only`, `Not deploying yet`, `Other (specify)`
   - Affects what conventions go in CLAUDE.md (e.g., env var handling, build artifacts).

## Tier 2 — Often needed for full set

Ask for full structure projects. Skip for starter unless something jumps out.

5. **Hard guardrails.**
   - Open-ended: "Are there things the agent should never do in this project? (e.g., 'never modify the database schema without asking', 'never commit directly to main', 'never call external APIs in tests')"
   - This becomes the guardrails section of CLAUDE.md. The user's answer here often reveals invisible context that wasn't in the PRD.

6. **Code conventions** — only ask if not signaled by existing config.
   - Open-ended: "Any conventions you want enforced beyond what your linter handles? (naming, file organization, patterns to prefer/avoid)"
   - If Prettier/ESLint/Black/Ruff configs already exist, skip — they handle this.

7. **Third-party services / integrations.**
   - Open-ended: "Which external services will this connect to? (auth provider, payment processor, LLM provider, email, analytics, etc.)"
   - Drives both the planning.md integrations section and skill selection (e.g., `cost-aware-llm-pipeline` if LLM is in the mix).

## Tier 3 — Only if PRD is unusually thin

Only escalate to these when the PRD genuinely lacks critical info. Better to have the user revise the PRD than try to extract everything via interview.

8. **Primary user / persona** — if the PRD doesn't say who it's for.
9. **Success criteria** — if the PRD doesn't define "done".
10. **Out-of-scope** — if the PRD doesn't have an explicit non-goals section.

If 2+ of these come up missing, that's a signal the PRD itself needs more work. Tell the user: "The PRD is missing [things]. I can fill in placeholders, but you'll get much better generated content if you spend 10 minutes adding those sections to PRD.md and re-running me."

## How to format the interview

Lead with one sentence framing why you're asking ("A few quick questions before I generate — these answers go into CLAUDE.md and shape the planning"). Then ask all questions in one message. Use whichever UI mechanism is available for the categorical ones; everything else as a numbered prose list.

After the user answers, do not ask follow-ups in another round unless something's truly ambiguous. The cost of one more round of "wait, also..." is high. Better to make a reasonable inference, mark it as an assumption in `decisions.md`, and let the user correct it later.

## What NOT to ask

- Anything the PRD already answers (re-reading the PRD is free; re-asking the user is not).
- Anything the existing files answer (`git config user.name`, `package.json` author, etc.).
- "What's the project name?" — get this from the PRD title or first line.
- "What problem does this solve?" — that's literally what the PRD is for.
- Asking for opinions on architecture choices the user hasn't reached yet ("what database should you use?"). Generate the doc with a placeholder and note that this is an open decision in `decisions.md` if it's a full set.
