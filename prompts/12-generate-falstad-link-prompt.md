# Prompt: Generate Falstad Link for a Circuit and Update baseline-solution.md

## Purpose

This prompt instructs an AI agent to construct a working Falstad circuit simulator link for a named circuit, then update `baseline-solution/baseline-solution.md` with the new link, replacing any existing placeholder or incorrect link.

---

## Step 1 — Ask the User

Begin by asking the user exactly this:

> **Which circuit should I work on?**

Wait for the user to reply. The expected reply is the circuit name as it appears in `baseline-solution/baseline-solution.md`, for example:

- `10 — Dual LED Flasher`
- `15 — Triac Timer`
- `20 — LED Chaser`
- `25 — Transistor Equalizer`
- `30 — Simple Inverter`
- `35 — LM386 Mini Amplifier`

---

## Step 2 — Read the Circuit Entry

Open `baseline-solution/baseline-solution.md` and locate the section for the named circuit. Read:

- The component list and values
- The circuit description
- The existing Falstad link (if any)

Also read the corresponding schematic image from `baseline-solution/data/schematics/images/` to verify component values and topology before writing the netlist.

---

## Step 3 — Write the Falstad Netlist

Write a Falstad plain-text netlist for the circuit using the format accepted by [https://www.falstad.com/circuit/circuitjs.html](https://www.falstad.com/circuit/circuitjs.html).

### Falstad netlist format rules

- First line: `$ 1 <timestep> <speed> <gridSize> <circuitScale> <voltageRange>`  
  Example: `$ 1 0.000005 10.20 50 5 50`
- Each subsequent line is one element. Common element prefixes:
  - `r` — resistor: `r <x1> <y1> <x2> <y2> 0 <ohms>`
  - `c` — capacitor: `c <x1> <y1> <x2> <y2> 0 <farads>`
  - `l` — inductor: `l <x1> <y1> <x2> <y2> 0 <henries>`
  - `d` — diode: `d <x1> <y1> <x2> <y2> 1 0.805904`
  - `t` — BJT transistor: `t <bx> <by> <cx> <cy> 0 -1 <vbe> <vce> <beta>` (NPN: last pnpflag=0, PNP: pnpflag=1)
  - `v` — voltage source: `v <x1> <y1> <x2> <y2> 0 0 40 <voltage> 0 0 0.5`
  - `w` — wire: `w <x1> <y1> <x2> <y2> 0`
  - `g` — ground: `g <x1> <y1> <x2> <y2> 0`
  - `O` — output/scope probe: `O <x1> <y1> <x2> <y2> 1`
  - `162` — LED: `162 <x1> <y1> <x2> <y2> 1 2.1 0 1 0.0010`
  - `a` — op-amp: `a <x1> <y1> <x2> <y2> 0 15 -15 1000000 0 0`
  - `s` — switch: `s <x1> <y1> <x2> <y2> 0 <state> false`

- If a component is not natively supported (e.g. TRIAC, CD4017, LM386 IC), use a functionally equivalent approximation and note it in the circuit description.
- Use a grid-aligned layout (coordinates in multiples of 16). Keep the circuit readable: space components at least 64 units apart, arrange left-to-right or top-to-bottom where possible.

---

## Step 4 — Encode the Netlist as a Falstad URL

The Falstad URL fragment is the netlist compressed and encoded as follows:

1. Encode the netlist string as UTF-8 bytes.
2. Compress with zlib (deflate, level 9).
3. Base64-encode using the **URL-safe alphabet** (`+` → `-`, `/` → `_`), with no padding (`=` stripped).
4. Prepend `$ ` and append as the URL fragment.

The final URL format is:

```
https://www.falstad.com/circuit/circuitjs.html#<encoded_fragment>
```

Use the Python script `baseline-solution/scripts/gen_falstad_urls.py` as a reference for the encoding step, or implement the encoding inline. Verify the URL is well-formed before inserting it.

---

## Step 5 — Update baseline-solution.md

Open `baseline-solution/baseline-solution.md` and replace the existing Falstad simulation line for the chosen circuit with the new link. The line format must be:

```markdown
**Falstad simulation:** [Link to circuit](<new_url>)
```

Replace the entire existing `**Falstad simulation:**` line. Do not alter any other content in the file.

---

## Step 6 — Commit and Push

Stage `baseline-solution/baseline-solution.md` and commit with a message of the form:

```
Update Falstad link for <circuit name>
```

Push to `origin/main`.

---

## Notes for the Agent

- If the encoded URL exceeds browser limits (approximately 2000 characters), simplify the netlist by reducing component count while preserving the core operating principle, and note the simplification in the circuit description.
- Do not invent component values. Use only values visible in the schematic image or stated in the circuit description.
- The goal is a link that loads and simulates correctly in Falstad with no manual editing required.
