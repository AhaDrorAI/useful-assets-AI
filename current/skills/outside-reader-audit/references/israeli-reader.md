# Israeli reader module — outside-reader-audit

Load this file **in addition to** SKILL.md when the text is aimed at an Israeli professional reader. That includes Hebrew text, and it also includes English text sent to someone in Israel.

The Core Rule does not change: read only the supplied text. The Output Format does not change, it only gains two sections. What changes is **the model of the reader in your head**.

## Why this module exists, and what it is not

`avoid-ai-writing` audits how a text sounds. This skill audits what it lands as. Landing is audience dependent, and the default audience in SKILL.md is "an intelligent general outsider", which in practice means an Anglo-American professional reader.

An Israeli professional reader is a different instrument. Same text, different verdict.

**Honesty about sourcing.** The directness norm below is documented (Cultural Atlas, "dugriut"). Most of the rest is a working model of Israeli professional reading, assembled from observation, not from a study. Treat it as a checklist that earns its place by catching real problems, and correct it when it misfires. Do not present its judgments as research.

---

# The Israeli reader model

## 1. Directness is the trust signal

Documented norm: Israelis prefer explicit statements over hedged ones. `אני רוצה` beats `האם ייתכן שאפשר`. Applied to a text, three consequences:

- **Hedging reads as evasion, not politeness.** `ייתכן ש`, `נראה לי ש`, `אשמח אם`, `רציתי לבדוק אם במקרה` all cost trust.
- **A slow reveal fails.** If the reader cannot say what this text wants within two lines, it is already lost. Anglo writing earns the point; Israeli writing states it and then earns it.
- **Softeners around a request make the request look weak,** not respectful. Ask plainly.

Flag: any sentence whose only job is to cushion the next one.

## 2. Marketing register is a negative signal

This is the sharpest reversal from the default model. Language that reads as confident to an American reader reads as blowing smoke to an Israeli one.

Flag hard:

- `פורץ דרך`, `מהפכני`, `ייחודי`, `הפתרון המושלם`, `הזדמנות שלא חוזרת`
- `אני נלהב מ`, `יש לי תשוקה ל`, `אני אוהב אתגרים`
- Adjective stacks with no number behind them.
- Any sentence that would work equally well for a different person or product. Israeli readers test for interchangeability fast.

The Israeli substitute for enthusiasm is **specificity**. `בניתי מערכת שהגיעה ל-200 משתמשים` does the work that `אני נלהב מבניית מערכות` fails to do.

## 3. Over-explaining shared context is its own failure

The English skill flags text that leans on hidden context. In Hebrew the more common failure is the mirror image: explaining things the reader already knows. It reads as an English text that was translated inward, or as talking down.

Do not explain to an Israeli reader:

- מילואים, שנת שבתון, מכינה, תואר ראשון ושני
- What Weizmann, the Technion, Mamram or 8200 are
- The structure of the Israeli education system
- Well known Israeli companies

Flag: `X, שהוא מוסד מחקר מוביל בישראל`. The reader knows. The clause signals the text was not written for them.

## 4. Under-explaining internal shorthand

The opposite side, and it is where Hebrew text actually breaks.

Flag every internal abbreviation and role name that lives inside one organisation or one sector:

- Ministry and municipality acronyms
- Internal role titles (`רכז`, `מדריך`, `מנחה`) that mean different things in different sectors, and nothing in tech
- Program and project names with no gloss
- Sector jargon from education, defence or academia used in front of a commercial reader

Ask per item: does this word mean the same thing to a hiring manager in a tech company as it does to the writer? If not, it needs a translation into outcome language, not a definition.

## 5. The network question fires first

Israeli professional networks are dense and the reader's first move is to place you. A text that gives no anchor leaves them unable to.

Anchors that work: current employer, city, sector, a shared institution, a named person or project. One is usually enough.

Flag: text that describes what the writer does at length and never says where they sit.

## 6. Titles are discounted, results are not

Israeli readers know titles inflate in small organisations. A title alone carries less than it does in the US. What carries:

- Numbers: users, budget, headcount, years, growth
- A named system that other people used
- A specific problem and what happened to it

