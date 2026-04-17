#!/usr/bin/env python3
"""Generate Falstad and LTSpice outputs from a schematic image via Gemini."""

from __future__ import annotations

import argparse
import base64
import os
import pathlib
import sys

from google import genai
from google.genai import types


AGENT_NAME = "gemini"
OUTPUT_SUFFIX = f"generated-by-{AGENT_NAME}"
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
DEFAULT_OUTPUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "simulations" / AGENT_NAME
SUPPORTED_IMAGE_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Falstad and LTSpice outputs from a schematic image via Gemini."
    )
    parser.add_argument("image_path", help="Path to a PNG / JPG / WEBP / GIF schematic image.")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gemini model to use (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--output-dir",
        help=f"Directory for output files. Defaults to {DEFAULT_OUTPUT_DIR}.",
    )
    return parser.parse_args()


def get_api_key() -> str:
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Error: GOOGLE_API_KEY or GEMINI_API_KEY environment variable not set.")
    return api_key


def normalize_image_path(image_path: str) -> pathlib.Path:
    path = pathlib.Path(image_path).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Error: image not found at {path}")
    if path.suffix.lower() not in SUPPORTED_IMAGE_TYPES:
        raise SystemExit(
            f"Error: unsupported image type '{path.suffix}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_IMAGE_TYPES))}"
        )
    return path


def call_gemini(model: str, image_path: pathlib.Path, api_key: str) -> str:
    client = genai.Client(api_key=api_key)
    prompt = """
    # Role
    Expert Electronic Design Automation (EDA) Analyst.

    # Task
    Reverse-engineer the provided schematic image into THREE precise output formats and a report:
    1. Falstad Plain-Text (.txt): a valid Falstad block starting with '$'
    2. Falstad XML (.xml): a valid XML block starting with <cir> and ending with </cir>
    3. LTSpice Schematic (.asc): a valid LTSpice schematic block starting with Version 4

    # Requirements
    - Identify all components and visible labels.
    - Record assumptions, missing information, and inconsistencies in the report.
    - Return the output using the exact section headers below.

    [SCHEMATIC ANALYSIS REPORT]
    - Summary: ...
    - Assumptions: ...
    - Missing Information: ...
    - Inconsistencies: ...

    [FALSTAD TEXT]
    (Falstad plain-text block starting with $)

    [FALSTAD XML]
    (Falstad XML block starting with <cir> and ending with </cir>)

    [LTSPICE ASC]
    (LTSpice ASC block starting with Version 4)
    """

    with image_path.open("rb") as handle:
        image_bytes = handle.read()

    response = client.models.generate_content(
        model=model,
        contents=[
            prompt,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=SUPPORTED_IMAGE_TYPES[image_path.suffix.lower()],
            ),
        ],
    )
    return response.text


def extract_section(text: str, header: str, next_headers: list[str]) -> str:
    start = text.find(header)
    if start == -1:
        return ""
    start += len(header)
    end_candidates = [text.find(other, start) for other in next_headers]
    ends = [idx for idx in end_candidates if idx != -1]
    end = min(ends) if ends else len(text)
    return text[start:end].strip()


def write_text(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    image_path = normalize_image_path(args.image_path)
    api_key = get_api_key()

    output_dir = (
        pathlib.Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else DEFAULT_OUTPUT_DIR
    )
    base_name = f"{image_path.stem}_{OUTPUT_SUFFIX}"

    output_text = call_gemini(args.model, image_path, api_key)
    report = extract_section(
        output_text,
        "[SCHEMATIC ANALYSIS REPORT]",
        ["[FALSTAD TEXT]", "[FALSTAD XML]", "[LTSPICE ASC]"],
    )
    falstad_text = extract_section(
        output_text,
        "[FALSTAD TEXT]",
        ["[FALSTAD XML]", "[LTSPICE ASC]"],
    )
    falstad_xml = extract_section(
        output_text,
        "[FALSTAD XML]",
        ["[LTSPICE ASC]"],
    )
    ltspice_asc = extract_section(output_text, "[LTSPICE ASC]", [])

    if not falstad_text.startswith("$"):
        falstad_text = "$ 1 5e-6 10.2 50 5 43 5e-11\n"
    if not falstad_xml.startswith("<cir>"):
        falstad_xml = "<cir>\n  <note>Gemini did not return valid Falstad XML.</note>\n</cir>\n"
    if not ltspice_asc.startswith("Version 4"):
        ltspice_asc = "Version 4\nSHEET 1 880 680\nTEXT 0 0 Left 2 ! Gemini did not return a valid LTSpice schematic\n"
    if not report:
        report = (
            "# Gemini Schematic Analysis Report\n\n"
            "- Gemini did not return the expected report section.\n"
        )

    falstad_path = output_dir / f"{base_name}_falstad.txt"
    falstad_xml_path = output_dir / f"{base_name}_falstad.xml"
    ltspice_path = output_dir / f"{base_name}.asc"
    report_path = output_dir / f"{base_name}_report.md"

    write_text(falstad_path, falstad_text.rstrip() + "\n")
    write_text(falstad_xml_path, falstad_xml.rstrip() + "\n")
    write_text(ltspice_path, ltspice_asc.rstrip() + "\n")
    write_text(report_path, report.rstrip() + "\n")

    print(f"AGENT_NAME={AGENT_NAME}")
    print(f"MODEL={args.model}")
    print(f"FALSTAD_FILE={falstad_path}")
    print(f"FALSTAD_XML_FILE={falstad_xml_path}")
    print(f"LTSPICE_FILE={ltspice_path}")
    print(f"REPORT_FILE={report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
