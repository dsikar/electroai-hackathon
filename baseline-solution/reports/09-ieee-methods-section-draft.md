# IEEE Methods Section Draft

Insertion note: the current workspace does not contain `ElectroAIHackathonIEEETemplate/conference_101719.tex`, so this draft is provided as a paper-ready standalone section for direct insertion into the manuscript's Methodology/Methods section.

## 3. Methodology

### 3.1 Multi-Agent Development Workflow

The experimental platform was developed through an iterative agent-assisted software engineering process in which multiple coding systems were used to generate, refine, and test distinct parts of the pipeline. Codex, Claude-based coding workflows, and Gemini were each used as development agents during implementation, with intermediate outputs retained as explicit artefacts rather than merged into an anonymous baseline. This development strategy was chosen to preserve architectural modularity and to maintain traceability between implementation changes and the agent systems that produced them. The same design principle was carried into the experimental pipeline itself: agent identity was preserved in file naming, directory layout, and task metadata so that downstream comparisons could distinguish outputs produced by Codex, Claude, and Gemini under a common workflow.

### 3.2 Web-Based Orchestration Layer

The execution environment was implemented as a local Python web application that serves as the orchestration layer for the schematic reconstruction benchmark. The application accepts an input directory of schematic images, enumerates supported raster image files, and constructs a task matrix containing one task for every image-agent pair. For each image, the backend schedules separate runs for Codex, Claude, and Gemini and writes outputs into agent-specific directories under a shared output root. This arrangement isolates artefacts by agent while preserving a common directory structure across the benchmark.

The orchestration backend maintains run state, task timing, and status transitions for the full matrix of jobs. Each task records start time, finish time, elapsed duration, produced files, missing files, standard output, standard error, and post-processing status. The web interface presents this state through overall and per-agent progress summaries, live task timers, and a task-card matrix that distinguishes pending, running, completed, completed-with-issues, failed, and canceled states. As a result, the interface acts not only as an operator dashboard but also as a structured observation layer for the experimental workflow.

### 3.3 Agent-Specific Execution Contract

Although the underlying implementations for Codex, Claude, and Gemini differ, they were normalized through a common runner abstraction. Each agent was invoked through a command of the form `<agent runner> <image path> --output-dir <output-root>/<agent>`, allowing heterogeneous model-specific scripts to be evaluated under the same operational contract. This abstraction reduced differences in invocation semantics while preserving agent-specific prompting, credentials, and output naming conventions within the runner scripts themselves.

For every schematic image, each runner attempted to produce the same required four-file output set: a Falstad plain-text circuit file, a Falstad XML file, an LTSpice `.asc` schematic file, and a Markdown report. Output filenames included an explicit `generated-by-<agent>` suffix so that artefacts could be traced to a specific execution path during later inspection. The uniform interface therefore supported controlled comparison without suppressing the identity of the underlying agent system.

### 3.4 Dual-Modality Design Generation

The benchmark was designed to evaluate whether a model could recover circuit structure from an image into more than one engineering representation. Each agent therefore attempted to reconstruct two complementary downstream design modalities. The first modality was a Falstad-compatible circuit representation, consisting of a plain-text CircuitJS/Falstad netlist and a parallel XML form. This modality supports rapid visual inspection and lightweight interactive simulation. The second modality was an LTSpice schematic representation stored as a `.asc` file. This modality targets a more conventional EDA workflow in which the recovered design can be inspected, rendered, and potentially extended within a standard circuit design environment.

The accompanying Markdown report served as a structured validation artefact rather than a mere log. It captured assumptions, missing information, inconsistencies, and validation findings identified by the runner. Taken together, the four required files provided a multi-view description of the reconstructed circuit: two simulator-oriented structural outputs, one LTSpice design artefact, and one textual account of uncertainty and potential failure modes.

### 3.5 Dynamic Falstad Rendering and Artefact Recovery

On the Falstad branch of the pipeline, the generated plain-text netlist was treated as an executable representation that could be rendered automatically within the CircuitJS environment. After task completion, the pipeline invoked a browser-automation post-processing step that loaded the generated netlist into Falstad/CircuitJS through an encoded circuit URL. A headless Chromium session driven by Playwright then queried the rendered page, verified that the circuit canvas was present, and captured preview images for dashboard display. This procedure converted model-generated circuit text into a visual inspection modality without requiring manual screenshotting.

The recovered preview image was stored as an additional task artefact and surfaced in the dashboard alongside the base outputs. Because preview capture depends on the validity of the generated Falstad text and on the external rendering environment, preview failure was treated as an explicit task issue rather than silently ignored. The Falstad preview therefore served both as a user-facing visualization and as an operational signal about whether the generated circuit text was sufficiently coherent to render.

### 3.6 LTSpice Retrieval and Secondary Visual Modality

The LTSpice branch of the pipeline was treated as a second design modality complementary to Falstad rather than as a passive file export. When an agent produced an LTSpice `.asc` file that matched the expected schematic format, the pipeline attempted a secondary rendering step using `ltspice2svg` to convert the schematic into a vector preview. Where enabled, a further Playwright-based rasterization stage converted the SVG into a PNG for dashboard display. These derivative artefacts made LTSpice outputs visually inspectable within the same evaluation interface used for Falstad previews.

This two-stage LTSpice recovery path was designed to remain non-fatal. Missing optional renderers, invalid placeholder `.asc` files, or failed preview generation did not redefine the formal success criteria of the benchmark. Instead, the pipeline recorded structured LTSpice preview states such as available, skipped, missing source, unavailable, disabled, or failed. In methodological terms, this allowed the study to distinguish between an agent's ability to produce a nominal LTSpice artefact and the system's ability to recover a usable visualization from that artefact.

### 3.7 Validation, Inconsistency Reporting, and Comparative Use

Validation was integrated directly into task finalization and was treated as part of the experimental method rather than as a convenience feature. After each run, the backend checked the presence of the required four-file contract, inspected the report for missing information, inconsistencies, validation failures, and placeholder language, and propagated these findings into task-level issue states. Outputs that were incomplete, malformed, or evidently fallback generations were therefore marked as `completed_with_issues` or `failed` instead of being counted as silent successes.

This validation layer is important for comparative analysis because raw file existence alone is not a sufficient indicator of reconstruction quality. By preserving per-agent outputs, surfacing explicit issue messages, and attaching both textual and visual artefacts to each task, the system supports reproducible comparison across agents at multiple levels: whether the expected files were produced, whether those files were structurally plausible, and whether the recovered Falstad and LTSpice representations could be rendered for inspection. The resulting methodology therefore supports experimental evaluation of circuit understanding as a multi-stage reconstruction problem rather than as a single-output generation task.
