<!-- Reference file for the avoid-ai-writing skill. Loaded on demand, not automatically.
     SKILL.md governs method, modes, severity tiers and output format. -->

# Preventing it at generation time

The rest of this skill is a cure. These are the controls that stop the patterns being written in the first place, which is cheaper than editing them out.

## Write to ASD-STE100

ASD-STE100 (Simplified Technical English) is the controlled-language standard for aircraft maintenance manuals: approved words used in one sense, short sentences, active voice, one instruction per sentence. It exists because an ambiguous sentence in that context can get somebody killed. Its constraints overlap heavily with this document's, so writing to it prevents most Tier 1 vocabulary and most of the longer constructions before they reach the page.

Two ways to apply it, in order of preference:

**A dedicated STE skill.** A separate skill that encodes the rules (sentence limits of 20 words procedural and 25 descriptive, allowed verb forms, a substitution dictionary, warning and caution structure) does the job properly and is invoked explicitly, usually as `/ste`. Ruben Hassid distributes a free one at [ste.rubenhassid.ai](http://ste.rubenhassid.ai). Keep it as its own skill rather than folding it in here: STE governs how prose is *generated*, this file governs how prose is *audited*, and the two want different trigger conditions.

**The one-line fallback.** With no skill installed, putting `Use ASD-STE100.` in the prompt still removes a large share of the problem, because the standard is well enough documented that models approximate it. Less reliable than the skill, and worth nothing on text that is already written. For that, use this file.

Either way, read "Where Simplified Technical English is wrong for this skill" above before turning it on for prose. The rules that catch padding are in this file already, under "Grammar patterns borrowed from Simplified Technical English"; the rules that flatten voice are the reason STE should not run over a personal post.

Scope it deliberately. STE suits guides, steps, explanations, API docs, release notes, emails, and internal documents. It flattens anything that depends on voice: narrative, humour, persuasion, a poem, a personal post. Turn it off for those and rely on the audit rules instead.

One caveat worth passing on. The official ASD-STE100 specification and its dictionary are copyright ASD. Any skill of this kind encodes paraphrased rules and a publicly sourced word list, which is fine for ordinary writing and not the same thing as compliance. For certified aerospace or defence deliverables, the free official specification at asd-ste100.org plus human sign-off is the requirement. Never describe output as certified.

## Keep Zinsser's fourth principle

STE delivers simplicity, brevity, and clarity. It has no opinion about humanity, and text optimised only for the first three reads like a manual regardless of subject. Zinsser's four principles are simplicity, brevity, clarity, and humanity. The fourth is the one that keeps a person audible in the prose.

For a project that generates a lot of prose, put the reminder where the model reads it every session, in `CLAUDE.md` or the equivalent:

> Follow Zinsser's four principles of quality writing: 1. Simplicity 2. Brevity 3. Clarity 4. Humanity.

This skill's "Missing first-person perspective" and "Over-polishing" rules exist for the same reason. If STE is on and the output has gone flat, humanity is the principle that went missing.

## Keep a project-local forbidden list

This file is general. The patterns that actually recur in one project, publication, or writer are narrower, and they change faster than a shared skill can be updated.

Keep a short `forbidden-patterns.md` next to the work, and tell the model to check every draft against both it and this skill. Add a line each time a new tell gets past you, with a one-line fix beside it. The file compounds: after a few weeks it catches more of your specific problems than any general list will, and it's the right home for house style that would be wrong to impose on everyone.

`forbidden-patterns.template.md` in this skill's folder is a starter, seeded with the patterns above and an empty house-style section.

## Start a fresh chat when quality drops

Long conversations degrade writing quality. The model drifts back toward the polished register, repeats phrasings it already used, and re-introduces patterns it removed earlier in the same session. This is a context problem, not a prompting problem, and no amount of re-instructing fixes it.

When a draft starts sounding like the thing you have been editing away from, open a new chat and paste back the source material and the forbidden list. Roughly halfway through a long session is usually early enough.
