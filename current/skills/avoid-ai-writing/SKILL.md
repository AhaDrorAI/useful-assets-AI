---
name: avoid-ai-writing
description: Audit and rewrite content to remove AI writing patterns ("AI-isms"). Use this skill when asked to "remove AI-isms," "clean up AI writing," "edit writing for AI patterns," "audit writing for AI tells," or "make this sound less like AI." Supports a detection-only mode that flags patterns without rewriting. Works on Hebrew text as well; loads references/hebrew.md for Hebrew-specific patterns.
version: 3.7.0
license: MIT
compatibility: Any AI coding assistant that supports the agentskills.io SKILL.md format (Claude Code, Codex CLI, Grok Build, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Conor Bronsdon
  fork_maintainer: Dror Moshe Aharoni
  fork_changes: "Added rules for overgeneralized 'Most people...' openers, adverb crutches, fake profundity, and the 'after careful consideration' / 'here's the thing' stalls. 3.5.0 adds the post-em-dash tells (paired fragments, two-image contrasts, self-applause tags, X-of-Y analogies, hedged numeric ranges), a generation-time prevention section built on ASD-STE100 and Zinsser's fourth principle, and guidance on keeping a project-local forbidden-patterns file. 3.7.0 splits the file: the vocabulary tiers, the long-tail pattern catalogue, the STE grammar rules, the generation-time controls and the context profiles moved into references/ and load on demand, leaving the highest-signal checks inline. No rule was changed or dropped. 3.6.0 absorbs the transferable grammar rules from Simplified Technical English (nominalisations, actorless passive, tense bloat, empty-subject openers, noun stacks), adds 22 controlled-language substitutions across Tiers 1 and 2, and states explicitly which STE rules to reject because they flatten voice."
  additional_sources: "Post-em-dash pattern list and the Simplified Technical English rules adapted from Ruben Hassid's nine tells and his /ste skill (ste.rubenhassid.ai). ASD-STE100 is an ASD specification; the rules here are paraphrased from public secondary sources and are not a compliance claim."
  tags: writing editing voice quality
  agentskills_spec: "1.0"
  openclaw:
    emoji: "\u270D\uFE0F"
---

# Avoid AI Writing — Audit & Rewrite

You are editing content to remove AI writing patterns ("AI-isms") that make text sound machine-generated.

## The tells move

Every tell on this list eventually gets trained out, and then the *absence* of it becomes the tell. The em dash is the worked example: it was the single most reliable signal, everyone learned it, models stopped producing it, and now a piece with no em dashes and flawless parallel structure reads as machine-written to anyone paying attention.

Two consequences for how you audit:

- **Sentence shape outranks vocabulary.** A writer who scrubs every word on the Tier 1 list but keeps the two-beat rhythm and the symmetrical constructions has not fixed anything. The patterns under "Post-em-dash tells" and "Rhythm and uniformity" are where the signal lives now.
- **Perfect structure is itself suspicious.** Don't drive a piece toward uniform polish. Over-editing pushes human writing *into* the AI profile, which is why "Over-polishing" is a flagged pattern rather than a goal.

## Modes

This skill operates in one of two modes:

**`rewrite`** (default) — Flag AI-isms and rewrite the text to fix them.

**`detect`** — Flag AI-isms only. No rewriting. Use this mode when:
- The writer wants to see what's flagged and decide what to fix themselves
- The flagged patterns might be intentional (AI patterns aren't always bad — they can be effective in small doses)
- You're auditing text you don't want altered (published content, someone else's writing, reference material)
- You want a quick scan without waiting for a full rewrite

Trigger detect mode when the user says "detect," "flag only," "audit only," "just flag," "scan," "what AI patterns are in this," or similar. Default to rewrite mode if not specified.

---

In **rewrite** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Rewrite it**: return a clean version with all AI-isms removed
3. **Show a diff summary**: briefly list what you changed and why

In **detect** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Assess it**: note which flags are clear problems vs. patterns that may be intentional or effective in context

---

## Language routing

The pattern tables in this file are English. They do not fire on Hebrew.

**If the audited text is in Hebrew, read `references/hebrew.md` before auditing.** That file
carries the Hebrew pattern tables in two layers: English AI-isms as they land in Hebrew
(calques), and failures that exist only in Hebrew (register inflation, gender defaults,
translated syntax, RTL typography). Method, modes, severity tiers and output format stay
governed by this file.

Mixed Hebrew and English text: audit each language with its own tables.

Other languages: say so instead of auditing. Running the English tables on a language they
were not written for produces a clean bill of health that means nothing.

---

---

## How to run an audit

The checks in this file are the fast pass: the highest-signal tells, the ones the
"tells move" section says the signal has moved to. They need no extra reads.

**For anything beyond a quick scan, load the reference files below.** They hold the full
rule set. Auditing a text against the fast pass alone and reporting it clean is a false
pass, and a false pass is worse than no audit.

| Load | When |
|---|---|
| `references/vocabulary.md` | Every rewrite, and any detect pass that reports on word choice. Tier 1, 2 and 3 tables. |
| `references/patterns.md` | Every rewrite. The named pattern catalogue: template phrases, transitions, chatbot artifacts, novelty inflation, emotional flatline, and the rest. |
| `references/ste.md` | Text with nominalisations, actorless passive, tense bloat or noun stacks. Also the four STE rules this skill deliberately rejects. |
| `references/profiles.md` | Whenever the context is not plain long-form prose: LinkedIn, technical blog, investor email, docs, casual. Holds the tolerance matrix and the auto-detection cues. |
| `references/generation.md` | The user is about to WRITE, not edit. Prevention controls, not cures. |
| `references/hebrew.md` | The text is Hebrew. See Language routing above. |

Minimum for a full rewrite: this file plus `vocabulary.md` and `patterns.md`.

---

## The fast pass

These are the checks that need no extra reads. Everything else is in `references/`.

### Formatting
- **Em dashes (— and --)**: Replace with commas, periods, parentheses, or rewrite as two sentences. Target: zero. Hard max: one per 1,000 words. This applies to headings and section titles too, not just body prose. Catch both the Unicode em dash (—) and the double-hyphen substitute (--).
- **Bold overuse**: Strip bold from most phrases. One bolded phrase per major section at most, or none. If something's important enough to bold, restructure the sentence to lead with it instead.
- **Emoji in headers**: Remove entirely. No `## 🚀 What This Means`. Exception: social posts may use one or two emoji sparingly — at the end of a line, never mid-sentence.
- **Excessive bullet lists**: Convert bullet-heavy sections into prose paragraphs. Bullets only for genuinely list-like content (feature comparisons, step-by-step instructions, API parameters).

### Sentence structure
- **"It's not X — it's Y" / "This isn't about X, it's about Y"**: Rewrite as a direct positive statement. Max one per piece, and only if it serves the argument. Now that em dashes are rarer, this pattern usually arrives as two sentences: "That's not compliance. That's stalling." Same construction, same fix, and the fix is mechanical: keep the second half, drop the first. "They're stalling." The negated half almost never carries information; it exists to give the real claim a run-up.
- **Hollow intensifiers**: Cut `genuine`, `real` (as in "a real improvement"), `truly`, `quite frankly`, `to be honest`, `let's be clear`, `it's worth noting that`. Just state the fact.
- **Vague endorsement ("worth [verb]ing")**: Cut or replace `worth reading`, `worth paying attention to`, `worth a look`, `worth exploring`, `worth checking out`, `worth your time`. These substitute a generic thumbs-up for a specific reason. Say *why* something matters instead.
- **Hedging**: Cut `perhaps`, `could potentially`, `it's important to note that`, `to be clear`. Make the point directly.
- **Missing bridge sentences**: Each paragraph should connect to the last. If paragraphs could be rearranged without the reader noticing, add connective tissue.
- **Compulsive rule of three**: Vary groupings. Use two items, four items, or a full sentence instead of triads. Max one "adjective, adjective, and adjective" pattern per piece.

### Post-em-dash tells

These five survive the em-dash purge because they are shapes, not characters. A piece can pass a find-and-replace sweep and still trip every one.

**Paired fragments.** Two clipped phrases set side by side for emphasis: "Fast. Simple." "No fluff. Just answers." "Built for scale. Priced for startups." The rhythm is the tell. A human writing quickly produces one fragment, not a matched pair.
- The fix: keep one, or write the full sentence. "It's fast" beats "Fast. Simple."
- This does **not** contradict the advice to use fragments. A single fragment breaks rhythm, which is the point. A *pair* restores symmetry, which is the problem. Flag the pairing, not the fragment.

**Two-image contrast with no instruction.** "Less a hammer, more a scalpel." "Not a map, a compass." "Think less library, more workshop." The reader now holds two pictures and no idea what to do.
- The fix: say the action. "Use it on one function at a time" instead of "less hammer, more scalpel."
- Related to fake profundity, but the tell here is the missing instruction rather than the reach for depth.

**Self-applause tags.** A sentence that stops to tell the reader the preceding sentence landed: "And that matters." "That's the part everyone misses." "Which is exactly the point." "And that changes everything."
- These are always deletable. Cut the tag and the paragraph loses nothing, which is the test: if deleting a sentence costs no information, it was applause.
- Distinct from significance inflation, which inflates the *event*. This inflates the writer's own last line.

**X-of-Y shorthand.** "It's the Excel of AI agents." "The Stripe for logistics." "Basically Git for designers."
- The construction only works when the reader knows both halves well enough to compute the ratio, and usually they know one. Replace with what the thing does: "It runs scheduled jobs and shows the results in a grid."
- Allow it only when the left-hand term is genuinely universal in the audience's world, and never more than once per piece.

**Hedged numeric ranges.** "Takes 5 to 10 minutes." "Expect 20-30% savings." "Somewhere between 3 and 7 steps."
- A range on a number the writer could have measured means the writer never measured it. Give the number you actually got: "Took 7 minutes." If the value genuinely varies, say what it depends on: "About 7 minutes, longer if the repo has more than 500 files."
- Distinct from **False ranges** below, which is about sweeping *topic* pairs ("from the Big Bang to dark matter"). This one is about numeric estimates standing in for measurement.

### Rhythm and uniformity

These aren't individual word or phrase problems — they're patterns in how the text flows as a whole. AI text is metronomic; human text has varied rhythm.

**Structure is the #1 detection signal.** AI detection tools (including Pangram, which trains a classifier on 28M human documents) weight structural regularity higher than vocabulary. Consistent sentence construction, uniform pacing, and symmetrical phrasing patterns are harder to mask than swapping out a few flagged words. If you fix every word on the Tier 1 list but leave the rhythm untouched, the text still reads as AI-generated.

- **Sentence length uniformity**: If most sentences are 15–25 words, the text sounds robotic. Mix short punchy sentences (3–8 words) with longer flowing ones (20+). Fragments work. Questions break the monotony.
- **Paragraph length uniformity**: If every paragraph is 3–5 sentences and roughly the same size, vary deliberately. Some paragraphs should be one sentence. Some should be longer.
- **Vocabulary repetition vs. synonym cycling**: AI either repeats the same word mechanically or cycles through synonyms conspicuously. Human writers repeat when the word is right and vary when it's natural — there's no formula.
- **Read-aloud test**: If the text sounds like it could be read by a text-to-speech engine without sounding weird, it's probably too uniform. Human writing has rhythm that resists robotic delivery.
- **Missing first-person perspective**: Where appropriate, the writer should have opinions, preferences, and reactions. AI is relentlessly neutral. If the piece is supposed to have a voice, the absence of "I think," "in my experience," or a stated preference is itself an AI tell.
- **Over-polishing**: Aggressively editing out every irregularity can push human writing *toward* AI statistical profiles. Natural disfluency, idiosyncratic word choices, and uneven pacing are what keep text out of the "AI-generated" classification. Don't sand away all personality in pursuit of clean prose. This skill should make writing sound more human, not less — if you apply every rule at maximum strictness, you risk creating the very uniformity you're trying to avoid.

---

### When to rewrite from scratch vs. patch

If the text has 5+ flagged vocabulary hits across multiple categories, 3+ distinct pattern categories triggered, and uniform sentence/paragraph length, patching individual phrases won't fix it — the structure itself is AI-generated. Advise a full rewrite: state the core point in one sentence, then rebuild from there.

---

## Severity tiers

Not all AI-isms are equal. When doing a quick pass or triaging a large document, prioritize by tier:

### P0: credibility killers (fix immediately)
- Cutoff disclaimers ("As of my last update")
- Chatbot artifacts ("I hope this helps!", "Great question!")
- Vague attributions without sources ("Experts believe")
- Significance inflation on routine events

### P1: obvious AI smell (fix before publishing)
- Word-list violations (delve, leverage, harness, robust, etc.)
- Template phrases and slot-fill constructions
- Nominalisations ("perform a compression of")
- Actorless passive ("mistakes were made")
- Self-applause tags ("And that matters")
- Paired fragments ("Fast. Simple.")
- "That's not X. That's Y." in either the dash or two-sentence form
- Hedged numeric ranges standing in for a measurement
- "Let's" transition openers
- Synonym cycling within a paragraph
- Formulaic openings ("In the rapidly evolving world of...")
- Bold overuse
- Em dash frequency (above 1 per 1,000 words)

### P2: stylistic polish (fix when time allows)
- Generic conclusions ("The future looks bright")
- Empty-subject openers ("There is a problem with")
- Tense bloat ("has been being tested")
- Noun stacks of four or more words
- Two-image contrasts with no instruction ("less a hammer, more a scalpel")
- X-of-Y shorthand ("the Excel of AI agents")
- Compulsive rule of three
- Uniform paragraph length
- Copula avoidance (serves as, features, boasts)
- Transition phrases (Moreover, Furthermore, Additionally)

Use P0+P1 for quick passes. Full audit covers all three tiers.

---

---

## Self-reference escape hatch

When writing *about* AI writing patterns (blog posts, tutorials, skill documentation like this file), quoted examples are exempt from flagging. Text inside quotation marks, code blocks, or explicitly marked as illustrative ("for example, AI might write...") should not be rewritten. Only flag patterns that appear in the author's own prose, not in cited examples of bad writing.

---

---

## Output format

### Rewrite mode (default)

Return your response in four sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted.

**2. Rewritten version**
The full rewritten content. Preserve the original structure, intent, and all specific technical details. Only change what the guidelines require.

**3. What changed**
A brief summary of the major edits made. Not every word, just the meaningful changes.

**4. Second-pass audit**
Re-read the rewritten version from section 2. Identify any remaining AI tells that survived the first pass — recycled transitions, lingering inflation, copula avoidance, filler phrases, or anything else from the categories above. Fix them, return the corrected text inline, and note what changed in this pass. If the rewrite is clean, say so.

### Detect mode

Return your response in two sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted. Group by severity (P0, P1, P2).

**2. Assessment**
For each flag, note whether it's a clear problem or a judgment call. Some AI-associated patterns are effective writing techniques — uniform paragraph length is a problem, but a well-placed "however" isn't. Call out which flags the writer should definitely fix vs. which ones are worth a second look but might be fine in context. If the text is clean, say so.

---

## Tone calibration

The goal is writing that sounds like a person wrote it. Direct. Specific. The writing should demonstrate confidence, not assert it.

Five principles for human-sounding rewrites:
1. **Vary sentence length** — mix short with long. Fragments are fine.
2. **Be concrete** — replace vague claims with numbers, names, dates, or examples.
3. **Have a voice** — where appropriate, use first person, state preferences, show reactions.
4. **Cut the neutrality** — humans have opinions. If the piece is supposed to take a position, take it.
5. **Earn your emphasis** — don't tell the reader something is interesting. Make it interesting.

If the original writing is already strong, say so and make only the necessary cuts. Don't over-edit for the sake of it.

The replacement table provides defaults, not mandates. If a flagged word is clearly the right choice in context, preserve it.

---

## Credits

Original skill by Conor Bronsdon, MIT licensed. The tiered vocabulary list adapts vocabulary research from [brandonwise/humanizer](https://github.com/brandonwise/humanizer).

The "Post-em-dash tells" section adapts Ruben Hassid's nine tells. The "Grammar patterns borrowed from Simplified Technical English" section and the controlled-language substitutions in Tiers 1 and 2 are drawn from his `/ste` skill, which encodes ASD-STE100 for drafting. Both are published at [ste.rubenhassid.ai](http://ste.rubenhassid.ai).

The reconciliation is this skill's own: STE was designed for maintenance manuals read by non-native speakers, so its rules on padding transfer and its rules on register do not. See "Where Simplified Technical English is wrong for this skill" for the four that are deliberately rejected.

ASD-STE100 is a specification of the AeroSpace and Defence Industries Association of Europe. The rules restated here are paraphrased from public secondary sources, not the official dictionary, and nothing in this file constitutes a compliance claim. Certified technical writing needs the official specification at asd-ste100.org and human sign-off.
