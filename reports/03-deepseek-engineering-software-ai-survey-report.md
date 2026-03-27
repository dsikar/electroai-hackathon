# EEAI Hackathon: Engineering Software & AI Integration Survey

## Executive Summary

This survey reveals that **AI integration in engineering software is rapidly accelerating**, with 2025-2026 marking a transition from experimental features to production-ready AI assistants. Major vendors including **Cadence, Siemens, Synopsys/Ansys, PTC, SolidWorks, and Autodesk** have all released AI-powered capabilities within the past 12 months.

Key patterns observed:
- **PCB/EDA AI is most mature** – Cadence Allegro X AI delivers 50-70% time reduction in PCB layout through reinforcement learning 
- **Mechanical CAD AI focuses on generative design and error diagnosis** – SolidWorks and Creo offer AI-guided error fixing and assembly generation 
- **Simulation AI enables agentic workflows** – Ansys 2026 R1 includes AI agents for mesh diagnostics and design exploration 
- **Open-source catching up** – KiCad (Huaqiu distribution) now includes AI Copilot for symbol/footprint generation from images 
- **Embedded AI development is well-supported** – MATLAB/Simulink provides end-to-end workflows for training and deploying edge AI models 

Gaps remain in **hydraulic and pneumatic system design**, where AI features are not yet prominent in mainstream tools.

---

## Top 10 Package Review

### 1. Allegro X AI (Cadence)

| Attribute | Detail |
|-----------|--------|
| **Vendor** | Cadence Design Systems |
| **Primary Use** | PCB layout, schematic capture, electronic design automation |
| **Relevance** | High for PCB design, electrical systems |

**AI Built-In Tools:** Allegro X AI uses reinforcement learning trained on Cadence’s internal design library (not customer data) to automate component placement, copper pours, and routing. It runs on secure AWS infrastructure and delivers 50–70% reduction in PCB design time .

**AI Used Alongside:** Not applicable – AI is natively integrated.

**Assessment:** Most mature AI integration among EDA tools. Supports feasibility studies, full board design, and design updates. Results show week-long tasks reduced to minutes .

---

### 2. Altium Designer

| Attribute | Detail |
|-----------|--------|
| **Vendor** | Altium |
| **Primary Use** | PCB design, schematic capture, harness design |
| **Relevance** | High for PCB, electrical systems, multi-board projects |

**AI Built-In Tools:** **None identified** in current documentation. Altium focuses on integrated harness design within the same environment but does not market AI copilot features as of March 2026 .

**AI Used Alongside:** Third-party AI tools (e.g., EMA’s AI integrations, external routing assistants) can complement Altium workflows.

**Assessment:** Industry-standard PCB tool but lagging in native AI integration compared to Cadence.

---

### 3. SolidWorks (Dassault Systèmes)

| Attribute | Detail |
|-----------|--------|
| **Vendor** | Dassault Systèmes |
| **Primary Use** | Mechanical CAD, systems design, industrial engineering |
| **Relevance** | High for mechanical integration, industrial workflows |

**AI Built-In Tools:** SolidWorks 2026x FD01 introduces multiple AI-powered beta features :
- **AI-guided error root cause analysis** – identifies why part model errors occur
- **Prompt-guided drawing generation** – specify size, format, views via natural language
- **AI-powered assembly structure generation** – create assembly structures from prompts
- **Context Assistant notifications** – suggests component patterns and configuration tips

**AI Used Alongside:** 3D EXPERIENCE platform integration.

**Assessment:** Rapidly expanding AI portfolio with practical CAD assistance features now in beta.

---

### 4. Ansys (Synopsys)

| Attribute | Detail |
|-----------|--------|
| **Vendor** | Synopsys (acquired Ansys) |
| **Primary Use** | Multiphysics simulation, systems design, embedded software |
| **Relevance** | High for simulation-driven design across electrical, mechanical, thermal |

**AI Built-In Tools:** Ansys 2026 R1 includes :
- **Generative AI and agentic workflows** – concept design exploration
- **Mesh Agent** – diagnoses model pre-processing failures
- **Discovery Validation Agent** – pre-identifies setup issues
- **Ansys SimAI Pro** – AI-powered simulation acceleration
- **Ansys Engineering Copilot** – expanded AI assistant coverage

**AI Used Alongside:** Integration with Synopsys tools (VC Functional Safety Manager, TPT) for automated safety verification.

**Assessment:** Leading in simulation AI with multi-agent approach to automation.

---

### 5. Siemens NX

| Attribute | Detail |
|-----------|--------|
| **Vendor** | Siemens Digital Industries |
| **Primary Use** | Integrated CAD/CAM/CAE, systems engineering, industrial design |
| **Relevance** | High for mechanical, manufacturing, and multi-domain systems |

