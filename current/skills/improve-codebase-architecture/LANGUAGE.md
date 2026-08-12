# Architecture vocabulary

Full definitions for the terms SKILL.md summarises. Read this when a candidate is hard to phrase, when a term feels fuzzy, or when deciding whether something really is shallow.

## Contents

- Core terms: module, interface, implementation, adapter
- Properties: depth, seam, leverage, locality
- Principles: deletion test, test surface, adapter counting, cost of shallowness
- Words to avoid, and why

## Core terms

**Module** — anything with an interface and an implementation. Deliberately scale-agnostic: a function, a class, a package, and a slice spanning three tiers are all modules. The concept works the same at every size, which is why one word covers all of them.
*Avoid:* unit, component, service.

**Interface** — everything a caller must know to use the module correctly. The type signature is the visible part and usually the smaller one. The rest: invariants the caller must maintain, ordering constraints, error modes, required configuration, performance characteristics, and any state left behind. When measuring whether a module is shallow, measure this, not the signature.
*Avoid:* API, signature. Both name only the type-level surface, which is exactly the part that misleads.

**Implementation** — the code inside the module.

**Adapter** — a concrete thing satisfying an interface at a seam. Size of adapter and size of implementation are independent: a Postgres repository is a small adapter over a large implementation; an in-memory fake is a large adapter over almost nothing.

## Properties

**Depth** — the ratio of behaviour to interface. A deep module hides a great deal behind a small, stable surface. A shallow one has an interface nearly as complex as the code beneath it, so a caller must understand the implementation to use it — which means the module is not hiding anything, only adding a hop.

Depth is not about line count. A 30-line module can be deep and a 3,000-line one shallow. The question is always: how much does a caller have to know?

**Seam** — the place where an interface lives, and therefore the place behaviour can be altered without editing code in place. Seams are where tests, fakes, and future variation attach. Missing seams are why legacy code resists testing.
*Avoid:* boundary. Too vague; it gets used for module edges, layer edges, and network edges interchangeably.

**Leverage** — what callers get from depth: a lot of capability for a little knowledge.

**Locality** — what maintainers get from depth: change, bugs, and knowledge concentrated in one place instead of smeared across callers. When a bug in one concept requires edits in five files, the concept has no locality. Locality is usually the more persuasive half of a candidate's benefit, because it is what the reader has personally suffered.

## Principles

**The deletion test.** Imagine the module deleted and its work inlined into every caller.

- Complexity **vanishes** → it was a pass-through. Deleting it is the improvement. This is a **collapse candidate**.
- Complexity **reappears, duplicated across N callers** → it was earning its keep, and probably deserves to be deeper still. This is a **deepening candidate**.

Both are real findings. They are not equal: a deepening candidate removes knowledge from callers, while a collapse candidate only removes a hop, so only the first can be ranked `Strong`. Where a deepening supersedes a pass-through — the pass-through disappears into the new module's implementation — report the deepening and mention the collapse inside it rather than as separate work.

This test is the main defence against generic cleanup advice, because it asks what the module *does for callers* rather than whether it looks tidy.

**The interface is the test surface.** Tests written against the interface survive refactors of the implementation; tests written against internals break on every change and get deleted. So "which tests get simpler" is a real measure of a proposed deepening, not a rhetorical flourish — if a candidate does not change what the tests can address, be suspicious of it.

**One adapter is a hypothetical seam; two adapters is a real one.** A single implementation behind an interface has never had to prove the interface is right. The second implementation is what tests it. Treat single-adapter abstractions as unvalidated, and be wary of proposing seams no second adapter is coming for.

**Shallowness has a compounding cost.** Each shallow module adds a hop without removing knowledge, so understanding one concept means opening five files. This is why the friction shows up as "I can't hold this in my head" long before it shows up as a bug.

## Words to avoid, and why

| Avoid | Use | Why |
|---|---|---|
| component, service, unit | module | Those words carry framework and deployment baggage; module is scale- and stack-neutral. |
| API, signature | interface | Both name only the type-level surface, hiding the invariants and error modes that make a module shallow. |
| boundary | seam | Overloaded across module, layer, and network edges. |
| "cleaner", "better structured" | locality, leverage | Unfalsifiable. Locality and leverage name a benefit the reader can check. |

Consistency is the point. A report that mixes vocabularies reads as generic advice, and generic advice gets skimmed.
