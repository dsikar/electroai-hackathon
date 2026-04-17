from __future__ import annotations

import argparse
import json
import mimetypes
import pathlib
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .agent_pipeline import REPO_ROOT, is_within, make_manager


WEBAPP_ROOT = pathlib.Path(__file__).resolve().parent
STATIC_ROOT = WEBAPP_ROOT / "static"
TEMPLATE_ROOT = WEBAPP_ROOT / "templates"
MANAGER = make_manager()


class PipelineRequestHandler(BaseHTTPRequestHandler):
    server_version = "CircuitPipelineWeb/0.1"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._serve_file(TEMPLATE_ROOT / "index.html", "text/html; charset=utf-8")
            return
        if parsed.path.startswith("/static/"):
            relative = parsed.path.removeprefix("/static/")
            target = STATIC_ROOT / relative
            if target.exists():
                content_type, _ = mimetypes.guess_type(target.name)
                self._serve_file(target, content_type or "application/octet-stream")
                return
        if parsed.path == "/api/state":
            self._respond_json(MANAGER.get_state())
            return
        if parsed.path == "/api/file":
            params = parse_qs(parsed.query)
            requested = params.get("path", [""])[0]
            target = pathlib.Path(requested).expanduser()
            if not requested or not target.exists() or not is_within(target.resolve(), REPO_ROOT):
                self.send_error(HTTPStatus.NOT_FOUND, "File not found.")
                return
            content_type, _ = mimetypes.guess_type(target.name)
            self._serve_file(target, content_type or "text/plain; charset=utf-8")
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found.")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        payload = self._read_json()
        try:
            if parsed.path == "/api/start":
                state = MANAGER.start_run(
                    payload["input_dir"],
                    payload["output_root"],
                    bool(payload.get("ltspice_png_enabled")),
                )
                self._respond_json(state)
                return
            if parsed.path == "/api/cancel":
                self._respond_json(MANAGER.cancel_run())
                return
            if parsed.path == "/api/refresh":
                state = MANAGER.refresh(
                    payload["input_dir"],
                    payload["output_root"],
                    bool(payload.get("ltspice_png_enabled")),
                )
                self._respond_json(state)
                return
        except RuntimeError as exc:
            self._respond_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found.")

    def log_message(self, format: str, *args: object) -> None:
        return

    def _serve_file(self, path: pathlib.Path, content_type: str) -> None:
        data = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def _respond_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the multi-agent circuit pipeline web app.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), PipelineRequestHandler)
    print(f"Serving pipeline dashboard at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
