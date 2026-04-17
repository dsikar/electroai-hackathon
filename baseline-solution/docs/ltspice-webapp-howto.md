# LTSpice Web App How-To

This guide is for another agent that needs to add LTSpice preview support to a lightweight web app quickly, without rediscovering the implementation details already worked out in this repo.

## Goal

Starting from an existing pipeline that already produces LTSpice `.asc` files, add two optional post-processing stages:

1. `.asc` -> `_ltspice.svg`
2. `_ltspice.svg` -> `_ltspice.png` behind a UI switch

The required four-file contract stays unchanged:

- `<stem>_generated-by-<agent>_falstad.txt`
- `<stem>_generated-by-<agent>_falstad.xml`
- `<stem>_generated-by-<agent>.asc`
- `<stem>_generated-by-<agent>_report.md`

The SVG and PNG files are secondary artifacts.

## Where The Current Implementation Lives

- Backend state and post-processing: `webapp/agent_pipeline.py`
- HTTP API wiring: `webapp/server.py`
- Dashboard UI logic: `webapp/static/app.js`
- Dashboard markup: `webapp/templates/index.html`
- Dashboard styles: `webapp/static/styles.css`
- User-facing docs: `docs/web-pipeline-app.md`
- Tests: `tests/test_ltspice_svg.py`

## Feature Shape

### LTSpice SVG

Use `ltspice2svg` as the converter for `.asc` -> `.svg`.

Current discovery order:

1. `LTSPICE2SVG_BIN`
2. `venv/bin/ltspice2svg`
3. `tools/ltspice2svg/ltspice2svg`
4. `PATH`

Optional symbols path:

- `LTSPICE2SVG_SYM_PATH`

Output naming:

- Input: `<stem>_generated-by-<agent>.asc`
- Output: `<stem>_generated-by-<agent>_ltspice.svg`

Important rule:

- Only attempt conversion if the `.asc` starts with `Version 4`.

That rule intentionally skips obvious placeholders like Codex `01`, which is not a schematic file.

### LTSpice PNG

Use Playwright/Chromium to rasterize the generated SVG into PNG.

Why this path:

- already available in this repo,
- avoids adding another system package,
- works well enough for publication and dashboard preview use.

Output naming:

- Input: `<stem>_generated-by-<agent>_ltspice.svg`
- Output: `<stem>_generated-by-<agent>_ltspice.png`

Important rule:

- PNG generation is disabled by default and controlled by a dashboard switch.

## Minimal Backend Changes

### 1. Add path helpers

You need stable helpers for:

- `ltspice_svg_path(asc_path)`
- `ltspice_png_path(svg_path)`

Keep naming deterministic. Do not hardcode string replacements in multiple places.

### 2. Add tool discovery helpers

Expose backend tool availability in state so the UI can tell the user what is missing.

Current state includes:

- `tool_config.ltspice_svg`
- `tool_config.ltspice_png`

That prevents the frontend from guessing why an artifact was not produced.

### 3. Extend task metadata

Each task should carry:

- `ltspice_svg_path`
- `ltspice_svg_status`
- `ltspice_svg_message`
- `ltspice_png_path`
- `ltspice_png_status`
- `ltspice_png_message`

Use status values that are easy for the UI to display directly. Current examples:

- `available`
- `skipped`
- `missing_source`
- `unavailable`
- `failed`
- `disabled`

### 4. Keep conversion non-fatal

Do not make SVG or PNG generation part of the formal success criteria for the agent run.

Correct behavior:

- required outputs missing -> task issue / failure as before
- optional preview conversion missing -> surface status and message
- placeholder `.asc` -> skip SVG cleanly
- PNG switch off -> mark PNG as `disabled`

### 5. Add the post-processing hooks in task finalization

The right place is the task finalization path, after the base outputs exist.

Current ordering:

1. inspect required files
2. inspect report
3. generate LTSpice SVG
4. optionally generate LTSpice PNG
5. generate Falstad preview PNG
6. finalize task status

That sequence matters because PNG depends on SVG.

## Minimal API Changes

Expose one boolean from the client:

- `ltspice_png_enabled`

Thread it through:

- `POST /api/start`
- `POST /api/refresh`
- manager state
- refresh snapshot

Keep the default `false`.

