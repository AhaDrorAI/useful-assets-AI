# מחשב חדש ל-Claude Code ו-Codex

המדריך הזה נכתב לאנשים שלא מפתחים קוד ביום-יום. אם מעולם לא פתחת טרמינל, אם המילה "פקודה" נשמעת מאיימת, ואם אתה רוצה שמישהו יחזיק לך את היד עד שהמחשב מוכן לעבודה עם סוכן קוד - זה בדיוק המקום להתחיל.

המטרה היא לא להפוך אותך למפתח. המטרה היא להביא אותך למצב שבו אפשר להגיד ל-Claude Code או Codex:

> "יש לי רעיון ו-PRD. תעזור לי לפתוח פרויקט חדש, לחבר GitHub, ולבנות את התשתית בצורה מסודרת."

## איך המדריך הזה מתחבר למה שכבר קיים באתר

באתר כבר יש מדריכים טובים למי שכבר יודע לפתוח טרמינל ולהריץ פקודות:

- מדריך Claude Code המלא: https://drorlounchpad.netlify.app/toolbox/guides/claude-code-getting-started
- מאגר ריפואים וכלים: https://drorlounchpad.netlify.app/toolbox/github-repos

העמוד הזה בא לפני שניהם. הוא מיועד לרגע שבו המשתמש עדיין לא יודע:

- מה זה טרמינל.
- איך פותחים אותו.
- מה זה אומר "להריץ פקודה".
- מה בטוח להריץ ומה דורש זהירות.
- איזה כלים חייבים להתקין לפני שאפשר בכלל להשתמש ב-Claude Code, Codex או במדריכים מתקדמים.

אחרי שהעמוד הזה מסתיים, המשתמש יכול לעבור למדריך Claude Code הקיים באתר.

## מה מתקינים כאן

נכין את המחשב בחמש תחנות פשוטות:

1. עורך קוד - המקום שבו רואים את קבצי הפרויקט.
2. טרמינל - חלון טקסט שבו מריצים פקודות.
3. Git ו-GitHub - הדרך לשמור גרסאות ולחבר את הפרויקט לריפו.
4. Node ו-Bun - כלים שמריצים פרויקטים מודרניים.
5. Claude Code ו-Codex - סוכני הקוד שיעזרו לבנות.

בסוף נוסיף כלים לפרויקטים נפוצים: Supabase, Netlify ו-Playwright.

## לפני שמתחילים

צריך:

- מחשב Windows או Mac.
- חשבון GitHub: https://github.com
- חשבון Claude מתאים ל-Claude Code.
- חשבון ChatGPT אם תרצה להשתמש ב-Codex דרך חשבון ChatGPT.
- חיבור אינטרנט יציב.
- 45-90 דקות שקטות.

אל תנסה להבין את כל עולם הפיתוח עכשיו. אנחנו רק מכינים את השולחן לעבודה.

## מה זה טרמינל

טרמינל הוא חלון שבו מדברים עם המחשב בעזרת טקסט במקום כפתורים.

במקום ללחוץ על כפתור "התקן", לפעמים כותבים פקודה כמו:

```bash
node --version
```

ואז לוחצים Enter.

המחשב מחזיר תשובה, למשל:

```bash
v24.15.0
```

זה אומר: Node מותקן, וזו הגרסה שלו.

### האם פקודות מסוכנות?

רוב הפקודות במדריך הזה רק בודקות גרסה, מתקינות כלי, או פותחות התחברות. אבל יש פקודות שכן יכולות למחוק קבצים או לשנות הרשאות.

במדריך הזה לא נריץ פקודות מחיקה. אם סוכן AI מציע פקודה עם מילים כמו `delete`, `remove`, `rm`, `reset`, `force`, עצור ושאל למה.

## איך פותחים טרמינל

### Windows

1. לחץ על כפתור Start.
2. כתוב `PowerShell`.
3. פתח את Windows PowerShell או Terminal.
4. ייפתח חלון עם שורה שמתחילה בערך כך:

