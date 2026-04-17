# Prompt: Regenerate the IEEE Abstract If Needed

## Context

Read the following before starting:
- `work-diary.md`
- `baseline-solution/prompts/09-ieee-methods-section-prompt.md`
- `baseline-solution/prompts/10-ieee-results-section-prompt.md`
- `baseline-solution/prompts/11-ieee-related-work-prompt.md`
- `baseline-solution/prompts/12-ieee-discussion-prompt.md`
- `baseline-solution/prompts/13-ieee-introduction-prompt.md`
- `baseline-solution/prompts/14-ieee-conclusion-prompt.md`
- `baseline-solution/prompts/15-ieee-future-work-prompt.md`
- the current IEEE manuscript source in:

```text
/home/daniel/git/electroai-hackathon/ElectroAIHackathonIEEETemplate/
```

In particular, read the current:
- abstract,
- introduction,
- methods,
- results,
- discussion,
- conclusion,
- and future work (if already added).

The manuscript has evolved through multiple prompt-driven updates, so the abstract may now be outdated or may no longer reflect the final paper structure and findings accurately.

---

## Task

Review the current abstract in the IEEE manuscript and determine whether it still accurately reflects the paper.

If the current abstract is still aligned with the manuscript:
- keep it,
- and provide a short note stating that no regeneration was necessary.

If the current abstract is stale, incomplete, or inconsistent with the updated manuscript:
- regenerate it,
- and replace it with a revised abstract suitable for the current paper.

This task is therefore:

1. evaluate the existing abstract,
2. regenerate it **if needed**,
3. ensure the final abstract matches the current manuscript.

---

## Required Evaluation Criteria

Check whether the current abstract accurately reflects:

1. the problem addressed by the paper,
2. the multi-agent nature of the study,
3. the use of schematic-image input,
4. the generation of Falstad and LTSpice artefacts,
5. the main reported findings,
6. the overall scope and contribution of the work.

If any of these have materially changed in the current manuscript, the abstract should be refreshed.

---

## If Regeneration Is Needed

The regenerated abstract must:

### 1. State the problem clearly

Describe the problem in concise engineering terms, such as:
- reconstructing machine-usable circuit representations from schematic images,
- evaluating whether modern AI agents can recover meaningful structural circuit information,
- benchmarking multi-agent performance on schematic understanding.

### 2. Summarise the method at a high level

Briefly mention:
- the use of multiple AI agents,
- the schematic-image-to-design pipeline,
- the dual-modality outputs (Falstad and LTSpice),
- and the validation-aware comparison framework.

Do not overload the abstract with implementation detail.

### 3. Summarise the main findings

The abstract must reflect the actual reported findings at a high level.

If supported by the manuscript, this may include:
- mixed performance across agents,
- partial success on simpler circuits,
- degradation or failure on more complex circuits,
- differences in reconstruction quality across modalities and models.

### 4. State the significance

End with a concise statement of what the study contributes, for example:
- a benchmark workflow,
- empirical evidence of current strengths/limitations,
- or a practical framework for evaluating AI-based schematic reconstruction.

---

## Writing Requirements

Write in IEEE abstract style:
- formal,
- compact,
- technically precise,
- self-contained,
- no citations,
- no bullet points.

The abstract should be:
- one coherent paragraph,
- concise but complete,
- aligned with the final manuscript,
- free of hype and overly broad claims.

Avoid:
- vague marketing language,
- unsupported claims,
- too much procedural detail,
- discussion-style interpretation.

The abstract should summarise the paper, not argue it.

---

## Output Format

Produce:

1. a determination of whether regeneration was necessary,
2. the final abstract text,
3. and, if appropriate, an updated IEEE manuscript source with the abstract revised.

If the abstract was retained with only minimal or no changes, state that explicitly.

If editing the LaTeX source directly:
- preserve IEEE formatting conventions,
- update only the abstract section unless other tiny consistency edits are essential.

---

## Acceptance Criteria

The output is complete when:

1. the existing abstract has been checked against the current manuscript,
2. a new abstract is generated only if needed,
3. the final abstract accurately reflects the current paper,
4. it is concise, IEEE-appropriate, and self-contained,
5. it is suitable for direct inclusion in the manuscript.

---

## Done

After completing the task:

1. summarise whether the abstract was retained or regenerated,
2. note whether the paper source was edited directly,
3. add a dated entry to `work-diary.md` describing:
   - that the abstract-refresh prompt was created,
   - that it checks whether regeneration is necessary before rewriting,
   - any important writing constraints captured in the prompt.

Sign the diary entry with your model/agent identifier.
