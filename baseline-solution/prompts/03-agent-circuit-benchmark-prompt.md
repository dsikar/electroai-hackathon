# Prompt: Agent Circuit Benchmark — Falstad + LTSpice from Schematic Image

## Context

Read the following before starting:
- `work-diary.md` — project history and decisions
- `baseline-solution/baseline-solution.md` — structure and style reference for the output document

## Setup

Identify yourself: record which model/agent you are (e.g. `claude-sonnet-4-6`, `gemini-2.0-flash`, `codex`) — you will use this as `<agent>` in all filenames and headings below.

Ensure the following directories exist (create if absent):
- `baseline-solution/simulations/` — for `.cir` files
- `baseline-solution/data/schematics/images/` — in case the user provides an image that needs to be stored here

---

## Step 1 — Ask the user for a circuit image

Ask the user:

> "Please provide a circuit schematic image. You can give me a file path, drop the file into the chat, or paste a URL. Also tell me the circuit number (e.g. 1, 2, 3…) so I can name the output files correctly."

Wait for the user to supply:
- The image (file path, inline, or URL) — call this `<image>`
- A circuit number — call this `<number>`

If the user does not supply a number, infer one from the filename or assign the next unused integer in `baseline-solution/simulations/`.

---

## Step 2 — Analyse the circuit

From the image, identify:
- Every component: type, reference designator, and value (e.g. R1 = 10 kΩ, C1 = 100 nF, Q1 = 2N3904 NPN)
- All nodes and how each component pin connects to them
- The power supply voltage(s) and any ground references
- The overall circuit function in one or two sentences

---

## Step 3 — Generate a Falstad simulation link

Write a Falstad plain-text circuit file that faithfully recreates the schematic. Each line is one element; see `baseline-solution/scripts/gen_falstad_urls.py` for the encoding utility already in the repo.

Encoding steps:
1. Write the Falstad circuit as a plain-text string.
2. Compress with `zlib` (deflate, level 9).
3. Base64-encode using the URL-safe alphabet (`-` and `_` instead of `+` and `/`), no padding.
4. Append as the fragment: `https://www.falstad.com/circuit/circuitjs.html#<encoded>`

Run the encoding (reuse `gen_falstad_urls.py` or inline the logic) and produce the final URL. If a component has no native Falstad equivalent (e.g. a specialised IC), use the closest functional approximation and note the substitution.

---

## Step 4 — Generate an LTSpice `.cir` file

Write a standard SPICE netlist for the circuit. Requirements:

- First line: a title comment (`.TITLE` or `* <circuit name>`)
- One line per component using SPICE element syntax (R, C, L, Q, D, V, etc.)
- `.MODEL` statements for any semiconductor devices not in the default library
- An appropriate analysis directive: `.TRAN` for time-domain, `.AC` for frequency, `.DC` for DC sweep — choose whichever best demonstrates the circuit's behaviour
- `.END` as the final line

Save the file as:

```
baseline-solution/simulations/<number>-<agent>-<circuit>.cir
```

Where `<circuit>` is a short kebab-case description derived from the circuit name (e.g. `dual-led-flasher`, `rc-low-pass`, `555-astable`).

Example path: `baseline-solution/simulations/01-claude-sonnet-4-6-dual-led-flasher.cir`

---

## Step 5 — Write the entry in `baseline-solution-3-agents.md`

If `baseline-solution/baseline-solution-3-agents.md` does not exist, create it with this header:

```markdown
# Baseline Solution 3 — Agent Circuit Benchmark

## Overview

Each section below records one agent's analysis of a circuit schematic image.
For each circuit the agent produced:
- A Falstad interactive simulation link reconstructed from the image.
- An LTSpice-compatible `.cir` netlist saved under `baseline-solution/simulations/`.

Agents are identified by model name. Multiple agents may analyse the same circuit;
their entries appear as separate subsections under the same circuit heading.

---
```

Then append the following block **at the end of the file**:

```markdown
## Circuit <number> — <Circuit Name>

### Agent: <agent>

<img src="data/schematics/images/<image filename>" alt="<Circuit Name>" width="600">

**Circuit description:** <2–4 sentence description of what the circuit does and how it works.>

**Component count:** <N> components

**Falstad simulation:** [Open in Falstad](<falstad URL>)

**LTSpice netlist:** [`simulations/<number>-<agent>-<circuit>.cir`](simulations/<number>-<agent>-<circuit>.cir)

> **Notes:** <any approximations made in Falstad or SPICE, or "None" if fully faithful>

---
```

If a `## Circuit <number>` heading already exists (another agent analysed the same circuit), do **not** add a second top-level heading — instead insert a new `### Agent: <agent>` subsection directly under the existing heading.

---

## Step 6 — Validate

- Confirm the `.cir` file is saved and non-empty.
- Confirm the Falstad URL is well-formed (starts with `https://www.falstad.com/circuit/circuitjs.html#` and has a non-empty fragment).
- Confirm the entry has been appended to `baseline-solution-3-agents.md`.

Report the results to the user:
- Falstad URL
- Path to the `.cir` file
- Path to the updated `baseline-solution-3-agents.md`

---

## Done

After completing all steps, add an entry to `work-diary.md` describing:
- Which circuit was analysed
- Which agent produced the outputs
- Any approximations made
- Files created or modified

Sign the entry with your model/agent identifier.
