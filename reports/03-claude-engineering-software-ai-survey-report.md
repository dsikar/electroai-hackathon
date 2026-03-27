**EEAI Hackathon**

Market & Technology Survey

AI in Engineering Design Software

*March 2026 \| Prepared for EEAI Hackathon Planning*

**Executive Summary**

This survey examines the top ten engineering software packages most
relevant to the EEAI Hackathon's focus areas: electrical schematic
capture, PCB layout, electronic design automation (EDA), systems design,
hydraulic and pneumatic system design, and industrial engineering
workflows. The research draws on vendor documentation, release notes,
and product pages published up to March 2026.

The headline finding is that AI integration across professional
engineering software is accelerating sharply, but the depth and
credibility of that integration varies considerably. EDA vendors —
particularly Cadence, Siemens (Mentor), and, to a notable degree, the
smaller Labcenter Electronics — have moved furthest from aspiration to
working product. Siemens' broader engineering platform (NX, Simcenter,
Capital) has embedded AI copilots, topology optimisers, and generative
design tools that are already generally available, not just roadmap
items. Ansys, now part of Synopsys, has shipped a multi-product
Engineering Copilot and seven AI+ product lines. MATLAB/Simulink has
launched MATLAB Copilot and deep AI toolboxes.

In contrast, EPLAN Electric P8 — the dominant tool in industrial
electrical schematic design — has AI roadmap activity and compelling
Hannover Messe demonstrations, but AI features are not yet productised
inside the P8 environment itself. Famic Technologies' Automation Studio
(hydraulics, pneumatics, PLC) and Festo's FluidSIM remain almost
entirely without built-in AI. KiCad, the leading open-source EDA tool,
has no native AI, though a rich community ecosystem of external MCP
servers and plugins is rapidly emerging around it.

The clearest opportunity gap for hackathon teams is in the fluid power
and industrial automation domains. Hydraulic and pneumatic design tools
are largely unserved by vendor AI. A secondary gap exists in intelligent
agent workflows that can bridge tools — for example, reading an EPLAN
schematic and generating PLC code, or taking a Proteus simulation output
and building a component report. These are natural hackathon challenges.

**Top 10 Engineering Package Review**

Each package is reviewed against the criteria set out in the survey
scope: engineering domain, AI built-in features, AI used alongside the
product, and maturity assessment.

|                                                                |                                                                                                                                                                                                              |
|----------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **1. Altium Designer / Altium 365** \| Altium (Autodesk Group) |                                                                                                                                                                                                              |
| **Primary domain**                                             | Schematic capture, PCB layout, EDA, harness design                                                                                                                                                           |
| **AI built-in features**                                       | ML component search; AI requirements management (LLM-based); BOM intelligence; AI-assisted procurement via Octopart; documented GPT Action integrations for lab control                                      |
| **AI alongside tool**                                          | Community-built ChatGPT/Claude workflows for firmware generation, embedded code, digital twin conversation with PCB designs; external AI test automation                                                     |
| **Maturity**                                                   | High. Long-established platform. AI features shipping in current versions. Cloud-first Altium 365 accelerates delivery.                                                                                      |
| **Why selected**                                               | *The leading commercial PCB/schematic tool in professional and educational contexts. Explicit AI machine learning marketing and documented community AI workflows make it highly relevant to the hackathon.* |

|                                                              |                                                                                                                                                                         |
|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **2. Cadence OrCAD X / Allegro X** \| Cadence Design Systems |                                                                                                                                                                         |
| **Primary domain**                                           | Schematic capture, PCB layout, signal integrity, power integrity, EDA                                                                                                   |
| **AI built-in features**                                     | Allegro X AI: AI-automated component placement, power plane synthesis, critical net routing; AI-driven DFM feedback; Live BOM with AI supply chain risk analysis        |
| **AI alongside tool**                                        | Integration with Dassault 3DEXPERIENCE; PSpice simulation co-analysis; OrCAD X cloud collaboration with AI automation                                                   |
| **Maturity**                                                 | High. Allegro X AI is a shipping product available from release 25.1. Enterprise customers such as Schneider Electric are using it in production.                       |
| **Why selected**                                             | *Industry-grade PCB EDA with the most advanced built-in AI layout automation in the sector. Strong hackathon relevance for AI-assisted layout optimisation challenges.* |

