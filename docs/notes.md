Arduino: ultra-constrained microcontroller platform → on-device inference only (no training)
Raspberry Pi: Linux-based edge device → supports full ML stacks and system integration
Libraries (Arduino): TensorFlow Lite for Microcontrollers, Edge Impulse, EloquentTinyML
Libraries (Raspberry Pi): TensorFlow, PyTorch, OpenCV, Ultralytics YOLO
Arduino typical role: sensor-edge intelligence (event detection, classification triggers)
Raspberry Pi typical role: edge AI hub (vision, speech, robotics control)
Hardware acceleration (Pi): Google Coral, Intel OpenVINO
Data flow pattern: Arduino → preprocessing/inference → Pi → aggregation/decision/API
Key constraint: memory (Arduino) vs thermal/CPU limits (Pi)
Design trend: distributed edge AI (split workloads across MCU + SBC)


Language models:
Arduino: ultra-small on-device models via TensorFlow Lite for Microcontrollers
Pi: runs compact LLMs (e.g. llama.cpp) locally
Tooling: Edge Impulse (MCU), Ollama (Pi)
Pattern: MCU = trigger/feature extraction → Pi = language reasoning
Constraint: quantisation + small context windows required for on-device LLMs

Scope for IoT ?

General VLMs applied to EE: GPT-4V, LLaVA show emergent ability to read schematics, but struggle with symbol grounding, topology, and multi-step reasoning
Diagram understanding research: work on chart/diagram QA (e.g. ChartQA) transfers partially, but EE schematics require graph extraction, not just visual QA
Circuit parsing pipelines: hybrid approaches (CV + graph reconstruction) outperform end-to-end VLMs; focus on symbol detection → netlist extraction → reasoning
Domain-specific datasets (limited): PubLayNet, DocVQA used as proxies; true EE-labelled datasets remain scarce
SPICE / code reasoning: LLMs (text-only or multimodal) can generate and interpret SPICE (e.g. Ngspice), but correctness depends on explicit constraints and verification loops
Key bottleneck: mapping pixels → structured circuit graph (nodes, components, connectivity) remains unsolved at scale
Evaluation gap: no standard benchmark for “schematic → simulation → reasoning” pipeline accuracy
Emerging direction: tool-augmented VLMs (vision + symbolic solvers + simulators) outperform standalone models
Practical systems: combine detection (e.g. YOLO) + OCR + rule-based netlist generation + simulation
Research opportunity: multimodal agents that close the loop (image → netlist → SPICE → verification → explanation)

Problem: Engineering diagrams (electrical, hydraulic, pneumatic) are locked in PDFs/images → not machine-readable or queryable
Pain point: Manual interpretation → engineers must trace connectivity, verify designs, and translate into simulation (e.g. SPICE) by hand → slow and error-prone
Cross-domain issue: Symbol + topology understanding differs across EE, hydraulics, pneumatics → no unified parsing or reasoning pipeline
Operational impact: Maintenance, fault diagnosis, and onboarding rely on expert knowledge → poor scalability and knowledge loss
Target problem statement:
Develop a vision-language system that converts engineering schematics into structured, simulation-ready representations and supports automated reasoning, validation, and fault analysis across domains.


