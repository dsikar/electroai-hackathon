# EEAI Hackathon: Engineering Software AI Gap Analysis

*Prepared by: Claude (claude-sonnet-4-6) | March 2026*

---

## 1. Executive Summary

The survey reports collectively show a market in transition: meaningful built-in AI exists in a small number of products, while the majority of engineering software either relies on conventional automation, wraps external AI at the platform level, or has no AI at all. The distribution is not random — it follows domain lines.

PCB layout and multi-physics simulation are the most advanced areas. Cadence Allegro X has shipped genuinely generative, reinforcement-learning-driven PCB automation; Ansys has deployed AI copilots across ten products. Systems engineering platforms (Siemens NX) have embedded conversational copilots and generative topology tools. In contrast, dedicated hydraulic and pneumatic design tools have no documented AI whatsoever. Industrial electrical schematic design (EPLAN) has compelling demonstrations but has not shipped AI inside the core product.

The strongest opportunity for the EEAI Hackathon is not to compete with the most capable vendor AI. It is to build AI-agent workflows around the gaps those products still leave open: fluid power design assistance, cross-tool orchestration, engineering-document interpretation, automated verification, and structured output generation. These are real, solvable problems that no vendor has addressed.

A secondary finding is that the source reports disagree significantly on Altium, EPLAN, and Proteus. That disagreement is itself informative — it indicates that AI marketing claims in engineering software frequently outpace what is actually in the shipping product. Hackathon challenge framing should account for this and be grounded in what teams can actually access and test.

---

## 2. Landscape Overview

Across the six source reports, the market divides into four tiers.

**Tier 1 — Genuine built-in AI (shipping and in production use):** Cadence Allegro X / OrCAD X, Siemens NX, Ansys, MATLAB/Simulink. These products have shipped AI that demonstrably changes engineering workflow speed and quality. The evidence is specific: benchmark studies, named enterprise customers, multiple release cycles. There is no significant disagreement across reports on this tier.

**Tier 2 — Meaningful but newer AI (shipping but recently introduced or architecturally narrow):** Proteus EDAi (v9.1, 2025), Autodesk Fusion 360, Siemens TIA Portal Engineering Copilot, Rockwell FactoryTalk Copilot. These products have real AI features, but either the features are new enough that independent verification is limited, or the AI addresses a narrower slice of the workflow than Tier 1.

**Tier 3 — AI at the platform or partner layer (not embedded in core design workflow):** Altium Designer, EPLAN Electric P8, Siemens Capital, Siemens Simcenter Amesim. These are mature products with AI activity at the surrounding ecosystem level — cloud platforms, partner integrations, roadmap items — but the core design environment either has no AI or has only peripheral AI features. The reports disagree most about products in this tier, which is itself evidence that the AI is not clearly present in day-to-day tooling.

**Tier 4 — No AI identified (conventional automation only):** Automation Studio, FluidSIM, KiCad (native). These products have no vendor-documented AI as of March 2026. Their automation is mature and rule-based, but there is no adaptive reasoning, generative design, or LLM integration in the product.

---

## 3. Gap Analysis

### 3.1 The vendor AI focus is narrow: layout and simulation dominate

The most advanced AI in the survey addresses two workflows: PCB layout optimisation (Cadence Allegro X) and simulation acceleration (Ansys SimAI, MATLAB ROM). Both of these are high-value, time-consuming, and amenable to reinforcement learning trained on large internal datasets. They are also premium-tier capabilities in expensive enterprise tools.

The implication is that AI development follows commercial incentive. Tasks that take expert engineers the most time — and where speed translates directly to revenue — have attracted investment. Tasks that are tedious but not billable (documentation, cross-tool translation, report generation) have not.

**Gap:** Verification, documentation, structured output generation, and cross-domain translation are underserved by built-in AI across the whole product landscape.

### 3.2 Fluid power design has no built-in AI

This is the strongest consensus finding across all six source reports. Automation Studio and FluidSIM — the dominant tools for hydraulic and pneumatic circuit design — have no documented AI features in vendor releases, technical documentation, or product pages as of March 2026.

The gap is large and clearly bounded. Both tools use standard file formats. Automation Studio exposes a scripting API. The engineering domain (component sizing, pressure drop calculation, topology selection) is well-defined and teachable. The physics is documented. This is not a hard integration problem — it is an unsolved one.

**Gap:** There is no AI assistant, copilot, or generative tool for dedicated hydraulic or pneumatic circuit design. This represents the clearest opportunity area in the entire survey.

