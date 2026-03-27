You are preparing a **gap analysis** for the **Electrical Engineering and AI Hackathon (EEAI Hackathon)** based on the engineering software AI survey reports already collected in this repository.

## Your Task

Read the available engineering software survey reports in the `reports/` folder and produce a clear gap analysis that compares the current landscape across the reviewed engineering tools.

Your aim is not to repeat each report in full. Your aim is to identify:

- where AI capability is already mature
- where AI support is partial, weak, or missing
- where engineering workflows still depend heavily on manual effort
- where hackathon participants could build useful AI-agent workflows or prototypes

## Inputs

Use the engineering software survey reports already present in the `reports/` directory, including the agent-specific reports and any shared source report if relevant.

Focus on findings related to:

- schematic capture
- PCB layout
- electrical design
- systems design
- hydraulic design
- pneumatic design
- simulation-linked workflows
- documentation, checking, optimisation, and automation

## Questions To Answer

Your gap analysis should address these questions:

1. Which engineering packages appear to have meaningful built-in AI capabilities?
2. Which packages mainly rely on conventional automation rather than AI?
3. Where is AI mostly external to the engineering package rather than built into it?
4. Which domains appear most advanced in AI adoption?
5. Which domains appear underserved?
6. What common gaps appear across the product landscape?
7. Where are the strongest opportunities for AI agents to support engineers outside the native tool features?
8. Which gaps are realistic and interesting enough to inform EEAI hackathon challenge themes?

## Required Output Structure

Produce a Markdown report with the following sections:

1. **Executive Summary**
- Short summary of the main gaps and the most promising opportunity areas.

2. **Landscape Overview**
- Concise summary of what the surveyed tools collectively show.

3. **Gap Analysis**
- Identify the main technical, workflow, and product gaps across the tools.

4. **Opportunity Areas For The Hackathon**
- Highlight the most useful challenge directions for students.

5. **Recommendations**
- Suggest how the hackathon problem framing should respond to the observed gaps.

## File Naming Requirement

Save the report in the `reports/` folder using this exact naming pattern:

`04-<agent-name>-gap-analysis.md`

Examples:

- `04-gemini-gap-analysis.md`
- `04-grok-gap-analysis.md`
- `04-claude-gap-analysis.md`

Use your own agent name in the filename.

## Quality Bar

- Be comparative, not repetitive.
- Focus on gaps, not just features.
- Be explicit about uncertainty where the source reports disagree or lack evidence.
- Write for an audience of engineering academics, technical organisers, and hackathon planners.
- Keep the output practical and useful for shaping the EEAI hackathon.