|                                                                            |                                                                                                                                                                                                                                                                    |
|----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **3. Siemens NX (Designcenter NX)** \| Siemens Digital Industries Software |                                                                                                                                                                                                                                                                    |
| **Primary domain**                                                         | Mechanical CAD, systems design, electronics integration, manufacturing, PLM                                                                                                                                                                                        |
| **AI built-in features**                                                   | NX X Copilot: natural language interface, voice commands, documentation-grounded guidance; Topology Optimizer (generative design, GPU-accelerated); DFM Advisor (AI manufacturability); Selection Prediction; Design Space Explorer (multi-objective optimisation) |
| **AI alongside tool**                                                      | Siemens Xcelerator platform; Teamcenter X PLM; Simcenter multiphysics; NVIDIA NIM microservices for further AI acceleration                                                                                                                                        |
| **Maturity**                                                               | High. Copilot shipping since June 2025. Generative design features mature across multiple releases. NVIDIA strategic partnership active.                                                                                                                           |
| **Why selected**                                                           | *The dominant mechanical/systems engineering platform with arguably the most complete built-in AI toolkit of any engineering package surveyed. Essential reference for the hackathon's systems design theme.*                                                      |

|                                                               |                                                                                                                                                                                                                                                                                                                                        |
|---------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **4. Proteus Design Suite 9.1** \| Labcenter Electronics Ltd. |                                                                                                                                                                                                                                                                                                                                        |
| **Primary domain**                                            | Schematic capture, mixed-mode SPICE simulation, microcontroller co-simulation (VSM), PCB layout, education                                                                                                                                                                                                                             |
| **AI built-in features**                                      | EDAi (v9.1, 2025): ProPilot for professional design — circuit-aware real-time AI co-pilot; ProTutor for education; supports GPT / Claude / DeepSeek / on-premise LLMs; MCP integration; schematic + simulation + firmware context                                                                                                      |
| **AI alongside tool**                                         | User-configurable LLM backends; self-hosted inference for data privacy; Claude Desktop integration planned/documented                                                                                                                                                                                                                  |
| **Maturity**                                                  | AI features are new (2025) but architecturally sophisticated. EDA core (schematic, VSM, PCB) is very mature (35+ years). EDAi open architecture is a differentiator.                                                                                                                                                                   |
| **Why selected**                                              | *Specifically requested in the hackathon brief. Notable for being a smaller vendor that has shipped a more deeply integrated AI system than several larger competitors. The EDAi architecture — live schematic/simulation context + open LLM choice + MCP support — is a model of how AI should be integrated into engineering tools.* |

|                                                               |                                                                                                                                                                                                                                                                                      |
|---------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **5. Siemens Capital** \| Siemens Digital Industries Software |                                                                                                                                                                                                                                                                                      |
| **Primary domain**                                            | Electrical system design, wire harness, E/E architecture, automotive/aerospace ECU development                                                                                                                                                                                       |
| **AI built-in features**                                      | Capital X cloud platform includes AI-enhanced workflow guidance; Fuse EDA AI Agent (Siemens EDA portfolio, announced DAC 2025) covers overlapping PCB domains. TIA-to-Capital AI prototype demonstrated at Hannover Messe 2025 (not yet productised)                                 |
| **AI alongside tool**                                         | Siemens Industrial Copilot; Teamcenter X; NX electromechanical co-design; Polarion requirements management                                                                                                                                                                           |
| **Maturity**                                                  | Capital itself is mature and widely deployed. AI integration is emerging: platform-level AI is advancing but tool-level AI features within Capital are at earlier stages than NX.                                                                                                    |
| **Why selected**                                              | *The dominant electrical systems design tool for automotive and aerospace. Covers wire harness, E/E architecture, and embedded software — domains central to the EEAI Hackathon. Included because of professional domain relevance even though direct built-in AI is less advanced.* |

