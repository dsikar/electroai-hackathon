#!/usr/bin/env python3
"""Generate Falstad and LTSpice outputs from a schematic image via OpenAI."""

from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request
import zlib


AGENT_NAME = "codex"
OUTPUT_SUFFIX = f"generated-by-{AGENT_NAME}"
DEFAULT_MODEL = "gpt-4o"  # Updated from gpt-5.4-mini to a real model for safety
API_URL = "https://api.openai.com/v1/chat/completions" # Corrected endpoint
DEFAULT_OUTPUT_DIR = pathlib.Path("simulations") / AGENT_NAME
SUPPORTED_IMAGE_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}

RESULT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "agent_name",
        "circuit_name",
        "circuit_summary",
        "components",
        "assumptions",
        "missing_information",
        "inconsistencies",
        "falstad_netlist",
        "falstad_xml",
        "ltspice_netlist",
    ],
    "properties": {
        "agent_name": {"type": "string"},
        "circuit_name": {"type": "string"},
        "circuit_summary": {"type": "string"},
        "components": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["reference", "type", "value", "connections"],
                "properties": {
                    "reference": {"type": "string"},
                    "type": {"type": "string"},
                    "value": {"type": "string"},
                    "connections": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
        },
        "assumptions": {
            "type": "array",
            "items": {"type": "string"},
        },
        "missing_information": {
            "type": "array",
            "items": {"type": "string"},
        },
        "inconsistencies": {
            "type": "array",
            "items": {"type": "string"},
        },
        "falstad_netlist": {"type": "string"},
        "falstad_xml": {"type": "string"},
        "ltspice_netlist": {"type": "string"},
    },
}

