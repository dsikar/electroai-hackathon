# 06 Print Scoring Rubric Prompt

Author: Claude Code

## Prompt Purpose

Use this prompt to instruct an agent or developer to create a print-ready scoring rubric
sheet for the ElectroAI Hackathon judges.

## Existing Source Material

The scoring criteria already defined in `docs/judging-criteria.md` must be used as the
authoritative source. The key content is reproduced below for reference.

### Scoring Scale (1–4)

| Score | Meaning |
|-------|---------|
| **1** | Not all core requirements implemented — major gaps; missing required artefacts or does not fully solve the task |
| **2** | All core requirements implemented — working prototype, repository, IEEE-style paper, and presentation all provided; works end-to-end at a solid level |
| **3** | Surpassed expectations — noticeably better: clever features, polish, real-world ready |
| **4** | Blew my mind — exceptional: innovative, engineering-relevant, wow factor |

**Guidance for a score of 4:** Use sparingly for projects that genuinely surprise or impress
— e.g., unusually accurate extraction on tricky real-world engineering inputs, useful
engineer-facing additions, elegant handling of edge cases, or clear potential to save serious
time and effort in engineering workflows. It should feel like *"this could actually change how
we work"*.

### Required Submission Artefacts

Each team must provide the following before judging begins:

1. **Working prototype** — a demonstrable prototype that runs or can be shown working end-to-end on a meaningful part of the task.
2. **GitHub repository link** — the final submission repo containing the prototype code and supporting materials.
3. **IEEE-style paper** — a PDF of the team's findings placed in the `docs/` directory of their repo, clearly named `<team name>-ieee.pdf`.
4. **Presentation** — a clearly named presentation file, `<team name>.pdf` or `<team name>.ppt`, placed in the `docs/` directory of the repo.

### Scoring Categories

The two scoring categories that need a score are:

1. **Understanding** — how well the team understood the engineering problem, constraints, and significance, as evidenced in the paper and presentation
2. **Solution** — how well the working prototype and repository address the task in practice

The result is by majority decision.

### Judges

- Dr Dave Muir (CSG)
- Leotis Buchanan (CSG)
- David Lee (Cubic)
- TBA

### Teams

Up to 10 teams will be scored.

---

## Prompt

Create a single print-ready HTML file containing the scoring rubric for the ElectroAI
Hackathon judges.

### Layout

The document should fit on **one or two A4 pages** (210mm × 297mm) in portrait orientation
and contain the following sections in order:

#### 1. Header

- Event name: **ElectroAI Hackathon**
- Title: **Judge Scoring Sheet**
- A field for the judge to write their name: `Judge: ___________________________`
- A field for the date: `Date: ___________________________`

#### 2. Scoring Scale Reference Box

A clearly boxed reference section showing the 1–4 scale with the label for each score, as
specified above. Include the guidance note for score 4 in smaller italic text beneath the
table. This box must appear at the top of the scoring sheet so judges can refer to it while
scoring without turning the page.

#### 3. Submission Requirements Box

A clearly boxed section listing the four required deliverables:

- Working prototype
- GitHub repository
- IEEE-style paper
- Presentation

Include the naming and location conventions for the paper and presentation.

#### 4. Scoring Table

A table with the following columns:

| Team # / Name | Reqs 1–4 | Understanding (1–4) | Solution (1–4) | Total (2–8) | Notes |
|---------------|----------|---------------------|----------------|-------------|-------|

- Ten rows (one per team), with alternating light background shading for readability.
- The `Reqs 1–4` column should contain four small handwritten check boxes labelled `1`, `2`, `3`, and `4` so the organiser can mark whether each submission requirement was met.
- The **Total** column should have enough space for the judge to write the sum.
- The **Notes** column should be wide enough for a short handwritten comment (at least 4 cm).
- All score cells should be large enough to write a single digit clearly (minimum 1.5 cm wide).

#### 5. Prize Category Summary

A small section below the table with boxes for the judge to record their
recommended winner after scoring is complete:

- Best Understanding → `Winner: ___________________________`
- Best Solution → `Winner: ___________________________`
- Overall Winner → `Winner: ___________________________`

#### 6. Footer

A small footer with the text:
*"ElectroAI Hackathon — Confidential judge scoring sheet"*

### Design Requirements

- Clean, professional, print-friendly style — black text on white background.
- Use a sans-serif font (e.g. Arial, Helvetica, or a Google Font such as Inter or Source Sans Pro).
- The scoring scale reference box should have a visible border and a light grey background to
  distinguish it from the table.
- All styling must be in a `<style>` block within the single HTML file — no external
  dependencies that require an internet connection at print time.
- Include a `@media print` CSS block that:
  - Sets paper size to A4 portrait (`@page { size: A4 portrait; margin: 15mm; }`)
  - Hides any browser UI elements
  - Preserves table borders and shading (`-webkit-print-color-adjust: exact; print-color-adjust: exact`)
- The file must print correctly from Chrome, Firefox, and Safari without manual adjustment.

### Output

Save the file as:

```
comms/hackathon-scoring-rubric.html
```

Open it in a browser and use **File → Print** (or Ctrl+P / Cmd+P) to print or save as PDF.
Print one copy per judge (three copies total).

---

## Author Attribution

This prompt was authored by Claude Code.
