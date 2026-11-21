# Steering blocks

> **Reconstructed file.** The uploaded copy of this skill named this file but did not contain it. This version was rebuilt on 2026-11-18 from the six block names in SKILL.md's diagnosis table. It is not copied from Anthropic's Fable 5 prompting guide. If you have the original file, replace this one with it.

Each block exists to correct one failure mode. Include a block only if you can name how this specific task would produce that failure. Paste the **Text** line verbatim into the prompt.

## 1. Scope discipline

- **Use when:** the deliverable is something to be *made* (a file, code, a document), and the request names its boundaries.
- **Skip when:** the task is open exploration, or the user asked for suggestions beyond the brief.
- **Failure it corrects:** the model adds features, files, sections or refactors nobody asked for.
- **Text:** "Deliver what is asked and stop there. If you see a worthwhile addition, list it at the end as a suggestion instead of building it."

## 2. Assess, don't act

- **Use when:** the deliverable is something to be *found out* (a diagnosis, a review, an assessment).
- **Skip when:** the user asked for the fix as well as the diagnosis.
- **Failure it corrects:** the model starts changing things while it was asked only to look.
- **Text:** "This is an assessment. Report what you find and what you would change, but do not make the changes."

## 3. Evidence grounding

- **Use when:** the turn is long (many tool calls, many files, research) and claims will pile up.
- **Skip when:** the answer is short and comes from material the user pasted.
- **Failure it corrects:** confident claims that no file, source or tool result supports.
- **Text:** "Tie each factual claim to the file, source or result it came from. If a claim rests on inference, say so."

## 4. Self-verification

- **Use when:** the output can be checked: code that can run, numbers that can be recomputed, links that can be opened.
- **Skip when:** the output is subjective (tone, style) or nothing can be executed.
- **Failure it corrects:** the model reports success without checking.
- **Text:** "Before you report the result, check it: run it, recompute it, or open it. Report what you checked and what you could not check."

## 5. Re-grounded summary

- **Use when:** the turn is long enough that the final answer might drift from the original request.
- **Skip when:** the task is one answer in one step.
- **Failure it corrects:** the final message summarises the work done instead of answering the question asked.
- **Text:** "End by restating the original request in one line, then answer it directly."

## 6. Act, don't survey

- **Use when:** the goal is clear but the route is open, and the user wants a result, not a plan.
- **Skip when:** the user asked for options or a plan before any work.
- **Failure it corrects:** the model lists approaches and asks which to take instead of taking the best one.
- **Text:** "Pick the approach you judge best and carry it out. Mention the main alternative in one line at the end."
