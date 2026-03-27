You are writing the **problem statement** for the **ElectroAI Hackathon**.

Your task is to produce a concise, technically credible problem statement for students, academic staff, judges, and external partners. The statement must be grounded in the repository's existing analysis, especially the gap analysis report, and must justify why this hackathon challenge is worth doing now.

## Core Challenge Direction

The hackathon is about building **AI-agent-driven applications** that can:

- take engineering images or diagrams as input
- analyse those images intelligently
- extract useful structure, components, connectivity, or intent
- generate outputs and files that are ready to be used in engineering tools such as:
  - **Proteus**
  - **LTspice**
  - **KiCad**

The emphasis is on practical engineering workflows, not just generic image recognition.

## Required Framing

The problem statement should clearly explain that students are being challenged to explore how AI agents can help bridge the gap between:

- unstructured engineering artefacts such as screenshots, PDFs, scans, photos, and schematic images
- structured, editable, simulation-ready, or design-ready engineering files

## Use The Gap Analysis

Use the repository's gap analysis findings to justify the problem statement.

You should explicitly incorporate the following types of gaps where supported by the report:

- AI maturity is uneven across engineering software
- strong built-in AI exists only in selected workflows
- many tools still rely on conventional automation rather than true AI reasoning
- cross-tool workflows remain poorly served
- verification, interpretation, and explanation remain weak
- hydraulic, pneumatic, industrial electrical, and image-to-structure workflows are underserved
- there is a clear opportunity for AI agents that work around and between engineering tools rather than only inside them

Do not invent gaps that are not supported by the existing reports.

## Inputs

Use the materials already in the repository, especially:

- the engineering software survey reports in `reports/`
- the gap analysis report in `reports/04-codex-gap-analysis.md`
- any notes or briefing materials that help keep the wording aligned with the hackathon direction

## What To Produce

Produce the following in Markdown:

1. **Problem Statement**
- A polished public-facing problem statement of approximately 250 to 500 words.

2. **Why This Problem Matters**
- 3 to 6 bullet points explaining why this is technically important, timely, and suitable for a hackathon.

3. **Examples Of Acceptable Student Directions**
- 4 to 8 bullet points showing the kinds of applications students might build, for example:
  - image to KiCad-ready structure
  - schematic image to LTspice netlist scaffold
  - diagram understanding and component extraction
  - image-based design review and verification assistant
  - cross-tool conversion and checking workflows

4. **Scope Guardrails**
- A short section explaining what the problem is **not**
- for example: not claiming perfect reverse engineering, not limited to a single vendor tool, not just OCR, not just a chatbot wrapper

## Style Requirements

- Write for an engineering audience
- Keep the tone technically serious, ambitious, and clear
- Avoid hype and generic AI marketing language
- Make the challenge sound difficult but tractable
- Keep the emphasis on engineering usefulness, structured outputs, and agentic workflows

## Output Quality Bar

The final result should be strong enough to use in:

- the README
- the hackathon website
- participant briefing materials
- sponsor or academic-facing summaries

It must read like a justified engineering challenge, not like a vague AI theme.

Write your problem statement into the docs directory, name 05-<your_name>-problem-statement.md

