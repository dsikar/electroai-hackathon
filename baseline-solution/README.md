# Baseline Solution

This directory contains the baseline workflow for reconstructing electronic schematics from images with three model-backed agents:

- `codex`
- `claude`
- `gemini`

Each agent takes a schematic image and produces:

- a Falstad plain-text netlist
- a Falstad XML export
- an LTSpice `.asc` schematic
- a Markdown report describing assumptions, missing information, and inconsistencies

The baseline also includes a lightweight web app for running the pipeline across a folder of images and reviewing the generated artifacts.

## Repository Layout

```text
baseline-solution/
├── data/
│   └── schematics/          Source schematics and reference images
├── docs/                    Additional implementation and usage notes
├── examples/                Small example inputs and outputs
├── images/                  Default image input folder for the web app
├── prompts/                 Prompt assets used during the project
├── reports/                 Draft writeups derived from baseline outputs
├── scripts/                 Single-agent runner scripts and utilities
├── simulations/             Generated outputs, grouped by agent
├── tests/                   Regression tests for LTSpice preview generation
└── webapp/                  Multi-agent dashboard and pipeline backend
```

## Output Contract

For each input image and agent, the baseline expects four primary files:

- `<stem>_generated-by-<agent>_falstad.txt`
- `<stem>_generated-by-<agent>_falstad.xml`
- `<stem>_generated-by-<agent>.asc`
- `<stem>_generated-by-<agent>_report.md`

Optional secondary artifacts may also be created:

- `<stem>_generated-by-<agent>_falstad.png`
- `<stem>_generated-by-<agent>_ltspice.svg`
- `<stem>_generated-by-<agent>_ltspice.png`

Primary outputs are the success criteria. Preview artifacts are helpful, but non-fatal.

## Setup

From this directory:

```bash
cd baseline-solution
python3 -m venv venv
venv/bin/pip install anthropic google-genai playwright
venv/bin/playwright install chromium
```

The Codex runner uses the standard library for HTTP calls, so it does not need an extra Python package.

Set whichever API keys you plan to use:

```bash
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export GOOGLE_API_KEY=...
```

Optional LTSpice SVG support:

- Put `ltspice2svg` on `PATH`
- or place it at `baseline-solution/venv/bin/ltspice2svg`
- or set `LTSPICE2SVG_BIN=/absolute/path/to/ltspice2svg`

Optional symbol path override:

```bash
export LTSPICE2SVG_SYM_PATH=/absolute/path/to/LTspice/lib/sym
```

## Run A Single Agent

Run one image through one agent:

```bash
venv/bin/python scripts/schematic_to_eda_codex.py images/01_circuit.png
venv/bin/python scripts/schematic_to_eda_claude.py images/01_circuit.png
venv/bin/python scripts/schematic_to_eda_gemini.py images/01_circuit.png
```

By default, outputs are written under:

- `simulations/codex/`
- `simulations/claude/`
- `simulations/gemini/`

You can override the destination with `--output-dir`.

## Run The Web App

Start the dashboard from `baseline-solution/`:

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

The dashboard:

- scans `images/` by default for input schematics
- writes results to `simulations/`
- runs all three agents against each discovered image
- shows task status, reports, Falstad previews, and LTSpice previews

The web app prefers `baseline-solution/venv/bin/python3` when that interpreter exists. Otherwise it falls back to the current Python interpreter.

## Tests

Run the LTSpice preview regression tests from `baseline-solution/`:

```bash
python3 -m unittest tests/test_ltspice_svg.py
```

These tests exercise the SVG and PNG post-processing logic against fixture `.asc` files already stored in `simulations/`.

## Included Reference Material

This directory already contains project artifacts beyond the runnable pipeline:

- [baseline-solution.md](/home/daniel/git/electroai-hackathon/baseline-solution/baseline-solution.md) documents manually reconstructed example circuits and Falstad links
- [baseline-solution-3-agents.md](/home/daniel/git/electroai-hackathon/baseline-solution/baseline-solution-3-agents.md) compares agent outputs for the benchmark circuits
- [docs/web-pipeline-app.md](/home/daniel/git/electroai-hackathon/baseline-solution/docs/web-pipeline-app.md) describes the dashboard behavior
- [docs/ltspice-webapp-howto.md](/home/daniel/git/electroai-hackathon/baseline-solution/docs/ltspice-webapp-howto.md) captures the LTSpice preview integration details

## Notes

- The Claude runner emits agent names using `claude-sonnet-4-6`, so its filenames differ slightly from the shorter `claude/` directory name.
- The Gemini runner accepts either `GOOGLE_API_KEY` or `GEMINI_API_KEY`.
- Some generated `.asc` files are placeholders rather than true LTSpice schematics; the pipeline skips SVG conversion when a file does not begin with `Version 4`.
