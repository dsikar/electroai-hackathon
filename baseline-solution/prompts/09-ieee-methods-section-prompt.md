# Prompt: Write the IEEE Methods Section for the Multi-Agent Web App Pipeline

## Context

Read the following before starting:
- `work-diary.md`
- `baseline-solution/prompts/03-agent-circuit-benchmark-prompt.md`
- `baseline-solution/prompts/04-output-spec-prompt.md`
- `baseline-solution/prompts/05-webapp-pipeline-prompt.md`
- `baseline-solution/prompts/08-falstad-preview-task-matrix-prompt.md`
- `baseline-solution/docs/web-pipeline-app.md`
- `baseline-solution/webapp/`
- `baseline-solution/scripts/`
- `ElectroAIHackathonIEEETemplate/conference_101719.tex` or the current IEEE paper source if it has moved

This project now includes a web-based orchestration layer that runs multiple AI agents over circuit schematic images and produces multiple downstream design modalities, including Falstad and LTSpice representations.

The Methods section you write must explain the development and operation of this system in a way suitable for inclusion in an IEEE-style research paper.

---

## Task

Write a polished **Methods section** for the IEEE paper describing the development workflow and system architecture behind the multi-agent web app pipeline.

The text should explain:

1. how the web app was developed,
2. how multiple coding/agent systems were engaged during development,
3. how the backend orchestrates Codex, Claude Code, and Gemini runs,
4. how generated code/text outputs are converted into two design modalities:
   - Falstad
   - LTSpice
5. how the pipeline dynamically queries Falstad and LTSpice-related subsystems to recover rendered artefacts,
6. how task validation, reporting, and preview generation are integrated,
7. how the resulting system supports experimental comparison across agents.

---

## Required Coverage

Your Methods section must explicitly describe all of the following.

### 1. Multi-agent development process

Explain that the web application and its associated pipeline were developed through iterative interaction with multiple AI coding agents, specifically:
- Codex
- Claude Code / Claude-based agent workflows
- Gemini

Describe this as part of the engineering workflow, not as marketing language.

The Methods text should make clear that:
- different agent systems were used to generate, refine, test, and adapt different parts of the pipeline,
- outputs from different agents were retained as distinct artefacts,
- the architecture intentionally preserved agent identity for downstream comparison,
- the development process itself was agent-assisted and modular.

### 2. Web app orchestration subsystem

Describe the local web app as the orchestration layer that:
- accepts an input folder of schematic images,
- enumerates valid image files,
- schedules one task per image-agent pair,
- writes outputs into per-agent directories,
- tracks task progress, completion status, timing, and validation state,
- exposes results in a task matrix UI.

Include the role of:
- the backend task manager,
- per-agent runner adapters,
- UI progress/timer reporting,
- per-task status categories.

### 3. Agent-specific execution layer

Explain that each agent is invoked through a script or runner abstraction with a uniform contract such as:

```text
<agent runner> <image path> --output-dir <output-root>/<agent>
```

The Methods text should explain that this abstraction allowed heterogeneous agent implementations to be evaluated under a common operational interface.

### 4. Dual-modality design generation

Explain that from the schematic image, each agent attempts to generate at least two downstream design modalities:

- Falstad circuit representation
- LTSpice schematic representation

Describe the specific outputs in engineering terms:
- Falstad plain-text circuit format
- Falstad XML
- LTSpice `.asc`
- report/validation artefact

Make clear that these modalities support both structural interpretation and downstream visualization/simulation workflows.

### 5. Dynamic Falstad querying and preview recovery

Describe the Falstad side of the pipeline:
- AI agents generate Falstad-compatible circuit text,
- the plain-text circuit is encoded or submitted into the Falstad/CircuitJS environment,
- the application dynamically queries the Falstad environment to recover rendered preview images,
- these previews are used as a visual modality for inspection inside the web dashboard.

If appropriate, describe this as browser automation or automated rendering rather than manual screenshotting.

### 6. LTSpice artefact retrieval and secondary modality generation

Describe the LTSpice side of the pipeline:
- AI agents generate LTSpice `.asc` representations,
- these are treated as a second design modality,
- downstream rendering/retrieval steps can generate additional visual artefacts for inspection,
- these artefacts are incorporated into the task-level evaluation/display pipeline.

The section should describe LTSpice as a second modality complementary to Falstad, rather than just a file export.

### 7. Validation and inconsistency reporting

Explain the role of validation:
- checking expected output files,
- inspecting report contents for missing information or inconsistencies,
- surfacing malformed or partial outputs,
- treating placeholder or incomplete generations as issues rather than silent success.

Make clear that this validation layer is part of the methodology for comparing agent performance, not just a UI convenience.

### 8. Relevance to the experimental study

Tie the system back to the paper’s experimental purpose:
- comparing agent performance on circuit understanding and reconstruction,
- preserving per-agent outputs,
- producing reproducible artefacts,
- enabling both textual and visual inspection of reconstructed designs.

---

## Writing Requirements

Write in a style suitable for an IEEE paper:
- formal,
- concise,
- technical,
- neutral in tone,
- no hype,
- no first-person diary voice.

The section should read like a real Methods section, not internal notes.

Prefer:
- coherent prose with subsection headings where appropriate,
- explicit system descriptions,
- precise terminology,
- references to pipeline stages and artefact types.

Avoid:
- casual wording,
- promotional claims,
- vague statements such as “the AI helped a lot,”
- long bullet lists in the final paper text.

---

## Output Format

Produce:

1. a **paper-ready Methods section draft**, and
2. if useful, a brief note on where it should be inserted into the current IEEE manuscript.

If editing the LaTeX paper directly, preserve IEEE formatting conventions already used in the manuscript.

If not editing directly, output the Methods section in clean Markdown or LaTeX-ready prose with clear subsection markers.

---

## Acceptance Criteria

The output is complete when:

1. it clearly explains the multi-agent development workflow,
2. it describes the web app orchestration subsystem,
3. it explains Codex, Claude, and Gemini as distinct agent execution paths,
4. it describes the Falstad and LTSpice dual-modality generation process,
5. it explains dynamic retrieval/rendering of artefacts from Falstad and LTSpice-related outputs,
6. it discusses validation and inconsistency reporting,
7. it is suitable for direct incorporation into the IEEE paper’s Methods section.

---

## Done

After completing the writing task:

1. summarise what was produced,
2. note whether the paper source was edited directly,
3. add a dated entry to `work-diary.md` describing:
   - that the IEEE Methods-section prompt was created,
   - that it covers the multi-agent web app and dual-modality Falstad/LTSpice workflow,
   - any important writing constraints captured in the prompt.

Sign the diary entry with your model/agent identifier.