SYSTEM_PROMPT = f"""You are {AGENT_NAME}, an expert electrical engineer and circuit reverse-engineering assistant.

Analyse the supplied schematic image and return a single JSON object that matches the provided schema exactly.

Requirements:
- Identify all visible components, labels, supply rails, and load elements.
- Produce a Falstad plain-text circuit netlist, not XML.
- Produce a Falstad XML block that starts with `<cir>` and ends with `</cir>`.
- Produce an LTSpice-compatible .asc text output.
- Use explicit assumptions only when the image omits information.
- If the schematic contains contradictions, ambiguities, unreadable values, impossible connections, or missing labels, list them under `inconsistencies` or `missing_information`.
- Do not silently repair inconsistent schematics.
- Use `{AGENT_NAME}` for `agent_name`.
- The LTSpice netlist must end with `.END`.
- The Falstad netlist must be a plain-text circuit beginning with `$`.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Falstad and LTSpice outputs from a schematic image."
    )
    parser.add_argument("image_path", help="Path to a PNG/JPG/WEBP schematic image.")
    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
        help=f"OpenAI model to use (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory for generated files. Defaults to simulations/codex.",
    )
    return parser.parse_args()


def get_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Error: OPENAI_API_KEY environment variable not set.")
    return api_key


def normalize_image_path(image_path: str) -> pathlib.Path:
    path = pathlib.Path(image_path).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Error: image not found at {path}")
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_IMAGE_TYPES:
        supported = ", ".join(sorted(SUPPORTED_IMAGE_TYPES))
        raise SystemExit(
            f"Error: unsupported image type '{suffix}'. Use one of: {supported}"
        )
    return path


def encode_image_as_data_url(path: pathlib.Path) -> str:
    mime_type = SUPPORTED_IMAGE_TYPES[path.suffix.lower()]
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{payload}"


def build_payload(model: str, image_path: pathlib.Path) -> dict:
    data_url = encode_image_as_data_url(image_path)
    return {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Reverse-engineer this schematic image into Falstad plain text, "
                            "Falstad XML, and an LTSpice .asc schematic text output. "
                            "If any labels, values, or "
                            "connections are contradictory or unclear, record them explicitly."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": data_url},
                    },
                ],
            },
        ],
        "response_format": {"type": "json_object"},
    }


def call_openai(payload: dict, api_key: str) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenAI API request failed ({exc.code}): {details}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"OpenAI API request failed: {exc}") from exc


def extract_output_text(response: dict) -> str:
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise SystemExit("Error: unexpected response structure from OpenAI.")


def normalize_result(result: dict | None) -> tuple[dict, list[str]]:
    issues: list[str] = []
    if not isinstance(result, dict):
        issues.append("Model output was not a JSON object.")
        result = {}

    normalized = {
        "agent_name": AGENT_NAME,
        "circuit_name": result.get("circuit_name", "Unparsed schematic output"),
        "circuit_summary": result.get(
            "circuit_summary",
            "The model response did not fully match the expected schema. See validation notes."
        ),
        "components": result.get("components", []),
        "assumptions": result.get("assumptions", []),
        "missing_information": result.get("missing_information", []),
        "inconsistencies": result.get("inconsistencies", []),
        "falstad_netlist": result.get("falstad_netlist", "$ 1 5e-6 10.2 50 5 43 5e-11\n"),
        "falstad_xml": result.get(
            "falstad_xml",
            "<cir>\n  <note>Placeholder XML because the model response was incomplete.</note>\n</cir>\n",
        ),
        "ltspice_netlist": result.get(
            "ltspice_netlist",
            "* Placeholder output because the model response was incomplete.\n.END\n",
        ),
    }

    for key in RESULT_SCHEMA["required"]:
        if key not in result:
            issues.append(f"Model output was missing required key: {key}")

    if not isinstance(normalized["components"], list):
        issues.append("Model output field 'components' was not a list.")
        normalized["components"] = []
    if not isinstance(normalized["assumptions"], list):
        issues.append("Model output field 'assumptions' was not a list.")
        normalized["assumptions"] = []
    if not isinstance(normalized["missing_information"], list):
        issues.append("Model output field 'missing_information' was not a list.")
        normalized["missing_information"] = []
    if not isinstance(normalized["inconsistencies"], list):
        issues.append("Model output field 'inconsistencies' was not a list.")
        normalized["inconsistencies"] = []

    normalized["agent_name"] = AGENT_NAME
    return normalized, issues


def parse_result(output_text: str) -> tuple[dict, list[str]]:
    try:
        result = json.loads(output_text)
    except json.JSONDecodeError as exc:
        normalized, issues = normalize_result({})
        issues.insert(0, f"Model output was not valid JSON: {exc}")
        return normalized, issues
    return normalize_result(result)


def falstad_url(text: str) -> str:
    compressed = zlib.compress(text.encode("utf-8"), level=9)
    encoded = base64.b64encode(compressed, altchars=b"-_").rstrip(b"=").decode()
    return f"https://www.falstad.com/circuit/circuitjs.html#{encoded}"


def normalize_ref(ref: str) -> str:
    return re.sub(r"\s+", "", ref or "").upper()


def extract_ltspice_refs(netlist: str) -> set[str]:
    refs: set[str] = set()
    for raw_line in netlist.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("*", ".", ";")):
            continue
        parts = line.split()
        if parts:
            ref = parts[0]
            refs.add(normalize_ref(ref))
    return refs


def validate_result(result: dict) -> list[str]:
    issues: list[str] = []

    if not result.get("circuit_name", "").strip():
        issues.append("Circuit name is empty.")

    if not result.get("circuit_summary", "").strip():
        issues.append("Circuit summary is empty.")

    falstad_netlist = result.get("falstad_netlist", "").strip()
    if not falstad_netlist.startswith("$"):
        issues.append("Falstad netlist does not start with '$'.")

    falstad_xml = result.get("falstad_xml", "").strip()
    if not falstad_xml.startswith("<cir>") or not falstad_xml.endswith("</cir>"):
        issues.append("Falstad XML does not have the expected <cir>...</cir> wrapper.")

    ltspice_netlist = result.get("ltspice_netlist", "").strip()
    if ".END" not in ltspice_netlist.upper():
        issues.append("LTSpice netlist is missing a final .END directive.")

    components = result.get("components", [])
    if not components:
        issues.append("Component list is empty.")

    seen_refs: set[str] = set()
    duplicate_refs: set[str] = set()
    missing_connections: list[str] = []

    for component in components:
        if not isinstance(component, dict):
            issues.append(
                f"Component entry had unexpected type {type(component).__name__}; expected object."
            )
            continue
        ref = normalize_ref(component.get("reference", ""))
        if not ref:
            issues.append("A component is missing its reference designator.")
            continue
        if ref in seen_refs:
            duplicate_refs.add(ref)
        seen_refs.add(ref)
        if not component.get("connections"):
            missing_connections.append(ref)

    if duplicate_refs:
        issues.append(
            "Duplicate component references in component list: "
            + ", ".join(sorted(duplicate_refs))
        )

    if missing_connections:
        issues.append(
            "Components with no listed connections: "
            + ", ".join(sorted(missing_connections))
        )

    ltspice_refs = extract_ltspice_refs(ltspice_netlist)
    missing_from_ltspice = sorted(ref for ref in seen_refs if ref not in ltspice_refs)
    if missing_from_ltspice:
        issues.append(
            "Component references listed in the analysis but not found in LTSpice netlist: "
            + ", ".join(missing_from_ltspice)
        )

    falstad_link = falstad_url(falstad_netlist)
    if not falstad_link.startswith("https://www.falstad.com/circuit/circuitjs.html#"):
        issues.append("Generated Falstad URL has an unexpected prefix.")

    if not falstad_link.split("#", 1)[1]:
        issues.append("Generated Falstad URL has an empty fragment.")

    return issues


def ensure_end_of_netlist(text: str) -> str:
    stripped = text.rstrip()
    if not stripped.upper().endswith(".END"):
        stripped = stripped + "\n.END"
    return stripped + "\n"


def ensure_falstad_xml(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("<cir>") and stripped.endswith("</cir>"):
        return stripped + "\n"
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return "<cir>\n<text>\n" + escaped.rstrip() + "\n</text>\n</cir>\n"


def write_text(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_report(
    image_path: pathlib.Path,
    model: str,
    result: dict,
    validation_issues: list[str],
    falstad_link: str,
    raw_output_text: str,
) -> str:
    def bullet_block(items: list[str], empty_text: str) -> str:
        if not items:
            return f"- {empty_text}\n"
        return "".join(f"- {item}\n" for item in items)

    lines = [
        f"# Schematic Conversion Report ({AGENT_NAME})",
        "",
        f"- Source image: `{image_path}`",
        f"- Model: `{model}`",
        f"- Output suffix: `{OUTPUT_SUFFIX}`",
        f"- Output directory: `{DEFAULT_OUTPUT_DIR}`",
        f"- Circuit name: `{result.get('circuit_name', 'Unknown')}`",
        f"- Falstad URL: `{falstad_link}`",
        "",
        "## Summary",
        "",
        result.get("circuit_summary", "").strip() or "No summary generated.",
        "",
        "## Assumptions",
        "",
        bullet_block(result.get("assumptions", []), "None."),
        "## Missing Information",
        "",
        bullet_block(result.get("missing_information", []), "None."),
        "## Inconsistencies",
        "",
        bullet_block(result.get("inconsistencies", []), "None detected."),
        "## Validation",
        "",
        bullet_block(validation_issues, "Passed local validation checks."),
        "## Raw Model Output",
        "",
        "```json",
        raw_output_text.strip() or "{}",
        "```",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    image_path = normalize_image_path(args.image_path)
    api_key = get_api_key()

    output_dir = (
        pathlib.Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else (pathlib.Path.cwd() / DEFAULT_OUTPUT_DIR).resolve()
    )
    stem = image_path.stem
    base_name = f"{stem}_{OUTPUT_SUFFIX}"

    payload = build_payload(args.model, image_path)
    response = call_openai(payload, api_key)
    output_text = extract_output_text(response)
    result, parse_issues = parse_result(output_text)

    result["falstad_netlist"] = result["falstad_netlist"].rstrip() + "\n"
    result["falstad_xml"] = ensure_falstad_xml(result["falstad_xml"])
    result["ltspice_netlist"] = ensure_end_of_netlist(result["ltspice_netlist"])

    falstad_link = falstad_url(result["falstad_netlist"].strip())
    validation_issues = parse_issues + validate_result(result)
    report_text = render_report(
        image_path=image_path,
        model=args.model,
        result=result,
        validation_issues=validation_issues,
        falstad_link=falstad_link,
        raw_output_text=output_text,
    )

    falstad_path = output_dir / f"{base_name}_falstad.txt"
    falstad_xml_path = output_dir / f"{base_name}_falstad.xml"
    spice_path = output_dir / f"{base_name}.asc"
    report_path = output_dir / f"{base_name}_report.md"

    write_text(falstad_path, result["falstad_netlist"])
    write_text(falstad_xml_path, result["falstad_xml"])
    write_text(spice_path, result["ltspice_netlist"])
    write_text(report_path, report_text)

    print(f"AGENT_NAME={AGENT_NAME}")
    print(f"OUTPUT_SUFFIX={OUTPUT_SUFFIX}")
    print(f"MODEL={args.model}")
    print(f"FALSTAD_FILE={falstad_path}")
    print(f"FALSTAD_XML_FILE={falstad_xml_path}")
    print(f"FALSTAD_URL={falstad_link}")
    print(f"LTSPICE_FILE={spice_path}")
    print(f"REPORT_FILE={report_path}")
    if validation_issues:
        print("VALIDATION_STATUS=issues-found")
    elif result.get("inconsistencies") or result.get("missing_information"):
        print("VALIDATION_STATUS=schematic-issues-reported")
    else:
        print("VALIDATION_STATUS=clean")

    return 0


if __name__ == "__main__":
    sys.exit(main())