|                                                                                              |                                                                                                                                                                                                                                                                                                               |
|----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **6. EPLAN Electric P8 / EPLAN Platform** \| EPLAN Software & Services (Friedhelm Loh Group) |                                                                                                                                                                                                                                                                                                               |
| **Primary domain**                                                                           | Electrical schematic design, control cabinet engineering, fluid power planning, PLC integration, industrial automation documentation                                                                                                                                                                          |
| **AI built-in features**                                                                     | EPLAN Copilot (Hannover Messe 2025 demo): AI mounting plate layout using Azure OpenAI. AI knowledge acquisition chatbot (AIDA division). Automated 3D panel layout. Most features are pre-release / roadmap for Platform 2026. P8 2025 itself does not yet ship general AI features in the product.           |
| **AI alongside tool**                                                                        | Siemens Industrial Copilot integration (TIA Portal prototype); Microsoft Azure OpenAI (backend); Rittal manufacturing integration                                                                                                                                                                             |
| **Maturity**                                                                                 | Core EPLAN P8 product: very mature (industry standard for 40 years). AI features: early stage — demonstrations exist but product-level AI shipping is expected with Platform 2026, not yet widely available.                                                                                                  |
| **Why selected**                                                                             | *The global standard for industrial electrical schematic design. Included because of its critical domain relevance to the hackathon. Its AI gap is also the most significant opportunity for hackathon participants — building AI agents that read and generate EPLAN data is a high-value unsolved problem.* |

|                                                                            |                                                                                                                                                                                                                                                                                                             |
|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **7. Ansys Electronics Desktop / Ansys Suite** \| Ansys (part of Synopsys) |                                                                                                                                                                                                                                                                                                             |
| **Primary domain**                                                         | Multi-physics simulation: electromagnetics, structural, fluids, photonics, electronics, signal integrity, system modelling                                                                                                                                                                                  |
| **AI built-in features**                                                   | Engineering Copilot (in 10 products from 2025 R2); SimAI (surrogate modelling, 10–100x faster design exploration); TwinAI (physics-AI digital twins); GeomAI (generative geometry); AI+ in 7 products; AnsysGPT (GPT-4o-based knowledge assistant); SimAI Pro (local GPU, 2026 R1)                          |
| **AI alongside tool**                                                      | Synopsys EDA chip-to-system workflow; NVIDIA Omniverse for AV perception validation; Azure AI Foundry                                                                                                                                                                                                       |
| **Maturity**                                                               | High. Engineering Copilot and SimAI are shipping products. Broad AI portfolio covers both productivity (copilot) and engineering AI (surrogate models, digital twins). Part of Synopsys accelerates silicon-to-system scope.                                                                                |
| **Why selected**                                                           | *The leading multi-physics simulation suite with directly relevant electromagnetic and electronics simulation capabilities (HFSS, AEDT, Maxwell). AI integration is broad and shipping. Hackathon relevance for students working on antenna design, EMC, power electronics, or multi-physics optimisation.* |

|                                       |                                                                                                                                                                                                                                                                                                          |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **8. MATLAB / Simulink** \| MathWorks |                                                                                                                                                                                                                                                                                                          |
| **Primary domain**                    | Systems modelling, control design, signal processing, AI/ML development, embedded systems, code generation, hydraulic/pneumatic modelling (Simscape)                                                                                                                                                     |
| **AI built-in features**              | MATLAB Copilot (generative AI assistant, 2025); Deep Learning Toolbox (full DL framework); Simulink AI blocks (Detect Drift, RL, incremental learning); Simscape Fluids (hydraulic/pneumatic + AI co-simulation); automated C/C++/CUDA/HDL code generation; MATLAB MCP Server for AI tool integration    |
| **AI alongside tool**                 | GitHub Copilot via MATLAB MCP Server; NVIDIA GPU acceleration; Python interop for ML frameworks; Qualcomm NPU and Infineon hardware deployment                                                                                                                                                           |
| **Maturity**                          | Very high. MATLAB is a foundational tool in engineering education and industry. AI/DL toolboxes have been developed over many years. MATLAB Copilot is the newest addition (2025). MCP Server is recent and growing.                                                                                     |
| **Why selected**                      | *The standard platform for model-based design, control systems, signal processing, and embedded AI across aerospace, automotive, and electronics. Unique dual role as both an engineering tool and an AI development environment. Highly relevant to the hackathon's cross-domain systems design theme.* |

