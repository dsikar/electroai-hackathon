# Prompt: Write the IEEE Results Section for the Multi-Agent Circuit Reconstruction Study

## Context

Read the following before starting:
- `work-diary.md`
- `baseline-solution/prompts/09-ieee-methods-section-prompt.md`
- `baseline-solution/prompts/04-output-spec-prompt.md`
- `baseline-solution/docs/web-pipeline-app.md`
- `baseline-solution/simulations/`
- `baseline-solution/images/`
- `ElectroAIHackathonIEEETemplate/` (the IEEE paper directory)
- the current IEEE manuscript source, e.g. `ElectroAIHackathonIEEETemplate/conference_101719.tex`

This repository already contains generated Falstad and LTSpice artefacts for multiple circuits and agents, including:
- Falstad plain-text and XML outputs,
- Falstad preview PNGs,
- LTSpice `.asc`,
- LTSpice SVG/PNG previews,
- per-task reports describing issues, assumptions, missing information, and inconsistencies.

Your job is to write a **Results section** for the IEEE paper based on the artefacts that are actually present in the directory.

---

## Task

Write a paper-ready **Results section** that discusses the observed outcomes of the multi-agent circuit-reconstruction pipeline.

The discussion must focus on:

1. the **partial success of the first four circuits**, and
2. the **failure of the last four circuits**.

You must ground the discussion in the artefacts present in the repository rather than inventing results.

In addition, you must:
- select relevant Falstad and LTSpice images already present in `baseline-solution/simulations/`,
- copy those image files into the IEEE paper directory,
- and reference them appropriately in the Results discussion so they can be incorporated into the manuscript.

---

## Required Interpretation

### 1. Split the results into two phases

Structure the analysis around:

- **Circuits 1–4:** partial success
- **Circuits 5–8:** failure or strong degradation

You must discuss this split explicitly and treat it as a meaningful result rather than a casual observation.

### 2. Partial success for the first four circuits

For the first four circuits, discuss what “partial success” means in terms of the available artefacts.

Examples of evidence you may draw on:
- Falstad previews that show recognizable but imperfect circuit structures,
- LTSpice previews that contain plausible but incomplete or structurally inconsistent schematic representations,
- report files that indicate validation issues rather than total collapse,
- visible differences between agents in reconstruction fidelity,
- cases where one modality appears stronger than the other.

Be specific about what the artefacts support.

### 3. Failure of the last four circuits

For circuits 5–8, discuss the evidence of failure or severe degradation.

You must comment on artefacts that visibly or textually suggest failure, for example:
- sparse or nearly empty Falstad outputs,
- low-information or low-variance previews,
- placeholder-style or malformed outputs,
- reports indicating substantial inconsistencies or missing information,
- outputs that do not preserve recognizable circuit topology,
- modality degradation in both Falstad and LTSpice views.

Make the failure discussion evidence-led.

### 4. Agent comparison

Discuss differences between:
- Codex
- Claude
- Gemini

But do so only to the extent that the existing artefacts support such claims.

If the artefacts suggest, for example:
- Claude produced the strongest Falstad reconstructions,
- Codex achieved some structurally meaningful but incomplete outputs,
- Gemini frequently degraded to sparse or weak reconstructions,

then say so carefully and tie the claim to observable outputs or report contents.

### 5. Dual-modality interpretation

Your Results discussion must treat Falstad and LTSpice as two complementary modalities.

Comment on whether:
- failures appear in both modalities,
- one modality remains more interpretable than the other,
- Falstad previews are more immediately useful for visual inspection,
- LTSpice previews reveal different classes of structural error.

### 6. Artefact-driven commentary

You must explicitly discuss **aspects of the results that are evident in the files already present in the directory**.

This means the Results section should refer to concrete signals visible in artefacts such as:
- preview images,
- report files,
- file completeness,
- validation findings,
- presence of low-content or placeholder outputs.

Do not write a generic “the results were mixed” section.

---

## Figure Requirements

### 1. Select representative images

Choose a small number of representative Falstad and LTSpice figures from the existing outputs.

Use images that best illustrate:
- a partial success case from circuits 1–4,
- a failure case from circuits 5–8,
- and, if useful, a contrast between agents or modalities.

Prefer already-generated artefacts such as:
- `*_falstad.png`
- `*_falstad_full.png`
- `*_ltspice.png`
- `*_ltspice.svg`

### 2. Copy images into the IEEE directory

Copy the selected image files into the IEEE paper directory so they can be included in the manuscript.

Use a clear destination under the IEEE workspace, for example:

```text
ElectroAIHackathonIEEETemplate/figures/
```

If that directory does not exist, create it.

Use sensible filenames that preserve agent/circuit meaning.

### 3. Refer to figures in the text

The Results draft should mention the copied figures in a paper-appropriate way, e.g.:
- “Fig. X shows…”
- “Representative Falstad reconstructions are shown in Fig. X…”
- “The LTSpice outputs in Fig. Y illustrate…”

If editing LaTeX directly, also add or prepare the corresponding figure includes.

---

## Writing Requirements

Write in IEEE paper style:
- formal,
- concise,
- technical,
- evidence-based,
- no hype,
- no casual diary tone.

The Results section should:
- interpret outcomes,
- compare observed performance,
- connect visual artefacts to technical implications,
- avoid unsupported claims.

Avoid:
- speculative claims not supported by the artefacts,
- generic statements with no evidence,
- excessive repetition of filenames in the prose.

---

## Output Format

Produce:

1. a **paper-ready Results section draft**, and
2. if appropriate, updated paper source or figure insertions in the IEEE manuscript directory.

If you edit the paper source directly:
- preserve IEEE formatting conventions,
- keep the prose consistent with the rest of the paper,
- and ensure the copied figure paths match the manuscript.

If you do not edit directly, provide clean prose and identify which figure files were copied.

---

## Acceptance Criteria

The output is complete when:

1. it discusses the **partial success of circuits 1–4**,
2. it discusses the **failure of circuits 5–8**,
3. it references evidence visible in the current artefacts,
4. it compares agents and modalities where justified,
5. it includes representative Falstad and LTSpice image selections,
6. those images are copied into the IEEE paper directory,
7. the text is suitable for direct incorporation into the IEEE Results section.

---

## Done

After completing the task:

1. summarise what was written,
2. list which images were copied into the IEEE directory,
3. note whether the paper source was edited directly,
4. add a dated entry to `work-diary.md` describing:
   - that the IEEE Results-section prompt was created,
   - that it focuses on partial success for the first four circuits and failure for the last four,
   - that it requires copying representative Falstad and LTSpice images into the IEEE paper directory.

Sign the diary entry with your model/agent identifier.