Flag: seniority claimed by title with no result attached.

## 7. Code switching is normal. Forced Hebrew is not

English technical terms inside Hebrew are correct Israeli professional register: `דיפלוי`, `פייפליין`, `סטייקהולדרים`, `בקאנד`, API, LLM. Translating them into Academy Hebrew (`צינור עיבוד`, `בעלי עניין`) makes a text read as machine translated or as written by an outsider.

Flag both directions:

- Hebrew equivalents forced onto terms nobody says in Hebrew.
- English used where a plain Hebrew word exists and is what people actually say. `לעשות אלייז'ן` is not a word.

Rule of thumb: would the writer say this word out loud in a meeting.

## 8. Length and patience

- **DM or WhatsApp:** short. Israeli readers reply to short. A long first message reads as a template regardless of content.
- **LinkedIn post:** length is tolerated if the first two lines pay.
- **Email:** the ask goes near the top, not after the background.
- Hebrew is denser than English. A paragraph translated from English is usually one third too long once it is in Hebrew.

Flag: background before the point.

## 9. The translated-CV tell

A Hebrew text that is visibly an English original in Hebrew clothing signals low effort, and the reader notices before they notice anything else.

Tells: English section headings kept in structure (`Professional Summary` rendered as `תקציר מקצועי` at the top of a Hebrew CV), American bullet grammar, `אני נלהב`, dates in US format, an objective statement.

## 10. Things the reader will notice and not say

Israeli professional readers are direct in the room and silent on the page. The audit should surface what they think and will not write back.

Common silent reactions:

- `למה הוא עוזב` — any text that hints at a transition invites this, and leaving it unaddressed is louder than addressing it.
- `מה הוא באמת עשה שם` — when a role is described in responsibilities rather than outcomes.
- `למי הוא מדבר` — when the text could have been sent to anyone.
- `זה AI` — and once that lands, nothing else in the text is read.

---

# Additions to the output format

Keep every section in SKILL.md. Add two, at the end, before `High-Level Fix`:

```markdown
**מה קורא ישראלי יחשוב ולא יכתוב**
- (the silent reactions from section 10, quoted as the reader would think them)

**רגיסטר וקוד סוויצ'ינג**
- Register verdict: too formal / right / too casual, and where
- Forced Hebrew on terms that live in English:
- English used where plain Hebrew is what people say:
```

Also state at the top of the audit which reader you assumed: sector, seniority, and whether they already know the writer.

---

# Israeli audience types

Extends the Audience list in SKILL.md.

| Text | Reader | The thing that kills it |
|---|---|---|
| פוסט לינקדאין בעברית | ציבור מקצועי ישראלי | שיווקיות, ופתיחה שלא משלמת |
| תגובה לפוסט | הכותב, ואחר כך הקהל שלו | תגובה שמדברת על עצמה במקום על הפוסט |
| DM לאיש קשר ישראלי | אדם עסוק שלא חייב לך כלום | אורך, ותבניתיות |
| מייל לגורם ממשלתי או מוסדי | פקיד שמחפש עובדות וזכאות | סיפור לפני העובדות |
| קורות חיים בעברית | מגייס ישראלי | תרגום מאנגלית, ותארים בלי תוצאות |
| הודעה לקולגה שעוזב לחו"ל או חוזר | חבר מקצועי | להתעלם מהפיל בחדר |

---

# What this module deliberately does not do

- It does not relax the Core Rule. Still read only the supplied text.
- It does not audit phrasing quality. That is `avoid-ai-writing` and its Hebrew module.
- It does not tell the writer to add slang or `דוגריות` as a style. Directness is a structural property (say the point first, drop the cushions), not a vocabulary.
- It does not model what an Israeli reader may look for and should not be given. Personal status signals belong to the writer's own rules, not to this audit.

---

# Sources and status

- Cultural Atlas, Israeli communication. Documented: dugriut, preference for explicit over hedged statements, expressive register.
- Everything else here is a working model, not research. Sections 3, 5, 6, 7, 9 and 10 are the ones most likely to need correction with use. Log corrections into this file rather than working around them.
