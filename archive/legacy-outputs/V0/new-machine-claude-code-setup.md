# מחשב חדש לעבודה עם Claude Code ו-Codex

המדריך הזה מיועד ליזם לא טכני שרוצה להקים מחשב חדש לעבודה עם סוכני קוד בלי להרגיש שהוא נכנס למרתף חשוך של התקנות. המטרה היא להגיע למצב פשוט: אפשר לפתוח טרמינל, להתחבר ל-GitHub, להריץ Claude Code או Codex, ליצור ריפו חדש, ולבנות פרויקט מתוך PRD/SPEC בלי להתחיל כל פעם מאפס.

## העיקרון

לא מתקינים את כל עולם ה-AI ביום אחד. מתקינים שכבות:

| שכבה | מטרה | חובה עכשיו? |
|---|---|---|
| בסיס | Git, GitHub CLI, עורך קוד, טרמינל | כן |
| Runtime | Node LTS, Bun, Python, uv | כן |
| Agents | Claude Code, Codex CLI | כן |
| Project tools | Supabase, Netlify, Playwright | לפי סוג הפרויקט |
| Workflow | CLAUDE.md, AGENTS.md, templates, checklists | כן, אבל קטן |
| מתקדם | CodeGraph, promptfoo, React Doctor, security skills | לא ביום הראשון |

המדד להצלחה: בסוף ההתקנה אפשר להריץ פקודות בדיקה, לפתוח פרויקט חדש, ולתת לסוכן לעבוד לפי תהליך מסודר.

## למה זה לא Skill

שלב "מחשב חדש" קורה לפני שיש לכם סביבת Claude Code או Codex יציבה, ולכן הוא לא צריך להיות Skill. אי אפשר להסתמך על Skill כדי להתקין את הכלי שמריץ Skills.

בשלב הזה משתמשים בשלושה דברים פשוטים:

- עמוד אתר שמסביר מה מתקינים ולמה.
- מדריך Markdown שאפשר לפתוח גם בלי סוכן.
- Prompt להעתקה לתוך Claude Code או Codex אחרי שהכלי כבר מותקן.

ה-Skill הראשון יגיע בשלב הבא: פתיחת פרויקט חדש מ-PRD/SPEC עד ריפו עובד.

## שלב 0: כלל בטיחות

לפני שמריצים פקודות שמורידות סקריפט מהאינטרנט:

- העדיפו דוקומנטציה רשמית.
- אל תדביקו API keys בצ'אט או בקובץ ציבורי.
- אל תפעילו `service_role` של Supabase בתוך כלי AI.
- אל תתנו לסוכן להריץ מחיקות או שינויי הרשאות בלי להבין למה.

## שלב 1: Git ו-GitHub

התקינו:

- Git
- GitHub CLI (`gh`)

בדיקת הצלחה:

```bash
git --version
gh --version
gh auth login
gh auth status
```

למה זה חשוב: הסוכן צריך לדעת ליצור branch, commit, PR, ולחבר פרויקט לריפו בלי שתעברו ידנית בין עשרה מסכים.

## שלב 2: Node LTS ו-Bun

התקינו Node.js LTS. נכון ל-17 במאי 2026, אתר Node מציג את v24.15.0 כגרסת LTS עדכנית.

בדיקה:

```bash
node --version
npm --version
```

התקינו גם Bun. Bun הוא runtime ו-package manager מהיר, ומתאים במיוחד לפרויקטים חדשים שבהם אין עדיין החלטה קיימת.

macOS / Linux:

```bash
curl -fsSL https://bun.com/install | bash
```

Windows PowerShell:

```powershell
powershell -c "irm bun.sh/install.ps1|iex"
```

בדיקה:

```bash
bun --version
```

כלל שימוש פשוט:

- פרויקט חדש: Bun הוא בחירה טובה.
- פרויקט קיים עם `package-lock.json`: התחילו עם npm.
- פרויקט קיים עם `pnpm-lock.yaml`: התחילו עם pnpm.
- אל תחליפו package manager באמצע פרויקט בלי לבקש מהסוכן לבדוק lockfiles, scripts ו-CI.

## שלב 3: Python ו-uv

גם אם הפרויקט שלכם הוא אתר, הרבה כלי AI, סקריפטים וניתוחים משתמשים ב-Python. התקינו את `uv` לניהול מהיר ונקי של Python tools.

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

בדיקה:

```bash
uv --version
```

## שלב 4: Claude Code

התקינו Claude Code מהדוקומנטציה הרשמית.

