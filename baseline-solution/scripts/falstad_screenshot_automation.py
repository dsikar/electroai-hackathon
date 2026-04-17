#!/usr/bin/env python3
"""Generate Falstad screenshots from pipeline netlists.

This is a post-processing utility for artifacts under:

    simulations/<agent>/<stem>_generated-by-<agent>_falstad.txt

It produces:

    <stem>_generated-by-<agent>_falstad.png
    <stem>_generated-by-<agent>_falstad_full.png

Playwright and a local Chromium install are required for actual screenshots:

    pip install playwright
    playwright install chromium
"""

from __future__ import annotations

import argparse
import asyncio
import pathlib
import sys
import urllib.parse
from dataclasses import dataclass


DEFAULT_BASE_URL = "https://www.falstad.com/circuit/circuitjs.html"
DEFAULT_SIMULATIONS_ROOT = pathlib.Path(__file__).resolve().parent.parent / "simulations"
KNOWN_AGENT_OUTPUT_IDS = {
    "codex": "codex",
    "claude": "claude-sonnet-4-6",
    "gemini": "gemini",
}


@dataclass(frozen=True)
class ScreenshotTask:
    agent: str
    stem: str
    netlist_path: pathlib.Path
    canvas_png_path: pathlib.Path
    viewport_png_path: pathlib.Path
    circuit_url: str
    warnings: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture Falstad screenshots for an existing pipeline output."
    )
    parser.add_argument(
        "agent",
        help="Agent output directory name, e.g. codex, claude, or gemini.",
    )
    parser.add_argument(
        "stem",
        help="Input stem used by the agent output, e.g. 01_circuit.",
    )
    parser.add_argument(
        "--simulations-root",
        default=str(DEFAULT_SIMULATIONS_ROOT),
        help=f"Root simulations directory (default: {DEFAULT_SIMULATIONS_ROOT}).",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Falstad/CircuitJS URL (default: {DEFAULT_BASE_URL}).",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=15000,
        help="Navigation timeout in milliseconds.",
    )
    parser.add_argument(
        "--render-wait-ms",
        type=int,
        default=2500,
        help="Extra wait after page load to let CircuitJS render.",
    )
    parser.add_argument(
        "--viewport-width",
        type=int,
        default=1400,
        help="Browser viewport width in CSS pixels.",
    )
    parser.add_argument(
        "--viewport-height",
        type=int,
        default=900,
        help="Browser viewport height in CSS pixels.",
    )
    parser.add_argument(
        "--scale-factor",
        type=float,
        default=2.0,
        help="Device scale factor for high-DPI screenshots.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve inputs and print the planned outputs without launching Playwright.",
    )
    return parser.parse_args()


def build_circuit_url(base_url: str, netlist_text: str) -> str:
    encoded_netlist = urllib.parse.quote(netlist_text, safe="")
    return f"{base_url}?hideSidebar=true&cct={encoded_netlist}"


def resolve_netlist_path(agent_dir: pathlib.Path, stem: str, agent: str) -> pathlib.Path:
    expected_output_id = KNOWN_AGENT_OUTPUT_IDS.get(agent, agent)
    expected_path = agent_dir / f"{stem}_generated-by-{expected_output_id}_falstad.txt"
    if expected_path.exists():
        return expected_path

    matches = sorted(agent_dir.glob(f"{stem}_generated-by-*_falstad.txt"))
    if not matches:
        raise SystemExit(
            f"Error: no Falstad netlist found for stem '{stem}' in {agent_dir}."
        )
    if len(matches) > 1:
        joined = ", ".join(str(match.name) for match in matches)
        raise SystemExit(
            f"Error: multiple Falstad netlists match stem '{stem}' in {agent_dir}: {joined}"
        )
    return matches[0]


def resolve_task(agent: str, stem: str, simulations_root: pathlib.Path, base_url: str) -> ScreenshotTask:
    agent_dir = simulations_root / agent
    if not agent_dir.exists():
        raise SystemExit(f"Error: agent directory not found: {agent_dir}")

    netlist_path = resolve_netlist_path(agent_dir, stem, agent)
    netlist_text = netlist_path.read_text(encoding="utf-8")
    warnings: list[str] = []
    if not netlist_text.strip():
        raise SystemExit(f"Error: Falstad netlist is empty: {netlist_path}")
    if not netlist_text.lstrip().startswith("$"):
        warnings.append("Falstad netlist does not start with '$'.")

    base_output_path = netlist_path.with_suffix("")
    canvas_png_path = base_output_path.with_suffix(".png")
    viewport_png_path = base_output_path.parent / f"{base_output_path.name}_full.png"
    circuit_url = build_circuit_url(base_url, netlist_text)

    return ScreenshotTask(
        agent=agent,
        stem=stem,
        netlist_path=netlist_path,
        canvas_png_path=canvas_png_path,
        viewport_png_path=viewport_png_path,
        circuit_url=circuit_url,
        warnings=warnings,
    )


