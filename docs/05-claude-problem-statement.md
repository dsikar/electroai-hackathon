# ElectroAI Hackathon: Problem Statement

---

## Problem Statement

Engineering design is visual before it is digital. Schematics are sketched on whiteboards, scanned from legacy documentation, photographed on site, extracted from PDFs, or shared as screenshots. These artefacts are readable by engineers, but they are not directly usable by the tools that matter: the simulators, layout editors, and design environments where real engineering work happens. Getting from an image to an editable, simulation-ready file is still a slow, manual process that depends on specialist knowledge and domain familiarity.

The software industry has begun addressing this problem, but unevenly. A gap analysis of the current engineering tool landscape — covering PCB design, systems simulation, industrial automation, and fluid power — shows that meaningful built-in AI exists only in selected workflows: primarily PCB layout optimisation in high-end enterprise tools, and simulation acceleration in premium multi-physics platforms. Most engineering software still relies on conventional automation: rule-based macros, template-driven assistance, and scripted routines that do not reason over engineering content. Cross-tool workflows are poorly served. Interpretation, extraction, and conversion across artefact types remain weak across the landscape. Dedicated tools for hydraulic and pneumatic circuit design have no documented AI at all.

The ElectroAI Hackathon challenges students to help close this gap from a different direction: not by building another feature inside an existing tool, but by building AI-agent workflows that work *around* and *between* tools — taking engineering artefacts as they actually appear in practice and producing structured outputs that engineering tools can use.

Teams are challenged to design systems that accept engineering images or diagram-like inputs — photographs of circuits, exported schematic PDFs, scanned hydraulic diagrams, or whiteboard sketches — analyse them intelligently, and generate outputs that are useful in real engineering workflows. This might mean extracting component lists, recognising circuit topology, inferring likely design intent, generating structured intermediate representations, or producing files ready to open in Proteus, LTspice, or KiCad.

The core engineering challenge is translation: from what an engineer can see, to what an engineering system can actually use. That translation requires more than OCR. It requires understanding component types, inferring connectivity from visual layout, reasoning about circuit intent, and producing outputs that are not just plausible but actionable. AI agents — combining vision-language models, structured prompting, rule-based checking, and tool-specific output generation — are the right technology to attempt this now. The question is how well, how reliably, and how usefully that can be done.

---

## Why This Problem Matters

- **The gap is real and documented.** Survey analysis of the engineering software landscape confirms that image interpretation, cross-tool conversion, and structured extraction from visual artefacts are weak across the market — including in tools that otherwise have sophisticated AI for other tasks.

- **The translation bottleneck is a daily friction in engineering practice.** Legacy documentation, site photographs, vendor datasheets, and hand-drawn schematics are a constant presence in real engineering workflows. None of these are directly importable into simulation tools without manual reconstruction.

- **AI agents make a viable approach possible now.** Vision-language models capable of interpreting technical diagrams, combined with structured prompting and agentic orchestration, have reached a point where useful engineering prototypes are within reach of a well-directed student team.

- **The output bar is engineering-specific, not just aesthetic.** A successful submission must produce something an engineer can actually use — a KiCad netlist, an LTspice simulation scaffold, a Proteus-compatible structure — not just a description of what was seen. That specificity makes this a more rigorous engineering challenge than a generic AI task.

- **The problem scales across domains.** The same core challenge — interpreting visual engineering artefacts and producing structured outputs — applies to electrical schematics, hydraulic circuits, pneumatic diagrams, and control system documentation. Teams can find a scope that suits their background.

- **Skills developed are directly transferable.** Agentic workflow design, structured prompting, engineering domain reasoning, and tool integration are skills with lasting value in professional engineering practice.

---

## Examples of Acceptable Student Directions

- **Schematic image to KiCad scaffold** — an agent that takes a photograph or screenshot of an electrical schematic and produces a KiCad-compatible netlist or schematic file that can be opened and refined in KiCad EDA.

- **Circuit diagram to LTspice simulation setup** — a workflow that analyses a circuit image, identifies components and values, infers connectivity, and generates a draft LTspice netlist ready for simulation.

- **Proteus-compatible component extraction and assembly** — an agent that extracts component identities, pin assignments, and likely connections from a schematic image and produces a Proteus-ready design file or structured import format.

- **Engineering-document understanding and structured extraction** — a system that processes multi-page PDFs or exported engineering documents, identifies schematic content, and generates structured component and connectivity tables that can be checked or imported.

- **Hydraulic or pneumatic circuit interpretation** — an agent that accepts an image of a hydraulic or pneumatic circuit diagram, identifies standard ISO symbols, infers circuit topology, and generates a structured representation with component list and connectivity.

- **Image-based design review and verification assistant** — a system that inspects a schematic image and flags likely errors, missing components, ambiguous connections, or violations of common design rules, producing an annotated output rather than a silent conversion.

- **Cross-tool conversion pipeline** — a workflow that takes image-derived circuit structure through multiple steps: extraction, validation, format conversion, and output to a specific tool format, with explanation at each stage.

- **Fault and anomaly explanation from diagram images** — an agent that takes an image of a real or simulated circuit condition, reasons about likely fault causes, and generates a structured diagnostic output grounded in the visible design.

---

## Scope Guardrails

This challenge is **not** about claiming perfect, lossless reverse engineering from any arbitrary image. Partial, approximate, and gracefully-degraded outputs that are useful to a working engineer are valid and encouraged.

This challenge is **not** limited to a single tool, format, or circuit domain. Electrical, hydraulic, pneumatic, and mixed-domain artefacts are all in scope. Outputs targeting Proteus, LTspice, or KiCad are all acceptable, as are structured intermediate formats that could feed any downstream tool.

This challenge is **not** satisfied by OCR. Reading text labels from an image is a small part of the problem. The engineering challenge is understanding topology, component types, connectivity, and intent — and producing outputs that reflect that understanding.

This challenge is **not** satisfied by a generic chatbot that describes what it sees without producing structured engineering value. An agent that returns a paragraph of prose about a schematic is not a valid submission. The output must be actionable in a real engineering workflow.

This challenge is **not** about replacing engineers. It is about building tools that help engineers move faster from image-based artefacts to usable engineering outputs — reducing friction in a part of the workflow that remains largely manual despite significant AI investment elsewhere in the industry.