**AI Built-In Tools:** **AI Make Machining Suggestion (MMS)** in NX X Manufacturing :
- Suggests toolpaths, tools, and parameters for machining features
- Works on face-by-face basis (2.5 and 3-axis machining)
- Learns from historical CAM data to generate personalized suggestions
- Future roadmap includes agentic workflows for full-part programming

**AI Used Alongside:** Not documented beyond built-in features.

**Assessment:** Strong AI application in CAM domain with clear roadmap toward autonomous programming.

---

### 6. Autodesk Fusion / AutoCAD

| Attribute | Detail |
|-----------|--------|
| **Vendor** | Autodesk |
| **Primary Use** | CAD, CAM, CAE, PCB design (Fusion Electronics), industrial design |
| **Relevance** | Broad across mechanical, electrical, and industrial workflows |

**AI Built-In Tools:** Autodesk AI capabilities include :
- **AutoCAD Smart Blocks** – recognizes similar geometry and suggests block conversion
- **Generative design** (Fusion) – AI-driven design exploration
- **Autodesk Assistant** – AI agent with MCP (Model Context Protocol) server integration
- Roadmap includes AI agents that can orchestrate across Autodesk products via natural language

**AI Used Alongside:** MCP servers enable Claude and other LLMs to access Autodesk data; users can build custom AI agents .

**Assessment:** Strategic platform-level AI investment with open MCP architecture enabling custom agent development.

---

### 7. MATLAB & Simulink (MathWorks)

| Attribute | Detail |
|-----------|--------|
| **Vendor** | MathWorks |
| **Primary Use** | Algorithm development, multidomain simulation, embedded AI deployment |
| **Relevance** | High for electrical systems, control design, embedded AI in engineered systems |

**AI Built-In Tools:** End-to-end embedded AI workflow :
- System-level simulation to validate AI behavior before deployment
- Multi-target deployment (C/C++, CUDA, HDL) from same Simulink model
- Compression techniques for resource-constrained edge devices
- Verification and validation for safety-critical systems
- Low-code apps for training AI models without deep expertise
- Integration with PyTorch, TensorFlow, ONNX, XGBoost

**AI Used Alongside:** PyTorch models can be imported and deployed through MATLAB/Simulink.

**Assessment:** Most comprehensive platform for **developing** AI that will run within engineered systems, rather than AI that assists design.

---

### 8. PTC Creo

| Attribute | Detail |
|-----------|--------|
| **Vendor** | PTC |
| **Primary Use** | CAD, generative design, simulation-driven design, manufacturing |
| **Relevance** | High for mechanical design, electrification, composites |

**AI Built-In Tools:** Creo 11 includes :
- **AI-powered generative design** – enhanced with minimum feature size limits, bearing load support, planar symmetry constraints
- Integration with Ansys-based simulation for simulation-driven design

**AI Used Alongside:** Creo+ SaaS offering with cloud collaboration.

**Assessment:** Established generative design capabilities with ongoing AI enhancements.

---

### 9. KiCad (Huaqiu Distribution)

| Attribute | Detail |
|-----------|--------|
| **Vendor** | KiCad (open source) / Huaqiu distribution |
| **Primary Use** | Open-source PCB design, schematic capture |
| **Relevance** | High for educational contexts, cost-sensitive PCB projects |

**AI Built-In Tools:** Huaqiu KiCad 9.0.7 distribution includes AI Copilot with :
- **Image-to-symbol generation** – paste component image, generate schematic symbol
- **Image-to-footprint generation** – supports IPC packages (BGA, DIP, SOP, QFN, etc.)
- **Pre-set prompt templates** – save and reuse AI prompts
- Integrated Freerouter for basic autorouting

**AI Used Alongside:** Not applicable – AI is built into the distribution.

**Assessment:** Most accessible AI-assisted PCB tool for students and open-source community; not in official KiCad (Huaqiu-specific).

---

### 10. Proteus (Labcenter Electronics)

| Attribute | Detail |
|-----------|--------|
| **Vendor** | Labcenter Electronics |
| **Primary Use** | Schematic capture, PCB layout, microcontroller simulation |
| **Relevance** | High for education, embedded system prototyping |

**AI Built-In Tools:** **None identified** in current documentation. Proteus focuses on mixed-mode simulation and microcontroller co-simulation.

**AI Used Alongside:** Students may use external AI tools (e.g., ChatGPT) for code generation or design assistance, but no native AI integration.

**Assessment:** Widely used in education but not yet incorporating AI features.

---

## Table: AI Built-In Tools Summary

