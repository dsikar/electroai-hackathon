# Prompt: Build a Web App for the Multi-Agent Circuit Pipeline

## Context

Read the following before starting:
- `work-diary.md`
- `baseline-solution/prompts/03-agent-circuit-benchmark-prompt.md`
- `baseline-solution/prompts/04-output-spec-prompt.md`
- `baseline-solution/scripts/`

This repository contains a schematic-analysis pipeline where each agent produces outputs for each image under:

```text
simulations/<agent>/
```

Per `04-output-spec-prompt.md`, each analysed schematic must produce exactly four files:

- `<stem>_generated-by-<agent>_falstad.txt`
- `<stem>_generated-by-<agent>_falstad.xml`
- `<stem>_generated-by-<agent>.asc`
- `<stem>_generated-by-<agent>_report.md`

The supported agents are:

- `codex`
- `claude`
- `gemini`

Your job is to build a **web-based app** that runs the pipeline for all three agents across a folder of schematic images.

---

## Goal

Create a local web application that lets a user:

1. Choose an **input folder** containing schematic images.
2. Choose an **output root folder** for generated agent outputs.
3. Run the pipeline for **Codex, Claude, and Gemini** across all valid images in the input folder.
4. View **live task progress**, including:
   - overall progress,
   - per-agent progress,
   - per-image progress,
   - elapsed time,
   - completion time for each task.
5. See which outputs were produced and whether each task succeeded, failed, or completed with validation issues.

The app should be pragmatic, local-first, and easy to run by a hackathon participant or organiser.

---

## Functional Requirements

### 1. Input folder selection

The app must provide a UI control to select or enter the input folder path.

Default value:

```text
baseline-solution/data/schematics/images/
```

The app must:
- scan the chosen folder for supported image files (`.png`, `.jpg`, `.jpeg`, `.webp`),
- list the discovered files in the UI before execution,
- ignore unsupported files,
- show a clear message if no valid input images are found.

### 2. Output folder selection

The app must provide a UI control to select or enter the output root folder.

Default value:

```text
baseline-solution/simulations/
```

Within that root, the app must write agent outputs to:

```text
<output-root>/codex/
<output-root>/claude/
<output-root>/gemini/
```

The app must create these directories if they do not already exist.

### 3. Agent execution

The app must run the pipeline for all three agents:
- `codex`
- `claude`
- `gemini`

The implementation must **reuse existing agent scripts where possible** instead of duplicating all generation logic inside the web layer.

If the scripts are not consistent yet, create a thin adapter layer so the web app can invoke each agent in a uniform way.

Design the backend around a per-agent command contract like:

```text
<agent runner> <image path> --output-dir <output-root>/<agent>
```

For each image and each agent, the backend should run one task and collect:
- task status,
- stdout/stderr,
- start time,
- end time,
- elapsed time,
- produced file paths.

### 4. Progress and timing UI

The web app must display:

- an **overall progress bar** for all tasks combined,
- a **per-agent progress bar**,
- a **task table or card list** showing each image-agent pair,
- a **live elapsed timer** while a task is running,
- a **completed in Xs** or **completed at HH:MM:SS** display when a task finishes.

Task states must be visually distinct:
- pending,
- running,
- completed,
- completed with issues,
- failed.

If a report file indicates validation issues or inconsistencies, the task should display `completed with issues` rather than plain `completed`.

### 5. Results display

For each completed task, the UI must show links or file paths to:
- Falstad `.txt`
- Falstad `.xml`
- LTSpice `.asc`
- report `.md`

Also show:
- the generated Falstad URL if available,
- whether the output set conforms to the four-file spec,
- whether the report contains inconsistencies or validation failures.

### 6. Validation

The app must verify, for each image-agent task, that the expected four files exist:

- `<stem>_generated-by-<agent>_falstad.txt`
- `<stem>_generated-by-<agent>_falstad.xml`
- `<stem>_generated-by-<agent>.asc`
- `<stem>_generated-by-<agent>_report.md`

If any file is missing, the task must be marked as failed or completed with issues, and the UI must state exactly which files are missing.

The app should also inspect the report file for signs of:
- inconsistencies,
- missing information,
- validation failures,
- placeholder or fallback output.

Surface those findings in the UI.

### 7. Run controls

The UI must support:
- `Start run`
- `Cancel run`
- `Refresh results`

If the user starts a new run, the app should not silently overwrite in-memory state for the old run without warning.

---

## Technical Requirements

### Architecture

Build a small local full-stack app:
- backend: Python
- frontend: simple web UI

Use a stack that is easy to run locally, for example:
- `FastAPI` + server-rendered templates, or
- `FastAPI` backend + lightweight frontend JS

Do **not** build a heavyweight enterprise scaffold.

Priorities:
- easy local setup,
- clear code structure,
- robust task orchestration,
- responsive progress updates.

### Backend behaviour

The backend should:
- discover images from the selected input folder,
- build the task matrix for all images × all agents,
- execute tasks in a controlled queue,
- stream or poll progress to the frontend,
- capture subprocess stdout/stderr,
- parse generated output files,
- expose run state to the frontend.

Use a structure that can later support concurrency, but keep the first implementation reliable and understandable.

### Frontend behaviour

The frontend should:
- feel intentional and usable, not generic,
- work on desktop and mobile,
- clearly show run configuration,
- make progress easy to scan,
- avoid ugly raw logs as the primary UI.

A clean operator dashboard is preferred over a marketing-style homepage.

### Configuration

The app should clearly document expected environment variables for each agent runner, for example:
- `OPENAI_API_KEY`
- Claude-related API key or auth configuration
- Gemini-related API key or auth configuration

The UI does not need to expose secrets directly, but missing configuration should be surfaced clearly before or during execution.

---

## File and Output Expectations

Create or update the necessary application files in the repository.

Include:
- backend app code,
- frontend templates/assets,
- any helper modules for agent runner abstraction,
- run-state/progress handling,
- documentation in `README.md` or a dedicated usage doc.

If you add new folders, keep them clearly named and repo-local.

Do not delete or overwrite existing agent scripts unless necessary; adapt around them where possible.

---

## Acceptance Criteria

The implementation is complete when:

1. I can launch the web app locally.
2. The UI defaults to the schematic image folder and simulation output root.
3. I can start a run that executes Codex, Claude, and Gemini tasks across all discovered images.
4. I can see:
   - overall progress,
   - per-agent progress,
   - per-task timers,
   - final completion times,
   - task statuses.
5. Each agent task writes outputs into:

```text
simulations/<agent>/
```

6. The app verifies the four-file output contract from `04-output-spec-prompt.md`.
7. The UI exposes report findings for inconsistencies and validation issues.
8. The code is documented well enough that another engineer can run and extend it.

---

## Implementation Notes

- Prefer a thin orchestration layer over rewriting agent-specific logic.
- Make the app resilient to partial failures: one failed agent/image task must not collapse the whole run.
- Treat missing files, malformed outputs, and placeholder outputs as meaningful states, not silent success.
- Use explicit file/path handling; avoid hard-coded assumptions outside the configured input and output roots.
- If agent scripts differ today, normalize them behind adapters.

---

## Done

After completing the implementation:

1. Summarise what was built.
2. List how to run the app locally.
3. Identify any remaining gaps or assumptions.
4. Add a dated entry to `work-diary.md` describing:
   - that the web pipeline prompt was created,
   - the purpose of the web app,
   - any important constraints captured in the prompt.

Sign the diary entry with your model/agent identifier.