```powershell
PS C:\Users\YourName>
```

זה המקום שבו מדביקים פקודות.

לא צריך לפתוח "Run as Administrator" אלא אם מדריך רשמי מבקש זאת במפורש.

### Mac

1. לחץ Command + Space.
2. כתוב `Terminal`.
3. לחץ Enter.
4. ייפתח חלון עם שורה שמסתיימת בערך כך:

```bash
yourname@MacBook ~ %
```

זה המקום שבו מדביקים פקודות.

מקור עזר: Apple מסבירה ש-Terminal הוא כלי לביצוע משימות דרך command line interface.

## איך מריצים פקודה

1. מעתיקים את הפקודה מהמדריך.
2. מדביקים בטרמינל.
3. לוחצים Enter.
4. מחכים לסיום.
5. קוראים את ההודעה האחרונה.

אם מופיע prompt ששואל שאלה, כמו `Do you want to continue?`, קוראים לפני שלוחצים.

אם מבקשים סיסמה, ייתכן שלא תראה תווים בזמן ההקלדה. זה תקין. הקלד את הסיסמה ולחץ Enter.

## מילון קטן

| מילה | פירוש פשוט |
|---|---|
| Terminal | חלון טקסט שבו מריצים פקודות |
| Command / פקודה | שורה שמבקשת מהמחשב לעשות משהו |
| Install | להתקין כלי חדש |
| Version | מספר הגרסה של כלי מותקן |
| Login / Auth | התחברות לחשבון |
| Git | מערכת ששומרת היסטוריה של שינויים בקבצים |
| GitHub | אתר שבו שומרים ריפואים ומשתפים קוד |
| Repo | תיקיית פרויקט ששמורה ב-GitHub |
| CLI | כלי שעובד דרך הטרמינל |
| Runtime | כלי שמריץ פרויקטים, למשל Node או Bun |

## שלב 1: התקן עורך קוד

עורך קוד הוא המקום שבו תראה את קבצי הפרויקט. גם אם הסוכן כותב עבורך את רוב הקוד, אתה צריך מקום לפתוח את התיקייה, לראות קבצים, ולפעמים להעתיק משהו.

בחר אחד:

- VS Code: https://code.visualstudio.com/download
- Cursor: https://cursor.com/download

למתחילים אני ממליץ להתחיל עם VS Code אם אין לך העדפה. Cursor טוב מאוד, אבל הוא עוד שכבת AI מעל עורך הקוד. כרגע אנחנו רוצים בסיס פשוט.

מה לעשות:

1. פתח את הקישור.
2. הורד את הגרסה שמתאימה ל-Windows או Mac.
3. התקן כמו כל תוכנה רגילה.
4. פתח את התוכנה פעם אחת כדי לוודא שהיא עובדת.

## שלב 2: התקן Git

Git שומר את ההיסטוריה של הפרויקט. זה מה שמאפשר לחזור אחורה, לפתוח branch, וליצור pull request.

קישור הורדה:

https://git-scm.com/downloads

### Windows

1. לחץ על Windows.
2. הורד את Git for Windows.
3. פתח את קובץ ההתקנה.
4. אפשר להשאיר את רוב ברירות המחדל.
5. אם נשאלת על editor, בחר VS Code אם הוא מופיע.

### Mac

אפשר להתקין דרך האתר הרשמי או דרך כלי מערכת. אם אתה לא בטוח, התחל מהאתר:

https://git-scm.com/downloads

### בדיקה

פתח טרמינל חדש והרץ:

```bash
git --version
```

אם הכל תקין תראה משהו כמו:

```bash
git version 2.53.0
```

לא חשוב שהמספר יהיה זהה. חשוב שלא תהיה הודעת שגיאה.

## שלב 3: התקן GitHub CLI

GitHub CLI הוא כלי שמאפשר לדבר עם GitHub מתוך הטרמינל. הוא יעזור בהמשך ליצור ריפו, לבדוק התחברות, לפתוח PR ולחבר פרויקט.