|                                                                        |                                                                                                                                                                                                                                                                                                                                    |
|------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **9. Siemens Simcenter Amesim** \| Siemens Digital Industries Software |                                                                                                                                                                                                                                                                                                                                    |
| **Primary domain**                                                     | Multi-domain system simulation: hydraulic, pneumatic, thermal, mechanical, electrical, electromechanical; 1D system modelling; HIL/SIL co-simulation                                                                                                                                                                               |
| **AI built-in features**                                               | Simcenter X Advanced (2025): AI documentation assistant, AI setup guidance, AI-augmented design exploration with HEEDS. AI in vehicle dynamics and real-time optimisation workflows. Note: core Amesim 1D simulation engine does not have deep AI integration; AI is primarily at the SaaS/optimisation layer.                     |
| **AI alongside tool**                                                  | Simcenter HEEDS (multi-objective AI optimisation); STAR-CCM+ CFD; MATLAB/Simulink; real-time targets; CAD co-simulation                                                                                                                                                                                                            |
| **Maturity**                                                           | Amesim core: very mature (industry standard for hydraulic/pneumatic system simulation). AI features in Simcenter X: new (November 2025). The Simcenter X SaaS platform is the main AI delivery vehicle.                                                                                                                            |
| **Why selected**                                                       | *The most relevant professional tool for hydraulic and pneumatic system simulation at the engineering level. Its inclusion represents the fluid power domain — a hackathon theme area with very limited AI tooling. Relevant to students designing hydraulic actuators, pneumatic control systems, or vehicle thermal management.* |

|                                                                             |                                                                                                                                                                                                                                                                                                                                        |
|-----------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **10. Automation Studio / FluidSIM** \| Famic Technologies / Festo Didactic |                                                                                                                                                                                                                                                                                                                                        |
| **Primary domain**                                                          | Hydraulic circuit design and simulation; pneumatic circuit design and simulation; electrical control diagrams; PLC simulation; industrial automation training                                                                                                                                                                          |
| **AI built-in features**                                                    | None identified. Both products are actively maintained but vendor documentation, release notes, and product pages contain no AI or ML features as of March 2026.                                                                                                                                                                       |
| **AI alongside tool**                                                       | Automation Studio: scripting API and Unity 3D linkage could be used to build external AI integrations. FluidSIM: standard file formats could be parsed by AI tools. No documented AI workflows found.                                                                                                                                  |
| **Maturity**                                                                | Core product maturity: high (both are long-established tools). AI maturity: none. This represents the clearest gap in the market for hackathon AI agent development.                                                                                                                                                                   |
| **Why selected**                                                            | *Included together as the dominant tools in hydraulic and pneumatic circuit design for both education and industry. Their AI gap is the most significant in the survey, and directly relevant to the hackathon's fluid power theme. Building AI wrappers, agents, or copilots around these tools is a clear and actionable challenge.* |

**Summary Table: AI Built-In Tools**

Green rows indicate products with shipping built-in AI features. Amber
rows indicate AI in development, demonstrated but not yet productised,
or only at the surrounding platform layer.

| **Product Name**                      | **AI Built-In Tools (as of March 2026)**                                                                                                                                                                                 |
|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Altium Designer / Altium 365**      | ML component search; AI requirements management; BOM intelligence; documented GPT Action workflows (lab control, firmware generation)                                                                                    |
| **Cadence OrCAD X / Allegro X**       | Allegro X AI: AI-automated component placement, power plane synthesis, critical net routing; AI-driven DFM advisor; Live BOM AI supply chain analysis                                                                    |
| **Siemens NX (Designcenter NX)**      | NX X Copilot (natural language, voice); Topology Optimizer (generative design); DFM Advisor; Design Space Explorer (multi-objective AI optimisation); ML Selection Prediction                                            |
| **Proteus Design Suite 9.1 (EDAi)**   | EDAi: ProPilot (circuit-aware real-time AI co-pilot, schematic + simulation + firmware context); ProTutor (AI-guided learning); open LLM architecture (GPT/Claude/DeepSeek/on-premise)                                   |
| **Siemens Capital**                   | Capital X cloud AI guidance; Fuse EDA AI Agent (PCB/semiconductor, announced 2025); TIA-to-Capital AI integration prototype (not productised). Limited direct AI within Capital itself.                                  |
| **EPLAN Electric P8 / Platform**      | EPLAN Copilot (mounting plate layout via Azure OpenAI, Hannover Messe 2025 demo — pre-release). AI knowledge chatbot (AIDA division). Platform 2026 AI features pending. P8 2025 itself: no AI shipped in product.       |
| **Ansys Electronics Desktop / Suite** | Engineering Copilot (10 products, 2025 R2, free to licensed users); SimAI (surrogate modelling, 10–100x faster exploration); TwinAI; GeomAI; AnsysGPT; AI+ in 7 products; SimAI Pro (local GPU, 2026 R1)                 |
| **MATLAB / Simulink**                 | MATLAB Copilot (2025); Deep Learning Toolbox (full ML/DL); Simulink AI blocks (drift detection, RL, incremental learning); Simscape Fluids + AI co-simulation; MATLAB MCP Server; automated GPU/FPGA/MCU code generation |
| **Siemens Simcenter Amesim**          | Simcenter X Advanced AI (documentation chat, setup guidance, AI-augmented design exploration via HEEDS, November 2025). Core Amesim 1D simulation: no deep AI integration.                                               |
| **Automation Studio / FluidSIM**      | None identified. No AI or ML features in vendor documentation, release notes, or product pages as of March 2026.                                                                                                         |

