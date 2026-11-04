# Attack surface checklist

Fill one row per entry point. "Who can call it" is the question that matters.

| Entry point | Where to look | Who can call it | Key used | Auth? | Ownership check? | Input validated? | Rate limited? |
|---|---|---|---|---|---|---|---|

## Where entry points hide
- **Database API**: every table/view/function in an exposed schema (`public`) is reachable at `/rest/v1/<name>` and `/rest/v1/rpc/<fn>` with the public anon key, and listed in `/graphql/v1`. The browser is not the only client: assume an attacker uses curl with your anon key.
- **Auth endpoints**: `/auth/v1/signup` accepts arbitrary `data` (becomes `raw_user_meta_data`). OAuth callbacks that read `?role=` or `?intended_role=` from the URL.
- **Next.js**: `src/app/api/**/route.ts`, Server Actions (`'use server'`), `middleware.ts`, route handlers that proxy to other services.
- **Serverless**: `netlify/functions/*` are deployed by default even if "kept for automation"; `supabase/functions/*`; Vercel `api/`.
- **Webhooks / bots**: Telegram, Stripe, GitHub, WhatsApp, form handlers. Public URL, guessable path.
- **Cron endpoints**: `/api/cron/*`. Must require a secret and fail closed.
- **Storage**: buckets (public?), upload policies, size/MIME limits, signed URL lifetime.
- **Static files**: anything in `public/` or the deploy folder is downloadable (`config.json`, `.env`, source maps, backups).
- **Admin tools**: local HTML panels, scripts with service keys, seed scripts with default passwords.
- **Third-party keys in the bundle**: anything `NEXT_PUBLIC_*` / `VITE_*` is public. Fine for publishable keys (anon, analytics), never for secret keys.
- **AI features**: endpoints that call paid LLM APIs (cost abuse), prompts built from user input (prompt injection into tools with write access).
