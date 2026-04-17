# Prompt: Regenerate the IEEE Paper Title If Needed

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
- `baseline-solution/prompts/16-ieee-abstract-refresh-prompt.md`
- the current IEEE manuscript source in:

```text
/home/daniel/git/electroai-hackathon/ElectroAIHackathonIEEETemplate/
```

In particular, read the current:
- title,
- abstract,
- introduction,
- methods,
- results,
- discussion,
- conclusion.

The manuscript has evolved through multiple prompt-driven revisions, so the original title may no longer be the best fit for the final framing, method, or findings.

---

## Task

Review the current paper title and determine whether it still accurately and effectively represents the manuscript.

If the current title is still appropriate:
- keep it,
- and provide a short note stating that no regeneration was necessary.

If the title is outdated, too narrow, too broad, or misaligned with the manuscript:
- regenerate it,
- and replace it with a revised title better suited to the current paper.

This task is therefore:

1. evaluate the current title,
2. regenerate it **if needed**,
3. ensure the final title matches the current manuscript.

---

## Required Evaluation Criteria

Check whether the current title accurately reflects:

1. the core problem addressed by the paper,
2. the multi-agent nature of the study,
3. the schematic-image reconstruction focus,
4. the use of Falstad and LTSpice artefacts or simulator-oriented outputs,
5. the benchmarking or comparative nature of the work,
6. the final scope and emphasis of the manuscript.

If the manuscript emphasis has shifted materially, the title should be refreshed.

---

## If Regeneration Is Needed

The regenerated title must:

### 1. Represent the actual paper scope

The title should reflect the current paper as it now exists, not an earlier project concept.

It should align with themes such as:
- AI-based schematic understanding,
- multi-agent comparison,
- circuit reconstruction from images,
- Falstad/LTSpice or simulator-oriented artefact generation,
- structural fidelity or reconstruction quality.

### 2. Be concise and IEEE-appropriate

The title should be:
- technically clear,
- reasonably compact,
- academically credible,
- and specific enough to convey the paper’s contribution.

Avoid titles that are:
- too vague,
- overly promotional,
- or excessively long.

### 3. Balance accuracy and readability

The title should be informative without becoming a full sentence.

It may use a subtitle if that improves clarity, for example:
- a question or broad framing clause,
- followed by a more specific description of the benchmark or reconstruction task.

Use a subtitle only if it materially improves the title.

### 4. Match the final abstract and contribution

The final title should feel consistent with the current abstract and the actual emphasis of the manuscript.

---

## Writing Requirements

The title must:
- be formal,
- avoid hype,
- avoid buzzword stacking,
- avoid claims stronger than the paper supports.

Prefer:
- clear engineering language,
- emphasis on schematic reconstruction or circuit understanding,
- a direct indication of the comparative or benchmark nature of the study if relevant.

Avoid:
- vague “AI for engineering” titles,
- overclaiming full automation or general intelligence,
- novelty claims that are not supported by the manuscript.

---

## Output Format

Produce:

1. a determination of whether title regeneration was necessary,
2. the final title,
3. optionally 2–3 alternative candidate titles if useful,
4. and, if appropriate, an updated IEEE manuscript source with the title revised.

If the current title is retained, state that explicitly.

If editing the LaTeX source directly:
- preserve the document formatting,
- update only the title line unless a tiny consistency edit is essential.

---

## Acceptance Criteria

The output is complete when:

1. the existing title has been checked against the current manuscript,
2. a new title is generated only if needed,
3. the final title accurately reflects the current paper,
4. it is concise, technical, and IEEE-appropriate,
5. it is suitable for direct inclusion in the manuscript.

---

## Done

After completing the task:

1. summarise whether the title was retained or regenerated,
2. note whether the paper source was edited directly,
3. add a dated entry to `work-diary.md` describing:
   - that the title-refresh prompt was created,
   - that it checks whether regeneration is necessary before rewriting,
   - any important writing constraints captured in the prompt.

Sign the diary entry with your model/agent identifier.
