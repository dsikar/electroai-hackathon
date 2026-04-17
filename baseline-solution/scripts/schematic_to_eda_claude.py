#!/usr/bin/env python3
"""Generate Falstad and LTSpice outputs from a schematic image via Anthropic Claude.

Mirrors the structure of schematic_to_eda_codex.py; swap API key env var and run.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python scripts/schematic_to_eda_claude.py images/01_circuit.png
    python scripts/schematic_to_eda_claude.py images/01_circuit.png --output-dir /some/other/dir

Outputs (default: simulations/claude/, named <stem>_generated-by-claude-sonnet-4-6.*):
    *_falstad.txt   Falstad plain-text netlist (URL-encodeable)
    *_falstad.xml   Falstad <cir> XML format
    *.asc           LTSpice schematic file
    *_report.md     Markdown report with component table, assumptions, validation
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import re
import sys
import zlib

import anthropic


AGENT_NAME = "claude-sonnet-4-6"
OUTPUT_SUFFIX = f"generated-by-{AGENT_NAME}"
DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_OUTPUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "simulations" / "claude"
MAX_TOKENS = 4096

SUPPORTED_IMAGE_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = f"""You are {AGENT_NAME}, an expert electrical engineer and circuit reverse-engineering assistant.

Analyse the supplied schematic image and return a single valid JSON object.
Return ONLY the JSON — no prose, no markdown fences, no text before or after.

Required top-level keys:
  agent_name          (string, must be "{AGENT_NAME}")
  circuit_name        (string)
  circuit_summary     (string, 2–4 sentences describing function and operation)
  components          (array; each item: reference, type, value, connections)
  assumptions         (array of strings — values or part numbers you assumed)
  missing_information (array of strings — labels or values absent from the image)
  inconsistencies     (array of strings — contradictions or ambiguities)
  falstad_netlist     (string — Falstad plain-text format, first line starts with "$")
  ltspice_netlist     (string — LTSpice .asc graphical schematic format)

Rules:
- Identify every visible component, net label, supply rail, and load element.
- Falstad netlist: plain-text coordinate-based format (NOT XML or JSON).
- LTSpice netlist: LTSpice .asc graphical schematic format. First line must be "Version 4",
  second line "SHEET 1 880 680", then WIRE, FLAG, IOPIN, SYMBOL, SYMATTR, and TEXT lines.
  Include a simulation directive as a TEXT line, e.g.: TEXT x y Left 2 !.tran 0 50m 0 10u
