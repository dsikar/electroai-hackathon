# Prompt: Write the IEEE Introduction Section from the Related Work and Methodology

## Context

Read the following before starting:
- `work-diary.md`
- `baseline-solution/prompts/09-ieee-methods-section-prompt.md`
- `baseline-solution/prompts/11-ieee-related-work-prompt.md`
- `baseline-solution/prompts/12-ieee-discussion-prompt.md`
- the current IEEE manuscript source in:

```text
/home/daniel/git/electroai-hackathon/ElectroAIHackathonIEEETemplate/
```

In particular, read the current versions of:
- the **Related Work** section,
- the **Methods** section,
- and the overall paper framing already present in the IEEE template.

The goal is to write a strong **Introduction section** that is consistent with the manuscript and is explicitly grounded in the existing Related Work and Methodology.

---

## Task

Write a polished **Introduction section** for the IEEE paper.

The Introduction must be derived from and consistent with:

1. the current **Related Work** section,
2. the current **Methods** section,
3. the overall purpose of the paper as currently framed in the IEEE manuscript.

The Introduction should set up:
- the problem,
- the motivation,
- the gap,
- the proposed approach,
- and the contribution of the paper.

---

## Required Coverage

### 1. Problem framing

Introduce the core problem addressed by the paper:
- understanding schematic images,
- reconstructing circuit structure,
- translating diagrammatic information into machine-usable design artefacts,
- and evaluating how well modern AI systems can perform this task.

The framing should make clear why schematic understanding is an important engineering problem rather than just a vision benchmark.

### 2. Motivation from the Related Work section

The Introduction must build naturally from the current Related Work section.

This means it should reflect themes such as:
- the rise of AI tools in engineering workflows,
- the relevance of multimodal and agent-based systems,
- the limitations of existing approaches for structural circuit recovery,
- and the gap identified in the related-work synthesis.

Do not write an introduction that ignores the current Related Work narrative.

### 3. Transition into the methodology

The Introduction must also anticipate the Methods section.

It should introduce, at a high level:
- the multi-agent benchmarking setup,
- the use of Codex, Claude, and Gemini,
- the dual-modality output strategy using Falstad and LTSpice,
- and the role of validation and artefact inspection.

These points should be introduced as motivation and contribution, not as full procedural detail.

### 4. Research gap

The Introduction must clearly state the gap the paper addresses.

Examples of the kind of gap statement expected:
- existing tools do not reliably recover structurally faithful circuit representations from schematic images,
- there is limited systematic comparison of agent systems on this task,
- simulator-ready multi-modality outputs are underexplored,
- validation-aware benchmarking of schematic reconstruction remains limited.

The gap statement should align with the current Related Work and Methods sections.

### 5. Paper contribution

The Introduction must make the paper’s contribution explicit.

Depending on what is already in the manuscript, the contribution statement should cover ideas such as:
- benchmarking multiple AI agents on schematic reconstruction,
- generating Falstad and LTSpice representations from images,
- using a web-based orchestration pipeline,
- validating outputs and surfacing inconsistencies,
- and analyzing success/failure behaviour across circuits of varying complexity.

The contribution statement should be clear and direct.

### 6. Optional paragraph on paper organization

If it fits the style of the existing manuscript, conclude with a short paragraph summarising the paper structure, e.g.:
- Section II covers related work,
- Section III covers methods,
- Section IV presents results,
- etc.

Only include this if it is consistent with the rest of the manuscript.

---

## Writing Requirements

Write in IEEE style:
- formal,
- concise,
- technical,
- coherent,
- neutral in tone.

The Introduction should:
- establish why the problem matters,
- define the gap,
- state the paper’s contribution,
- and guide the reader into the rest of the paper.

Avoid:
- generic AI hype,
- overly broad claims,
- repeating the Methods section in detail,
- copying the Related Work section into the Introduction.

The section should be introductory and synthetic, not procedural.

---

## Output Format

Produce:

1. a **paper-ready Introduction section draft**, and
2. if appropriate, an updated IEEE manuscript source with the section inserted or revised.

If editing LaTeX directly:
- preserve the manuscript’s existing style and section structure,
- ensure consistency with the current Related Work and Methods sections.

If not editing directly, output clean prose suitable for direct insertion.

---

## Acceptance Criteria

The output is complete when:

1. it is clearly grounded in the current Related Work and Methods sections,
2. it frames the problem and motivation clearly,
3. it identifies the research gap,
4. it states the paper’s contribution,
5. it is consistent with the rest of the IEEE manuscript,
6. it is suitable for direct inclusion as the paper’s Introduction.

---

## Done

After completing the task:

1. summarise what was produced,
2. note whether the paper source was edited directly,
3. add a dated entry to `work-diary.md` describing:
   - that the IEEE Introduction prompt was created,
   - that it is based on the current Related Work and Methodology,
   - any important writing constraints captured in the prompt.

Sign the diary entry with your model/agent identifier.
