---
name: avoid-ai-writing
description: Audit and rewrite content to remove AI writing patterns ("AI-isms"). Use this skill when asked to "remove AI-isms," "clean up AI writing," "edit writing for AI patterns," "audit writing for AI tells," or "make this sound less like AI." Supports a detection-only mode that flags patterns without rewriting. Works on Hebrew text as well; loads references/hebrew.md for Hebrew-specific patterns.
version: 3.6.0
license: MIT
compatibility: Any AI coding assistant that supports the agentskills.io SKILL.md format (Claude Code, Codex CLI, Grok Build, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Conor Bronsdon
  fork_maintainer: Dror Moshe Aharoni
  fork_changes: "Added rules for overgeneralized 'Most people...' openers, adverb crutches, fake profundity, and the 'after careful consideration' / 'here's the thing' stalls. 3.5.0 adds the post-em-dash tells (paired fragments, two-image contrasts, self-applause tags, X-of-Y analogies, hedged numeric ranges), a generation-time prevention section built on ASD-STE100 and Zinsser's fourth principle, and guidance on keeping a project-local forbidden-patterns file. 3.6.0 absorbs the transferable grammar rules from Simplified Technical English (nominalisations, actorless passive, tense bloat, empty-subject openers, noun stacks), adds 22 controlled-language substitutions across Tiers 1 and 2, and states explicitly which STE rules to reject because they flatten voice."
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

## What to remove or fix

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

### Words and phrases to replace

Words are organized into three tiers based on how reliably they signal AI-generated text. This tiered approach — adapted from [brandonwise/humanizer](https://github.com/brandonwise/humanizer)'s vocabulary research — reduces false positives on words that are fine in isolation but suspicious in clusters.

- **Tier 1 — Always flag.** These words appear 5–20x more often in AI text than human text. Replace on sight.
- **Tier 2 — Flag in clusters.** Individually fine, but two or more in the same paragraph is a strong AI signal. Flag when they appear together.
- **Tier 3 — Flag by density.** Common words that AI simply overuses. Only flag when they make up a noticeable fraction of the text (roughly 3%+ of total words).

#### Tier 1 — Always replace

| Replace | With |
|---|---|
| delve / delve into | explore, dig into, look at |
| landscape (metaphor) | field, space, industry, world |
| tapestry | (describe the actual complexity) |
| realm | area, field, domain |
| paradigm | model, approach, framework |
| embark | start, begin |
| beacon | (rewrite entirely) |
| testament to | shows, proves, demonstrates |
| robust | strong, reliable, solid |
| comprehensive | thorough, complete, full |
| cutting-edge | latest, newest, advanced |
| leverage (verb) | use |
| pivotal | important, key, critical |
| underscores | highlights, shows |
| meticulous / meticulously | careful, detailed, precise |
| seamless / seamlessly | smooth, easy, without friction |
| game-changer / game-changing | describe what specifically changed and why it matters |
| hit differently / hits different | (say what specifically changed, or cut) |
| utilize | use |
| watershed moment | turning point, shift (or describe what changed) |
| marking a pivotal moment | (state what happened) |
| the future looks bright | (cut — say something specific or nothing) |
| only time will tell | (cut — say something specific or nothing) |
| nestled | is located, sits, is in |
| vibrant | (describe what makes it active, or cut) |
| thriving | growing, active (or cite a number) |
| despite challenges… continues to thrive | (name the challenge and the response, or cut) |
| showcasing | showing, demonstrating (or cut the clause) |
| deep dive / dive into | look at, examine, explore |
| unpack / unpacking | explain, break down, walk through |
| bustling | busy, active (or cite what makes it busy) |
| intricate / intricacies | complex, detailed (or name the specific complexity) |
| complexities | (name the actual complexities, or use "problems" / "details") |
| ever-evolving | changing, growing (or describe how) |
| enduring | lasting, long-running (or cite how long) |
| daunting | hard, difficult, challenging |
| holistic / holistically | complete, full, whole (or describe what's included) |
| actionable | practical, useful, concrete |
| impactful | effective, significant (or describe the impact) |
| learnings | lessons, findings, takeaways |
| thought leader / thought leadership | expert, authority (or describe their actual contribution) |
| best practices | what works, proven methods, standard approach |
| at its core | (cut — just state the thing) |
| synergy / synergies | (describe the actual combined effect) |
| interplay | relationship, connection, interaction |
| in order to | to |
| due to the fact that | because |
| serves as | is |
| features (verb) | has, includes |
| boasts | has |
| presents (inflated) | is, shows, gives |
| commence | start, begin |
| ascertain | find out, determine, learn |
| endeavor | effort, attempt, try |
| keen (as intensifier) | interested, eager, enthusiastic (or cut — just state the interest) |
| after careful consideration | (cut — claims deliberation that didn't happen; just give the decision) |
| here's the thing | (cut — a stall before the point; just make the point) |
| let me be clear | (cut — a warm-up; start one sentence later) |
| the truth is | (cut — same warm-up; the claim that follows is the sentence) |
| what's wild is | (cut — pre-announces a reaction the reader should have) |
| ensure / verify / validate | make sure, check, confirm it works |
| utilise (any spelling) | use |
| initiate | start |
| terminate / cease | stop, end |
| in the event that | if |
| prior to | before |
| subsequent to | after |
| by means of / via (non-route sense) | through, with, by |
| symphony (metaphor) | (describe the actual coordination or combination) |
| embrace (metaphor) | adopt, accept, use, switch to |

#### Tier 2 — Flag when 2+ appear in the same paragraph

These words are legitimate on their own. When two or more show up together, the paragraph likely needs a rewrite.

| Replace | With |
|---|---|
| harness | use, take advantage of |
| navigate / navigating | work through, handle, deal with |
| foster | encourage, support, build |
| elevate | improve, raise, strengthen |
| unleash | release, enable, unlock |
| streamline | simplify, speed up |
| empower | enable, let, allow |
| bolster | support, strengthen, back up |
| spearhead | lead, drive, run |
| resonate / resonates with | connect with, appeal to, matter to |
| revolutionize | change, transform, reshape (or describe what changed) |
| facilitate / facilitates | enable, help, allow, run |
| underpin | support, form the basis of |
| nuanced | specific, subtle, detailed (or name the actual nuance) |
| crucial | important, key, necessary |
| multifaceted | (describe the actual facets, or cut) |
| ecosystem (metaphor) | system, community, network, market |
| myriad | many, numerous (or give a number) |
| plethora | many, a lot of (or give a number) |
| encompass | include, cover, span |
| catalyze | start, trigger, accelerate |
| reimagine | rethink, redesign, rebuild |
| galvanize | motivate, rally, push |
| augment | add to, expand, supplement |
| perform / conduct / execute (an action) | do, run |
| obtain / acquire / procure | get |
| sufficient / adequate | enough |
| accomplish | do, finish |
| necessitate / require | need, must |
| demonstrate | show |
| modify / alter | change |
| retain | keep |
| indicate | show, point to |
| additional / supplementary | more |
| approximately | about (or the measured number) |
| remainder | rest |
| cultivate | build, develop, grow |
| illuminate | clarify, explain, show |
| elucidate | explain, clarify, spell out |
| juxtapose | compare, contrast, set side by side |
| paradigm-shifting | (describe what actually shifted) |
| transformative / transformation | (describe what changed and how) |
| cornerstone | foundation, basis, key part |
| paramount | most important, top priority |
| poised (to) | ready, set, about to |
| burgeoning | growing, emerging (or cite a number) |
| nascent | new, early-stage, emerging |
| quintessential | typical, classic, defining |
| overarching | main, central, broad |
| underpinning / underpinnings | basis, foundation, what supports |

#### Tier 3 — Flag only at high density

These are normal words. Only flag them when the text is saturated with them — a sign that AI filled space with vague praise instead of specifics.

| Word | What to do |
|---|---|
| significant / significantly | Replace some with specifics: numbers, comparisons, examples |
| innovative / innovation | Describe what's actually new |
| effective / effectively | Say how or cite a metric |
| dynamic / dynamics | Name the actual forces or changes |
| scalable / scalability | Describe what scales and to what |
| compelling | Say why it compels |
| unprecedented | Name the precedent it breaks (or cut) |
| exceptional / exceptionally | Cite what makes it an exception |
| remarkable / remarkably | Say what's worth remarking on |
| sophisticated | Describe the sophistication |
| instrumental | Say what role it played |
| world-class / state-of-the-art / best-in-class | Cite a benchmark or comparison |

### Template phrases (avoid)

These slot-fill constructions signal that a sentence was generated, not written. If a phrase has a blank where a noun or adjective could go and still sound the same, it's too generic.

- "a [adjective] step towards [adjective] AI infrastructure" → describe the specific capability, benchmark, or outcome
- "a [adjective] step forward for [noun]" → same rule: say what actually changed
- "Whether you're [X] or [Y]" → false-breadth construction. Pick the audience you're actually addressing, or cut. "Whether you're a startup founder or an enterprise architect" means nothing — it's just "everyone."
- "I recently had the pleasure of [verb]-ing" → review/social AI pattern. Just say what happened: "I talked to," "I read," "I attended."

### Transition phrases to remove or rewrite
- "Moreover" / "Furthermore" / "Additionally" → restructure so the connection is obvious, or use "and," "also," "on top of that"
- "In today's [X]" / "In an era where" → cut or state specific context
- "It's worth noting that" / "Notably" → just state the fact
- "Here's what's interesting" / "Here's what caught my eye" / "Here's what stood out" → reader-steering frames. Let the content signal its own importance. If you need a lead-in, make it specific: "The revenue number matters because..." not "Here's the interesting part."
- "In conclusion" / "In summary" / "To summarize" → your conclusion should be obvious
- "When it comes to" → just talk about the thing directly
- "At the end of the day" → cut
- "That said" / "That being said" → cut or use "but," "yet," or "however." Don't overuse any one of them.

### Structural issues
- **Uniform paragraph length**: Vary deliberately. Include some 1-2 sentence paragraphs and some longer ones. If every paragraph is roughly the same size, fix it.
- **Formulaic openings**: If the piece opens with broad context before getting to the point ("In the rapidly evolving world of..."), rewrite to lead with the news or the insight. Context can come second.
- **Suspiciously clean grammar**: Don't sand away all personality. Deliberate fragments, sentences starting with "And" or "But," comma splices for effect: if the natural voice uses them, keep them.

### Significance inflation
- Phrases like "marking a pivotal moment in the evolution of..." or "a watershed moment for the industry" inflate routine events into history-making ones. State what happened and let the reader judge significance.
- If the sentence still works after you delete the inflation clause, delete it.

### Copula avoidance
- AI text avoids "is" and "has" by substituting fancier verbs: "serves as," "features," "boasts," "presents," "represents." These sound like a press release.
- Default to "is" or "has" unless a more specific verb genuinely adds meaning.

### Synonym cycling
- AI rotates synonyms to avoid repeating a word: "developers… engineers… practitioners… builders" in the same paragraph. Human writers repeat the clearest word.
- If the same noun or verb appears three times in a paragraph and that's the right word, keep all three. Forced variation reads as thesaurus abuse.

### Vague attributions
- "Experts believe," "Studies show," "Research suggests," "Industry leaders agree" — without naming the expert, study, or leader. Either cite a specific source or drop the attribution and state the claim directly.

### Filler phrases
- Strip mechanical padding that adds words without meaning:
  - "It is important to note that" → (just state it)
  - "In terms of" → (rewrite)
  - "The reality is that" → (cut or just state the claim)
- Note: "In order to," "Due to the fact that," and "At the end of the day" are covered in the word/phrase table and transition sections above — don't duplicate rules.

### Generic conclusions
- "The future looks bright," "Only time will tell," "One thing is certain," "As we move forward" — these are filler disguised as conclusions. Cut them. If the piece needs a closing thought, make it specific to the argument.

### Chatbot artifacts
- "I hope this helps!", "Certainly!", "Absolutely!", "Great question!", "Feel free to reach out," "Let me know if you need anything else" — these are conversational tics from chat interfaces, not writing. Remove entirely.
- Also watch for: "In this article, we will explore…" or "Let's dive in!" — these are AI-generated meta-narration. Cut or rewrite with a direct opening.

### "Let's" constructions
- "Let's explore," "Let's take a look," "Let's break this down," "Let's examine" — AI uses "let's" as a false-collaborative opener to ease into a topic. It's filler that delays the actual point. Just start with the point. "Let's dive in" is covered above under chatbot artifacts, but the pattern is broader than that — flag any "let's + verb" that's functioning as a transition rather than a genuine invitation to act.

### Notability name-dropping
- AI text piles on prestigious citations to manufacture credibility: "cited in The New York Times, BBC, Financial Times, and The Hindu." If a source matters, use it with context: "In a 2024 NYT interview, she argued..." One specific reference beats four name-drops.

### Superficial -ing analyses
- Strings of present participles used as pseudo-analysis: "symbolizing the region's commitment to progress, reflecting decades of investment, and showcasing a new era of collaboration." These say nothing. Replace with specific facts or cut entirely.

### Promotional language
- AI defaults to tourism-brochure prose: "nestled within the breathtaking foothills," "a vibrant hub of innovation," "a thriving ecosystem." Replace with plain description: "is a town in the Gonder region," "has 12 startups." If you wouldn't say it in conversation, cut it.

### Formulaic challenges
- "Despite challenges, [subject] continues to thrive" or "While facing headwinds, the organization remains resilient." This is a non-statement. Name the actual challenge and the actual response, or cut the sentence.

### False ranges
- AI creates false breadth by pairing unrelated extremes: "from the Big Bang to dark matter," "from ancient civilizations to modern startups." These sound sweeping but say nothing. List the actual topics or pick the one that matters.

### Inline-header lists
- Bullet lists where each item starts with a bold header that repeats itself: "**Performance:** Performance improved by..." Strip the bold header and write the point directly. If the list items need headers, they should probably be paragraphs.

### Title case headings
- AI over-capitalizes headings: "Strategic Negotiations And Key Partnerships" instead of "Strategic negotiations and key partnerships." Use sentence case for subheadings. Title case only for the piece's main title, if at all.

### Cutoff disclaimers
- "While specific details are limited based on available information," "As of my last update," "I don't have access to real-time data." These are model limitations leaking into prose. Either find the information or remove the hedge. Never publish a sentence that admits the writer didn't look something up.

### Novelty inflation
- AI text treats established concepts as if the speaker invented or discovered them: "He introduced a term," "She coined the phrase," "a concept nobody's naming," "a failure mode nobody talks about." In reality, most ideas in a conversation are applications of existing concepts, not inventions.
- Two problems. First, it's factually risky: if the concept already has a Wikipedia page or conference talks from last year, claiming novelty makes the writer look uninformed. Second, it flatters the subject in a way that reads as promotional rather than analytical.
- The fix: describe what the person *did with* the concept, not that they discovered it. "Michel walked through how context poisoning works in practice" instead of "Michel introduced a term I hadn't heard before: context poisoning." If you're unsure whether something is novel, assume it isn't and frame accordingly.
- Related patterns to flag: "the failure mode nobody's naming," "a problem nobody talks about," "the insight everyone's missing," "what nobody tells you about." These are engagement-bait framings that claim scarcity of knowledge where none exists.

### Emotional flatline
- AI claims emotions as a structural crutch without conveying them through the writing: "What surprised me most," "I was fascinated to discover," "What struck me was," "I was excited to learn," "The most interesting part."
- Two problems. First, it's tell-don't-show: if the thing is genuinely surprising, the reader should feel that from the content, not from the writer announcing it. Second, these phrases are massively overused as list introductions and transitions. They're filler wearing an emotion costume.
- This pattern isn't always AI. It's also a sign of lazy human writing on autopilot. Flag it either way.
- The fix isn't "never say surprised." It's: if you claim an emotion, the writing around it should earn it. Otherwise cut the claim and present the thing directly.
- Related pattern: "hit differently" / "hits different." AI uses trendy colloquialisms as a shortcut to sound relatable without earning the emotional beat. If something genuinely affected you, describe how. Otherwise cut.

### False concession structure
- "While X is impressive, Y remains a challenge" or "Although X has made strides, Y is still an open question." AI uses this to sound balanced without actually weighing anything. Both halves are vague. Either make the concession specific (name what's impressive, name the actual challenge) or pick a side and argue it.

### Rhetorical question openers
- "But what does this mean for developers?" / "So why should you care?" / "What's next?" � AI uses rhetorical questions to stall before the actual point. If you know the answer, just say it. Rhetorical questions are earned by strong setup, not dropped as section transitions.

### Parenthetical hedging
- "(and, increasingly, Z)" / "(or, more precisely, Y)" / "(and perhaps more importantly, W)" � AI inserts parenthetical asides to sound nuanced without committing. If the aside matters, give it its own sentence. If it doesn't, cut it.

### Numbered list inflation
- "Three key takeaways" / "Five things to know" / "Here are the top seven" � AI defaults to numbered lists because they're structurally safe. Only use numbered lists when the content genuinely has that many discrete, parallel items. If you're padding to hit a number, the list shouldn't exist.

### Reasoning chain artifacts
- "Let me think step by step," "Breaking this down," "To approach this systematically," "Step 1:," "Here's my thought process," "First, let's consider," "Working through this logically" — these are artifacts of chain-of-thought reasoning leaking into published prose. The reader doesn't need to see the scaffolding. State the conclusion, then the evidence.
- Also watch for numbered reasoning steps that read like an internal monologue rather than an argument meant for an audience.

### Sycophantic tone
- "Great question!", "Excellent point!", "You're absolutely right!", "That's a really insightful observation" — these are conversational rewards from chat interfaces, not writing. Remove entirely.
- Distinct from chatbot artifacts: sycophancy specifically validates the reader/questioner rather than just performing helpfulness.

### Acknowledgment loops
- "You're asking about," "The question of whether," "To answer your question," "That's a great question. The..." — AI restates the prompt before answering. In writing, this is pure filler. The reader knows what they asked. Just answer.
- Related pattern: opening a section by summarizing what the previous section said. If the structure is clear, the reader doesn't need a recap.

### Confidence calibration phrases
- "It's worth noting that," "Interestingly," "Surprisingly," "Importantly," "Significantly," "Notably," "Certainly," "Undoubtedly," "Without a doubt" — AI uses these to signal how the reader should feel about a fact instead of letting the fact speak for itself.
- "Here's what's interesting," "Here's the interesting part," "Here are the parts I found interesting" — reader-steering cue that pre-interprets importance. Works when followed by genuinely surprising data; fails when it introduces a restatement of something obvious (which is the AI default).
- One "notably" in a 2,000-word piece is fine. Three in 500 words is AI-style emphasis stacking. Flag by density.

### Excessive structure
- Too many headers in short text: more than 3 headings in under 300 words is almost always AI trying to look organized. Merge sections or use prose transitions instead.
- Too many list items: 8+ bullet points in under 200 words means the content should be a paragraph, not a list.
- Formulaic section headers: "Overview," "Key Points," "Summary," "Conclusion," "Introduction" — these are default AI scaffolding. Use headers that tell the reader something specific about what follows.

### Overgeneralized openers ("Most people...")
- "Most people don't realize," "Most people think X, but," "Nobody talks about," "99% of you are doing this wrong," "Everyone's [X], but the smart ones [Y]." AI and engagement-bait writing both open by inventing a silent majority to correct. It manufactures a false hook and asserts a statistic nobody counted.
- The fix: drop the imaginary crowd and open with the actual claim. "Most people think alignment is an engineering problem" becomes "Alignment is usually treated as an engineering problem, and that framing is the mistake."
- Related: "Just a quick update," "To provide a quick update," "Wanted to share a quick thought." Filler runways before the real content. Cut and start with the update itself.

### Adverb crutches
- AI leans on adverbs to inject drama a plain verb would carry better: "quietly runs," "seamlessly integrates," "effortlessly scales," "single-handedly transforms." The adverb is doing emotional work the sentence hasn't earned.
- The fix: cut the adverb, or replace verb-plus-adverb with one strong verb. "Quietly runs in the background" is just "runs in the background." If the adverb carries real information (how, how much), keep it; if it only adds mood, cut it.

### Fake profundity
- Inflating a mundane fact into a grand statement: "It's not just a budget, it's a statement of intent," "This isn't a feature, it's a philosophy," "That number tells a story." AI reaches for false depth to make the ordinary sound momentous.
- Note this overlaps the "it's not X, it's Y" structure but the tell is the reach for cosmic significance, not the sentence shape. Either back the claim with what specifically makes it meaningful, or state the plain fact and let the reader weigh it.

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

### Grammar patterns borrowed from Simplified Technical English

Controlled-language standards were built to stop ambiguity, not to defeat AI detectors, but four of their rules catch constructions this list otherwise misses. Models reach for all four constantly, because each one lets a sentence sound complete while committing to less.

**Nominalisations.** An action turned into a noun, propped up by an empty verb: "perform a compression of the log files," "conduct an analysis," "provide assistance," "make a determination," "do an evaluation of."
- The fix is always the same: the noun already contains the verb. "Compress the log files." "Analyse it." "Help." "Decide."
- Fastest single edit in this document. Look for *perform / conduct / provide / make / do / carry out* followed by a noun ending in -tion, -ment, -ance, or -ing.

**Passive voice with no actor.** "The files are processed," "mistakes were made," "the decision was reached," "it is recommended that."
- Passive is legitimate when the actor is genuinely unknown or irrelevant ("the server was rebooted overnight"). It is an AI tell when it hides who acted, because the model often does not know and the passive lets it avoid saying.
- The fix: name the actor. "The pipeline processes the files." If naming the actor is impossible, that is worth noticing, not smoothing over.

**Tense bloat.** "We have received your request," "the system is currently running," "this has been being tested since March."
- Present perfect and continuous forms pad a sentence without adding information. Simple past or present nearly always carries the same meaning in fewer words: "We got your request." "The system runs diagnostics now." "We started testing in March."

**Empty-subject openers.** "There is a problem with the parser," "There are three bolts on the panel," "It is important that."
- These delay the real subject by one clause. Rewrite with the actual subject in front: "The parser drops trailing commas." "The panel has three bolts."
- Related: noun stacks of four or more words ("runway light connection resistance calibration"). Break them with prepositions: "calibration of the resistance in the runway light connection." Three words is the practical ceiling.

Two smaller ones, worth a scan rather than a rule: Latin abbreviations (`e.g.` → "for example", `i.e.` → "that is", `etc.` → finish the list or cut it), and semicolons joining two independent clauses, which almost always read better as two sentences.

### Where Simplified Technical English is wrong for this skill

STE optimises for a non-native reader parsing a maintenance manual under time pressure. That is not the goal here, and importing it wholesale produces text that fails this skill's own tests. Four rules to *not* carry over:

- **It bans contractions.** Contractions are one of the strongest human signals in ordinary prose. Keep "it's," "don't," "you're." Drop contractions only in formal documents where the register genuinely calls for it.
- **It bans phrasal verbs**, replacing "set up" with "install" and "go down" with "decrease." That trade runs backwards for everything except technical procedures: the Latinate word is the one that sounds machine-written. Prefer the phrasal verb in prose.
- **It caps sentence length** at 20 words for procedures and 25 for description. A whole piece written to that cap is uniformly short, and uniformity is the top structural detection signal. Use the caps as an upper bound on individual sentences in documentation, never as a target, and keep the length variance that "Rhythm and uniformity" calls for.
- **Its one-meaning rulings are aviation jargon.** "Do a test" instead of "test the system," "obey the steps" instead of "follow the steps," "check" banned as a verb. Correct in a manual, strange anywhere else. Ignore them outside certified technical writing.

The general principle: take STE's rules about *padding* and leave its rules about *register*. Padding is padding in any genre. Register is what makes writing sound like a person.

### Rhythm and uniformity

These aren't individual word or phrase problems — they're patterns in how the text flows as a whole. AI text is metronomic; human text has varied rhythm.

**Structure is the #1 detection signal.** AI detection tools (including Pangram, which trains a classifier on 28M human documents) weight structural regularity higher than vocabulary. Consistent sentence construction, uniform pacing, and symmetrical phrasing patterns are harder to mask than swapping out a few flagged words. If you fix every word on the Tier 1 list but leave the rhythm untouched, the text still reads as AI-generated.

- **Sentence length uniformity**: If most sentences are 15–25 words, the text sounds robotic. Mix short punchy sentences (3–8 words) with longer flowing ones (20+). Fragments work. Questions break the monotony.
- **Paragraph length uniformity**: If every paragraph is 3–5 sentences and roughly the same size, vary deliberately. Some paragraphs should be one sentence. Some should be longer.
- **Vocabulary repetition vs. synonym cycling**: AI either repeats the same word mechanically or cycles through synonyms conspicuously. Human writers repeat when the word is right and vary when it's natural — there's no formula.
- **Read-aloud test**: If the text sounds like it could be read by a text-to-speech engine without sounding weird, it's probably too uniform. Human writing has rhythm that resists robotic delivery.
- **Missing first-person perspective**: Where appropriate, the writer should have opinions, preferences, and reactions. AI is relentlessly neutral. If the piece is supposed to have a voice, the absence of "I think," "in my experience," or a stated preference is itself an AI tell.
- **Over-polishing**: Aggressively editing out every irregularity can push human writing *toward* AI statistical profiles. Natural disfluency, idiosyncratic word choices, and uneven pacing are what keep text out of the "AI-generated" classification. Don't sand away all personality in pursuit of clean prose. This skill should make writing sound more human, not less — if you apply every rule at maximum strictness, you risk creating the very uniformity you're trying to avoid.

### When to rewrite from scratch vs. patch

If the text has 5+ flagged vocabulary hits across multiple categories, 3+ distinct pattern categories triggered, and uniform sentence/paragraph length, patching individual phrases won't fix it — the structure itself is AI-generated. Advise a full rewrite: state the core point in one sentence, then rebuild from there.

---

## Severity tiers

Not all AI-isms are equal. When doing a quick pass or triaging a large document, prioritize by tier:

### P0 � Credibility killers (fix immediately)
- Cutoff disclaimers ("As of my last update")
- Chatbot artifacts ("I hope this helps!", "Great question!")
- Vague attributions without sources ("Experts believe")
- Significance inflation on routine events

### P1 � Obvious AI smell (fix before publishing)
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

### P2 � Stylistic polish (fix when time allows)
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

## Preventing it at generation time

Everything above is a cure. These are the controls that stop the patterns being written in the first place, which is cheaper than editing them out.

### Write to ASD-STE100

ASD-STE100 (Simplified Technical English) is the controlled-language standard for aircraft maintenance manuals: approved words used in one sense, short sentences, active voice, one instruction per sentence. It exists because an ambiguous sentence in that context can get somebody killed. Its constraints overlap heavily with this document's, so writing to it prevents most Tier 1 vocabulary and most of the longer constructions before they reach the page.

Two ways to apply it, in order of preference:

**A dedicated STE skill.** A separate skill that encodes the rules (sentence limits of 20 words procedural and 25 descriptive, allowed verb forms, a substitution dictionary, warning and caution structure) does the job properly and is invoked explicitly, usually as `/ste`. Ruben Hassid distributes a free one at [ste.rubenhassid.ai](http://ste.rubenhassid.ai). Keep it as its own skill rather than folding it in here: STE governs how prose is *generated*, this file governs how prose is *audited*, and the two want different trigger conditions.

**The one-line fallback.** With no skill installed, putting `Use ASD-STE100.` in the prompt still removes a large share of the problem, because the standard is well enough documented that models approximate it. Less reliable than the skill, and worth nothing on text that is already written. For that, use this file.

Either way, read "Where Simplified Technical English is wrong for this skill" above before turning it on for prose. The rules that catch padding are in this file already, under "Grammar patterns borrowed from Simplified Technical English"; the rules that flatten voice are the reason STE should not run over a personal post.

Scope it deliberately. STE suits guides, steps, explanations, API docs, release notes, emails, and internal documents. It flattens anything that depends on voice: narrative, humour, persuasion, a poem, a personal post. Turn it off for those and rely on the audit rules instead.

One caveat worth passing on. The official ASD-STE100 specification and its dictionary are copyright ASD. Any skill of this kind encodes paraphrased rules and a publicly sourced word list, which is fine for ordinary writing and not the same thing as compliance. For certified aerospace or defence deliverables, the free official specification at asd-ste100.org plus human sign-off is the requirement. Never describe output as certified.

### Keep Zinsser's fourth principle

STE delivers simplicity, brevity, and clarity. It has no opinion about humanity, and text optimised only for the first three reads like a manual regardless of subject. Zinsser's four principles are simplicity, brevity, clarity, and humanity. The fourth is the one that keeps a person audible in the prose.

For a project that generates a lot of prose, put the reminder where the model reads it every session, in `CLAUDE.md` or the equivalent:

> Follow Zinsser's four principles of quality writing: 1. Simplicity 2. Brevity 3. Clarity 4. Humanity.

This skill's "Missing first-person perspective" and "Over-polishing" rules exist for the same reason. If STE is on and the output has gone flat, humanity is the principle that went missing.

### Keep a project-local forbidden list

This file is general. The patterns that actually recur in one project, publication, or writer are narrower, and they change faster than a shared skill can be updated.

Keep a short `forbidden-patterns.md` next to the work, and tell the model to check every draft against both it and this skill. Add a line each time a new tell gets past you, with a one-line fix beside it. The file compounds: after a few weeks it catches more of your specific problems than any general list will, and it's the right home for house style that would be wrong to impose on everyone.

`forbidden-patterns.template.md` in this skill's folder is a starter, seeded with the patterns above and an empty house-style section.

### Start a fresh chat when quality drops

Long conversations degrade writing quality. The model drifts back toward the polished register, repeats phrasings it already used, and re-introduces patterns it removed earlier in the same session. This is a context problem, not a prompting problem, and no amount of re-instructing fixes it.

When a draft starts sounding like the thing you have been editing away from, open a new chat and paste back the source material and the forbidden list. Roughly halfway through a long session is usually early enough.

## Self-reference escape hatch

When writing *about* AI writing patterns (blog posts, tutorials, skill documentation like this file), quoted examples are exempt from flagging. Text inside quotation marks, code blocks, or explicitly marked as illustrative ("for example, AI might write...") should not be rewritten. Only flag patterns that appear in the author's own prose, not in cited examples of bad writing.

---

## Context profiles

Pass an optional context hint to adjust rule strictness. If no context is specified, auto-detect from content cues (short + hashtags = social, code blocks = technical, salutation = email, default = blog).

### Profile definitions

**`linkedin`** � Short-form social. Punchy fragments, visual formatting matter.
**`blog`** � Default. Standard long-form prose. All rules apply at full strength.
**`technical-blog`** � Long-form with code, architecture, APIs. Technical terms get a pass.
**`investor-email`** � High-trust audience. Tighten everything; promotional language is the biggest risk.
**`docs`** � Documentation, READMEs, guides. Clarity over voice.
**`casual`** � Slack messages, internal notes, quick replies. Only catch the worst offenders.

### Tolerance matrix

Rules not listed in the table apply at full strength across all profiles.

| Rule | linkedin | blog | technical-blog | investor-email | docs | casual |
|------|----------|------|----------------|----------------|------|--------|
| Em dashes | relaxed (2/post OK) | strict | strict | strict | relaxed | skip |
| Bold overuse | relaxed (bold hooks OK) | strict | strict | strict | relaxed | skip |
| Emoji in headers | relaxed (1-2 end-of-line OK) | strict | strict | strict | skip | skip |
| Excessive bullets | skip (lists work on LinkedIn) | strict | relaxed (technical lists OK) | strict | skip (lists are docs) | skip |
| Hedging | strict | strict | relaxed ("may" is accurate in technical) | strict | relaxed | skip |
| Word table (full list) | strict | strict | **partial** (see below) | strict | relaxed | P0 only |
| Promotional language | relaxed (some sell is expected) | strict | strict | **extra strict** | strict | skip |
| Significance inflation | strict | strict | strict | **extra strict** | relaxed | skip |
| Copula avoidance | skip | strict | relaxed | strict | skip | skip |
| Uniform paragraph length | skip (short-form) | strict | strict | strict | relaxed | skip |
| Numbered list inflation | relaxed | strict | relaxed | strict | skip | skip |
| Rhetorical questions | relaxed (1 as hook OK) | strict | strict | strict | strict | skip |
| Transition phrases | skip (short-form) | strict | strict | strict | relaxed | skip |
| Generic conclusions | skip | strict | strict | **extra strict** | skip | skip |

**Technical-blog word table exceptions:** These terms have legitimate technical meaning and should not be flagged in technical context: `robust`, `comprehensive`, `seamless`, `ecosystem`, `leverage` (when discussing actual platform leverage/APIs), `facilitate`, `underpin`, `streamline`. Still flag: `delve`, `tapestry`, `beacon`, `embark`, `testament to`, `game-changer`, `harness`.

**"Extra strict"** means: flag even borderline instances. In investor emails, a single "thriving ecosystem" can undermine the whole message.

**"Skip"** means: don't audit this category for this profile. The rule doesn't apply or isn't worth the edit.

### Auto-detection cues

When no context is specified, infer from these signals:

| Signal | Inferred context |
|--------|-----------------|
| Under 300 words + hashtags or mentions | `linkedin` |
| Code blocks, API references, or technical architecture | `technical-blog` |
| Salutation ("Hi [name]", "Dear") + investor/fundraising language | `investor-email` |
| Step-by-step instructions, parameter docs, README structure | `docs` |
| No strong signals | `blog` (safest default � all rules apply) |

If auto-detection feels wrong, say which profile you're using and why. The user can override.

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
