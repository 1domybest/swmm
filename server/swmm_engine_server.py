#!/usr/bin/env python3
"""Small HTTP server that exposes the PySWMM HTML bridge.

The browser sends rainfall and blockage controls. This server advances SWMM by
one step and returns the state payload that overall_drainage_diagram.html knows
how to render.
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import threading
import zipfile
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from swmm_html_bridge import (  # noqa: E402
    DEFAULT_CONTRACT,
    DEFAULT_MODEL,
    PySwmmUnavailable,
    SwmmHtmlBridge,
    load_json,
)
from editor_layout_to_swmm_inp import (  # noqa: E402
    ConversionError,
    convert_layout,
    render_conversion_report,
    render_inp,
    render_mapping_json,
)


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


class EngineSession:
    def __init__(self, model_path: Path, contract_path: Path, step_seconds: int = 1) -> None:
        self.model_path = model_path
        self.contract_path = contract_path
        self.step_seconds = step_seconds
        self.lock = threading.RLock()
        self.bridge: SwmmHtmlBridge | None = None
        self.step_index = 0
        self.last_payload: dict[str, Any] | None = None

    def close(self) -> None:
        with self.lock:
            if self.bridge is not None:
                self.bridge.close()
                self.bridge = None

    def reset(self, step_seconds: int | None = None) -> dict[str, Any]:
        with self.lock:
            self.close()
            if step_seconds is not None:
                self.step_seconds = max(1, int(step_seconds))
            self.step_index = 0
            self.last_payload = None
            return {
                "ok": True,
                "status": "reset",
                "stepSeconds": self.step_seconds,
            }

    def ensure_bridge(self, step_seconds: int | None = None) -> SwmmHtmlBridge:
        if step_seconds is not None:
            next_step_seconds = max(1, int(step_seconds))
            if next_step_seconds != self.step_seconds:
                self.reset(next_step_seconds)
        if self.bridge is None:
            self.bridge = SwmmHtmlBridge(
                self.model_path,
                self.contract_path,
                step_seconds=self.step_seconds,
                disable_model_storm_inflows=True,
            )
        return self.bridge

    def step(self, control_payload: dict[str, Any]) -> dict[str, Any]:
        with self.lock:
            bridge = self.ensure_bridge(int(control_payload.get("stepSeconds", self.step_seconds) or 1))
            state = bridge.step(control_payload)
            self.step_index += 1
            state["ok"] = True
            state["stepIndex"] = self.step_index
            self.last_payload = state
            return state


def json_bytes(payload: dict[str, Any], status: int = 200) -> tuple[int, bytes]:
    return status, json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


def sanitize_download_name(value: Any, fallback: str = "generated_from_editor.inp") -> str:
    text = str(value or fallback).strip() or fallback
    safe = "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in text)
    if not safe.endswith(".inp"):
        safe += ".inp"
    return safe


def sanitize_zip_name(value: Any, fallback: str = "swmm-editor-export.zip") -> str:
    text = str(value or fallback).strip() or fallback
    safe = "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in text)
    if not safe.endswith(".zip"):
        safe += ".zip"
    return safe


def build_editor_conversion_payload(payload: dict[str, Any]) -> dict[str, Any]:
    layout = payload.get("layout", payload)
    if not isinstance(layout, dict):
        raise ConversionError("Request body must contain an EditorLayout object or { layout }.")
    scale_m_per_px = float(payload.get("scaleMPerPx", 0.5) or 0.5)
    map_height = float(payload.get("mapHeight", 2000.0) or 2000.0)
    title = str(payload.get("title") or "SWMM model generated from React editor layout")
    result = convert_layout(layout, scale_m_per_px=scale_m_per_px, map_height=map_height)
    inp_text = render_inp(result, title=title)
    report = render_conversion_report(result, inp_text=inp_text)
    mapping = render_mapping_json(result)
    return {
        "ok": len(result.errors) == 0,
        "inpText": inp_text,
        "report": report,
        "mapping": mapping,
        "warnings": result.warnings,
        "errors": result.errors,
    }


def make_handler(session: EngineSession) -> type[BaseHTTPRequestHandler]:
    class SwmmEngineHandler(BaseHTTPRequestHandler):
        server_version = "SwmmEngineServer/0.1"

        def log_message(self, format: str, *args: Any) -> None:
            sys.stderr.write("[swmm-engine] " + format % args + "\n")

        def send_json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            self.wfile.write(body)

        def send_text_download(self, status: int, body: str, filename: str, warnings: list[str]) -> None:
            encoded = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Expose-Headers", "Content-Disposition, X-Editor-Inp-Warnings")
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            if warnings:
                self.send_header("X-Editor-Inp-Warnings", json.dumps(warnings, ensure_ascii=False))
            self.end_headers()
            self.wfile.write(encoded)

        def send_zip_download(self, status: int, body: bytes, filename: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Expose-Headers", "Content-Disposition")
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.end_headers()
            self.wfile.write(body)

        def read_json_body(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length") or "0")
            if length <= 0:
                return {}
            raw = self.rfile.read(length)
            return json.loads(raw.decode("utf-8"))

        def do_OPTIONS(self) -> None:  # noqa: N802
            self.send_response(HTTPStatus.NO_CONTENT)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/health":
                self.send_json(
                    HTTPStatus.OK,
                    {
                        "ok": True,
                        "service": "swmm-engine",
                        "modelPath": str(session.model_path),
                        "contractPath": str(session.contract_path),
                        "stepSeconds": session.step_seconds,
                        "hasActiveSession": session.bridge is not None,
                        "stepIndex": session.step_index,
                    },
                )
                return
            if self.path == "/contract":
                self.send_json(HTTPStatus.OK, load_json(session.contract_path))
                return
            self.send_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not_found", "path": self.path})

        def do_POST(self) -> None:  # noqa: N802
            try:
                payload = self.read_json_body()
                if self.path == "/session/start":
                    reset_payload = session.reset(int(payload.get("stepSeconds", session.step_seconds) or 1))
                    self.send_json(HTTPStatus.OK, reset_payload)
                    return
                if self.path == "/session/reset":
                    reset_payload = session.reset(int(payload.get("stepSeconds", session.step_seconds) or 1))
                    self.send_json(HTTPStatus.OK, reset_payload)
                    return
                if self.path == "/session/step":
                    self.send_json(HTTPStatus.OK, session.step(payload))
                    return
                if self.path == "/editor/convert/validate":
                    conversion = build_editor_conversion_payload(payload)
                    self.send_json(HTTPStatus.OK, {
                        "ok": conversion["ok"],
                        "inpText": conversion["inpText"],
                        "report": conversion["report"],
                        "mapping": conversion["mapping"],
                    })
                    return
                if self.path == "/editor/convert/download":
                    conversion = build_editor_conversion_payload(payload)
                    if not conversion["ok"]:
                        self.send_json(HTTPStatus.UNPROCESSABLE_ENTITY, {
                            "ok": False,
                            "error": "editor_layout_conversion_has_errors",
                            "report": conversion["report"],
                            "mapping": conversion["mapping"],
                        })
                        return
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
                        archive.writestr("model.inp", conversion["inpText"])
                        archive.writestr(
                            "conversion-report.json",
                            json.dumps(conversion["report"], ensure_ascii=False, indent=2),
                        )
                        archive.writestr(
                            "swmm-react-mapping.json",
                            json.dumps(conversion["mapping"], ensure_ascii=False, indent=2),
                        )
                    filename = sanitize_zip_name(payload.get("filename"))
                    self.send_zip_download(HTTPStatus.OK, zip_buffer.getvalue(), filename)
                    return
                if self.path == "/editor/export-inp":
                    filename = sanitize_download_name(payload.get("filename"))
                    conversion = build_editor_conversion_payload(payload)
                    status = HTTPStatus.OK if conversion["ok"] else HTTPStatus.UNPROCESSABLE_ENTITY
                    self.send_text_download(status, conversion["inpText"], filename, conversion["warnings"])
                    return
                self.send_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "not_found", "path": self.path})
            except ConversionError as exc:
                self.send_json(
                    HTTPStatus.BAD_REQUEST,
                    {
                        "ok": False,
                        "error": "editor_layout_conversion_failed",
                        "message": str(exc),
                    },
                )
            except PySwmmUnavailable as exc:
                self.send_json(
                    HTTPStatus.SERVICE_UNAVAILABLE,
                    {
                        "ok": False,
                        "error": "pyswmm_unavailable",
                        "message": str(exc),
                    },
                )
            except StopIteration:
                session.close()
                self.send_json(
                    HTTPStatus.CONFLICT,
                    {
                        "ok": False,
                        "error": "simulation_finished",
                        "message": "SWMM simulation has finished. Reset the session to start again.",
                    },
                )
            except Exception as exc:  # pragma: no cover - server safety net
                self.send_json(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {
                        "ok": False,
                        "error": exc.__class__.__name__,
                        "message": str(exc),
                    },
                )

    return SwmmEngineHandler


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the SWMM engine HTTP server for the drainage HTML viewer.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--step-seconds", type=int, default=1)
    args = parser.parse_args()

    session = EngineSession(args.model, args.contract, step_seconds=max(1, args.step_seconds))
    server = ThreadingHTTPServer((args.host, args.port), make_handler(session))
    print(f"SWMM engine server listening on http://{args.host}:{args.port}")
    print(f"Model: {args.model}")
    print(f"Contract: {args.contract}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        session.close()
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
