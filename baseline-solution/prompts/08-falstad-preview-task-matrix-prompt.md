# Prompt: Add Falstad Preview Images to the Web App Task Matrix

## Context

Read the following before starting:
- `work-diary.md`
- `baseline-solution/prompts/04-output-spec-prompt.md`
- `baseline-solution/prompts/05-webapp-pipeline-prompt.md`
- `baseline-solution/webapp/agent_pipeline.py`
- `baseline-solution/webapp/templates/index.html`
- `baseline-solution/webapp/static/app.js`
- `baseline-solution/webapp/static/styles.css`
- `baseline-solution/scripts/`

The current web app runs the agent pipeline and shows task results in the task matrix. Each successful task already produces a Falstad plain-text file:

```text
<stem>_generated-by-<agent>_falstad.txt
```

The next feature is to automatically turn that Falstad text output into a rendered PNG preview and display that preview in the appropriate task card in the web UI.

---

## Goal

Extend the pipeline so that, after a task completes and the Falstad `.txt` file exists, the system:

1. submits the Falstad text circuit to Falstad,
2. captures a PNG image of the rendered circuit,
3. saves that PNG alongside the task outputs,
4. shows the image in the matching task-matrix cell for that image-agent pair,
5. scales the image to fit the task card cleanly without breaking the layout.

This feature is specifically for the **web-based multi-agent pipeline dashboard**.

---

## Functional Requirements

### 1. Falstad PNG generation

For each completed task:
- locate the Falstad plain-text output:

```text
<stem>_generated-by-<agent>_falstad.txt
```

- submit that content to Falstad,
- load the circuit in Falstad,
- capture a PNG render of the circuit,
- save it in the same agent output directory.

Required filename:

```text
<stem>_generated-by-<agent>_falstad.png
```

Example:

```text
simulations/codex/01_circuit_generated-by-codex_falstad.png
```

### 2. Placement in the task matrix

Each task card in the dashboard must include a Falstad preview area.

If the PNG exists:
- display it in the task card for the matching task,
- place it in a visually stable location in the card,
- keep the rest of the task metadata readable.

If the PNG does not exist:
- do not break the layout,
- show a compact placeholder or status message such as `Falstad preview unavailable`.

### 3. Scaling behaviour

The preview image must:
- scale to fit the available card width,
- preserve aspect ratio,
- avoid overflowing the card,
- remain readable on both desktop and mobile.

Use CSS that keeps the image contained and visually tidy.

### 3a. Click-to-enlarge popup

If the preview image is clicked:
- open a popup, modal, or lightbox-style overlay,
- show the same Falstad preview image at full scale or as large as the viewport reasonably allows,
- preserve aspect ratio,
- allow the user to close the popup easily.

The enlarged view should:
- sit above the dashboard UI,
- dim or visually separate the background,
- work on desktop and mobile,
- avoid clipping the image unnecessarily.

The task card should therefore support two states:
- embedded scaled preview in the matrix,
- full-size popup view on click.

### 4. Task state integration

The backend should treat Falstad PNG generation as part of the task result handling.

If Falstad text exists but PNG generation fails:
- do **not** mark the whole task as silently successful,
- add a clear issue to the task,
- surface that issue in the task card and report/debug output.

If PNG generation succeeds:
- expose the PNG path in task metadata,
- make it available to the UI through the existing API state payload.

### 5. Validation

The task validator should now also check for the Falstad preview PNG when appropriate.

Important distinction:
- the four-file contract from `04-output-spec-prompt.md` still remains the formal required output set,
- the PNG is an additional web-app preview artifact,
- missing PNG should be surfaced as a UI/output issue, not confused with the base four-file contract.

### 6. Debug visibility

The current app includes a debug panel and per-task stdout/stderr.

Extend that so Falstad preview generation is debuggable:
- log when PNG capture starts,
- log when it succeeds,
- log when it fails,
- include the failure reason in the task issues/debug output.

---

## Technical Requirements

### Implementation strategy

Use a pragmatic approach that fits the repo and current app design.

You may:
- automate Falstad through browser automation,
- use an existing local script if one already exists,
- add a new helper utility if needed.

But the end result must be integrated into the web pipeline flow rather than being a separate manual step.

### Integration points

You will likely need to update:
- backend pipeline manager / task finalization logic,
- API state payload,
- task card template,
- frontend rendering logic,
- CSS for preview layout,
- possibly a helper script or image-generation utility.

### Output location

Save the PNG in the same agent output directory as the other task artifacts:

```text
simulations/<agent>/
```

Do not place preview PNGs in unrelated temp or frontend-only folders unless they are purely ephemeral intermediate files.

### Robustness

- Do not let one failed preview generation crash the full run.
- Do not let one failed preview block other tasks.
- Make the app usable even when Falstad preview generation is unavailable or partially failing.

---

## UI Requirements

The task card should show:
- status,
- timer,
- output links,
- issues,
- debug section,
- and now the Falstad preview image.

The preview should feel like part of the operator dashboard, not an afterthought.

Prefer:
- a compact framed preview block,
- a consistent image area across cards,
- restrained styling that matches the existing dashboard look.

Avoid:
- oversized screenshots that dominate the card,
- layout jumps when images load,
- raw image links without visual embedding.

When clicked, the preview should transition into a clear enlarged viewing mode rather than opening as an unstyled browser tab.

---

## Acceptance Criteria

The feature is complete when:

1. A completed task with a Falstad `.txt` file also attempts to generate:

```text
<stem>_generated-by-<agent>_falstad.png
```

2. The PNG is saved under:

```text
simulations/<agent>/
```

3. The task matrix displays the PNG in the correct task card.
4. Clicking the preview opens a popup/lightbox showing the image at full scale or viewport-limited maximum size.
5. The preview scales to fit the card on desktop and mobile.
6. Missing or failed preview generation is shown as an issue/debug message.
7. The app remains stable when preview generation fails.
8. The implementation is documented clearly enough that another engineer can run and maintain it.

---

## Done

After completing the implementation:

1. Summarise what changed.
2. Explain how Falstad PNG generation works.
3. Note any environment/tooling assumptions for the preview capture step.
4. Add a dated entry to `work-diary.md` describing:
   - that the Falstad preview prompt was created,
   - that it adds PNG generation and task-matrix embedding,
   - any important implementation constraints captured in the prompt.

Sign the diary entry with your model/agent identifier.