קישור רשמי:

https://cli.github.com/

מה לעשות:

1. פתח את הקישור.
2. הורד את הגרסה ל-Windows או Mac.
3. התקן.
4. פתח טרמינל חדש.

בדיקה:

```bash
gh --version
```

התחברות:

```bash
gh auth login
```

מה לבחור בדרך כלל:

- GitHub.com
- HTTPS
- Login with a web browser

בסוף בדוק:

```bash
gh auth status
```

אם כתוב שאתה מחובר ל-GitHub, התחנה הזו הסתיימה.

## שלב 4: התקן Node.js

Node הוא כלי שמריץ הרבה פרויקטים מודרניים של אתרים ואפליקציות. גם Codex מותקן דרך Node/npm בדרך הנפוצה ביותר.

קישור רשמי:

https://nodejs.org/en/download

מה לעשות:

1. פתח את הקישור.
2. בחר גרסת LTS.
3. הורד Installer ל-Windows או Mac.
4. התקן עם ברירות המחדל.
5. סגור ופתח טרמינל חדש.

בדיקה:

```bash
node --version
npm --version
```

מה זה `npm`? זה כלי שמגיע עם Node ועוזר להתקין חבילות. כרגע לא צריך להבין מעבר לזה.

## שלב 5: התקן Claude Code

Claude Code הוא סוכן קוד שעובד מהמחשב שלך ויכול לקרוא, לערוך ולהריץ את הפרויקט המקומי.

דוקומנטציה רשמית:

https://code.claude.com/docs/en/setup

### Windows PowerShell

הדבק ב-PowerShell:

```powershell
irm https://claude.ai/install.ps1 | iex
```

### Mac

הדבק ב-Terminal:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### בדיקה

סגור ופתח טרמינל חדש, ואז הרץ:

```bash
claude --version
```

אחר כך:

```bash
claude doctor
```

`doctor` היא בדיקת בריאות. היא מנסה לזהות בעיות התקנה נפוצות.

### התחברות

הרץ:

```bash
claude
```

עקוב אחרי ההוראות במסך. בדרך כלל ייפתח דפדפן ותתבקש להתחבר לחשבון Claude.

אם אתה רואה `command not found`, סגור ופתח טרמינל חדש. אם זה עדיין קורה, חזור לדוקומנטציה הרשמית או בקש מסוכן AI להסביר את התקלה בלי להריץ פקודות נוספות.

## שלב 6: התקן Codex CLI

Codex CLI הוא סוכן הקוד של OpenAI שעובד דרך הטרמינל.

מקור רשמי:

https://github.com/openai/codex

הרץ:

```bash
npm install -g @openai/codex
```

בדיקה:

```bash
codex
```

אם נפתח מסך של Codex או תהליך התחברות, זה עובד.

## שלב 7: התקן Bun

Bun הוא כלי מהיר להרצת פרויקטים חדשים ולהתקנת חבילות. אתה לא חייב להבין אותו עכשיו. חשוב רק לדעת שהוא יכול להיות שימושי בפרויקטים חדשים.

דוקומנטציה רשמית:

https://bun.sh/docs/installation

### Windows PowerShell

```powershell
powershell -c "irm bun.sh/install.ps1|iex"
```

### Mac

```bash
curl -fsSL https://bun.com/install | bash
```

בדיקה:

```bash
bun --version
```

כלל פשוט:

- בפרויקט חדש אפשר להשתמש ב-Bun.
- בפרויקט קיים לא מחליפים כלי התקנה בלי לשאול את הסוכן לבדוק מה כבר קיים.

## שלב 8: התקן uv

`uv` הוא כלי שעוזר להריץ כלי Python בצורה נקייה. לא כל פרויקט צריך אותו ביום הראשון, אבל הוא שימושי מאוד בעולם סוכני הקוד.

דוקומנטציה רשמית:

https://docs.astral.sh/uv/getting-started/installation/

### Windows PowerShell

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Mac

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

בדיקה:

```bash
uv --version
```

## שלב 9: כלים לפי סוג פרויקט

לא חייבים להתקין את הכל עכשיו. התקן רק אם זה רלוונטי לפרויקטים שלך.

### Supabase

Supabase משמש ל-Database, משתמשים, התחברות, Storage ועוד.

דוקומנטציה:

https://supabase.com/docs/guides/local-development/cli/getting-started

בדיקה בלי התקנה קבועה:

```bash
npx supabase --help
```

בפרויקט שמשתמש ב-Bun:

```bash
bunx supabase --help
```

חשוב: אל תכניס `service_role` key לצ'אט או לכלי AI. זה מפתח חזק מדי.

### Netlify

Netlify משמש לפרסום אתרים.

דוקומנטציה:

https://docs.netlify.com/api-and-cli-guides/cli-guides/get-started-with-cli/

התקנה:

```bash
npm install -g netlify-cli
```

התחברות:

```bash
netlify login
```

בדיקה:

```bash
netlify --version
```

### Playwright

Playwright מאפשר לבדוק אתר בדפדפן אמיתי. זה שימושי כשסוכן בונה UI וצריך לוודא שהכפתורים באמת עובדים.

דוקומנטציה:

https://playwright.dev/docs/intro

מתקינים בתוך פרויקט, לא סתם על המחשב:

```bash
npm init playwright@latest
```

## בדיקת סיום

פתח טרמינל חדש והריץ את הפקודות האלו אחת-אחת:

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
```

אם פקודה אחת נכשלת, אל תמשיך להתקין עוד כלים. עצור ופתור את הבעיה.

## מה אומרים לסוכן אחרי ההתקנה

אחרי ש-Claude Code או Codex עובדים, אפשר לתת להם את ההודעה הזו:

```text
I am setting up this computer for AI coding work.

Please help me verify the setup slowly and safely.

I am not a developer, so explain every step in plain language.

Do not install anything before showing me:
1. What you are checking
2. Why it matters
3. The exact command
4. What a successful result should look like
5. What could go wrong

Check these tools:
- Git
- GitHub CLI
- Node and npm
- Bun
- uv
- Claude Code
- Codex CLI
- Netlify CLI if installed
- Supabase CLI if installed

After each check, wait for the result before moving to the next step.
```

## מה לא לעשות ביום הראשון

אל תתקין עדיין:

- הרבה MCP servers.
- מערכות memory מורכבות.
- כלים שמבקשים הרבה הרשאות.
- אוטומציות שמריצות קוד בלי אישור.
- כלי אבטחה/בדיקות מתקדמים לפני שיש פרויקט ראשון.

השלב הבא הוא לא עוד התקנות. השלב הבא הוא workflow לפתיחת פרויקט חדש מתוך PRD/SPEC.

## אם נתקעים

העתק לסוכן:

```text
I am stuck during setup.

Here is the command I ran:
[paste command]

Here is the full output:
[paste output]

Please explain:
1. What probably happened
2. Whether this is dangerous
3. The smallest safe next step
4. What not to do

Do not suggest deleting files or changing permissions unless you explain why.
```

## קישורים רשמיים

- VS Code: https://code.visualstudio.com/download
- Cursor: https://cursor.com/download
- Git: https://git-scm.com/downloads
- GitHub CLI: https://cli.github.com/
- Node.js: https://nodejs.org/en/download
- Claude Code setup: https://code.claude.com/docs/en/setup
- Codex CLI: https://github.com/openai/codex
- Bun: https://bun.sh/docs/installation
- uv: https://docs.astral.sh/uv/getting-started/installation/
- Supabase CLI: https://supabase.com/docs/guides/local-development/cli/getting-started
- Netlify CLI: https://docs.netlify.com/api-and-cli-guides/cli-guides/get-started-with-cli/
- Playwright: https://playwright.dev/docs/intro
