# Prompt: Write the IEEE Future Work Section from the Current Manuscript

## Context

Read the following before starting:
- `work-diary.md`
- `baseline-solution/prompts/09-ieee-methods-section-prompt.md`
- `baseline-solution/prompts/10-ieee-results-section-prompt.md`
- `baseline-solution/prompts/12-ieee-discussion-prompt.md`
- `baseline-solution/prompts/14-ieee-conclusion-prompt.md`
- the current IEEE manuscript source in:

```text
/home/daniel/git/electroai-hackathon/ElectroAIHackathonIEEETemplate/
```

In particular, read the current:
- Methods section,
- Results section,
- Discussion section,
- Conclusion section.

The goal is to write a **Future Work section** that follows directly from the current manuscript and the limitations/failure modes already identified.

---

## Task

Write a polished **Future Work section** for the IEEE paper.

The section must:

1. follow directly from the current manuscript findings,
2. identify credible next steps for extending the research,
3. connect proposed next steps to observed limitations and failure modes,
4. remain technical, specific, and realistic.

This should be a standalone section, not just a final sentence appended to the Conclusion.

---

## Required Coverage

### 1. Dataset and benchmark expansion

Discuss future work related to improving the experimental benchmark, for example:
- increasing the number of circuits,
- expanding circuit diversity,
- including more analogue, digital, mixed-signal, and power-electronics schematics,
- improving image quality and annotation consistency,
- building a more systematic benchmark dataset for schematic reconstruction.

### 2. Structural evaluation improvements

Discuss future work on evaluation methodology, such as:
- topology-aware scoring,
- graph-based structural comparison,
- component- and net-level correctness metrics,
- netlist equivalence checks,
- stronger validation of structural fidelity across modalities.

### 3. Functional verification

Discuss the need for future work that goes beyond visual plausibility, for example:
- simulation-based checking,
- behavioural comparison of reconstructed circuits,
- consistency checks between Falstad and LTSpice outputs,
- automated functional validation against reference circuits.

### 4. Model and agent improvements

Discuss future work involving better AI systems or workflows, such as:
- improved prompting strategies,
- tool-augmented agents,
- multi-stage decomposition,
- self-checking or verifier agents,
- stronger multimodal reasoning pipelines,
- model ensembles or repair loops.

### 5. Pipeline and tooling improvements

Discuss engineering extensions to the current pipeline, such as:
- more robust web-based orchestration,
- richer preview and debug tooling,
- automatic report summarisation,
- improved environment/configuration handling,
- better agent standardisation,
- reproducibility improvements.

### 6. Practical engineering relevance

Discuss future work needed to make the system more useful in real engineering workflows, for example:
- handling scanned or noisy schematics,
- support for larger industrial diagrams,
- integration with EDA toolchains,
- support for reusable schematic corpora,
- interactive correction workflows with a human engineer in the loop.

---

## Writing Requirements

Write in IEEE style:
- formal,
- concise,
- technical,
- realistic,
- directly connected to the findings.

The section should:
- propose specific next steps,
- explain why they matter,
- and avoid generic statements like “more research is needed.”

Avoid:
- hype,
- vague wish lists,
- introducing entirely new claims not motivated by the paper.

Future work should emerge naturally from the observed success and failure modes in the manuscript.

---

## Output Format

Produce:

1. a **paper-ready Future Work section draft**, and
2. if appropriate, an updated IEEE manuscript source with the section inserted.

If editing LaTeX directly:
- preserve the manuscript’s formatting and section structure.

If not editing directly, output clean prose suitable for direct insertion.

---

## Acceptance Criteria

The output is complete when:

1. it is grounded in the current manuscript,
2. it proposes concrete and credible next steps,
3. it addresses dataset, evaluation, verification, model, and tooling extensions,
4. it is clearly linked to the observed limitations and failure modes,
5. it is suitable for direct inclusion in the IEEE paper.

---

## Done

After completing the task:

1. summarise what was produced,
2. note whether the paper source was edited directly,
3. add a dated entry to `work-diary.md` describing:
   - that the IEEE Future Work prompt was created,
   - that it is grounded in the current manuscript and observed limitations,
   - any important writing constraints captured in the prompt.

Sign the diary entry with your model/agent identifier.
