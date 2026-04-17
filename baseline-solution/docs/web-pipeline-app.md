# Multi-Agent Pipeline Web App

Implementation handoff:

- See `docs/ltspice-webapp-howto.md` for the agent-focused integration guide for LTSpice SVG and PNG support.

## Run

From `baseline-solution/`:

```bash
python3 -m webapp.server
```

Default address:

```text
http://127.0.0.1:8765
```

Optional host and port:

```bash
python3 -m webapp.server --host 0.0.0.0 --port 9000
```

## What It Does

The app runs the schematic pipeline across:

- `codex`
- `claude`
- `gemini`

For each image discovered in the selected input folder, it launches one task per agent and writes outputs into:

```text
<output-root>/codex/
<output-root>/claude/
<output-root>/gemini/
```

Each task expects exactly four files:

- `<stem>_generated-by-<agent>_falstad.txt`
- `<stem>_generated-by-<agent>_falstad.xml`
- `<stem>_generated-by-<agent>.asc`
- `<stem>_generated-by-<agent>_report.md`

When `ltspice2svg` is available, the app also writes an optional LTSpice vector preview:

- `<stem>_generated-by-<agent>_ltspice.svg`

When the LTSpice PNG switch is enabled in the dashboard, the app also rasterizes that SVG into:

- `<stem>_generated-by-<agent>_ltspice.png`

The dashboard task cards can now embed:

- a Falstad preview image rendered from the Falstad `.txt` output
- an LTSpice preview image rendered from the LTSpice PNG when available, or directly from the LTSpice SVG otherwise

Clicking either preview opens a larger modal view in the dashboard. The task cards and summary area also provide stronger signposting for work in progress and the most recently completed task.

## Defaults

- Input folder: `data/schematics/images/`
- Output root: `simulations/`

## Environment

The app depends on the underlying runner scripts, so the relevant credentials must already be available in the shell environment:

- Codex: `OPENAI_API_KEY`
- Claude: `ANTHROPIC_API_KEY`
- Gemini: `GOOGLE_API_KEY` or `GEMINI_API_KEY`

Optional LTSpice SVG conversion:

- Put `ltspice2svg` on `PATH`, place it at `venv/bin/ltspice2svg`, or set `LTSPICE2SVG_BIN=/absolute/path/to/ltspice2svg`.
- If your LTSpice symbols live outside the default location, set `LTSPICE2SVG_SYM_PATH=/absolute/path/to/LTspice/lib/sym`.
- LTSpice PNG conversion uses Playwright/Chromium from the project virtualenv when the dashboard switch is enabled.

## Notes

- The web app uses the existing runner scripts rather than reimplementing the generation pipeline.
- It validates the expected four-file output contract after each task.
- If a valid LTSpice schematic `.asc` exists and `ltspice2svg` is available, the app automatically creates or refreshes the matching `_ltspice.svg`.
- If the LTSpice PNG switch is enabled and the SVG exists, the app also creates or refreshes the matching `_ltspice.png`.
- If a report indicates inconsistencies, missing information, placeholder output, or validation failures, the task is marked as completed with issues.
- One failed task does not stop the rest of the run unless the user cancels the run.

## Falstad Preview PNGs

After a task finishes and its Falstad plain-text file exists, the pipeline now attempts to generate an additional preview artifact:

- `<stem>_generated-by-<agent>_falstad.png`

This preview is created by running `scripts/falstad_screenshot_automation.py`, which loads the Falstad text output into CircuitJS and captures a rendered PNG. The preview path is exposed in task metadata and displayed directly in the dashboard task card. Clicking the embedded preview opens a larger modal view.

Preview generation is treated as a secondary web-app artifact:

- the original four-file contract remains the formal task output set,
- preview failures do not delete or invalidate the base outputs,
- but a missing or failed preview is surfaced as a task issue and in debug output.

### Preview Runtime Assumptions

Falstad preview generation depends on the local Playwright setup used by `scripts/falstad_screenshot_automation.py`:

- Python package: `playwright`
- Browser runtime: Chromium installed via Playwright

Example setup inside `baseline-solution/venv`:

```bash
venv/bin/pip install playwright
venv/bin/playwright install chromium
```
