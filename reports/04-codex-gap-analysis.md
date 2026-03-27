# EEAI Hackathon Engineering Software AI Gap Analysis

## Executive Summary

The survey reports point to a clear pattern: AI maturity in engineering software is uneven, concentrated in a handful of high-value domains, and often overstated by vendor marketing. PCB / EDA, high-end simulation, and broad engineering platforms now contain credible built-in AI in selected workflows such as placement, routing, optimisation, copilot assistance, and simulation acceleration. In contrast, hydraulic, pneumatic, industrial electrical schematic, and cross-tool workflows remain weakly served.

The strongest opportunity for the EEAI Hackathon is not to compete directly with the most advanced vendor features. It is to build AI-agent workflows around the gaps those products still leave open: cross-tool orchestration, engineering-document interpretation, verification, structured extraction, report generation, and domain-specific assistance in fluid power and industrial automation.

## Landscape Overview

Across the reports, the market splits into four broad groups.

First, a small set of products appear to have meaningful built-in AI capability in shipping or near-shipping form. Cadence Allegro X / OrCAD X is the clearest example in PCB layout automation. Siemens NX and the wider Siemens ecosystem also appear consistently in the stronger-AI category, especially for copilot, optimisation, and broader systems workflows. Ansys and MATLAB / Simulink are repeatedly identified as strong in AI-supported simulation, optimisation, and engineering analysis.

Second, several products sit in a mixed category where AI exists, but its role is narrower, less mature, or partly external. Altium appears in this group: some reports describe AI-assisted requirements, BOM intelligence, or cloud intelligence, while others conclude that native AI remains limited and that much of the innovation sits in surrounding tools. Autodesk products also sit here, with stronger platform-level AI and assistant capabilities than domain-specific AI for electrical engineering tasks.

Third, industrial electrical tooling appears to have strong automation but weaker confirmed built-in AI. EPLAN is the main example. The reports agree that it is important and highly relevant, but they disagree on whether current AI capability is genuinely embedded in the product or still largely partner-driven, roadmap-based, or demonstrated externally.

Fourth, hydraulic and pneumatic software remains the weakest category. Automation Studio, FluidSIM, and similar tools are repeatedly described as low-AI or no-AI environments. This is the cleanest gap across the full survey set.

There is also inconsistency in the product list across reports. That matters. It suggests the market is moving quickly and that some claimed capabilities are version-dependent, vendor-framed, or hard to distinguish from advanced automation. The gap analysis therefore needs to focus on robust patterns rather than individual marketing claims.

## Gap Analysis

### 1. Meaningful built-in AI exists, but only in selected workflows

The reports are most aligned on three areas of relative maturity:

- PCB / EDA layout optimisation, especially in Cadence products
- simulation and optimisation support, especially in Ansys and MATLAB / Simulink
- broad copilot or assistant functionality in large engineering platforms such as Siemens NX and Autodesk ecosystems

This means AI is no longer absent from engineering software, but it is still concentrated in premium workflows where the commercial value is obvious: faster layout, faster simulation, faster programming, or easier interaction with complex software.

### 2. Many products still rely on conventional automation rather than AI

A recurring pattern across the reports is that vendors blur the line between:

- rule-based automation
- template-driven assistance
- optimisation
- genuine AI capability

Industrial schematic tools and many mainstream engineering products still depend heavily on macros, design rules, scripted automation, template reuse, and conventional optimisation. These are valuable, but they do not amount to the kind of reasoning, interpretation, or adaptive assistance that hackathon teams may assume already exists.

This is especially important for challenge framing. The opportunity is not merely "add more automation." It is to target tasks where reasoning over engineering artefacts is still missing.

### 3. External AI is often more important than built-in AI

The surveys repeatedly show that real-world AI usage often happens outside the engineering package:

- LLMs used for documentation, code generation, and explanation
- external layout and optimisation engines connected to PCB tools
- AI agents built around files, APIs, or cloud services rather than embedded natively
- workflow bridging across products that do not speak to each other intelligently

This is a major structural gap. Even when individual tools have useful AI features, they rarely provide a coherent agentic workflow across the wider engineering process.

### 4. Cross-tool workflows remain poorly served

This is one of the most important gaps for the hackathon.

The reports suggest that modern engineering work is still fragmented across multiple tools for:

- schematic capture
- PCB layout
- simulation
- PLC / controls
- documentation
- manufacturing outputs
- fluid-power modelling

The vendors are improving single-product intelligence, but there is little evidence of strong AI that can:

- read outputs from one tool and generate meaningful inputs for another
- preserve engineering intent across domains
- generate structured reports from design data
- verify consistency across schematic, simulation, BOM, and documentation layers