### 3.3 Industrial electrical schematic design is a gap between importance and AI delivery

EPLAN Electric P8 is the global standard for industrial electrical schematic design. The reports agree on its importance. They also agree that AI has not shipped inside P8 itself. EPLAN's Hannover Messe 2025 demonstrations showed an AI-powered mounting plate layout tool, and the AIDA R&D division is active, but Platform 2026 is the anticipated delivery vehicle for product-level AI features.

There is some disagreement in the source reports here: the Grok and ChatGPT reports credit EPLAN with "automated circuit diagram generation" and "moderate" AI maturity. The Claude source report and the Codex gap analysis are more precise — these are automation features (macros, rules, templates) not AI reasoning. That distinction matters for hackathon challenge design.

**Gap:** Industrial electrical schematic design — motor control circuits, I/O mapping, cable schedules, cabinet layout — is still primarily manual in the dominant tool. AI that interprets a machine specification and generates an EPLAN-compatible schematic outline would address a real and unmet need.

### 3.4 Cross-tool workflow intelligence does not exist as a product

Modern engineering projects use multiple tools from different vendors. A typical industrial automation project might use Altium for PCBs, EPLAN for electrical schematics, Siemens TIA Portal for PLC code, Automation Studio for hydraulics, and MATLAB for control system validation. Each of these tools is improving its internal AI, but none provides an intelligent bridge to any other.

There is no product that can:
- Read a hydraulic circuit from FluidSIM and suggest the corresponding PLC I/O map
- Take a Proteus schematic and generate a BOM with live pricing
- Convert a MATLAB Simulink model output into a plain-language engineering report
- Check consistency between a schematic in Altium and documentation in a PDF

The MCP protocol, which Proteus and MATLAB have both adopted or documented, makes this class of integration significantly easier to prototype. The building blocks exist. The bridges do not.

**Gap:** Cross-tool orchestration is completely absent as a vendor feature, and MCP tooling now makes it tractable as a hackathon prototype.

### 3.5 Verification and review remain manual even where generation is AI-driven

Even in products with the most advanced generative AI (Cadence Allegro X, Siemens NX), the reports indicate that verification of AI-generated outputs is still largely manual. Engineers run DRC checks, review placements, and validate simulation results by hand. There is no AI that can explain *why* a generated design is correct, flag likely errors before manual review, or run targeted edge-case simulations automatically.

This is particularly significant as generative design becomes more common. The bottleneck shifts from creation to validation. The reports do not show any product that has solved this.

**Gap:** AI-assisted verification agents — tools that run automated checks, explain design decisions, and flag likely failures in AI-generated outputs — are absent from the market.

### 3.6 Source report disagreements indicate marketing-reality gaps

The six source reports disagree notably on three products:

| Product | Range of assessments |
|---|---|
| Altium Designer | "High maturity" (Claude) to "None identified" (DeepSeek) to "Low-medium" (ChatGPT) |
| EPLAN Electric P8 | "Automated circuit generation" (Grok, ChatGPT) vs "No AI in P8 product" (Claude) |
| Proteus Design Suite | "Very high / architecturally sophisticated" (Claude, Grok) vs "None identified / Low" (Mistral, Grok v2) |

In all three cases, the most likely explanation is that vendor marketing language conflates automation with AI, and that feature availability is strongly version-dependent (Proteus EDAi is a 2025 addition not reflected in older sources). The Claude source report is the most consistently precise about this distinction.

**Implication for challenge design:** Hackathon teams should verify AI feature availability in the specific tool version they will use. Challenge themes should not assume any Tier 3 product has shipping, accessible AI.

---

## 4. Opportunity Areas for the Hackathon

### 4.1 AI assistance for fluid power design (highest novelty and clearest gap)

Build an AI agent that supports hydraulic or pneumatic circuit design in environments where no vendor AI exists.

Possible directions:
- Circuit diagram interpretation: parse a FluidSIM or Automation Studio file (or an image of a hydraulic schematic) to identify components, topology, and likely design intent
- Component sizing assistant: take a specification (flow rate, pressure, actuator load) and suggest appropriate valve, pump, or cylinder specifications
- Fault and failure explanation: given a described symptom in a hydraulic or pneumatic system, reason about likely component failures
- Design review: flag common errors (undersized lines, missing check valves, incorrect relief valve settings)

This area is completely uncontested from a vendor perspective and directly relevant to real engineering practice.