async def inspect_canvas(page) -> dict:
    return await page.evaluate(
        """() => {
            const canvas = document.querySelector("canvas");
            if (!canvas) {
                return {state: "missing"};
            }
            const width = canvas.width || 0;
            const height = canvas.height || 0;
            if (!width || !height) {
                return {state: "zero-size", width, height};
            }

            const ctx = canvas.getContext("2d", {willReadFrequently: true});
            if (!ctx) {
                return {state: "no-context", width, height};
            }

            const stepX = Math.max(1, Math.floor(width / 24));
            const stepY = Math.max(1, Math.floor(height / 24));
            const colors = new Set();
            let opaquePixels = 0;

            for (let y = 0; y < height; y += stepY) {
                for (let x = 0; x < width; x += stepX) {
                    const pixel = ctx.getImageData(x, y, 1, 1).data;
                    const key = `${pixel[0]},${pixel[1]},${pixel[2]},${pixel[3]}`;
                    colors.add(key);
                    if (pixel[3] > 0) {
                        opaquePixels += 1;
                    }
                    if (colors.size > 6) {
                        return {
                            state: "ok",
                            width,
                            height,
                            colors: colors.size,
                            opaquePixels,
                        };
                    }
                }
            }

            return {
                state: colors.size <= 1 ? "flat" : "low-variance",
                width,
                height,
                colors: colors.size,
                opaquePixels,
            };
        }"""
    )


async def capture_screenshots(task: ScreenshotTask, args: argparse.Namespace) -> tuple[list[str], dict]:
    try:
        from playwright.async_api import TimeoutError as PlaywrightTimeoutError
        from playwright.async_api import async_playwright
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Error: Playwright is not installed. Install it with "
            "'pip install playwright' and then run 'playwright install chromium'."
        ) from exc

    warnings = list(task.warnings)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page(
            viewport={
                "width": args.viewport_width,
                "height": args.viewport_height,
            },
            device_scale_factor=args.scale_factor,
        )

        try:
            await page.goto(
                task.circuit_url,
                wait_until="domcontentloaded",
                timeout=args.timeout_ms,
            )
            try:
                await page.wait_for_load_state("networkidle", timeout=args.timeout_ms)
            except PlaywrightTimeoutError:
                warnings.append(
                    "Timed out waiting for network idle; continued after DOM load."
                )
            await page.wait_for_timeout(args.render_wait_ms)

            canvas = page.locator("canvas").first
            if await canvas.count() == 0:
                raise SystemExit("Error: Falstad page did not render a canvas element.")

            canvas_state = await inspect_canvas(page)
            if canvas_state.get("state") != "ok":
                warnings.append(f"Canvas check warning: {canvas_state}")

            task.canvas_png_path.parent.mkdir(parents=True, exist_ok=True)
            await canvas.screenshot(path=str(task.canvas_png_path), scale="css")
            await page.screenshot(path=str(task.viewport_png_path), scale="css")
        finally:
            await browser.close()

    return warnings, canvas_state


def print_summary(
    task: ScreenshotTask,
    warnings: list[str],
    canvas_state: dict | None,
    *,
    dry_run: bool,
) -> None:
    print(f"AGENT={task.agent}")
    print(f"STEM={task.stem}")
    print(f"NETLIST_FILE={task.netlist_path}")
    print(f"CIRCUIT_URL={task.circuit_url}")
    print(f"CANVAS_PNG={task.canvas_png_path}")
    print(f"VIEWPORT_PNG={task.viewport_png_path}")
    print(f"DRY_RUN={'true' if dry_run else 'false'}")
    if canvas_state is not None:
        print(f"CANVAS_STATE={canvas_state}")
    if warnings:
        print("STATUS=completed-with-warnings")
        for warning in warnings:
            print(f"WARNING={warning}")
    else:
        print("STATUS=completed")


async def async_main(args: argparse.Namespace) -> int:
    simulations_root = pathlib.Path(args.simulations_root).expanduser().resolve()
    task = resolve_task(args.agent, args.stem, simulations_root, args.base_url)

    if args.dry_run:
        print_summary(task, task.warnings, canvas_state=None, dry_run=True)
        return 0

    warnings, canvas_state = await capture_screenshots(task, args)
    print_summary(task, warnings, canvas_state, dry_run=False)
    return 0


def main() -> int:
    args = parse_args()
    return asyncio.run(async_main(args))


if __name__ == "__main__":
    sys.exit(main())