This makes cross-tool agents one of the clearest opportunity areas.

### 5. Hydraulic and pneumatic design is the clearest underserved domain

This is the strongest consensus finding in the reports.

Dedicated hydraulic and pneumatic environments appear to have:

- little or no credible built-in AI
- limited public evidence of generative design
- limited evidence of copilot workflows
- continued dependence on simulation plus manual interpretation

Some reports mention automation or adjacent analytics, but none show fluid power tools matching the AI maturity seen in EDA or major simulation platforms. That gap is large enough to support multiple hackathon themes.

### 6. Industrial electrical schematic design also shows a gap between importance and AI maturity

EPLAN and related industrial electrical tooling are central to real engineering practice, but the reports do not show the same level of confirmed, shipping AI capability as the strongest EDA products.

The gap here is not lack of relevance. It is that:

- the workflow is important
- the pain points are real
- the automation is mature
- but the AI layer appears partial, unclear, or still emerging

That makes industrial electrical design a good hackathon target because the problem is real, but the vendor solution space is not yet saturated.

### 7. Verification, interpretation, and explanation remain weak

Even in tools with credible AI, there is limited evidence of strong support for:

- engineering document interpretation
- schematic understanding from images or PDFs
- automated reasoning over topology and connectivity
- standards-aware explanation
- report generation from design artefacts
- transparent verification of AI-generated outputs

This matters because many of the most practical engineering bottlenecks are not in drawing the design from scratch. They are in checking, understanding, translating, documenting, and validating it.

### 8. Evidence quality is uneven across the source reports

The source reports disagree in several places, especially around:

- whether Proteus has meaningful native AI
- how far Altium's AI goes beyond adjacent cloud or BOM features
- whether EPLAN's AI is embedded, partnered, demonstrated, or still emerging
- which products genuinely belong in the "top 10"

That uncertainty is itself useful. It suggests the hackathon should avoid overclaiming that "engineering tools already solve this with AI" and should instead frame the challenge around validated workflow gaps.

## Opportunity Areas For The Hackathon

The most promising hackathon directions are the ones that sit outside the strongest existing vendor features and address clear workflow pain.

### 1. Cross-tool engineering agents

Build agents that connect two or more tools or artefacts, for example:

- schematic to BOM / documentation
- schematic to simulation setup
- simulation results to plain-language report
- industrial electrical design to PLC / control logic scaffolding

This is a strong area because the reports consistently show fragmentation between products.

### 2. Schematic and engineering-document understanding

Build agents that can interpret:

- electrical schematics
- wiring diagrams
- hydraulic circuits
- pneumatic layouts
- engineering PDFs and images

The goal would be structured extraction, validation, explanation, or conversion into downstream engineering artefacts.

### 3. Fluid power AI assistance

Build AI support around hydraulic and pneumatic tools where vendor AI is weakest. Useful outputs could include:

- component identification
- fault explanation
- performance optimisation suggestions
- structured documentation
- training and tutoring support

This is a high-novelty area because the market appears thinly served.

### 4. Verification and review agents

Build agents that review engineering artefacts for:

- consistency
- missing information
- likely errors
- standards issues
- manufacturability or simulation-readiness

This plays to a genuine gap across the reports: verification is still labour-intensive even where generation is improving.

### 5. Engineering communication and deliverable generation

Build agents that produce:

- technical summaries
- design rationales
- lab or project reports
- IEEE-style paper scaffolds
- presentation content from project artefacts

This is especially suitable for a student hackathon because it links engineering work directly to academic and professional outputs.

## Recommendations

- Frame the hackathon around AI agents working across engineering workflows, not just AI inside individual tools.
- Avoid claiming that all major engineering tools already have mature built-in AI. The evidence does not support that.
- Prioritise challenge areas where vendor AI remains weak: hydraulic, pneumatic, industrial electrical schematic, cross-tool integration, document interpretation, and verification.
- Treat PCB / EDA automation as a comparative benchmark rather than the main novelty area, because some vendors are already significantly advanced there.
- Emphasise practical outputs that engineering academics and judges will value: validation, traceability, explanation, interoperability, and professional documentation.
- In workshops, distinguish clearly between conventional automation and genuine AI-assisted reasoning so students target real gaps.
- Use the survey disagreements as a prompt for careful challenge design: if a vendor feature is unclear, assume teams should build around the workflow gap rather than depend on proprietary AI claims.

The most defensible high-level framing is this: the market is starting to embed AI inside engineering tools, but there is still a large unsolved space around understanding, connecting, validating, and explaining engineering artefacts across tools and domains. That is where the EEAI Hackathon can be both credible and original.
