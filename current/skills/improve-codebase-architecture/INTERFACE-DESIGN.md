# Designing the deepened interface

Read this during Step 6, once the user has chosen a candidate and the discussion turns to what the new interface should look like.

## Contents

- Generate alternatives before converging
- Pressure-testing a proposed interface
- Common shapes
- When to stop

## Generate alternatives before converging

Offer two or three genuinely different shapes, not one shape with cosmetic variations. Different means the caller's mental model differs, not the parameter list. Name the tradeoff each one makes and say which you would choose, so the user is picking between positions rather than being asked to do the design.

Useful axes to vary:

- **Where the decision lives** — does the caller choose the strategy, or does the module infer it?
- **How state is carried** — argument, constructor, ambient context, returned handle?
- **What the module refuses** — a narrower interface that rejects more inputs is often the deeper one, because every rejected case is a case the caller no longer reasons about.
- **How errors surface** — thrown, returned, or made unrepresentable by the types.

## Pressure-testing a proposed interface

Walk each candidate interface through these before settling:

- **Name the callers.** Every current caller must be expressible. One that is not is either a missed requirement or a caller that should not exist — decide which, out loud.
- **Add the next feature.** Take something plausibly coming and check whether it fits behind the interface or forces it open. An interface that only fits today's callers is not deep, only fitted.
- **Write the test signature.** If a good test is awkward to write against the interface, the interface is wrong. The interface is the test surface.
- **Count the adapters.** One is hypothetical. If no second adapter is coming — not even a fake — question whether the seam belongs there.
- **State the invariants.** Anything a caller must maintain that the types do not enforce is part of the interface, and every one of them makes it wider. Can any be enforced instead of documented?

## Common shapes

- **Facade over a cluster** — the fix when understanding one concept means opening five files. Deepest when the cluster becomes genuinely private afterwards; if callers still reach past it, nothing was hidden.
- **Port with adapters** — the fix when a concrete dependency has leaked across a seam. Justified by the second adapter, which is usually the test fake.
- **Parse, don't validate** — return a type that makes the invalid state unrepresentable rather than a boolean plus a convention. Removes error modes from the interface entirely, which is the largest depth gain available for the least code.
- **Collapse the pass-through** — sometimes the answer is deletion. The deletion test said complexity vanishes, so merge the module into its caller. This is a collapse candidate rather than a deepening one: worth doing, never the headline, and usually absorbed into whichever deepening supersedes it.

## When to stop

Stop when the interface is described well enough that someone could implement it without asking you a question, and the user can say what would go behind it. That is the decision. Hand it to the spec or ticket flow — writing the code is a separate session, with a fresh context window and the decision as its input.