macOS / Linux / WSL:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://claude.ai/install.ps1 | iex
```

בדיקה:

```bash
claude --version
claude doctor
```

התחברות:

```bash
claude
```

אם אתם על Windows: מומלץ להתקין Git for Windows כדי ש-Claude Code יוכל להשתמש ב-Git Bash כאשר צריך.

## שלב 5: Codex CLI

התקינו Codex CLI כדי שתהיה לכם גם דרך עבודה עם סוכן הקוד של OpenAI.

```bash
npm install -g @openai/codex
```

או ב-macOS עם Homebrew:

```bash
brew install --cask codex
```

בדיקה:

```bash
codex
```

העדיפו התחברות עם חשבון ChatGPT כאשר זה מתאים לתוכנית שלכם. API key מתאים יותר למערכות אוטומטיות, לא להתחלה רגועה.

## שלב 6: כלי פרויקט

### Supabase

לפרויקטים עם Database/Auth/Storage:

```bash
npx supabase --help
```

או בפרויקט Bun:

```bash
bunx supabase --help
```

חשוב: לפי דוקומנטציית Supabase, התקנה גלובלית עם `npm install -g supabase` אינה נתמכת. לשימוש קבוע בפרויקט:

```bash
npm install supabase --save-dev
```

### Netlify

לאתרים ופרויקטים שמפורסמים ב-Netlify:

```bash
npm install -g netlify-cli
netlify login
```

בדיקות שימושיות:

```bash
netlify --version
netlify status
```

### Playwright

לבדיקות UI אמיתיות בדפדפן:

```bash
npm init playwright@latest
```

או:

```bash
pnpm create playwright
```

בפרויקט Bun אפשר להשתמש ב-Playwright, אבל אם ההתקנה שואלת שאלות או נתקעת, התחילו עם נתיב npm הרשמי ואז התאימו.

## שלב 7: שכבת Workflow

צרו תיקיית templates אישית, למשל:

```bash
mkdir -p ~/ai-workflows/templates
```

שמרו בה:

- `CLAUDE.md` בסיסי לפרויקטים.
- `AGENTS.md` בסיסי ל-Codex.
- תבנית PRD.
- תבנית SPEC.
- checklist לפתיחת פרויקט חדש.
- checklist ל-"אני תקוע".

הכלל: הסוכן לא אמור לנחש איך אתם עובדים. הוא אמור לקרוא קובץ קצר וברור.

## CLAUDE.md / AGENTS.md בסיסי

אפשר להתחיל מזה:

```markdown
# Project Operating Rules

You are my coding partner.

Before writing code:
- Understand the goal.
- Ask for missing product decisions.
- Create or update a short plan.
- Identify the smallest working slice.

When editing:
- Keep changes scoped.
- Do not rewrite unrelated files.
- Prefer existing patterns.
- Explain risky changes before making them.

Before completion:
- Run relevant checks.
- Summarize what changed.
- List what still needs attention.
```

## בדיקת בריאות מלאה

הריצו:

```bash
git --version
gh auth status
node --version
npm --version
bun --version
uv --version
claude --version
claude doctor
codex
netlify --version
```

אם משהו נכשל, לא ממשיכים להתקנות מתקדמות. פותרים קודם את השכבה שנכשלה.

## מה לא להתקין ביום הראשון

אל תתחילו עם:

- עשרה MCP servers.
- זיכרון מתמשך מורכב.
- Orchestration של צוות agents.
- Auto-accept מלא לכל פעולה.
- החלפה גורפת של package manager בפרויקטים קיימים.

אלו כלים טובים, אבל רק אחרי שהבסיס יציב.

## Bootstrap Prompt לסוכן: מחשב חדש

העתיקו לסוכן:

```text
I am setting up a new computer for Claude Code and Codex work.

Goal:
- Prepare a reliable local environment for building projects from PRD/SPEC.
- Connect GitHub.
- Install only the tools needed for a safe first workflow.

Please:
1. Detect my OS and shell.
2. Check whether Git, gh, Node, npm, Bun, uv, Claude Code, Codex, Netlify CLI, and Supabase CLI are installed.
3. Do not install anything yet. First show me a table of missing tools, why each matters, install command, and verification command.
4. Mark risky commands clearly.
5. After I approve, install one layer at a time and verify each layer before continuing.
```

## מקורות רשמיים

- Claude Code setup: https://code.claude.com/docs/en/setup
- Codex CLI: https://github.com/openai/codex
- Node.js downloads: https://nodejs.org/en/download
- Bun installation: https://bun.sh/docs/installation
- uv installation: https://docs.astral.sh/uv/getting-started/installation/
- GitHub CLI: https://cli.github.com/
- Supabase CLI: https://supabase.com/docs/guides/local-development/cli/getting-started
- Netlify CLI: https://docs.netlify.com/api-and-cli-guides/cli-guides/get-started-with-cli/
- Playwright: https://playwright.dev/docs/intro
