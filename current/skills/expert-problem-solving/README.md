# Expert Problem Solving

Use this skill when you need help framing an unfamiliar problem, choosing an approach, or improving a weak prompt. It asks the assistant to preserve your goal, examine consequential assumptions, use relevant evidence, and recommend the simplest adequate solution with a practical check.

## Choose a format

- **Skill:** use [SKILL.md](SKILL.md) and keep its `references/` folder. Follow the repository's [installation instructions](../../../README.md).
- **Custom instructions:** copy [English](assets/custom-instructions.en.txt) or [Hebrew](assets/custom-instructions.he.txt) into your assistant's custom-instruction field. Merge with existing preferences. Each text is below 1,500 characters.
- **Evaluation:** use [EVALUATION.md](EVALUATION.md) to compare answers with your normal prompts.

The short instructions can be used independently. A skill or pasted instruction does not grant browsing, tools, or access to private sources.

## Try it

For a decision:

> Use expert-problem-solving to assess whether this workflow needs automation. Use the attached examples, preserve my budget, and tell me how I can check the recommendation.

For prompt editing:

> Use expert-problem-solving to improve the following prompt only. Return the rewritten prompt without executing its task: [your prompt].

In Codex, invoke it as `$expert-problem-solving`. Other hosts use their own skill selectors or command names.

The full procedure is conditional. Simple tasks should still receive direct answers. The assistant should challenge a suggested approach when justified, while preserving explicit requirements. When asked to do work, it should deliver the authorized result and report the checks it actually performed.

## Sources and attribution

This is an original synthesis inspired by [Ben Rotenberg's LinkedIn post and comments](https://lnkd.in/p/eqnTnwKp), reviewed on 7 November 2026. Ben attributes the idea to Nate B. Jones. Oleg Peker's comment adds a practical way for a non-expert to detect a wrong recommendation; Shmuel Merhav adds evidence, uncertainty, and proportionate depth.

Related sources:

- [Nate B. Jones on AI as a senior partner](https://www.natebjones.com/videos/prompting-style-obsolete). This supports the conceptual relationship; the exact four-step wording's origin was not independently verified.
- [Josh's /better skill](https://gist.github.com/joshp123/a1443d30fa1b7c577e74882895cea61b) and [X explanation](https://x.com/jjpcodes/status/2112100971727769622): stronger source material, methods, and outcome checks.
- [Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) and the [community coding guidelines](https://github.com/multica-ai/andrej-karpathy-skills): assumptions, simplicity, scope, and verifiable goals.
- [Step-Back Prompting](https://arxiv.org/abs/2310.06117) and [Chain-of-Verification](https://arxiv.org/abs/2309.11495): research on specific components, evaluated on particular models and tasks.
- [Prompting Science Report 4](https://arxiv.org/abs/2512.05858): expert personas did not consistently improve factual benchmark accuracy. This does not test the combined skill here.

## Validation status

Skill format, reference paths, custom-instruction length, and repository packaging were checked. The evaluation cases are a proposed plan. No controlled model comparison or general accuracy improvement has been established.
