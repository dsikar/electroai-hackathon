# Prompt: Write the IEEE Related Work Section Using the Root-Level Reports

## Context

Read the following before starting:
- `work-diary.md`
- `baseline-solution/prompts/09-ieee-methods-section-prompt.md`
- `baseline-solution/prompts/10-ieee-results-section-prompt.md`
- the root-level reports directory:

```text
/home/daniel/git/electroai-hackathon/reports/
```

In particular, review these materials:
- `reports/03-chatgpt-engineering-software-ai-survey-report.md`
- `reports/03-claude-engineering-software-ai-survey-report.md`
- `reports/03-deepseek-engineering-software-ai-survey-report.md`
- `reports/03-gemini-engineering-software-ai-survey-report.md`
- `reports/03-grok-engineering-software-ai-survey-report.md`
- `reports/03-mistral-engineering-software-ai-survey-report.md`
- `reports/04-claude-gap-analysis.md`
- `reports/04-codex-gap-analysis.md`

Also read the current IEEE manuscript source in:

```text
/home/daniel/git/electroai-hackathon/ElectroAIHackathonIEEETemplate/
```

The goal is to write a **Related Work section** for the IEEE paper that is informed by the project’s existing survey and gap-analysis materials.

---

## Task

Write a polished **Related Work section** suitable for direct inclusion in the IEEE paper.

The section must synthesise the root-level survey and gap-analysis materials into a coherent narrative about:

1. AI tools and workflows in engineering software,
2. AI-assisted circuit interpretation and reconstruction,
3. multimodal and agent-based systems relevant to schematic understanding,
4. limitations of existing tools for structural circuit recovery,
5. and the gap that motivates this project.

This section must be grounded in the repository’s existing reports, not written as a generic literature overview.

---

## Required Source Use

You must explicitly use the **root-level reports directory** as a primary input source.

This means:
- draw on the survey reports in `reports/03-*.md`,
- draw on the gap analyses in `reports/04-*.md`,
- use them to structure and support the Related Work discussion,
- and reflect the repo’s prior synthesis rather than ignoring it.

You may also use any references already included in the IEEE paper or cited in those reports, but the root-level reports must be a central input.

---

## Required Coverage

### 1. Engineering-software AI landscape

Summarise the landscape of AI-enabled engineering tools described in the survey materials.

This should include discussion of categories such as:
- design assistants,
- analysis assistants,
- simulation-oriented tools,
- workflow automation tools,
- code- or script-generating assistants,
- engineering copilots or agent systems.

The Related Work text should not simply list tools; it should explain the broader landscape and its relevance to circuit understanding.

### 2. Circuit and schematic interpretation

Discuss prior or adjacent work relevant to:
- interpreting schematic images,
- extracting structure from circuit diagrams,
- converting visual circuit information into machine-usable representations,
- recovering netlists or simulator-compatible forms from diagrams.

Where the reports identify weaknesses in current tools, fold those observations into the narrative.

### 3. Multimodal and agentic approaches

Discuss the relevance of:
- multimodal models,
- agent-based coding systems,
- tool-using AI systems,
- pipeline-based orchestration across multiple models.

Tie this to the present project’s use of Codex, Claude, Gemini, Falstad, and LTSpice.

### 4. Gaps in existing work

The section must clearly articulate the gap identified in the root-level gap-analysis reports.

This should include limitations such as:
- weak structural fidelity,
- lack of direct simulator-ready outputs,
- poor support for preserving circuit topology,
- limited validation of generated engineering artefacts,
- insufficient support for cross-model comparison,
- or the absence of a practical multi-agent benchmarking workflow.

### 5. Positioning of the present work

The Related Work section must conclude by positioning the present study relative to the surveyed landscape.

Make clear how this project differs from or contributes beyond prior tools/workflows, for example by:
- benchmarking multiple agent systems on a common task,
- generating dual design modalities,
- integrating validation and preview workflows,
- or focusing specifically on structural circuit reconstruction from schematic images.

---

## Writing Requirements

Write in IEEE style:
- formal,
- technical,
- concise,
- synthetic rather than repetitive,
- neutral in tone.

The section should read like a strong academic Related Work section, not like notes extracted from reports.

Prefer:
- grouped themes,
- comparison and synthesis,
- clear statement of the identified gap,
- prose that leads naturally into the Methods/Results sections.

Avoid:
- long unstructured lists of tools,
- casual commentary,
- unsupported claims,
- duplicating the survey reports verbatim.

---

## Output Format

Produce:

1. a **paper-ready Related Work section draft**, and
2. if appropriate, an updated IEEE paper source with the new section inserted.

If editing LaTeX directly, preserve the formatting and section style already used in the paper.

If not editing directly, output clean prose with logical subsectioning if needed.

---

## Acceptance Criteria

The output is complete when:

1. it synthesises the root-level reports in `reports/`,
2. it covers the engineering-software AI landscape,
3. it discusses schematic/circuit interpretation and multimodal or agentic approaches,
4. it clearly states the gap motivating the present work,
5. it positions the current project within that landscape,
6. it is suitable for direct inclusion in the IEEE manuscript.

---

## Done

After completing the task:

1. summarise what was produced,
2. note whether the paper source was edited directly,
3. add a dated entry to `work-diary.md` describing:
   - that the IEEE Related Work prompt was created,
   - that it explicitly references the root-level `reports/` materials,
   - any important writing constraints captured in the prompt.

Sign the diary entry with your model/agent identifier.