## Minimal UI Changes

### Control panel

Add a checkbox in the control panel:

- label: `LTSpice PNG`
- behavior: when checked, request PNG generation during start/refresh

### Tool availability

Show both:

- LTSpice SVG tool status
- LTSpice PNG tool status

This makes it obvious whether the problem is:

- missing `ltspice2svg`
- missing Playwright
- disabled switch
- invalid source `.asc`

### Task artifact list

Each task should show links or statuses for:

- `ltspice_svg`
- `ltspice_png`

Do not hide non-available artifacts entirely. Show the status text instead.

That saves debugging time.

## Rasterization Implementation Notes

The current PNG renderer uses Playwright to load the SVG through a data URL and then screenshots the `img` element.

Why data URL instead of a local file path inside HTML:

- no local web server needed,
- no path escaping issues,
- no browser file-origin surprises for a plain SVG load.

The working shape is:

1. read SVG bytes
2. base64 encode
3. build `data:image/svg+xml;base64,...`
4. render `<img id="circuit" src="...">`
5. screenshot the element

This is more reliable than screenshotting the whole page if you only want the circuit image.

## Test Strategy

Do not invent fake fixtures when real agent outputs already exist.

Use the real `.asc` files from:

- `simulations/claude/01_circuit_generated-by-claude-sonnet-4-6.asc`
- `simulations/claude/02_cicuit_generated-by-claude-sonnet-4-6.asc`
- `simulations/codex/01_circuit_generated-by-codex.asc`
- `simulations/codex/02_cicuit_generated-by-codex.asc`
- `simulations/gemini/01_circuit_generated-by-gemini.asc`
- `simulations/gemini/02_cicuit_generated-by-gemini.asc`

Current expected matrix:

- Claude `01`: SVG available, PNG available when enabled
- Claude `02`: SVG available, PNG available when enabled
- Codex `01`: SVG skipped, PNG missing_source
- Codex `02`: SVG available, PNG available when enabled
- Gemini `01`: SVG available, PNG available when enabled
- Gemini `02`: SVG available, PNG available when enabled

Note the Gemini files are minimal placeholder schematics but still start with `Version 4`, so `ltspice2svg` accepts them.

### Why tests use a temp workspace

Do not write new PNGs into the checked-in `simulations/` tree during tests.

Instead:

1. create a temp workspace
2. copy the real fixture `.asc` files into temp agent folders
3. run conversion there

That keeps tests repeatable and avoids dirtying tracked outputs.

## Current Test Coverage

See `tests/test_ltspice_svg.py`.

It covers:

1. direct SVG generation from fixture `.asc` files
2. direct PNG generation from generated SVG files
3. refresh-state SVG reporting against repo fixtures
4. refresh-state PNG reporting with the switch off
5. refresh-state PNG reporting with the switch on

Run with:

```bash
python3 -m py_compile webapp/agent_pipeline.py webapp/server.py tests/test_ltspice_svg.py
venv/bin/python -m unittest tests.test_ltspice_svg -v
```

## Common Failure Modes

### `ltspice2svg` missing

Symptom:

- SVG status becomes `unavailable`

Fix:

- install binary into `venv/bin/ltspice2svg`
- or set `LTSPICE2SVG_BIN`

### Placeholder `.asc` file

Symptom:

- SVG status becomes `skipped`

Fix:

- none; this is expected for invalid non-schematic outputs

### Playwright missing

Symptom:

- PNG status becomes `unavailable`

Fix:

```bash
venv/bin/pip install playwright
venv/bin/playwright install chromium
```

### PNG switch off

Symptom:

- PNG status becomes `disabled`

Fix:

- enable the checkbox in the dashboard
- or pass `ltspice_png_enabled: true` to refresh/start

## If You Need The Fastest Path

If another agent just needs to replicate this feature elsewhere, the shortest safe sequence is:

1. copy the path helpers and status fields
2. copy the `ltspice2svg` discovery pattern
3. add one boolean switch to start/refresh state
4. run SVG conversion in task finalization
5. run PNG conversion from SVG with Playwright only when the switch is on
6. expose both artifacts and statuses in the UI
7. port the `tests/test_ltspice_svg.py` fixture-driven tests

That is enough to get the feature working without redesigning the app.
