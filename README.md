<div align="left">
  <img src="comms/5100_SST_Hackathon_update_-_digital_screen_AL1c.jpg" width="80%" alt="ElectroAI Hackathon Splash Image">
</div>

# ElectroAI Hackathon: Engineering Translation

**Bridging the Gap Between Visual Schematics and Digital Simulation**

The **ElectroAI Hackathon** (April 6 - 10, 2026) is a technically serious student event focused on using **AI Agents** to solve a persistent friction in engineering practice: the "translation bottleneck."

**[Register Now](https://forms.gle/Ajmfw7kZdqPx9pWHA)**

## The Problem Statement
Engineering design is visual before it is digital. Schematics are sketched on whiteboards, scanned from legacy documentation, or shared as screenshots. While readable by engineers, these artifacts are not directly usable by the tools that matter—simulators, layout editors, and design environments like KiCad, LTspice, or Proteus.

Gap analysis of the current engineering software landscape confirms that image interpretation, structured extraction, and cross-tool conversion remain weak. The ElectroAI Hackathon challenges you to bridge this gap by building AI-agent workflows that can reason over engineering content and produce actionable outputs.

## The Challenge
Teams are challenged to design AI-agent systems that accept engineering images or diagram-like inputs (photographs, PDFs, scans, whiteboard sketches), analyze them intelligently, and generate outputs ready for use in real engineering workflows.

This is more than OCR. It requires **Engineering Translation**:
- **Recognizing** component types and values from visual symbols.
- **Inferring** circuit topology and connectivity.
- **Reasoning** about design intent and functional blocks.
- **Generating** structured files (netlists, scaffolds, or tables) usable by professional EDA tools.
---

## Success Criteria

- **Engineering usefulness:** Outputs should be directly usable in a real engineering workflow, such as simulation, documentation, review, or further design work.
- **Technical accuracy:** Solutions should identify components, values, topology, and functional blocks with defensible engineering logic.
- **Structured output:** Teams should produce clear machine-readable or engineer-ready outputs such as netlists, structured tables, JSON, or simulator scaffolds.
- **Transparent reasoning:** Good solutions should highlight ambiguities, assumptions, and possible errors rather than hiding uncertainty.
- **Documentation quality:** Each team should submit a clear IEEE-style paper that explains the problem, approach, technical decisions, results, and limitations in a professional engineering format.
- **Practical delivery:** Projects should be demonstrated as credible working prototypes, not just conceptual ideas or slideware.

## Tools (full licence) available to CSG students
- **Siemens NX**
- **Matlab/Simulink**
- **Proteus**
- **Many more**

## Open source tools used in baseline solutions
- **LTSpice**
- **Falstad**
  
## IEEE Standard Article with Findings
Each team is required to produce a professional engineering article in IEEE format detailing their findings, methodology, and results. This is a critical output of the hackathon, ensuring that technical decisions and performance are documented with the same rigour as the prototype itself.

You can use the following article as an example of the expected structure and depth:
- **[Example IEEE Article: Can AI See Structure in Schematics?](ElectroAIHackathonIEEETemplate/ElectroAIHackathonIEEETemplate.pdf)**
- **[IEEE LaTeX Template Repository](https://github.com/dsikar/ElectroAIHackathonIEEETemplate)**

## Judge Panel

- **[Dr Dave Muir](https://uk.linkedin.com/in/dr-dave-d-muir-883b3b39)**: Lecturer Eng. Systems (AI-Automation, Electrical & STEM), Prog. Director Renewable Energy & Power Sys. Man. MSc., Dept of Engineering, School of Science & Technology, University Sustainability Operations Lead, City St George's University of London.
- **[Leotis Buchanan](https://ca.linkedin.com/in/leotis-buchanan)**: AI/ML Engineer, PhD Research Student at City St George's, University of London.
- **[David Lee](https://www.cubic.com/transportation)**: System Support Engineer, Cubic Transportation Systems
- **Nicola Farquharson**: IT Consultant

## Event Schedule & Support

| Day | Date | Time | Event | Lead | Location | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Tuesday | April 7, 2026 | 11:00-12:00 | [Intro session pptx](docs/EEAI_IntroRev2.pptx) | Dave Muir | Microsoft Teams / AG06 | Event introduction and team selection |
| Wednesday | April 8, 2026 | 10:00-12:00 | Setting up AI Agents | Daniel Sikar | Microsoft Teams / AG01 | Turn up whenever you can, Dave will also be present for support |
| Wednesday | April 8, 2026 | 15:00-17:00 | Setting up AI Agents | Daniel Sikar | Microsoft Teams / AG06 | Turn up whenever you can, Dave will also be present for support |
| Thursday | April 9, 2026 | 10:00-11:30 | [Data Visualisation Presentation Slides](docs/SofiiaMyrvodaDataVizPresentation.pdf) | Sofiia Myrvoda | Microsoft Teams / A111 | Turn up whenever you can, Dave will also be present for support |
| Thursday | April 9, 2026 | 13:30-15:00 | Coding with LLM APIs using Python and Google Colab | Syed Mahbubul Huq | Microsoft Teams / A111 | Turn up whenever you can, Dave and Daniel will also be present for support |
| Thursday-Friday | April 9-10, 2026 | 21:00-08:00 | Allnighter | Daniel Sikar | Microsoft Teams / TBC | Turn up whenever you can, whether you are starting from scratch or fine-tuning your project for the final presentation. Pizza, Monster and snacks provided |
| Friday | April 10, 2026 | 10:00-13:00 | Fine-tuning and presentation practice | Daniel | Microsoft Teams / AG01 | Lunch provided 13:00-14:00 |
| Friday | April 10, 2026 | 14:00-16:00 | Presentations, deliberations and awards | Dr Dave Muir, Leotis Buchanan, David Lee| Microsoft Teams / AG04 | Lunch provided 13:00-14:00 |

**All online sessions will use the Microsoft Teams meeting link listed below.**
```
Microsoft Teams meeting

Join:
https://teams.microsoft.com/meet/313823308641173?p=bQU78Ar5AGnrIU2yRj

Meeting ID:
313 823 308 641 173

Passcode:
Nu2yD6VN
```

### Workshops (Tue April 7 – Thu April 9)
Join us for three days of focused technical sessions covering agent setup, LLM API workflows, and technical documentation:
- **Building AI Agents:** Learn how to design workflows specifically for schematic analysis.
- **Programmatic LLM Interaction:** Master expert prompting techniques to interact with models programmatically—**no previous software engineering skills required.**
- **Data & Documentation:** Techniques for effective data visualization and professional engineering documentation.

### The Allnighter (Thu April 9)
Join the overnight build session from **21:00 to 08:00** online or in person, with the in-person venue to be confirmed. Pizza, Monster, and snacks will be provided.

### Support & Baseline
- **Introduction Presentation:** [EEAI_IntroRev2.pptx](docs/EEAI_IntroRev2.pptx)
- **Baseline Solution:** Every team will receive a functional baseline solution to jumpstart their project.
- **Baseline Solution 1:** [Image2Spice](https://github.com/EndryuN/Image2Spice) (local clone: [baseline-solution-1](baseline-solution-1)) was provided by MSc Data Science student Andrew Nguyen who also participated in the Clinical AI Hackathon.
- **Expert Mentoring:** Access to mentors specialized in AI agentic tools and electrical engineering.
- **Community:** Join our official **Discord** for real-time support and updates: https://discord.gg/R3GpYZBXZ

### Final Presentation (Fri April 10)
Deliver your final project and presentation to our panel of judges.

## Winning Teams
- **Team Andrew:** [Image2Spice](https://github.com/EndryuN/Image2Spice)
- **Team Ben:** [Baseline Solution](https://github.com/dsikar/electroai-hackathon/tree/main/baseline-solution)

---

## The Master Prompt
Use this "System Instruction" to ground your AI agent in the hackathon’s specific technical context:

> **Role:** You are an expert Electrical Engineering AI Agent specializing in schematic interpretation and structured data extraction. Your goal is to bridge the gap between visual engineering artifacts (PDFs, scans, photos, screenshots) and actionable engineering formats (KiCad, LTspice, Proteus, or structured JSON/XML).
>
> **The Problem:** Engineering diagrams are often locked in non-digital formats. Manual conversion to simulation-ready files is slow and error-prone. You must move beyond simple OCR to perform "Engineering Translation."
>
> **Your Task:**
> 1. **Analyze:** Deconstruct the visual input to identify component types, values, and visual topology.
> 2. **Reason:** Infer connectivity and circuit intent. Recognize standard ISO/IEEE symbols and identify functional blocks.
> 3. **Extract:** Generate a structured representation (e.g., a KiCad netlist, an LTspice scaffold, or a component-and-connectivity table).
> 4. **Validate:** Identify potential ambiguities or design rule violations in the source image.
>
> **Success Criteria:**
> - **Engineering usefulness:** Produce outputs that an engineer can use directly in simulation, documentation, review, or further design work.
> - **Technical accuracy:** Prioritize correct components, values, topology, and functional interpretation over superficial visual similarity.
> - **Structured output:** Return machine-readable or engineer-ready outputs such as netlists, structured tables, JSON, or simulator scaffolds.
> - **Transparency:** Flag ambiguities, assumptions, and possible errors rather than guessing incorrectly.
> - **Documentation support:** Contribute material that can feed into a clear IEEE-style paper describing the method, results, and limitations.

---

## Outputs & Judging
- **Working Prototype:** Each team should deliver a credible prototype that demonstrates engineering translation in practice, not just a concept.
- **IEEE-Style Paper:** Each team should submit a professional paper documenting the problem, method, technical decisions, results, and limitations.
- **Professional Judging:** Entries will be judged on engineering usefulness, technical accuracy, structured output quality, and clarity about assumptions or ambiguity.
- **Transferable Skills:** Participants will build practical experience in agentic workflows, technical documentation, and engineering-focused AI development.
