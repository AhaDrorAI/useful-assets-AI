---
name: strategic-build
description: Decide whether a piece of build work is worth doing, and how much effort it deserves, using Shreyas Doshi's LNO effort framing and three levels of product work (impact, execution, optics), pre-mortems, and Marty Cagan's empowered-team vs feature-team lens. Use when the user asks "should I build this?", "is this worth it?", "what should I prioritise?", is about to make a reusable abstraction or architectural bet, is evaluating a feature request, suspects busy-work or "product theater", or wants a pre-mortem before a big build. Not for detailed sprint planning or code-level design.
metadata:
  last_reviewed: "2026-11-18"
  review_every_days: "180"
---

# Strategic Build

Help the user put effort where it compounds, and spend as little as possible where it does not.

This skill is a judgment aid, not a scoring machine. Each lens below asks a question. Use the lenses the decision needs, state what each one shows, and give a recommendation. Do not run all of them on a small decision.

## Source note

The frameworks are paraphrased from public talks and writing by Shreyas Doshi (LNO, the three levels, pre-mortems) and Marty Cagan (*Empowered*). The wording here is a summary, not a quotation. Do not present any sentence in this file to the user as a direct quote. If the user wants the original, point them to the authors' own writing.

## Choose the lens

| The user's question | Lens |
|---|---|
| "Is this task worth doing well?" / "I'm drowning in tasks" | 1. LNO effort |
| "Why do we keep disagreeing about this?" / "We shipped but nothing moved" | 2. Three levels |
| "We're about to commit to a big build or bet" | 3. Pre-mortem |
| "We just get handed features to build" | 4. Empowered vs feature team |
| "Should I make this reusable / abstract it now?" | 5. Abstraction timing |

If the request matches more than one row, use at most two lenses and say which you used.

## 1. LNO: match effort to return

Classify each task by the return on doing it **well**:

- **Leverage (L):** doing it well returns many times the effort. Examples: a decision that shapes months of work, a core interface many features will use, a key hire.
- **Neutral (N):** the return is roughly proportional to the effort. Most routine work.
- **Overhead (O):** it must get done, but doing it well returns little. Examples: routine status updates, expense forms, minor formatting.

The point of LNO is effort allocation, not deletion. Overhead tasks often still have to be done.

- For L tasks: give full attention and the best hours. Do them excellently.
- For N tasks: do them well enough, without perfectionism.
- For O tasks: do them fast and "good enough", batch them, delegate or automate them. Skip an O task only if nothing depends on it, and say what you assumed.

Signals that a task is Leverage: other work is blocked on it; it will be reused or relied on repeatedly; it is hard to reverse; it changes what the user learns about users or the market. Treat these as signals for judgment, not as a points system.

**Output:** a short table: task, class (L/N/O), one-line reason, recommended effort level.

## 2. Three levels: impact, execution, optics

Any piece of work can be judged at three levels:

- **Impact:** does it change an outcome that matters (users, revenue, learning)?
- **Execution:** is it being built well and delivered reliably?
- **Optics:** how it is perceived and communicated.

Two uses:

1. **Diagnose disagreement.** People who argue about a plan often argue at different levels: one about impact, one about execution. Name the level each position is at.
2. **Check the order.** If the impact of the work is unclear, settle that first. Excellent execution of work with no impact is wasted. Optics matter, but they cannot replace impact.

**Output:** for the work in question, one line per level: what is known, what is unclear. If impact is unclear, recommend the one question or test that would settle it before more execution.

## 3. Pre-mortem

Use before a build that is expensive or hard to reverse.

1. Assume the work has failed six months from now.
2. List the reasons it failed. Aim for breadth: users, technology, data, team, timing, dependencies.
3. Pick the risks that are both likely and severe. Usually 2 to 4 risks meet both tests; use judgment, do not force a number.
4. For each, give a mitigation or a cheap test that would reveal the risk early.
5. Recommend: build as planned, build with changes, run a test first, or do not build.

Base each risk on the user's situation. If a risk is generic ("scope creep"), make it specific to this project or drop it.

## 4. Empowered team vs feature team

From Cagan: a **feature team** is handed a list of features and measured by delivery. An **empowered team** is handed a problem and measured by whether the outcome moved.

Use this lens when the user receives feature requests without the problem behind them.

- Restate the feature request as the problem it is meant to solve and the outcome that would show it worked.
- If the user cannot name the problem, recommend asking the requester before building.
- If the user is a solo builder, apply the same test to their own feature ideas.

Do not lecture the user about their organisation. Help them reframe the request in front of them.

## 5. Abstraction timing

When asked to make something reusable:

- If the code has one real use, build it specifically.
- If it has two uses, duplicate with care and note the shared shape.
- If it has three or more real uses, or a confirmed upcoming third, extract the shared version.

This "rule of three" is a heuristic. Override it when the cost of divergence is high (security, money, data integrity), and say why.

## Recommendation format

End with:

```text
Recommendation: [build / build with changes / test first / defer / do quickly and move on]
Why: [the one or two findings that decided it]
Lens(es) used: [...]
What would change this: [the observation that would reverse the recommendation]
```

## Boundaries

- Do not invent examples about real companies or people. If an illustration helps, label it as hypothetical.
- Do not push the user to drop work they have already decided to do. If you disagree, say so once with the reason, then help them do it well.
- If a decision depends on data the user has not shared (usage numbers, revenue, deadlines), ask for it or state the assumption.
