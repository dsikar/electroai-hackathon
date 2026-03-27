# ElectroAI Hackathon Problem Statement

## Problem Statement

Many engineering workflows still begin with unstructured artefacts: screenshots of schematics, scanned drawings, exported PDFs, whiteboard sketches, photographed circuits, and image-based documentation. These artefacts may be readable by engineers, but they are not directly usable by the tools that support simulation, editing, verification, and design iteration. Converting them into structured engineering data remains time-consuming and heavily manual.

Current engineering software does include AI in selected areas, especially in some PCB layout, simulation, and high-end optimisation workflows. However, the gap analysis for this repository shows that AI maturity remains uneven. Many tools still depend primarily on conventional automation rather than true reasoning over engineering content, and cross-tool workflows remain poorly served. Interpretation, verification, explanation, and conversion from images into editable engineering structure are still weak across the landscape.

The ElectroAI Hackathon challenges students to build AI-agent-driven applications that help close this gap. Teams are invited to design systems that can take engineering images or diagram-like inputs, analyse them intelligently, and generate outputs that are useful in real engineering workflows. This may include extracting components, recognising connectivity, identifying likely circuit intent, generating structured intermediate representations, or producing files ready to be used in tools such as Proteus, LTspice, and KiCad.

The emphasis is not on generic OCR or a simple chatbot wrapper. The challenge is to create practical engineering workflows in which AI agents help transform unstructured visual artefacts into editable, simulation-ready, design-ready, or verification-ready outputs. Students are encouraged to combine image understanding, structured extraction, rule-based checking, prompting, tool integration, and engineering reasoning to produce applications that are technically useful, explainable, and grounded in real design practice.

This problem is worth tackling now because the strongest gaps are no longer at the level of basic automation alone. They sit between tools, across artefact types, and in the translation from what an engineer can see to what an engineering system can actually use. That makes this an important and credible challenge for an AI-and-engineering hackathon.

## Why This Problem Matters

- Engineering teams still spend significant manual effort interpreting diagrams and recreating them in tools before simulation, checking, or reuse can begin.
- The current software landscape shows uneven AI maturity, with strong features in selected products but persistent weakness in image interpretation, cross-tool conversion, and verification.
- AI agents offer a credible way to combine vision, prompting, structured extraction, and tool-specific output generation into practical engineering workflows.
- This challenge is well suited to a hackathon because useful prototypes can be built without needing to replace existing engineering tools entirely.
- The problem is relevant to academic, educational, and professional engineering practice, especially where documentation is incomplete, image-based, or spread across multiple systems.

## Examples Of Acceptable Student Directions

- An application that takes a schematic image and generates a KiCad-ready structured scaffold for further editing.
- An agent that analyses a circuit diagram image and produces an LTspice netlist draft or simulation setup scaffold.
- A workflow that extracts components, labels, and likely connectivity from an engineering PDF and generates a structured intermediate representation.
- A design-review assistant that inspects an image or exported schematic and flags likely omissions, ambiguities, or verification issues.
- A cross-tool agent that converts image-derived circuit structure into artefacts that can be checked in Proteus, LTspice, or KiCad.
- A system that pairs image understanding with rule-based validation so outputs are not only generated, but also explained and checked.

## Scope Guardrails

This problem is **not** about claiming perfect reverse engineering from any image.

This problem is **not** limited to a single vendor tool or file format.

This problem is **not** just OCR, and it is **not** satisfied by a generic chatbot that describes what it sees without producing structured engineering value.

This problem is **not** about replacing engineers. It is about building AI-agent workflows that help engineers move faster from image-based artefacts to usable engineering outputs.
