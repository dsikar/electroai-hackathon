from __future__ import annotations

import base64
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_INPUT_DIR = REPO_ROOT / "images"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "simulations"
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
VENV_PYTHON = REPO_ROOT / "venv" / "bin" / "python3"
RUNNER_PYTHON = VENV_PYTHON if VENV_PYTHON.exists() else pathlib.Path(sys.executable)
VENV_LTSPICE2SVG = REPO_ROOT / "venv" / "bin" / "ltspice2svg"
LOCAL_LTSPICE2SVG = REPO_ROOT / "tools" / "ltspice2svg" / "ltspice2svg"
FALSTAD_PREVIEW_SCRIPT = REPO_ROOT / "scripts" / "falstad_screenshot_automation.py"


@dataclass(frozen=True)
class AgentSpec:
    key: str
    label: str
    script_path: pathlib.Path
    env_vars: tuple[str, ...]
    suffix_agent: str

    @property
    def suffix(self) -> str:
        return f"generated-by-{self.suffix_agent}"

    def build_command(self, image_path: pathlib.Path, output_root: pathlib.Path) -> list[str]:
        return [
            str(RUNNER_PYTHON),
            str(self.script_path),
            str(image_path),
            "--output-dir",
            str(output_root / self.key),
        ]

    def expected_files(self, stem: str, output_root: pathlib.Path) -> dict[str, pathlib.Path]:
        base_dir = output_root / self.key
        base_name = f"{stem}_{self.suffix}"
        return {
            "falstad_text": base_dir / f"{base_name}_falstad.txt",
            "falstad_xml": base_dir / f"{base_name}_falstad.xml",
            "ltspice_asc": base_dir / f"{base_name}.asc",
            "report": base_dir / f"{base_name}_report.md",
        }

    def falstad_preview_file(self, stem: str, output_root: pathlib.Path) -> pathlib.Path:
        base_dir = output_root / self.key
        base_name = f"{stem}_{self.suffix}"
        return base_dir / f"{base_name}_falstad.png"


AGENTS = [
    AgentSpec(
        key="codex",
        label="Codex",
        script_path=REPO_ROOT / "scripts" / "schematic_to_eda_codex.py",
        env_vars=("OPENAI_API_KEY",),
        suffix_agent="codex",
    ),
    AgentSpec(
        key="claude",
        label="Claude",
        script_path=REPO_ROOT / "scripts" / "schematic_to_eda_claude.py",
        env_vars=("ANTHROPIC_API_KEY",),
        suffix_agent="claude-sonnet-4-6",
    ),
    AgentSpec(
        key="gemini",
        label="Gemini",
        script_path=REPO_ROOT / "scripts" / "schematic_to_eda_gemini.py",
        env_vars=("GOOGLE_API_KEY", "GEMINI_API_KEY"),
        suffix_agent="gemini",
    ),
]