### 4.2 Schematic and engineering-document understanding

Build agents that can interpret structured or unstructured engineering artefacts:
- Electrical schematics (Proteus, KiCad, EPLAN formats or exported images)
- Wiring diagrams and P&IDs
- Engineering PDFs and specification documents

Useful outputs would include structured extraction (component lists, connectivity tables), validation against design rules, plain-language explanation, or conversion into downstream artefacts (BOM, PLC tag list, simulation setup).

KiCad's S-expression file format is human-readable and well-documented. Proteus EDAi already demonstrates what schematic-aware AI looks like — a hackathon project that extends this approach to KiCad, or applies it to EPLAN output formats, would be both practical and well-scoped.

### 4.3 Cross-tool engineering agents

Build agents that bridge two or more tools using standard file formats or MCP:
- Proteus schematic → BOM with live Octopart pricing
- Automation Studio hydraulic model → PLC I/O suggestion for TIA Portal
- MATLAB Simulink output → plain-language performance report
- EPLAN project → structured commissioning checklist

The Proteus MCP server documentation and MATLAB MCP Server provide concrete entry points. Cross-tool agents do not require deep integration with proprietary APIs — they work on exported files and standard formats.

### 4.4 Verification and review agents

Build agents that review AI-generated or manually created designs:
- Run targeted DRC-style checks against component datasheets
- Identify missing information (decoupling capacitors, pull-up resistors, missing ground connections)
- Flag standard violations (IPC, IEC, ISO)
- Explain AI-generated design decisions in plain language

This targets the verification gap that persists even in the most AI-advanced tools. It also has clear academic value: a verification agent that explains *why* a design choice is correct or incorrect is directly useful for engineering education.

### 4.5 Engineering communication and deliverable generation

Build agents that produce professional outputs from engineering artefacts:
- Technical design summaries from schematics or simulation results
- Lab report scaffolds from Proteus or MATLAB simulation data
- IEEE-paper-style abstracts from project descriptions and results
- Commissioning and test documentation from EPLAN or TIA Portal data

This is particularly suitable for a student hackathon because it connects engineering work to academic and professional output formats that participants understand and value.

---

## 5. Recommendations

**Frame challenges around AI agents working across engineering workflows, not AI inside individual tools.** The most capable vendor AI is not accessible, teachable, or improvable within a hackathon. The gaps in cross-tool intelligence, fluid power design, and verification are accessible, well-defined, and produce tangible outputs.

**Prioritise domains where vendor AI is absent or clearly missing.** Hydraulic and pneumatic design, industrial electrical schematic generation, and cross-tool integration are the strongest areas. These are not niche — they represent a large proportion of industrial engineering practice.

**Do not frame PCB layout AI as a hackathon challenge.** Cadence Allegro X has genuinely solved this for enterprise users. Student projects in this space will not produce competitively interesting results, and teams will spend most of their time working around tool access limitations.

**Distinguish explicitly between automation and AI in workshops and challenge briefs.** Several source reports conflate these, and students will make the same mistake. A design rule checker is not AI. A macro template is not AI. Targeted challenge framing that requires reasoning, interpretation, or adaptive behaviour will produce more interesting submissions.

**Use accessible tools as the challenge platform where possible.** KiCad (free), Proteus (time-limited demo with EDAi), MATLAB Student, and Automation Studio (trial) are all accessible without commercial licences. EPLAN, Cadence, and Siemens NX require institutional or educational licence arrangements that may create access inequality across teams.

**Treat Proteus EDAi as the reference example of good AI integration architecture.** It provides live schematic context to the AI, supports self-hosted models for IP privacy, exposes an MCP interface, and works for both professional and educational users. Challenge workshops should use it to demonstrate what well-integrated AI looks like, because it sets a concrete bar that student projects should aspire to match or extend.

**Acknowledge source uncertainty in challenge briefs.** The source reports disagree on Altium, EPLAN, and Proteus. Teams selecting these as their platform should be advised to verify AI feature availability in the version they can actually install. Challenges built on claimed AI features that turn out to be unavailable will waste time and frustrate participants.

---

*Sources: 03-claude-engineering-software-ai-survey-report.md, 03-gemini-engineering-software-ai-survey-report.md, 03-chatgpt-engineering-software-ai-survey-report.md, 03-grok-engineering-software-ai-survey-report.md, 03-mistral-engineering-software-ai-survey-report.md, 03-deepseek-engineering-software-ai-survey-report.md*
