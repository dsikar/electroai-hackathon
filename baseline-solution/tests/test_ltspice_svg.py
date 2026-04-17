from __future__ import annotations

import pathlib
import shutil
import tempfile
import unittest

from webapp.agent_pipeline import PipelineManager, TaskRecord, ltspice_png_path, ltspice_svg_path


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


FIXTURES = {
    "01_circuit:claude": {
        "source": REPO_ROOT / "simulations" / "claude" / "01_circuit_generated-by-claude-sonnet-4-6.asc",
        "expected_status": "available",
    },
    "02_cicuit:claude": {
        "source": REPO_ROOT / "simulations" / "claude" / "02_cicuit_generated-by-claude-sonnet-4-6.asc",
        "expected_status": "available",
    },
    "01_circuit:codex": {
        "source": REPO_ROOT / "simulations" / "codex" / "01_circuit_generated-by-codex.asc",
        "expected_status": "skipped",
    },
    "02_cicuit:codex": {
        "source": REPO_ROOT / "simulations" / "codex" / "02_cicuit_generated-by-codex.asc",
        "expected_status": "available",
    },
    "01_circuit:gemini": {
        "source": REPO_ROOT / "simulations" / "gemini" / "01_circuit_generated-by-gemini.asc",
        "expected_status": "available",
    },
    "02_cicuit:gemini": {
        "source": REPO_ROOT / "simulations" / "gemini" / "02_cicuit_generated-by-gemini.asc",
        "expected_status": "available",
    },
}


class LtspiceSvgTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.workspace = pathlib.Path(self.tempdir.name)
        self.manager = PipelineManager()
        self.input_dir = self.workspace / "images"
        self.output_root = self.workspace / "simulations"
        self.input_dir.mkdir()
        self.output_root.mkdir()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _make_task(self, task_id: str) -> TaskRecord:
        stem, agent = task_id.split(":", 1)
        return TaskRecord(
            task_id=task_id,
            agent=agent,
            agent_label=agent.title(),
            image_name=f"{stem}.png",
            image_path=str(self.workspace / f"{stem}.png"),
        )

    def _stage_fixture_workspace(self) -> None:
        stems = {task_id.split(":", 1)[0] for task_id in FIXTURES}
        for stem in stems:
            (self.input_dir / f"{stem}.png").write_bytes(b"fixture")

        for task_id, fixture in FIXTURES.items():
            _stem, agent = task_id.split(":", 1)
            agent_dir = self.output_root / agent
            agent_dir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(fixture["source"], agent_dir / fixture["source"].name)

    def test_generate_ltspice_svg_for_fixture_asc_files(self) -> None:
        for task_id, fixture in FIXTURES.items():
            with self.subTest(task_id=task_id):
                asc_copy = self.workspace / fixture["source"].name
                shutil.copyfile(fixture["source"], asc_copy)
                svg_output = ltspice_svg_path(asc_copy)
                task = self._make_task(task_id)

                message = self.manager._generate_ltspice_svg(task, asc_copy, svg_output)

                self.assertEqual(task.ltspice_svg_status, fixture["expected_status"])
                self.assertEqual(task.ltspice_svg_path, str(svg_output))
                if fixture["expected_status"] == "available":
                    self.assertIsNone(message)
                    self.assertIsNone(task.ltspice_svg_message)
                    self.assertTrue(svg_output.exists())
                    self.assertGreater(svg_output.stat().st_size, 0)
                else:
                    self.assertIsNone(message)
                    self.assertEqual(
                        task.ltspice_svg_message,
                        "LTSpice SVG skipped because the .asc output is not a schematic file.",
                    )
                    self.assertFalse(svg_output.exists())

    def test_generate_ltspice_png_for_fixture_svg_files(self) -> None:
        for task_id, fixture in FIXTURES.items():
            with self.subTest(task_id=task_id):
                asc_copy = self.workspace / fixture["source"].name
                shutil.copyfile(fixture["source"], asc_copy)
                svg_output = ltspice_svg_path(asc_copy)
                png_output = ltspice_png_path(svg_output)
                task = self._make_task(task_id)

                self.manager._generate_ltspice_svg(task, asc_copy, svg_output)
                message = self.manager._generate_ltspice_png(task, svg_output, png_output, enabled=True)

                self.assertEqual(task.ltspice_png_path, str(png_output))
                if fixture["expected_status"] == "available":
                    self.assertIsNone(message)
                    self.assertEqual(task.ltspice_png_status, "available")
                    self.assertIsNone(task.ltspice_png_message)
                    self.assertTrue(png_output.exists())
                    self.assertGreater(png_output.stat().st_size, 0)
                else:
                    self.assertIsNone(message)
                    self.assertEqual(task.ltspice_png_status, "missing_source")
                    self.assertEqual(
                        task.ltspice_png_message,
                        "LTSpice PNG unavailable because the LTSpice SVG output is missing.",
                    )
                    self.assertFalse(png_output.exists())

    def test_refresh_reports_expected_ltspice_svg_statuses_for_fixture_tasks(self) -> None:
        state = self.manager.refresh(str(REPO_ROOT / "images"), str(REPO_ROOT / "simulations"))

        for task_id, fixture in FIXTURES.items():
            with self.subTest(task_id=task_id):
                task = next(item for item in state["tasks"] if item["task_id"] == task_id)
                self.assertEqual(task["ltspice_svg_status"], fixture["expected_status"])
                self.assertEqual(
                    task["ltspice_svg_path"],
                    str(ltspice_svg_path(pathlib.Path(task["expected_files"]["ltspice_asc"]))),
                )
                if fixture["expected_status"] == "available":
                    self.assertIsNone(task["ltspice_svg_message"])
                    self.assertTrue(pathlib.Path(task["ltspice_svg_path"]).exists())
                else:
                    self.assertEqual(
                        task["ltspice_svg_message"],
                        "LTSpice SVG skipped because the .asc output is not a schematic file.",
                    )

    def test_refresh_leaves_ltspice_png_disabled_when_switch_is_off(self) -> None:
        self._stage_fixture_workspace()
        state = self.manager.refresh(str(self.input_dir), str(self.output_root), ltspice_png_enabled=False)

        for task_id in FIXTURES:
            with self.subTest(task_id=task_id):
                task = next(item for item in state["tasks"] if item["task_id"] == task_id)
                self.assertEqual(task["ltspice_png_status"], "disabled")
                self.assertEqual(task["ltspice_png_message"], "LTSpice PNG conversion is disabled.")
                self.assertFalse(pathlib.Path(task["ltspice_png_path"]).exists())

    def test_refresh_generates_ltspice_png_when_switch_is_on(self) -> None:
        self._stage_fixture_workspace()
        state = self.manager.refresh(str(self.input_dir), str(self.output_root), ltspice_png_enabled=True)

        for task_id, fixture in FIXTURES.items():
            with self.subTest(task_id=task_id):
                task = next(item for item in state["tasks"] if item["task_id"] == task_id)
                if fixture["expected_status"] == "available":
                    self.assertEqual(task["ltspice_png_status"], "available")
                    self.assertIsNone(task["ltspice_png_message"])
                    self.assertTrue(pathlib.Path(task["ltspice_png_path"]).exists())
                else:
                    self.assertEqual(task["ltspice_png_status"], "missing_source")
                    self.assertEqual(
                        task["ltspice_png_message"],
                        "LTSpice PNG unavailable because the LTSpice SVG output is missing.",
                    )
                    self.assertFalse(pathlib.Path(task["ltspice_png_path"]).exists())


if __name__ == "__main__":
    unittest.main()