| Product Name | AI Built-In Tools |
|--------------|------------------|
| **Allegro X AI** | Reinforcement learning for PCB placement/routing; 50-70% time reduction; feasibility studies; design updates |
| **Altium Designer** | None identified |
| **SolidWorks** | AI-guided error analysis; prompt-driven drawing generation; AI-powered assembly structure generation (beta) |
| **Ansys** | Generative AI; Mesh Agent; Discovery Validation Agent; SimAI Pro; Engineering Copilot |
| **Siemens NX** | AI Make Machining Suggestion (toolpath/tool/parameter recommendations); personalized suggestions from historical data |
| **Autodesk Fusion/AutoCAD** | Smart Blocks; generative design; Autodesk Assistant; MCP server for AI agent integration |
| **MATLAB/Simulink** | End-to-end embedded AI workflow; PyTorch integration; low-code AI training; multi-target deployment |
| **PTC Creo** | AI-powered generative design with feature size limits, bearing load support, symmetry constraints |
| **KiCad (Huaqiu)** | AI Copilot: image-to-symbol; image-to-footprint; pre-set prompts; auto-router integration |
| **Proteus** | None identified |

---

## Observations

### Where AI Is Genuinely Built In

1. **PCB Design Automation (Cadence Allegro X AI)** – Most mature: reinforcement learning model trained on professional design patterns delivers measurable productivity gains (50-70%) .

2. **CAD Error Diagnosis & Generation (SolidWorks, Creo)** – AI helps diagnose why features fail and can generate assemblies or drawings from prompts .

3. **Simulation Automation (Ansys)** – Agentic AI (Mesh Agent, Validation Agent) automates pre-processing and setup, reducing manual simulation configuration .

4. **CAM Programming (Siemens NX)** – AI suggests machining strategies and learns from past programming history .

5. **Generative Design (Creo, Fusion)** – AI explores design alternatives within defined constraints .

### Where AI Is Mostly External

- **Altium Designer** and **Proteus** show no native AI features; users must rely on third-party add-ons or external tools.

- **KiCad official** lacks AI; only the Huaqiu distribution includes AI Copilot features .

### Domains More Advanced

- **PCB layout automation** (Allegro X AI)
- **Simulation** (Ansys agents)
- **Generative mechanical design** (Creo, Fusion)
- **Embedded AI development** (MATLAB/Simulink)

### Domains Underserved

- **Hydraulic system design** – No AI features identified in dedicated hydraulic tools; integration occurs within mechanical platforms (Creo, SolidWorks) but not AI-specific.
- **Pneumatic system design** – Similarly lacking AI; likely covered through general CAD AI features rather than domain-specific AI.
- **Open-source EDA** – AI only available in third-party distributions, not official releases.

---

## Hackathon Relevance

### What This Landscape Suggests

1. **AI in engineering software is at an inflection point** – Major vendors are shipping AI features, but adoption and workflow integration remain early-stage.

2. **The gap between "AI-assisted" and "fully automated" is large** – Current tools assist with specific tasks but don’t yet offer autonomous design.

3. **Hydraulic/pneumatic domains present opportunity** – No dedicated AI tools identified; students could build AI agents that interpret schematics or suggest component sizing.

### Potential Hackathon Themes

| Gap | Potential AI-Agent Project |
|-----|---------------------------|
| **Hydraulic/pneumatic design** | LLM-based assistant that reads circuit diagrams, calculates component sizes, or suggests valve configurations |
| **Cross-tool orchestration** | MCP server connecting Altium or Proteus to LLMs for natural-language PCB layout commands (inspired by Autodesk’s MCP approach ) |
| **EDA automation for open-source** | Build AI Copilot features for official KiCad (image-to-symbol, placement suggestions) |
| **Documentation generation** | AI agent that generates manufacturing docs, BOMs, and assembly instructions from design files |
| **Design rule checking with AI** | ML-based DRC that learns from past design violations to predict issues before layout |
| **Embedded AI integration** | Use MATLAB/Simulink to design and deploy an AI model for predictive maintenance or virtual sensing in a hardware prototype |

### Recommended Hackathon Tracks

1. **AI-Assisted Engineering Design** – Build agents that help engineers design faster (PCB, hydraulic, pneumatic, or mechanical systems)

2. **AI for Manufacturing** – CAM programming, machining optimization, or quality inspection workflows

3. **Embedded AI in Engineered Systems** – Deploy AI on edge devices for real-time control, monitoring, or diagnostics using MATLAB/Simulink workflows 

4. **Open-Source Engineering AI** – Extend KiCad, FreeCAD, or other open tools with AI capabilities

### Suggested Workshops

- **"Building MCP Servers for Engineering Tools"** – Based on Autodesk’s MCP architecture 
- **"AI-Assisted PCB Design with Cadence Allegro X AI"** – Demo of reinforcement learning in action
- **"Deploying AI on Microcontrollers with MATLAB"** – End-to-end embedded AI workflow
- **"Prompt Engineering for CAD Generation"** – Hands-on with SolidWorks AI features

---
