---
name: fable-5-prompt-writer
description: Writes a single, ready-to-paste task prompt tuned to Claude Fable 5 and Claude Mythos 5 behavior. Use this whenever the user wants a prompt for Fable 5 or Mythos 5, says they are "about to ask Fable to..." or "how should I word this for Fable 5", mentions Fable/Mythos prompting, or hands over a rough task description and wants it turned into a prompt for those models. Also use it when the user is drafting any substantial one-off request for Fable 5 — a build, an analysis, a research task — even if they never say the word "prompt".
---

# Fable 5 prompt writer

Turn a user's rough intent into one prompt they can paste into a chat with Claude Fable 5 or Claude Mythos 5.

## The whole point: subtract, don't assemble

The Fable 5 prompting guide lists roughly a dozen steering snippets. It is tempting to treat that as a checklist and staple all of them onto every prompt. Don't. The same guide warns that prompts and skills built for earlier models are often *too prescriptive* for Fable 5 and actively degrade its output. Fable 5 follows instructions well enough that a short, targeted nudge does the work that used to require enumerating every behavior by name.

Each steering block you add is a bet that the task will produce the behavior it corrects. Bet wrong and you have spent the model's attention correcting something that was never going to happen, while diluting the instructions that mattered.

So the selection criteria in the reference file do the deciding — each block's "use when" and "skip when" lines, checked against this specific task. Not a sense of how many a good prompt ought to have. **None is a legitimate answer.** A simple, well-framed task needs no steering at all, and adding some to look thorough makes the prompt worse.

## What is out of scope here

This skill produces a *chat prompt*. Everything below is harness-level and must never appear in the output, no matter how prominent it is in the guide:

- Effort settings (`high`, `xhigh`) — an API parameter, not prompt text
- `send_to_user` tool definitions
- Subagent delegation instructions — unless the user says they are in Claude Code or another harness that has subagents
- Memory-file conventions ("store one lesson per file")
- Context-budget reassurance ("you have ample context remaining")
- Autonomous-pipeline reminders ("the user is not watching") — the user *is* watching; that is what a chat is
- Client timeout and streaming advice

If the user's situation genuinely calls for one of these, say so in a sentence *outside* the prompt. Don't smuggle it in.

## Step 1: Do you have enough to write?

Interview only if the brief is thin. A brief is thick enough when you can answer all three:

1. **What is the deliverable?** A file, a decision, a diagnosis, an explanation.
2. **What is it for?** Who reads it or runs it next, and what does it unblock. This one is load-bearing — see the intent frame below.
3. **What does "done" look like?** The condition that makes the answer correct rather than merely plausible.

If two or more are missing, ask — at most three questions, and prefer offering candidate answers over open-ended prompting. If only one is missing and you can infer it credibly, infer it and state the assumption when you hand over the prompt. Fable 5 handles ambiguity well; a prompt does not need every corner nailed down, it needs the *purpose* clear.

## Step 2: Diagnose the task

Read the task against these three axes. The answers select the blocks.

| Axis | Question | Pulls in |
|---|---|---|
| **Deliverable** | Is the user asking for something to be *made*, or for something to be *found out*? | Made → scope discipline. Found out → assess-don't-act. |
| **Turn shape** | One answer, or a long stretch of tool calls and building? | Long → evidence-grounding, self-verification, re-grounded summary. |
| **Specification** | Is the goal clear but the route open? | Open route → act-don't-survey. |

Then read `references/steering-blocks.md` and pull only what the diagnosis calls for. That file has each block's text and the failure mode it exists to correct — if you can't name the failure mode this task would produce, don't include the block.

## Step 3: Compose

```
[Intent frame — 1-3 sentences]

[The task — plainly stated, including any constraints and inputs]

[Done condition — what makes this correct]

[Steering blocks the diagnosis selected — verbatim from the reference file, if any]
```

**The intent frame is the highest-value part of the whole prompt** and the one users most often skip. Fable 5 connects a task to relevant knowledge much better when it knows what the work is *for*, because it can infer the hundred small judgment calls you didn't specify. Shape:

> I'm working on [the larger effort] for [who it's for]. They need [what the output enables]. With that in mind: [request].

Fill it from the interview. Never leave the brackets in the output — a prompt with unfilled placeholders is not a finished prompt.

## The reasoning-extraction trap

Watch for this one, because users ask for it constantly and it backfires specifically on Fable 5.

If the user wants "show me your reasoning", "explain your thinking step by step", or "walk me through how you got there," **do not write that into the prompt.** Instructions to echo, transcribe, or narrate internal reasoning can trip Fable 5's reasoning-extraction safety classifier, which returns a refusal and, in API setups, silently falls back to Opus 4.8. The user gets a worse model and no idea why.

Rewrite it as a request for a *rationale on the decision*, which is a legitimate deliverable and gets them what they actually wanted:

- Instead of "explain your reasoning as you go" → "for each recommendation, give the evidence it rests on and the main alternative you rejected"
- Instead of "show your thinking" → "state the assumption behind each estimate"
- Instead of "think out loud through the tradeoffs" → "name the two or three tradeoffs that decided this and where each one landed"

The distinction: asking about the *substance of a judgment* is fine; asking for a transcript of the model's internal process is what trips it. Mention the swap when handing over the prompt — it's non-obvious and the user should know why.

## Step 4: Hand it over

Output the prompt in a fenced code block so it can be copied cleanly, and nothing else inside that block.

After the block, three lines maximum:
- Any assumption you inferred rather than asked about
- Why you chose the blocks you chose (one clause each — the user should be able to overrule you)
- A harness-level note *only if* one genuinely applies (e.g. "if your interface exposes an effort setting, this is a `high` task")

Do not explain the Fable 5 guide back to the user. They wanted a prompt.