- State every assumption explicitly; never invent values silently.
- Record every contradiction, unreadable value, or missing label in the appropriate field.
"""

USER_TEXT = (
    "Reverse-engineer this schematic into a Falstad plain-text netlist "
    "and an LTSpice .asc netlist. "
    "Record any unclear, contradictory, or missing information in the JSON fields."
)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Falstad + LTSpice outputs from a schematic image via Claude."
    )
    parser.add_argument("image_path", help="Path to a PNG / JPG / WEBP / GIF schematic image.")
    parser.add_argument(
        "--model",
        default=os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL),
        help=f"Anthropic model to use (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--output-dir",
        help=f"Directory for output files. Defaults to {DEFAULT_OUTPUT_DIR}.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Image + API
# ---------------------------------------------------------------------------

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


def call_claude(model: str, image_path: pathlib.Path, api_key: str) -> str:
    client = anthropic.Anthropic(api_key=api_key)
    media_type = SUPPORTED_IMAGE_TYPES[image_path.suffix.lower()]
    image_data = base64.b64encode(image_path.read_bytes()).decode("ascii")

    message = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": USER_TEXT},
                ],
            }
        ],
    )
    return message.content[0].text


# ---------------------------------------------------------------------------
# JSON parsing
# ---------------------------------------------------------------------------

def extract_json(text: str) -> str:
    """Strip markdown fences if Claude wraps the JSON in a code block."""
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    return match.group(1) if match else text.strip()


def parse_result(output_text: str) -> dict:
    try:
        result = json.loads(extract_json(output_text))
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Model output was not valid JSON: {exc}\n\n"
            f"First 400 chars:\n{output_text[:400]}"
        ) from exc
    result["agent_name"] = AGENT_NAME
    return result


# ---------------------------------------------------------------------------
# Falstad URL encoding  (identical to gen_falstad_urls.py)
# ---------------------------------------------------------------------------

def falstad_url(text: str) -> str:
    compressed = zlib.compress(text.encode("utf-8"), level=9)
    encoded = base64.b64encode(compressed, altchars=b"-_").rstrip(b"=").decode()
    return f"https://www.falstad.com/circuit/circuitjs.html#{encoded}"


# ---------------------------------------------------------------------------
# Validation  (mirrors schematic_to_eda_codex.py)
# ---------------------------------------------------------------------------

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
            refs.add(normalize_ref(parts[0]))
    return refs


def validate_result(result: dict) -> list[str]:
    issues: list[str] = []

    if not result.get("circuit_name", "").strip():
        issues.append("Circuit name is empty.")
    if not result.get("circuit_summary", "").strip():
        issues.append("Circuit summary is empty.")

    falstad = result.get("falstad_netlist", "").strip()
    if not falstad.startswith("$"):
        issues.append("Falstad netlist does not start with '$'.")

    ltspice = result.get("ltspice_netlist", "").strip()
    if not ltspice.startswith("Version 4"):
        issues.append("LTSpice .asc file does not start with 'Version 4'.")

    components = result.get("components", [])
    if not components:
        issues.append("Component list is empty.")

    seen: set[str] = set()
    duplicates: set[str] = set()
    no_connections: list[str] = []

    for comp in components:
        ref = normalize_ref(comp.get("reference", ""))
        if not ref:
            issues.append("A component entry is missing its reference designator.")
            continue
        if ref in seen:
            duplicates.add(ref)
        seen.add(ref)
        if not comp.get("connections"):
            no_connections.append(ref)

    if duplicates:
        issues.append("Duplicate references: " + ", ".join(sorted(duplicates)))
    if no_connections:
        issues.append(
            "Components with no connections listed: " + ", ".join(sorted(no_connections))
        )

    ltspice_refs = extract_ltspice_refs(ltspice)
    absent = sorted(r for r in seen if r not in ltspice_refs)
    if absent:
        issues.append(
            "Components in analysis absent from LTSpice netlist: " + ", ".join(absent)
        )

    link = falstad_url(falstad)
    if not link.startswith("https://www.falstad.com/circuit/circuitjs.html#"):
        issues.append("Falstad URL has an unexpected prefix.")
    if not link.split("#", 1)[1]:
        issues.append("Falstad URL fragment is empty.")

    return issues


# ---------------------------------------------------------------------------
# Falstad plain-text → XML conversion
# ---------------------------------------------------------------------------

def falstad_plain_to_xml(text: str) -> str:
    """Convert a Falstad plain-text netlist to the <cir> XML element format.

    Header line mapping ($ f ts ic cb vr pb mts):
        $ 1 0.000005 10.2 50 5 43 5e-11
        → <cir f="1" ts="0.000005" ic="10.2" cb="50" pb="43" vr="5" mts="5e-11">

    Element mappings:
        r  x1 y1 x2 y2 flags resistance       → <r  x="..." f="..." r="..."/>
        c  x1 y1 x2 y2 flags capacitance       → <c  x="..." f="..." c="..."/>
        l  x1 y1 x2 y2 flags inductance        → <l  x="..." f="..." l="..."/>
        d  x1 y1 x2 y2 flags model             → <d  x="..." f="..." model="..."/>
        v  x1 y1 x2 y2 flags wf freq amp ...   → <v  x="..." f="..." wf="..." maxv="..."/>
        t  x1 y1 x2 y2 flags pnp base hfe ...  → <t  x="..." f="..." pnp="..." hfe="..."/>
        a  x1 y1 x2 y2 flags gain              → <a  x="..." f="..." gain="..."/>
        s  x1 y1 x2 y2 flags state             → <s  x="..." f="..." state="..."/>
        w  x1 y1 x2 y2 flags                   → <w  x="..." f="..."/>
        g  x1 y1 x2 y2 flags                   → <g  x="..." f="..."/>
        o  ...                                  → (skipped — scope probe)
    """
    def field(parts: list[str], idx: int, default: str = "0") -> str:
        return parts[idx] if len(parts) > idx else default

    xml_lines: list[str] = []
    header_written = False

    for raw in text.splitlines():
        parts = raw.split()
        if not parts:
            continue

        kind = parts[0]

        # ── Header ──────────────────────────────────────────────────────────
        if kind == "$":
            f   = field(parts, 1, "1")
            ts  = field(parts, 2, "0.000005")
            ic  = field(parts, 3, "0")
            cb  = field(parts, 4, "50")
            vr  = field(parts, 5, "5")   # field[5] in text → vr attr
            pb  = field(parts, 6, "43")  # field[6] in text → pb attr
            mts = field(parts, 7, "5e-11")
            xml_lines.append(
                f'<cir f="{f}" ts="{ts}" ic="{ic}" cb="{cb}" pb="{pb}" vr="{vr}" mts="{mts}">'
            )
            header_written = True
            continue

        # Skip anything before the header or scope probes
        if not header_written or kind == "o":
            continue

        x1, y1, x2, y2 = (field(parts, i) for i in (1, 2, 3, 4))
        coords = f"{x1} {y1} {x2} {y2}"
        fl = field(parts, 5)

        if kind == "r":
            xml_lines.append(f'  <r x="{coords}" f="{fl}" r="{field(parts, 6)}"/>')

        elif kind == "c":
            xml_lines.append(f'  <c x="{coords}" f="{fl}" c="{field(parts, 6)}"/>')

        elif kind == "l":
            xml_lines.append(f'  <l x="{coords}" f="{fl}" l="{field(parts, 6)}"/>')

        elif kind == "d":
            xml_lines.append(f'  <d x="{coords}" f="{fl}" model="{field(parts, 6, "default")}"/>')

        elif kind == "v":
            # v x1 y1 x2 y2 flags waveform freq amplitude dc phase
            wf   = field(parts, 6)   # waveform type
            maxv = field(parts, 8)   # amplitude (peak / DC voltage)
            xml_lines.append(f'  <v x="{coords}" f="{fl}" wf="{wf}" maxv="{maxv}"/>')

        elif kind == "t":
            # t x1 y1 x2 y2 flags pnp base_v hfe ...
            pnp = field(parts, 6)
            hfe = field(parts, 8, "100")
            xml_lines.append(f'  <t x="{coords}" f="{fl}" pnp="{pnp}" hfe="{hfe}"/>')

        elif kind == "a":
            xml_lines.append(f'  <a x="{coords}" f="{fl}" gain="{field(parts, 6, "1000000")}"/>')

        elif kind == "s":
            xml_lines.append(f'  <s x="{coords}" f="{fl}" state="{field(parts, 6)}"/>')

        elif kind == "w":
            xml_lines.append(f'  <w x="{coords}" f="{fl}"/>')

        elif kind == "g":
            xml_lines.append(f'  <g x="{coords}" f="{fl}"/>')

        else:
            # Unknown element — preserve as generic with raw trailing fields
            raw_attrs = " ".join(parts[5:])
            xml_lines.append(f'  <{kind} x="{coords}" f="{fl}" raw="{raw_attrs}"/>')

    if not header_written:
        xml_lines.insert(0, '<cir f="1" ts="0.000005" ic="0" cb="50" pb="43" vr="5" mts="5e-11">')

    xml_lines.append("</cir>")
    return "\n".join(xml_lines) + "\n"


# ---------------------------------------------------------------------------
# Post-processing
# ---------------------------------------------------------------------------

def ensure_end(text: str) -> str:
    stripped = text.rstrip()
    if not stripped.upper().endswith(".END"):
        stripped += "\n.END"
    return stripped + "\n"


def write_text(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Report  (adds component table compared to codex version)
# ---------------------------------------------------------------------------

def render_report(
    image_path: pathlib.Path,
    model: str,
    result: dict,
    validation_issues: list[str],
    falstad_link: str,
) -> str:
    def bullets(items: list[str], empty: str) -> str:
        return f"- {empty}\n" if not items else "".join(f"- {i}\n" for i in items)

    components = result.get("components", [])
    comp_rows = "\n".join(
        "| {ref} | {typ} | {val} | {conn} |".format(
            ref=c.get("reference", "?"),
            typ=c.get("type", "?"),
            val=c.get("value", "?"),
            conn=", ".join(c.get("connections", [])),
        )
        for c in components
    )

    lines = [
        f"# Schematic Conversion Report ({AGENT_NAME})",
        "",
        f"- **Source image:** `{image_path}`",
        f"- **Model:** `{model}`",
        f"- **Circuit name:** {result.get('circuit_name', '(unknown)')}",
        f"- **Falstad URL:** {falstad_link}",
        "",
        "## Summary",
        "",
        result.get("circuit_summary", "").strip(),
        "",
        "## Components",
        "",
        "| Reference | Type | Value | Connections |",
        "|-----------|------|-------|-------------|",
        comp_rows,
        "",
        "## Assumptions",
        "",
        bullets(result.get("assumptions", []), "None."),
        "## Missing Information",
        "",
        bullets(result.get("missing_information", []), "None."),
        "## Inconsistencies",
        "",
        bullets(result.get("inconsistencies", []), "None detected."),
        "## Validation",
        "",
        bullets(validation_issues, "Passed all local validation checks."),
    ]
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    args = parse_args()
    image_path = normalize_image_path(args.image_path)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("Error: ANTHROPIC_API_KEY environment variable not set.")

    output_dir = (
        pathlib.Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else DEFAULT_OUTPUT_DIR
    )
    base_name = f"{image_path.stem}_{OUTPUT_SUFFIX}"

    print(f"Analysing {image_path.name} with {args.model} ...", file=sys.stderr)
    output_text = call_claude(args.model, image_path, api_key)
    result = parse_result(output_text)

    result["falstad_netlist"] = result["falstad_netlist"].rstrip() + "\n"
    result["ltspice_netlist"] = result["ltspice_netlist"].rstrip() + "\n"

    falstad_link = falstad_url(result["falstad_netlist"].strip())
    validation_issues = validate_result(result)
    report_text = render_report(
        image_path=image_path,
        model=args.model,
        result=result,
        validation_issues=validation_issues,
        falstad_link=falstad_link,
    )

    falstad_path     = output_dir / f"{base_name}_falstad.txt"
    falstad_xml_path = output_dir / f"{base_name}_falstad.xml"
    spice_path       = output_dir / f"{base_name}.asc"
    report_path      = output_dir / f"{base_name}_report.md"

    write_text(falstad_path, result["falstad_netlist"])
    write_text(falstad_xml_path, falstad_plain_to_xml(result["falstad_netlist"]))
    write_text(spice_path, result["ltspice_netlist"])
    write_text(report_path, report_text)

    # Machine-readable summary — same KEY=VALUE convention as codex script
    print(f"AGENT_NAME={AGENT_NAME}")
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