**Observations**

**Where AI is genuinely built in**

Four products have shipped substantive, production-quality AI features
that are available to licensed users today:

- Cadence OrCAD X / Allegro X AI offers the most advanced AI-automated
  PCB layout of any tool surveyed. Allegro X AI reduces component
  placement from days to minutes and is used in production at Schneider
  Electric. This is not a demo.

- Siemens NX (Designcenter NX) has the most comprehensive built-in AI
  for mechanical and systems engineering, including a conversational
  copilot (NX X Copilot), GPU-accelerated generative topology
  optimisation, and an AI-driven manufacturability checker. This has
  evolved across several release cycles.

- Ansys 2025 R2 ships a cross-portfolio Engineering Copilot (10
  products), SimAI surrogate modelling, and seven AI+ product lines.
  This is the broadest AI deployment across a single vendor's simulation
  portfolio.

- Proteus EDAi (v9.1) is notable for its architecture: the AI assistant
  has live access to schematic, simulation state, and firmware — not
  just a generic LLM wrapper. Its support for self-hosted models and MCP
  protocol is ahead of much larger vendors.

**Where AI is mostly external or at the platform level**

Several products have AI activity but it is primarily at the surrounding
platform or partner-integration layer, not embedded in the core design
workflow:

- EPLAN Electric P8 has compelling AI demonstrations (Hannover Messe
  2025 Copilot for mounting plate layout) and an active AIDA R&D
  division, but AI features are not yet shipping in P8 itself. The
  Platform 2026 release is the anticipated delivery vehicle.

- Siemens Capital AI is mainly delivered through the Xcelerator platform
  ecosystem (Capital X SaaS, Teamcenter X) rather than through core
  Capital design tools. The TIA Portal integration with Eplan is a
  prototype.

- MATLAB/Simulink occupies a dual role: it is both an AI platform
  (engineers build AI in it) and a design environment with AI features
  (MATLAB Copilot, MCP Server). The AI toolboxes are mature but serve a
  different function from design-layer copilots.

- Simcenter Amesim gains AI primarily through the Simcenter X SaaS
  platform and HEEDS optimisation engine, not through changes to the
  Amesim 1D simulation core.

**Which domains appear more advanced**

PCB/EDA is the most advanced domain for built-in AI. Cadence and Siemens
EDA have been working on AI-automated layout since the DARPA IDEA
programme (2018). Schematic-level AI is following closely (Proteus EDAi,
Altium AI features). Mechanical/systems design has mature generative
design and topology optimisation (NX) but copilot-style conversational
AI is newer. Multi-physics simulation (Ansys) has the broadest AI
portfolio but it is primarily support-level and surrogate modelling.

**Which domains are still underserved**

Fluid power (hydraulic and pneumatic design) has no meaningful AI
integration in its dedicated tools. Neither Automation Studio nor
FluidSIM has any vendor AI features. This is the clearest gap in the
market. Industrial electrical schematic design (EPLAN) is also behind —
the dominant tool in its domain has AI on the roadmap but not yet in the
product. The gap between marketing language and available features is
widest in these two domains.

**Hackathon Relevance**