def is_within(path: pathlib.Path, parent: pathlib.Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def discover_images(input_dir: pathlib.Path) -> list[pathlib.Path]:
    if not input_dir.exists() or not input_dir.is_dir():
        return []
    return sorted(
        [
            path
            for path in input_dir.iterdir()
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        ],
        key=lambda path: path.name.lower(),
    )


def env_ready(agent: AgentSpec) -> tuple[bool, list[str]]:
    present = [name for name in agent.env_vars if os.getenv(name)]
    return bool(present), list(agent.env_vars)


def ltspice_svg_path(asc_path: pathlib.Path) -> pathlib.Path:
    return asc_path.with_name(f"{asc_path.stem}_ltspice.svg")


def ltspice_png_path(svg_path: pathlib.Path) -> pathlib.Path:
    return svg_path.with_suffix(".png")


def resolve_ltspice2svg_binary() -> pathlib.Path | None:
    configured = os.getenv("LTSPICE2SVG_BIN")
    candidates: list[pathlib.Path] = []
    if configured:
        candidates.append(pathlib.Path(configured).expanduser())
    candidates.extend([VENV_LTSPICE2SVG, LOCAL_LTSPICE2SVG])

    for candidate in candidates:
        if candidate.exists() and os.access(candidate, os.X_OK):
            return candidate.resolve()

    discovered = shutil.which("ltspice2svg")
    if not discovered:
        return None
    candidate = pathlib.Path(discovered)
    return candidate.resolve() if candidate.exists() and os.access(candidate, os.X_OK) else None


def ltspice_svg_tool_config() -> dict[str, Any]:
    binary = resolve_ltspice2svg_binary()
    return {
        "available": binary is not None,
        "path": str(binary) if binary else None,
        "env_var": "LTSPICE2SVG_BIN",
        "sym_path_env_var": "LTSPICE2SVG_SYM_PATH",
    }


def ltspice_png_tool_config() -> dict[str, Any]:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        return {
            "available": False,
            "renderer": "playwright",
            "python": str(RUNNER_PYTHON),
        }
    return {
        "available": True,
        "renderer": "playwright",
        "python": str(RUNNER_PYTHON),
    }


def extract_key_values(output: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in output.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.isupper():
            values[key] = value.strip()
    return values


def extract_markdown_section(text: str, heading: str) -> list[str]:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return []
    start = match.end()
    remainder = text[start:]
    next_heading = re.search(r"^## ", remainder, re.MULTILINE)
    section = remainder[: next_heading.start()] if next_heading else remainder
    return [line[2:].strip() for line in section.splitlines() if line.startswith("- ")]


def inspect_report(report_path: pathlib.Path) -> dict[str, Any]:
    if not report_path.exists():
        return {
            "exists": False,
            "has_issues": True,
            "issue_messages": ["Report file is missing."],
        }

    text = report_path.read_text(encoding="utf-8", errors="replace")
    validation = extract_markdown_section(text, "Validation")
    missing = extract_markdown_section(text, "Missing Information")
    inconsistencies = extract_markdown_section(text, "Inconsistencies")
    lowered = text.lower()

    issue_messages: list[str] = []
    if validation and not any(line.startswith("Passed") for line in validation):
        issue_messages.extend(f"Validation: {line}" for line in validation)
    if missing and not all(line in {"None.", "None detected."} for line in missing):
        issue_messages.extend(f"Missing information: {line}" for line in missing)
    if inconsistencies and not all(line in {"None.", "None detected."} for line in inconsistencies):
        issue_messages.extend(f"Inconsistency: {line}" for line in inconsistencies)
    if any(keyword in lowered for keyword in ("placeholder", "did not return", "incomplete")):
        issue_messages.append("Report indicates placeholder or fallback output.")

    return {
        "exists": True,
        "has_issues": bool(issue_messages),
        "issue_messages": issue_messages,
    }


@dataclass
class TaskRecord:
    task_id: str
    agent: str
    agent_label: str
    image_name: str
    image_path: str
    status: str = "pending"
    started_at: float | None = None
    finished_at: float | None = None
    duration_seconds: float | None = None
    stdout: str = ""
    stderr: str = ""
    return_code: int | None = None
    expected_files: dict[str, str] = field(default_factory=dict)
    produced_files: dict[str, str] = field(default_factory=dict)
    missing_files: list[str] = field(default_factory=list)
    issue_messages: list[str] = field(default_factory=list)
    falstad_url: str | None = None
    ltspice_svg_path: str | None = None
    ltspice_svg_status: str = "unavailable"
    ltspice_svg_message: str | None = None
    ltspice_png_path: str | None = None
    ltspice_png_status: str = "disabled"
    ltspice_png_message: str | None = None
    falstad_preview_path: str | None = None
    falstad_preview_status: str = "unavailable"
    falstad_preview_message: str | None = None
    preview_debug: list[str] = field(default_factory=list)
    command: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "agent": self.agent,
            "agent_label": self.agent_label,
            "image_name": self.image_name,
            "image_path": self.image_path,
            "status": self.status,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": self.duration_seconds,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "return_code": self.return_code,
            "expected_files": self.expected_files,
            "produced_files": self.produced_files,
            "missing_files": self.missing_files,
            "issue_messages": self.issue_messages,
            "falstad_url": self.falstad_url,
            "ltspice_svg_path": self.ltspice_svg_path,
            "ltspice_svg_status": self.ltspice_svg_status,
            "ltspice_svg_message": self.ltspice_svg_message,
            "ltspice_png_path": self.ltspice_png_path,
            "ltspice_png_status": self.ltspice_png_status,
            "ltspice_png_message": self.ltspice_png_message,
            "falstad_preview_path": self.falstad_preview_path,
            "falstad_preview_status": self.falstad_preview_status,
            "falstad_preview_message": self.falstad_preview_message,
            "preview_debug": self.preview_debug,
            "command": self.command,
        }


class PipelineManager:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._worker: threading.Thread | None = None
        self._cancel = threading.Event()
        self._current_process: subprocess.Popen[str] | None = None
        self._state: dict[str, Any] = self._empty_state()

    def _empty_state(self) -> dict[str, Any]:
        return {
            "run_id": None,
            "run_status": "idle",
            "input_dir": str(DEFAULT_INPUT_DIR),
            "output_root": str(DEFAULT_OUTPUT_ROOT),
            "ltspice_png_enabled": False,
            "default_input_dir": str(DEFAULT_INPUT_DIR),
            "default_output_root": str(DEFAULT_OUTPUT_ROOT),
            "images": [],
            "tasks": [],
            "started_at": None,
            "finished_at": None,
            "error": None,
            "debug_log": [],
        }

    def _snapshot(self) -> dict[str, Any]:
        state = json.loads(json.dumps(self._state))
        tasks = state.get("tasks", [])
        total = len(tasks)
        finished = sum(1 for task in tasks if task["status"] in {"completed", "completed_with_issues", "failed", "canceled"})
        running = sum(1 for task in tasks if task["status"] == "running")
        by_agent: dict[str, dict[str, Any]] = {}
        for agent in AGENTS:
            agent_tasks = [task for task in tasks if task["agent"] == agent.key]
            agent_finished = sum(
                1
                for task in agent_tasks
                if task["status"] in {"completed", "completed_with_issues", "failed", "canceled"}
            )
            by_agent[agent.key] = {
                "label": agent.label,
                "total": len(agent_tasks),
                "finished": agent_finished,
                "running": sum(1 for task in agent_tasks if task["status"] == "running"),
                "progress": 0 if not agent_tasks else round(agent_finished / len(agent_tasks) * 100, 2),
            }

        state["summary"] = {
            "total": total,
            "finished": finished,
            "running": running,
            "progress": 0 if not total else round(finished / total * 100, 2),
            "by_agent": by_agent,
        }
        state["agent_config"] = {
            agent.key: {
                "label": agent.label,
                "env_vars": list(agent.env_vars),
                "configured": env_ready(agent)[0],
            }
            for agent in AGENTS
        }
        state["tool_config"] = {
            "ltspice_svg": ltspice_svg_tool_config(),
            "ltspice_png": ltspice_png_tool_config(),
        }
        return state

    def get_state(self) -> dict[str, Any]:
        with self._lock:
            return self._snapshot()

    def start_run(self, input_dir: str, output_root: str, ltspice_png_enabled: bool = False) -> dict[str, Any]:
        with self._lock:
            if self._worker and self._worker.is_alive():
                raise RuntimeError("A pipeline run is already in progress.")

            input_path = pathlib.Path(input_dir).expanduser().resolve()
            output_path = pathlib.Path(output_root).expanduser().resolve()
            images = discover_images(input_path)
            if not images:
                raise RuntimeError("No valid schematic images were found in the selected input folder.")

            tasks: list[TaskRecord] = []
            for image in images:
                for agent in AGENTS:
                    expected = {
                        key: str(path)
                        for key, path in agent.expected_files(image.stem, output_path).items()
                    }
                    tasks.append(
                        TaskRecord(
                            task_id=f"{image.stem}:{agent.key}",
                            agent=agent.key,
                            agent_label=agent.label,
                            image_name=image.name,
                            image_path=str(image),
                            expected_files=expected,
                            ltspice_svg_path=str(ltspice_svg_path(pathlib.Path(expected["ltspice_asc"]))),
                            ltspice_png_path=str(
                                ltspice_png_path(ltspice_svg_path(pathlib.Path(expected["ltspice_asc"])))
                            ),
                        )
                    )

            self._cancel = threading.Event()
            self._state = {
                "run_id": uuid.uuid4().hex,
                "run_status": "running",
                "input_dir": str(input_path),
                "output_root": str(output_path),
                "ltspice_png_enabled": bool(ltspice_png_enabled),
                "default_input_dir": str(DEFAULT_INPUT_DIR),
                "default_output_root": str(DEFAULT_OUTPUT_ROOT),
                "images": [str(image) for image in images],
                "tasks": [task.to_dict() for task in tasks],
                "started_at": time.time(),
                "finished_at": None,
                "error": None,
                "debug_log": [],
            }
            self._worker = threading.Thread(
                target=self._run_pipeline,
                args=(self._state["run_id"],),
                daemon=True,
            )
            self._worker.start()
            return self._snapshot()

    def cancel_run(self) -> dict[str, Any]:
        with self._lock:
            if self._state["run_status"] not in {"running", "canceling"}:
                return self._snapshot()
            self._state["run_status"] = "canceling"
            self._cancel.set()
            process = self._current_process
        if process and process.poll() is None:
            process.terminate()
        return self.get_state()

    def refresh(self, input_dir: str, output_root: str, ltspice_png_enabled: bool = False) -> dict[str, Any]:
        input_path = pathlib.Path(input_dir).expanduser().resolve()
        output_path = pathlib.Path(output_root).expanduser().resolve()
        images = discover_images(input_path)
        tasks: list[dict[str, Any]] = []
        for image in images:
            for agent in AGENTS:
                task = TaskRecord(
                    task_id=f"{image.stem}:{agent.key}",
                    agent=agent.key,
                    agent_label=agent.label,
                    image_name=image.name,
                    image_path=str(image),
                    expected_files={
                        key: str(path)
                        for key, path in agent.expected_files(image.stem, output_path).items()
                    },
                    ltspice_svg_path=str(
                        ltspice_svg_path(agent.expected_files(image.stem, output_path)["ltspice_asc"])
                    ),
                    ltspice_png_path=str(
                        ltspice_png_path(
                            ltspice_svg_path(agent.expected_files(image.stem, output_path)["ltspice_asc"])
                        )
                    ),
                )
                self._finalize_task(
                    task,
                    agent,
                    image,
                    output_path,
                    return_code=0,
                    stdout="",
                    stderr="",
                    generate_preview=False,
                    generate_ltspice_png=bool(ltspice_png_enabled),
                )
                tasks.append(task.to_dict())

        with self._lock:
            if self._worker and self._worker.is_alive():
                raise RuntimeError("Cannot refresh while a pipeline run is in progress.")
            self._state = {
                "run_id": None,
                "run_status": "idle",
                "input_dir": str(input_path),
                "output_root": str(output_path),
                "ltspice_png_enabled": bool(ltspice_png_enabled),
                "default_input_dir": str(DEFAULT_INPUT_DIR),
                "default_output_root": str(DEFAULT_OUTPUT_ROOT),
                "images": [str(image) for image in images],
                "tasks": tasks,
                "started_at": None,
                "finished_at": None,
                "error": None,
                "debug_log": [],
            }
            return self._snapshot()

    def _append_debug(self, message: str) -> None:
        with self._lock:
            self._state.setdefault("debug_log", []).append(
                {
                    "timestamp": time.time(),
                    "message": message,
                }
            )
            self._state["debug_log"] = self._state["debug_log"][-200:]

    def _update_task(self, task_id: str, **updates: Any) -> None:
        with self._lock:
            for task in self._state["tasks"]:
                if task["task_id"] == task_id:
                    task.update(updates)
                    return

    def _run_pipeline(self, run_id: str) -> None:
        try:
            state = self.get_state()
            output_root = pathlib.Path(state["output_root"])
            for task in state["tasks"]:
                if self._cancel.is_set():
                    self._append_debug(f"Canceled before starting {task['task_id']}.")
                    self._update_task(task["task_id"], status="canceled")
                    continue

                agent = next(spec for spec in AGENTS if spec.key == task["agent"])
                image_path = pathlib.Path(task["image_path"])
                configured, env_vars = env_ready(agent)
                if not configured:
                    self._append_debug(
                        f"Skipping task {task['task_id']} because required environment is missing: {', '.join(env_vars)}"
                    )
                    self._update_task(
                        task["task_id"],
                        status="failed",
                        started_at=time.time(),
                        finished_at=time.time(),
                        duration_seconds=0,
                        return_code=1,
                        stderr=f"Missing required environment variables: {', '.join(env_vars)}",
                        issue_messages=[f"Missing required environment variables: {', '.join(env_vars)}"],
                    )
                    continue
                started = time.time()
                command = agent.build_command(image_path, output_root)
                self._append_debug(
                    f"Starting task {task['task_id']} with command: {' '.join(command)}"
                )
                self._update_task(
                    task["task_id"],
                    status="running",
                    started_at=started,
                    command=command,
                )

                process = subprocess.Popen(
                    command,
                    cwd=REPO_ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                with self._lock:
                    self._current_process = process

                while process.poll() is None:
                    if self._cancel.is_set():
                        self._append_debug(f"Terminate requested for {task['task_id']}.")
                        process.terminate()
                        break
                    time.sleep(0.2)

                stdout, stderr = process.communicate()
                finished = time.time()
                self._append_debug(
                    f"Finished task {task['task_id']} with return code {process.returncode}."
                )
                task_record = TaskRecord(
                    task_id=task["task_id"],
                    agent=task["agent"],
                    agent_label=task["agent_label"],
                    image_name=task["image_name"],
                    image_path=task["image_path"],
                    status="failed",
                    started_at=started,
                    finished_at=finished,
                    duration_seconds=round(finished - started, 2),
                    stdout=stdout,
                    stderr=stderr,
                    return_code=process.returncode,
                    expected_files=task["expected_files"],
                    command=command,
                )
                self._finalize_task(
                    task_record,
                    agent,
                    image_path,
                    output_root,
                    process.returncode,
                    stdout,
                    stderr,
                    generate_preview=True,
                    generate_ltspice_png=bool(state.get("ltspice_png_enabled")),
                )
                task_payload = task_record.to_dict()
                task_payload.pop("task_id", None)
                self._update_task(task["task_id"], **task_payload)
                with self._lock:
                    self._current_process = None

            with self._lock:
                self._state["finished_at"] = time.time()
                if self._cancel.is_set():
                    self._state["run_status"] = "canceled"
                else:
                    self._state["run_status"] = "completed"
        except Exception as exc:
            self._append_debug(f"Worker crashed: {exc!r}")
            with self._lock:
                self._state["run_status"] = "failed"
                self._state["finished_at"] = time.time()
                self._state["error"] = repr(exc)
                self._current_process = None

    def _finalize_task(
        self,
        task: TaskRecord,
        agent: AgentSpec,
        image_path: pathlib.Path,
        output_root: pathlib.Path,
        return_code: int,
        stdout: str,
        stderr: str,
        generate_preview: bool,
        generate_ltspice_png: bool,
    ) -> None:
        expected = agent.expected_files(image_path.stem, output_root)
        falstad_text_path = expected["falstad_text"]
        ltspice_asc_path = expected["ltspice_asc"]
        ltspice_svg_output_path = ltspice_svg_path(ltspice_asc_path)
        ltspice_png_output_path = ltspice_png_path(ltspice_svg_output_path)
        falstad_preview_path = agent.falstad_preview_file(image_path.stem, output_root)
        task.expected_files = {key: str(path) for key, path in expected.items()}
        task.produced_files = {
            key: str(path) for key, path in expected.items() if path.exists()
        }
        task.missing_files = [name for name, path in expected.items() if not path.exists()]
        task.stdout = stdout
        task.stderr = stderr
        task.return_code = return_code
        task.ltspice_svg_path = str(ltspice_svg_output_path)
        task.ltspice_png_path = str(ltspice_png_output_path)

        metadata = extract_key_values(stdout)
        if "FALSTAD_URL" in metadata:
            task.falstad_url = metadata["FALSTAD_URL"]

        if not task.produced_files and return_code == 0 and not stdout and not stderr:
            task.status = "pending"
            task.issue_messages = []
            task.missing_files = []
            return

        report_info = inspect_report(expected["report"])
        task.issue_messages = list(report_info["issue_messages"])
        if task.missing_files:
            task.issue_messages.extend(
                f"Missing required output: {name}" for name in task.missing_files
            )

        ltspice_svg_message = self._generate_ltspice_svg(task, ltspice_asc_path, ltspice_svg_output_path)
        if task.ltspice_svg_status == "failed" and ltspice_svg_message:
            task.issue_messages.append(ltspice_svg_message)
        ltspice_png_message = self._generate_ltspice_png(
            task,
            ltspice_svg_output_path,
            ltspice_png_output_path,
            enabled=generate_ltspice_png,
        )
        if task.ltspice_png_status == "failed" and ltspice_png_message:
            task.issue_messages.append(ltspice_png_message)

        preview_message: str | None = None
        task.preview_debug = []
        if falstad_text_path.exists() and generate_preview and not falstad_preview_path.exists():
            preview_message = self._generate_falstad_preview(task, agent, image_path, output_root)

        if falstad_preview_path.exists():
            task.falstad_preview_path = str(falstad_preview_path)
            task.falstad_preview_status = "available"
            task.falstad_preview_message = None
        elif falstad_text_path.exists():
            task.falstad_preview_path = None
            task.falstad_preview_status = "unavailable"
            task.falstad_preview_message = preview_message or "Falstad preview unavailable."
            task.issue_messages.append(task.falstad_preview_message)
        else:
            task.falstad_preview_path = None
            task.falstad_preview_status = "missing_source"
            task.falstad_preview_message = "Falstad preview unavailable because the Falstad text output is missing."

        if return_code != 0:
            task.status = "failed"
        elif task.missing_files or task.issue_messages:
            task.status = "completed_with_issues"
        elif task.falstad_preview_status != "available" and falstad_text_path.exists():
            task.status = "completed_with_issues"
        else:
            task.status = "completed"

    def _generate_ltspice_svg(
        self,
        task: TaskRecord,
        asc_path: pathlib.Path,
        svg_path: pathlib.Path,
    ) -> str | None:
        task.ltspice_svg_path = str(svg_path)
        if not asc_path.exists():
            task.ltspice_svg_status = "missing_source"
            task.ltspice_svg_message = "LTSpice SVG unavailable because the .asc output is missing."
            return None

        text = asc_path.read_text(encoding="utf-8", errors="replace")
        if not text.lstrip().startswith("Version 4"):
            task.ltspice_svg_status = "skipped"
            task.ltspice_svg_message = "LTSpice SVG skipped because the .asc output is not a schematic file."
            return None

        binary = resolve_ltspice2svg_binary()
        if binary is None:
            task.ltspice_svg_status = "unavailable"
            task.ltspice_svg_message = "LTSpice SVG unavailable because ltspice2svg is not installed."
            return None

        if svg_path.exists() and svg_path.stat().st_mtime >= asc_path.stat().st_mtime:
            task.ltspice_svg_status = "available"
            task.ltspice_svg_message = None
            return None

        command = [str(binary), "-export", str(svg_path)]
        sym_path = os.getenv("LTSPICE2SVG_SYM_PATH")
        if sym_path:
            command.extend(["-symPath", sym_path])
        command.append(str(asc_path))
        self._append_debug(f"Starting LTSpice SVG conversion for {task.task_id}.")

        try:
            result = subprocess.run(
                command,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=90,
            )
        except Exception as exc:
            task.ltspice_svg_status = "failed"
            task.ltspice_svg_message = f"LTSpice SVG generation failed: {exc!r}"
            self._append_debug(f"LTSpice SVG conversion failed for {task.task_id}: {exc!r}")
            return task.ltspice_svg_message

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        if result.returncode != 0 or not svg_path.exists():
            detail = stderr or stdout or f"exit code {result.returncode}"
            task.ltspice_svg_status = "failed"
            task.ltspice_svg_message = f"LTSpice SVG generation failed: {detail}"
            self._append_debug(
                f"LTSpice SVG conversion failed for {task.task_id} with return code {result.returncode}."
            )
            return task.ltspice_svg_message

        task.ltspice_svg_status = "available"
        task.ltspice_svg_message = None
        self._append_debug(f"LTSpice SVG conversion succeeded for {task.task_id}.")
        return None

    def _generate_ltspice_png(
        self,
        task: TaskRecord,
        svg_path: pathlib.Path,
        png_path: pathlib.Path,
        *,
        enabled: bool,
    ) -> str | None:
        task.ltspice_png_path = str(png_path)
        if not enabled:
            task.ltspice_png_status = "disabled"
            task.ltspice_png_message = "LTSpice PNG conversion is disabled."
            return None

        if not svg_path.exists():
            task.ltspice_png_status = "missing_source"
            task.ltspice_png_message = "LTSpice PNG unavailable because the LTSpice SVG output is missing."
            return None

        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            task.ltspice_png_status = "unavailable"
            task.ltspice_png_message = "LTSpice PNG unavailable because Playwright is not installed."
            return None

        if png_path.exists() and png_path.stat().st_mtime >= svg_path.stat().st_mtime:
            task.ltspice_png_status = "available"
            task.ltspice_png_message = None
            return None

        svg_bytes = svg_path.read_bytes()
        svg_data_url = "data:image/svg+xml;base64," + base64.b64encode(svg_bytes).decode("ascii")
        html = (
            "<!doctype html><html><body style=\"margin:0;background:white\">"
            f"<img id=\"circuit\" src=\"{svg_data_url}\" "
            "style=\"display:block;max-width:none;background:white\">"
            "</body></html>"
        )
        self._append_debug(f"Starting LTSpice PNG conversion for {task.task_id}.")

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                page = browser.new_page(viewport={"width": 1600, "height": 1200}, device_scale_factor=2)
                page.set_content(html, wait_until="load")
                image = page.locator("#circuit")
                image.wait_for(state="visible", timeout=5000)
                image.screenshot(path=str(png_path))
                browser.close()
        except Exception as exc:
            task.ltspice_png_status = "failed"
            task.ltspice_png_message = f"LTSpice PNG generation failed: {exc!r}"
            self._append_debug(f"LTSpice PNG conversion failed for {task.task_id}: {exc!r}")
            return task.ltspice_png_message

        if not png_path.exists():
            task.ltspice_png_status = "failed"
            task.ltspice_png_message = "LTSpice PNG generation failed: output file was not created."
            self._append_debug(f"LTSpice PNG conversion failed for {task.task_id}: output file missing.")
            return task.ltspice_png_message

        task.ltspice_png_status = "available"
        task.ltspice_png_message = None
        self._append_debug(f"LTSpice PNG conversion succeeded for {task.task_id}.")
        return None

    def _generate_falstad_preview(
        self,
        task: TaskRecord,
        agent: AgentSpec,
        image_path: pathlib.Path,
        output_root: pathlib.Path,
    ) -> str | None:
        command = [
            str(RUNNER_PYTHON),
            str(FALSTAD_PREVIEW_SCRIPT),
            agent.key,
            image_path.stem,
            "--simulations-root",
            str(output_root),
        ]
        self._append_debug(f"Starting Falstad preview capture for {task.task_id}.")
        task.preview_debug.append(f"$ {' '.join(command)}")

        if not FALSTAD_PREVIEW_SCRIPT.exists():
            message = "Falstad preview helper script is missing."
            self._append_debug(f"Falstad preview failed for {task.task_id}: {message}")
            task.preview_debug.append(message)
            return message

        try:
            result = subprocess.run(
                command,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=90,
            )
        except Exception as exc:
            message = f"Falstad preview generation failed: {exc!r}"
            self._append_debug(f"Falstad preview failed for {task.task_id}: {exc!r}")
            task.preview_debug.append(message)
            return message

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        if stdout:
            task.preview_debug.extend(f"stdout: {line}" for line in stdout.splitlines())
        if stderr:
            task.preview_debug.extend(f"stderr: {line}" for line in stderr.splitlines())

        if result.returncode != 0:
            message = (
                "Falstad preview generation failed."
                + (f" {stderr}" if stderr else "")
            ).strip()
            self._append_debug(
                f"Falstad preview failed for {task.task_id} with return code {result.returncode}."
            )
            return message

        self._append_debug(f"Falstad preview capture succeeded for {task.task_id}.")
        task.preview_debug.append("Falstad preview capture succeeded.")
        return None


def make_manager() -> PipelineManager:
    return PipelineManager()
