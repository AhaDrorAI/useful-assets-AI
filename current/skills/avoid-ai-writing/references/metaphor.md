<!-- Reference file for the avoid-ai-writing skill. Loaded on demand, not automatically.
     SKILL.md governs method, modes, severity tiers and output format. -->

# Analogy and metaphor control

The default is literal. Most AI metaphors are decoration on a point that was
already clear, and decoration is where the machine voice lives.

Two separate failures hide under "metaphor," and they need different fixes:

- A **stated analogy** compares two things on purpose ("think of it as a
  bridge between..."). It fails when the literal sentence was shorter.
- A **dead metaphor verb** smuggles an image into an ordinary sentence
  ("we sanded down the onboarding"). It fails because the writer never
  decided what actually happened.

The verb list at the bottom is the higher-yield check. Stated analogies are
easy to spot and get cut in most edits. The verbs survive, because they read
as ordinary prose until you ask what physical action is being claimed.

## The permission test

Use a stated analogy only if **all five** pass. Any failure means write it
literally:

1. The subject is genuinely unfamiliar, abstract, or technical to this audience.
2. The analogy makes it easier to understand, not just nicer to read.
3. It is shorter than the literal explanation.
4. It is exact enough not to mislead when the reader pushes on it.
5. It reads normally aloud.

Point 3 kills most of them. If the analogy needs a sentence of setup and a
sentence of unpacking, the literal version was already the short one.

## Frequency budget

| Length | Analogies allowed |
|---|---|
| Under 800 words | 0 |
| 800 to 1,500 words | 1 |
| Every additional 1,500 words | 1 more |

Never stack two images in the same paragraph, and never extend one metaphor
across sections. A metaphor that returns three times has become the argument,
which means the argument was never made.

## Banned setups

These phrases announce an analogy is coming. Flag the phrase, then check the
analogy behind it against the permission test.

Think of it as, Imagine, Picture, It's like, As if, As though, Works like,
Acts like, Functions as, In a sense, You can think of, Sort of like,
The X of Y, A bridge between, A lens for, A roadmap for, A blueprint for,
The engine of, The backbone of, The DNA of, The heartbeat of.

`The X of Y` is also covered in SKILL.md as X-of-Y shorthand. Same pattern,
flag once.

## Banned metaphor families

For abstract work (strategy, products, process, organisations, ideas), these
image families are exhausted. They carry no information and mark the text as
generated:

journey, roadmap, battlefield, war, machine-for-people, ecosystem,
engine and fuel, map and compass, north star, signal and noise (unless the
subject is literally signal processing), iceberg, tip of the iceberg,
flywheel, scaffolding, plumbing, gardening and pruning, chess, sports and
teams, puzzle and pieces, recipe and ingredients, muscle and reps,
immune system, gravity, orbit.

Exception: a family is fine when the subject is literally that thing. A post
about actual gardening may garden.

## Banned metaphor verbs

This is the part that survives every other sweep. When applied to ideas,
strategy, products, teams, or process, these verbs claim a physical action
that never happened:

sanded down, bolted on, stripped back, stitched together, woven, layered,
carved out, baked in, distilled, unpacked, crystallized, sharpened, surfaced,
amplified, anchored, framed, mapped, cemented, bridged, threaded, forged,
tightened, unlocked, seeded, cultivated, nurtured, wrestled with, untangled,
peeled back, dialled in, doubled down.

Replace with a literal verb that names the decision: cut, added, removed,
changed, joined, caused, showed, explained, reduced, clarified, fixed, named,
listed, compared, chose, rejected, delayed, measured, rewrote.

The rewrite usually exposes a missing fact, which is the real value of the
check:

- "We sanded down the onboarding." → "We cut onboarding from 6 steps to 3."
- "The insight is baked into the product." → "Every screen shows the cost
  before the user commits."
- "We unpacked the failure." → "We found the retry loop had no backoff."
- "Their strategy is anchored in trust." → "They publish every incident
  report within 48 hours."

Note the pattern: the literal version needs a number, a name, or a mechanism.
The metaphor existed to avoid supplying one.

## Adjacent, already covered elsewhere

Do not double-flag. These live in SKILL.md or `patterns.md`:

- Two-image contrast with no instruction ("less a hammer, more a scalpel")
- X-of-Y shorthand ("the Excel of AI agents")
- Promotional and tourism-brochure prose ("a thriving ecosystem")
- Fake profundity ("that number tells a story")

## Where this rule is wrong

A metaphor that carries real load is good writing, and stripping every image
produces the flat register this skill spends the rest of its length arguing
against. Three cases to leave alone:

- The subject has no literal vocabulary yet. New technical work often has
  only borrowed words.
- The metaphor is the field's standard term. `garbage collection`,
  `handshake`, `inheritance`, `pipeline`, `bottleneck`. These are names,
  not images. Do not flag them.
- The writer's own voice runs on imagery and the piece is theirs to sign.
  Flag the frequency if it is high; do not neutralise the voice.
