# Optional methods

Read only the row relevant to the obstacle. These are techniques to try, not universal performance guarantees.

| Obstacle | Method | Observable output | Limitation |
| --- | --- | --- | --- |
| Details obscure the governing rule | Step back to the relevant principle, then apply it to the actual case | A short principle and its application | A true general rule can still be misapplied; verify conditions |
| User starts with a favored solution | Compare that solution with a simpler baseline and a genuinely different approach | Tradeoffs tied to the user's success criteria | Preserve explicit requirements; avoid contrarianism for its own sake |
| A consequential factual claim may be wrong | Formulate a specific verification question and check an original source or tool result | Claim, source, conclusion, remaining uncertainty | Repeating the same model answer is not external corroboration |
| One approach may dominate through anchoring | Generate genuinely different candidates before comparing them | Distinct mechanisms, failure modes, and a selection rationale | Separate calls can reduce shared context but still share model biases |
| Several solutions address a checkable reasoning problem | If supported and warranted, use multiple independently generated candidates and compare their final answers | Agreement/disagreement and a separate correctness check | Majority agreement can be wrong; does not establish the best subjective strategy |
| A plan looks plausible but may fail in practice | Pre-mortem and falsification | Most consequential failure condition plus a small test | Imagined failure is a hypothesis, not observed evidence |
| A finished document may rely on hidden context | Review from the intended reader's perspective using only the artifact | Missing information and unclear implications | Clarity review does not fact-check the claims |

## Useful checks by task type

- **Workflow:** compare time and error rates on representative cases against the current process.
- **Recommendation:** identify the condition that would reverse the ranking and how to verify it.
- **Analysis:** reconcile totals to the source and investigate exceptions that affect the conclusion.
- **Software:** reproduce the relevant behavior and check the actual user path or functional result.
- **Writing:** ask a target reader to identify the main claim, supporting evidence, and next action.
- **Prompt improvement:** check that the rewritten prompt preserves the user's requested deliverable, constraints, and permissions.

Use a minimum sufficient check. Report whether it was executed, its actual result, and its limits.