The survey landscape suggests several actionable challenge framings for
the EEAI Hackathon. The most defensible and novel are in the domains
where vendor AI is absent or minimal — where student teams are genuinely
building something new rather than recreating existing product features.

**High-value challenge areas**

**1. AI agents for fluid power design (highest novelty)**

Neither Automation Studio nor FluidSIM has any AI. A hackathon team
could build an agent that reads a hydraulic or pneumatic circuit
description (or even an image of a circuit diagram), identifies
component specifications, validates against physical constraints, and
suggests alternative components or design improvements. The open file
formats of both tools make this tractable. This is a completely
uncontested space from a vendor perspective.

**2. AI copilot for EPLAN schematic generation**

EPLAN P8 is the global standard for industrial electrical design but has
no shipped AI. Building an agent that can take a machine specification
document, extract I/O requirements, and generate an EPLAN-compatible
schematic (or at minimum a structured schematic outline with component
suggestions) would directly address a documented engineering bottleneck.
EPLAN has published its data standards, making this technically
accessible.

**3. Cross-tool AI bridging agents**

Many engineering workflows span multiple tools. Examples: reading a
Proteus schematic and automatically generating a BOM with live pricing
from Octopart; taking a Simcenter Amesim model and generating a
plain-language performance report; building a pipeline from MATLAB
Simulink model to EPLAN schematic. None of these bridges exist as
products. The MCP protocol now makes this class of integration
significantly easier to prototype.

**4. AI-assisted circuit review for KiCad**

KiCad is free, open-source, widely used in education and hackathons, and
has no native AI. The human-readable S-expression file format is ideal
for AI parsing. External tools and MCP servers already exist in
community repositories (several documented in this survey). A hackathon
challenge could focus on building a reliable AI design review agent that
checks KiCad schematics against common design rules, datasheet
parameters, and component availability — significantly advancing
community tooling.

**5. AI optimisation wrapper for existing simulation tools**

Where tools like Automation Studio or FluidSIM expose scripting APIs or
standard formats, hackathon teams could build an AI optimisation loop
that drives the simulation tool through parameter sweeps, applies ML
surrogate modelling to speed up exploration, and presents results in
natural language. This is the approach Ansys uses with SimAI — but
applied to tools that have no such capability built in.

**Workshop and challenge framing recommendations**

- Workshop 1 — Understanding the landscape: Survey walk-through covering
  tools, AI maturity, and API access. Hands-on with Proteus EDAi, KiCad,
  and MATLAB Copilot as reference examples of different AI integration
  levels.

- Workshop 2 — MCP and agent architecture: How to build MCP servers for
  engineering tools. Reference: Proteus's published MCP documentation
  and the KiCad MCP community projects.

- Workshop 3 — Fluid power domain introduction: Overview of
  hydraulic/pneumatic design, Automation Studio and FluidSIM as
  challenge platforms. Guest from industry on real-world fluid power
  design bottlenecks.

- Challenge track A — EDA AI: Build an AI agent for KiCad or Proteus
  that adds a missing capability (component selection, DRC explanation,
  firmware suggestion, BOM generation).

- Challenge track B — Industrial automation AI: Build an AI agent for
  EPLAN or Automation Studio that automates a tedious workflow
  (schematic generation from spec, mounting plate layout, hydraulic
  circuit validation).

- Challenge track C — Cross-tool intelligence: Build an agent pipeline
  that bridges two or more engineering tools using standard file formats
  or MCP, delivering an insight or output that neither tool provides
  alone.

**Uncertainty and limitations**

This survey is based on vendor documentation, release notes, and
credible third-party sources current to March 2026. AI feature claims in
engineering software marketing frequently outpace actual shipping
functionality. Where evidence is limited to conference demonstrations or
press releases rather than technical documentation, this has been noted
explicitly. Teams should verify feature availability in the specific
tool versions accessible to them before scoping challenges around
particular products.

Hackathon access to commercial tools (Cadence, Siemens NX, EPLAN, Ansys)
may require educational licensing arrangements. Proteus offers a
time-limited demo. KiCad, MATLAB (student), and Automation Studio
(trial) are accessible without a commercial licence.

*EEAI Hackathon Survey \| March 2026 \| Prepared for academic and
industry planning purposes*
