#!/usr/bin/env python3
"""FastAPI/WebSocket SWMM runtime server for the React editor.

The React editor sends only control inputs such as rainfall and blockage.
Hydraulic state is advanced by PySWMM and streamed back once per simulation
step. The editor layout can be posted directly to /engine/start; the server
converts it into a temporary INP model and keeps the generated mapping for
runtime snapshots.
"""

from __future__ import annotations

import argparse
import asyncio
import io
import json
import math
import sys
import tempfile
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, Response
except ModuleNotFoundError as exc:  # pragma: no cover - import guard for local setup
    FASTAPI_IMPORT_ERROR: ModuleNotFoundError | None = exc
    FastAPI = HTTPException = WebSocket = WebSocketDisconnect = None  # type: ignore[assignment]
    CORSMiddleware = JSONResponse = Response = None  # type: ignore[assignment]
else:
    FASTAPI_IMPORT_ERROR = None


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from editor_layout_to_swmm_inp import (  # noqa: E402
    DEFAULT_CATCHMENT_AREA_M2,
    DEFAULT_HORIZONTAL_SLOPE,
    DEFAULT_MANHOLE_RAINFALL_FACTOR,
    DEFAULT_RUNOFF_COEFFICIENT,
    ConversionError,
    convert_layout,
    render_conversion_report,
    render_inp,
    render_mapping_json,
)
from swmm_html_bridge import (  # noqa: E402
    DEFAULT_CONTRACT,
    DEFAULT_MODEL,
    CONTROL_LINK_TYPES,
    MIN_BLOCKED_FLOW_CMS,
    PySwmmUnavailable,
    build_runtime_control_model,
    cross_section_depth,
    display_velocity_mps,
    full_flow_area_sqm,
    full_flow_capacity_cms,
    import_pyswmm,
    load_json,
    safe_attr,
    safe_number,
    storm_inflow_peak_by_node,
)


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_STEP_SECONDS = 1
DEFAULT_MAX_RAINFALL_MM_PER_HOUR = 100.0
DEFAULT_SPEED_MULTIPLIER = 1.0
MAX_SPEED_MULTIPLIER = 10.0
MAX_RAINFALL_RATIO = 10.0


@dataclass
class RuntimeModelSpec:
    model_path: Path
    mapping: dict[str, Any]
    report: dict[str, Any]
    source: str
    temp_dir: tempfile.TemporaryDirectory[str] | None = None

    def cleanup(self) -> None:
        if self.temp_dir is not None:
            self.temp_dir.cleanup()
            self.temp_dir = None


def clamp_ratio(value: Any) -> float:
    parsed = safe_number(value, 0.0)
    if parsed > 1.0:
        parsed = parsed / 100.0
    return max(0.0, min(1.0, parsed))


def clamp_rainfall_ratio(value: Any) -> float:
    parsed = safe_number(value, 0.0)
    if parsed > 1.0:
        parsed = parsed / 100.0
    return max(0.0, min(MAX_RAINFALL_RATIO, parsed))


def clamp_speed_multiplier(value: Any) -> float:
    return max(1.0, min(MAX_SPEED_MULTIPLIER, safe_number(value, DEFAULT_SPEED_MULTIPLIER)))


def sanitize_download_name(value: Any, fallback: str) -> str:
    text = str(value or fallback).strip() or fallback
    safe = "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in text)
    if not safe.endswith(".inp"):
        safe += ".inp"
    return safe


def sanitize_zip_name(value: Any, fallback: str) -> str:
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


def build_runtime_model_spec(payload: dict[str, Any]) -> RuntimeModelSpec:
    layout = payload.get("layout")
    if isinstance(layout, dict):
        conversion = build_editor_conversion_payload(payload)
        if not conversion["ok"]:
            raise HTTPException(
                status_code=422,
                detail={
                    "ok": False,
                    "error": "editor_layout_conversion_has_errors",
                    "report": conversion["report"],
                    "mapping": conversion["mapping"],
                },
            )
        temp_dir = tempfile.TemporaryDirectory(prefix="swmm-react-runtime-")
        model_path = Path(temp_dir.name) / "react_editor_runtime.inp"
        model_path.write_text(conversion["inpText"], encoding="utf-8")
        return RuntimeModelSpec(
            model_path=model_path,
            mapping=conversion["mapping"],
            report=conversion["report"],
            source="react-editor-json",
            temp_dir=temp_dir,
        )

    model_path = Path(payload.get("modelPath") or DEFAULT_MODEL).expanduser()
    if not model_path.is_absolute():
        model_path = ROOT / model_path
    contract_path = Path(payload.get("contractPath") or DEFAULT_CONTRACT).expanduser()
    if not contract_path.is_absolute():
        contract_path = ROOT / contract_path
    return legacy_contract_model_spec(model_path, contract_path)


def legacy_contract_model_spec(model_path: Path, contract_path: Path) -> RuntimeModelSpec:
    contract = load_json(contract_path)
    mapping = {
        "version": 1,
        "source": "swmm-html-contract",
        "editorNodes": {},
        "editorLinks": {},
        "swmmNodes": {
            node_id: {
                "section": meta.get("nodeType"),
                "sourceEditorId": None,
                "sourceEditorType": "contract",
                "sourceEditorName": node_id,
                "reactPoint": meta.get("map", {}),
                "swmmCoordinate": meta.get("map", {}),
                "invertElevation": meta.get("elevationM"),
                "maxDepth": meta.get("maxDepthM"),
            }
            for node_id, meta in (contract.get("swmmIndexes", {}).get("nodes") or {}).items()
        },
        "swmmLinks": {
            link_id: {
                "kind": meta.get("linkType"),
                "fromNode": meta.get("fromNode"),
                "toNode": meta.get("toNode"),
                "sourceEditorId": None,
                "sourceEditorType": "contract",
                "sourceEditorName": link_id,
                "pipeKind": "default",
                "length": meta.get("lengthM"),
                "diameter": (meta.get("crossSection") or {}).get("geom1"),
                "roughness": meta.get("roughnessN"),
                "initialSetting": 1.0,
            }
            for link_id, meta in (contract.get("swmmIndexes", {}).get("links") or {}).items()
        },
    }
    report = {
        "ok": True,
        "counts": {
            "junctions": len(contract.get("swmmIndexes", {}).get("nodes") or {}),
            "conduits": len(contract.get("swmmIndexes", {}).get("links") or {}),
            "warnings": 0,
            "errors": 0,
        },
        "warnings": [],
        "errors": [],
        "dynamicControls": {
            "rainfallTargets": sorted(storm_inflow_peak_by_node(model_path)),
            "rainfallTargetWeights": {},
            "dryWeatherTargets": [],
            "blockageTargets": [
                {"swmmLinkId": link_id, "sourceEditorId": None, "sourceEditorName": link_id, "pipeKind": "default"}
                for link_id, meta in mapping["swmmLinks"].items()
                if meta.get("kind") in {"CONDUIT", "ORIFICE", "WEIR", "PUMP"}
            ],
        },
    }
    return RuntimeModelSpec(model_path=model_path, mapping=mapping, report=report, source="swmm-html-contract")


def rainfall_cms_for_percent(
    ratio: float,
    *,
    max_rainfall_mm_per_hour: float,
    catchment_area_m2: float = DEFAULT_CATCHMENT_AREA_M2,
    runoff_coefficient: float = DEFAULT_RUNOFF_COEFFICIENT,
) -> float:
    rainfall_mm_per_hour = max(0.0, max_rainfall_mm_per_hour) * ratio
    return rainfall_mm_per_hour / 1000.0 / 3600.0 * catchment_area_m2 * runoff_coefficient


def link_capacity_from_mapping(link_id: str, mapping: dict[str, Any]) -> float:
    link_meta = (mapping.get("swmmLinks") or {}).get(link_id) or {}
    if str(link_meta.get("kind") or "").upper() != "CONDUIT":
        return 0.0
    diameter = safe_number(link_meta.get("diameter"), 0.0)
    roughness = safe_number(link_meta.get("roughness"), 0.013)
    length = max(safe_number(link_meta.get("length"), 0.0), 0.001)
    from_node = (mapping.get("swmmNodes") or {}).get(link_meta.get("fromNode")) or {}
    to_node = (mapping.get("swmmNodes") or {}).get(link_meta.get("toNode")) or {}
    from_elev = safe_number(from_node.get("invertElevation"), 0.0)
    to_elev = safe_number(to_node.get("invertElevation"), from_elev - DEFAULT_HORIZONTAL_SLOPE * length)
    slope = max(abs(from_elev - to_elev) / length, DEFAULT_HORIZONTAL_SLOPE)
    if diameter <= 0 or roughness <= 0:
        return 0.0
    area = math.pi * diameter * diameter / 4.0
    hydraulic_radius = diameter / 4.0
    return (1.0 / roughness) * area * (hydraulic_radius ** (2.0 / 3.0)) * math.sqrt(slope)


class RealtimeSwmmSession:
    def __init__(
        self,
        spec: RuntimeModelSpec,
        *,
        step_seconds: int,
        max_rainfall_mm_per_hour: float,
    ) -> None:
        self.spec = spec
        self.step_seconds = max(1, int(step_seconds))
        self.max_rainfall_mm_per_hour = max_rainfall_mm_per_hour
        self.speed_multiplier = DEFAULT_SPEED_MULTIPLIER
        self.step_index = 0
        self.rainfall_ratio = 0.0
        self.blockages_by_id: dict[str, float] = {}
        self.last_snapshot: dict[str, Any] | None = None

        self.mapping = spec.mapping
        self.report = spec.report
        self.swmm_nodes = self.mapping.get("swmmNodes") or {}
        self.swmm_links = self.mapping.get("swmmLinks") or {}
        self.node_connected_links = self.build_node_connected_links()
        self.control_link_ids = self.build_control_link_ids()
        dynamic_controls = self.report.get("dynamicControls") or {}
        rainfall_targets = [str(node_id) for node_id in dynamic_controls.get("rainfallTargets") or []]
        raw_rainfall_weights = dynamic_controls.get("rainfallTargetWeights") or {}
        self.rainfall_target_weights = {
            str(node_id): max(0.0, safe_number(weight, 1.0))
            for node_id, weight in raw_rainfall_weights.items()
        } if isinstance(raw_rainfall_weights, dict) else {}
        self.rainfall_targets = sorted(set(rainfall_targets) | set(self.rainfall_target_weights.keys()))

        self.runtime_model_path = build_runtime_control_model(spec.model_path)
        Simulation, Nodes, Links = import_pyswmm()
        self.sim = Simulation(str(self.runtime_model_path))
        self.sim.__enter__()
        self.sim.step_advance(self.step_seconds)
        self.nodes = Nodes(self.sim)
        self.links = Links(self.sim)
        self._iterator = iter(self.sim)

    def build_node_connected_links(self) -> dict[str, set[str]]:
        connected: dict[str, set[str]] = {}
        for link_id, meta in self.swmm_links.items():
            from_node = str(meta.get("fromNode") or "")
            to_node = str(meta.get("toNode") or "")
            if from_node:
                connected.setdefault(from_node, set()).add(link_id)
            if to_node:
                connected.setdefault(to_node, set()).add(link_id)
        return connected

    def build_control_link_ids(self) -> set[str]:
        targets = {
            str(target.get("swmmLinkId"))
            for target in (self.report.get("dynamicControls") or {}).get("blockageTargets") or []
            if target.get("swmmLinkId")
        }
        if targets:
            return targets
        return {
            link_id
            for link_id, meta in self.swmm_links.items()
            if str(meta.get("kind") or "").upper() in {"CONDUIT", "ORIFICE", "WEIR", "PUMP"}
        }

    def get_node(self, node_id: str) -> Any | None:
        try:
            return self.nodes[node_id]
        except Exception:
            return None

    def get_link(self, link_id: str) -> Any | None:
        try:
            return self.links[link_id]
        except Exception:
            return None

    def close(self) -> None:
        try:
            self.sim.__exit__(None, None, None)
        finally:
            self.spec.cleanup()

    def update_controls(self, payload: dict[str, Any]) -> dict[str, Any]:
        if "rainfallRatio" in payload or "rainfall" in payload:
            self.rainfall_ratio = clamp_rainfall_ratio(payload.get("rainfallRatio", payload.get("rainfall", self.rainfall_ratio)))

        if "speedMultiplier" in payload:
            self.speed_multiplier = clamp_speed_multiplier(payload.get("speedMultiplier"))

        next_blockages: dict[str, float] = {}
        raw_blockages = payload.get("blockagesById") or {}
        if isinstance(raw_blockages, dict):
            for raw_id, raw_value in raw_blockages.items():
                blockage = clamp_ratio(raw_value.get("blockage", raw_value.get("blockageRatio", 0.0)) if isinstance(raw_value, dict) else raw_value)
                next_blockages[str(raw_id)] = blockage
        for exception in payload.get("exceptions", []) if isinstance(payload.get("exceptions"), list) else []:
            blockage = clamp_ratio(exception.get("blockage", 0.0))
            for link_id in exception.get("swmmLinks", []):
                next_blockages[str(link_id)] = blockage

        if "blockagesById" in payload or "exceptions" in payload:
            self.blockages_by_id = next_blockages

        return self.control_state()

    def control_state(self) -> dict[str, Any]:
        return {
            "rainfallRatio": self.rainfall_ratio,
            "rainfallPercent": round(self.rainfall_ratio * 100.0, 2),
            "blockagesById": self.blockages_by_id,
            "maxRainfallMmPerHour": self.max_rainfall_mm_per_hour,
            "speedMultiplier": self.speed_multiplier,
        }

    def apply_rainfall(self) -> None:
        inflow_cms = rainfall_cms_for_percent(
            self.rainfall_ratio,
            max_rainfall_mm_per_hour=self.max_rainfall_mm_per_hour,
        )
        for node_id in self.rainfall_targets:
            weight = self.rainfall_target_weights.get(node_id, 1.0)
            node = self.get_node(node_id)
            if node is not None:
                node.generated_inflow(inflow_cms * weight)

    def blockage_for_link(self, link_id: str) -> float:
        blockage = self.blockages_by_id.get(link_id, 0.0)
        meta = self.swmm_links.get(link_id) or {}
        for node_id in (str(meta.get("fromNode") or ""), str(meta.get("toNode") or "")):
            blockage = max(blockage, self.blockages_by_id.get(node_id, 0.0))
        return max(0.0, min(1.0, blockage))

    def apply_blockage_to_link(self, link_id: str, blockage_ratio: float) -> None:
        link = self.get_link(link_id)
        if link is None:
            return
        meta = self.swmm_links.get(link_id) or {}
        link_type = str(meta.get("kind") or "").upper()
        open_ratio = max(0.0, min(1.0, 1.0 - blockage_ratio))

        try:
            if link_type in CONTROL_LINK_TYPES:
                link.target_setting = open_ratio
                return
        except Exception:
            pass

        capacity = link_capacity_from_mapping(link_id, self.mapping)
        if capacity <= 0:
            return
        try:
            link.flow_limit = 0.0 if open_ratio >= 0.999 else max(capacity * open_ratio, MIN_BLOCKED_FLOW_CMS)
        except Exception:
            return

    def apply_blockages(self) -> None:
        for link_id in self.control_link_ids:
            self.apply_blockage_to_link(link_id, self.blockage_for_link(link_id))

    def apply_controls(self) -> None:
        self.apply_rainfall()
        self.apply_blockages()

    def collect_node_states(self) -> dict[str, Any]:
        states: dict[str, Any] = {}
        for node_id, meta in self.swmm_nodes.items():
            node = self.get_node(node_id)
            if node is None:
                continue
            max_depth = max(safe_number(meta.get("maxDepth"), 1.0), 0.001)
            depth = safe_attr(node, "depth")
            states[node_id] = {
                "depthM": depth,
                "headM": safe_attr(node, "head"),
                "invertElevationM": safe_number(meta.get("invertElevation"), 0.0),
                "depthRatio": max(0.0, min(2.0, depth / max_depth)),
                "totalInflowCms": safe_attr(node, "total_inflow"),
                "floodingCms": safe_attr(node, "flooding"),
            }
        return states

    def collect_link_states(self) -> dict[str, Any]:
        states: dict[str, Any] = {}
        for link_id, meta in self.swmm_links.items():
            link = self.get_link(link_id)
            if link is None:
                continue
            flow = safe_attr(link, "flow")
            raw_velocity = abs(safe_attr(link, "velocity"))
            depth = safe_attr(link, "depth")
            full_depth = max(safe_number(meta.get("diameter"), 0.0), 0.001)
            capacity = link_capacity_from_mapping(link_id, self.mapping)
            if capacity <= 0:
                capacity = full_flow_capacity_cms({
                    "linkType": meta.get("kind"),
                    "lengthM": meta.get("length"),
                    "roughnessN": meta.get("roughness"),
                    "computedSlope": DEFAULT_HORIZONTAL_SLOPE,
                    "crossSection": {
                        "shape": "CIRCULAR",
                        "geom1": meta.get("diameter"),
                        "geom2": 0,
                        "barrels": 1,
                    },
                })
            velocity_meta = {
                "linkType": meta.get("kind"),
                "crossSection": {
                    "shape": "CIRCULAR",
                    "geom1": meta.get("diameter"),
                    "geom2": 0,
                    "barrels": 1,
                },
            }
            velocity = display_velocity_mps(velocity_meta, flow, raw_velocity)
            if velocity <= 0 and abs(flow) > 0:
                area = full_flow_area_sqm(velocity_meta)
                velocity = abs(flow) / area if area > 0 else 0.0
            states[link_id] = {
                "kind": meta.get("kind"),
                "flowCms": flow,
                "velocityMps": velocity,
                "depthM": depth,
                "fullness": max(0.0, min(2.0, depth / full_depth)),
                "capacityCms": capacity,
                "capacityRatio": abs(flow) / capacity if capacity > 0 else 0.0,
                "direction": "reverse" if flow < -0.0005 else "forward",
                "targetSetting": safe_attr(link, "target_setting", 1.0),
                "currentSetting": safe_attr(link, "current_setting", 1.0),
                "blockageRatio": self.blockage_for_link(link_id),
            }
        return states

    def aggregate_editor_states(self, node_states: dict[str, Any], link_states: dict[str, Any]) -> dict[str, Any]:
        editor_states: dict[str, Any] = {}
        for editor_id, refs in (self.mapping.get("editorNodes") or {}).items():
            linked_node_ids = [node_id for node_id in refs.get("swmmNodes", []) if node_id in node_states]
            linked_link_ids = set(link_id for link_id in refs.get("swmmLinks", []) if link_id in link_states)
            is_manhole_editor_node = any(
                (self.swmm_nodes.get(node_id) or {}).get("sourceEditorType") == "manhole"
                for node_id in linked_node_ids
            )
            is_storage_facility_editor_node = any(
                (self.swmm_nodes.get(node_id) or {}).get("sourceEditorType") in {"catchBasin", "facility"}
                for node_id in linked_node_ids
            )
            if is_manhole_editor_node or is_storage_facility_editor_node:
                for node_id in linked_node_ids:
                    linked_link_ids.update(self.node_connected_links.get(node_id, set()))
            linked_node_states = [node_states[node_id] for node_id in linked_node_ids]
            linked_link_states = [link_states[link_id] for link_id in linked_link_ids if link_id in link_states]
            if not linked_node_states and not linked_link_states:
                continue
            editor_states[editor_id] = {
                "maxDepthRatio": max((state.get("depthRatio", 0.0) for state in linked_node_states), default=0.0),
                "maxFullness": max((state.get("fullness", 0.0) for state in linked_link_states), default=0.0),
                "maxCapacityRatio": max((state.get("capacityRatio", 0.0) for state in linked_link_states), default=0.0),
                "maxBlockageRatio": max((state.get("blockageRatio", 0.0) for state in linked_link_states), default=0.0),
                "flowCms": max((state.get("flowCms", 0.0) for state in linked_link_states), key=abs, default=0.0),
                "maxVelocityMps": max((state.get("velocityMps", 0.0) for state in linked_link_states), key=abs, default=0.0),
                "totalInflowCms": max((state.get("totalInflowCms", 0.0) for state in linked_node_states), default=0.0),
            }
        for editor_id, refs in (self.mapping.get("editorLinks") or {}).items():
            linked_link_states = [link_states[link_id] for link_id in refs.get("swmmLinks", []) if link_id in link_states]
            if not linked_link_states:
                continue
            editor_states[editor_id] = {
                "maxFullness": max((state.get("fullness", 0.0) for state in linked_link_states), default=0.0),
                "maxCapacityRatio": max((state.get("capacityRatio", 0.0) for state in linked_link_states), default=0.0),
                "maxBlockageRatio": max((state.get("blockageRatio", 0.0) for state in linked_link_states), default=0.0),
                "flowCms": max((state.get("flowCms", 0.0) for state in linked_link_states), key=abs, default=0.0),
                "maxVelocityMps": max((state.get("velocityMps", 0.0) for state in linked_link_states), key=abs, default=0.0),
            }
        return editor_states

    def collect_snapshot(self, event_type: str = "snapshot") -> dict[str, Any]:
        node_states = self.collect_node_states()
        link_states = self.collect_link_states()
        editor_states = self.aggregate_editor_states(node_states, link_states)
        return {
            "type": event_type,
            "ok": True,
            "sourceOfTruth": "SWMM",
            "source": self.spec.source,
            "modelPath": str(self.spec.model_path),
            "runtimeModelPath": str(self.runtime_model_path),
            "modelTime": self.model_time_iso(),
            "stepSeconds": self.step_seconds,
            "stepIndex": self.step_index,
            "control": self.control_state(),
            "nodes": node_states,
            "links": link_states,
            "editorObjects": editor_states,
            "summary": {
                "nodeCount": len(node_states),
                "linkCount": len(link_states),
                "rainfallTargetCount": len(self.rainfall_targets),
                "blockageTargetCount": len(self.control_link_ids),
                "activeBlockageCount": sum(1 for value in self.blockages_by_id.values() if value > 0),
            },
        }

    def model_time_iso(self) -> str | None:
        try:
            return self.sim.current_time.isoformat()
        except Exception:
            return None

    def step(self) -> dict[str, Any]:
        self.apply_controls()
        next(self._iterator)
        self.step_index += 1
        self.last_snapshot = self.collect_snapshot("tick")
        return self.last_snapshot


class SwmmRuntimeEngine:
    def __init__(self) -> None:
        self.session: RealtimeSwmmSession | None = None
        self.task: asyncio.Task[None] | None = None
        self.lock = asyncio.Lock()
        self.websockets: set[WebSocket] = set()
        self.last_start_payload: dict[str, Any] | None = None
        self.last_error: str | None = None

    def status_payload(self) -> dict[str, Any]:
        session = self.session
        return {
            "ok": True,
            "running": session is not None and self.task is not None and not self.task.done(),
            "hasSession": session is not None,
            "stepIndex": session.step_index if session else 0,
            "stepSeconds": session.step_seconds if session else DEFAULT_STEP_SECONDS,
            "modelTime": session.model_time_iso() if session else None,
            "control": session.control_state() if session else {
                "rainfallRatio": 0.0,
                "rainfallPercent": 0.0,
                "blockagesById": {},
                "maxRainfallMmPerHour": DEFAULT_MAX_RAINFALL_MM_PER_HOUR,
                "speedMultiplier": DEFAULT_SPEED_MULTIPLIER,
            },
            "websocketClients": len(self.websockets),
            "lastError": self.last_error,
        }

    async def start(self, payload: dict[str, Any]) -> dict[str, Any]:
        async with self.lock:
            await self.stop_locked()
            step_seconds = max(1, int(payload.get("stepSeconds") or DEFAULT_STEP_SECONDS))
            max_rainfall = safe_number(payload.get("maxRainfallMmPerHour"), DEFAULT_MAX_RAINFALL_MM_PER_HOUR)
            spec = build_runtime_model_spec(payload)
            try:
                session = RealtimeSwmmSession(
                    spec,
                    step_seconds=step_seconds,
                    max_rainfall_mm_per_hour=max_rainfall,
                )
            except Exception:
                spec.cleanup()
                raise
            session.update_controls(payload.get("control") or payload)
            self.session = session
            self.last_start_payload = payload
            self.last_error = None
            self.task = asyncio.create_task(self.run_loop())
            snapshot = session.collect_snapshot("started")

        await self.broadcast(snapshot)
        return {
            "ok": True,
            "running": True,
            "status": self.status_payload(),
            "report": session.report,
            "mapping": session.mapping,
            "snapshot": snapshot,
        }

    async def stop_locked(self) -> None:
        if self.task is not None:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            self.task = None
        if self.session is not None:
            self.session.close()
            self.session = None

    async def stop(self) -> dict[str, Any]:
        async with self.lock:
            await self.stop_locked()
        payload = self.status_payload()
        await self.broadcast({"type": "stopped", **payload})
        return payload

    async def reset(self, payload: dict[str, Any]) -> dict[str, Any]:
        next_payload = payload or self.last_start_payload
        if not next_payload:
            return await self.stop()
        return await self.start(next_payload)

    async def update_controls(self, payload: dict[str, Any]) -> dict[str, Any]:
        async with self.lock:
            if self.session is None:
                raise HTTPException(status_code=409, detail="SWMM engine is not running.")
            control = self.session.update_controls(payload)
            snapshot = self.session.collect_snapshot("control")
        await self.broadcast(snapshot)
        return {"ok": True, "control": control, "snapshot": snapshot}

    async def run_loop(self) -> None:
        while self.session is not None:
            started_at = time.monotonic()
            try:
                snapshot = self.session.step()
            except StopIteration:
                self.last_error = "simulation_finished"
                await self.broadcast({"type": "finished", **self.status_payload()})
                async with self.lock:
                    await self.stop_locked()
                return
            except Exception as exc:  # pragma: no cover - runtime safety net
                self.last_error = f"{exc.__class__.__name__}: {exc}"
                await self.broadcast({"type": "error", "ok": False, "message": self.last_error})
                async with self.lock:
                    await self.stop_locked()
                return

            await self.broadcast(snapshot)
            elapsed = time.monotonic() - started_at
            step_delay = self.session.step_seconds / max(DEFAULT_SPEED_MULTIPLIER, self.session.speed_multiplier)
            await asyncio.sleep(max(0.0, step_delay - elapsed))

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.websockets.add(websocket)
        await websocket.send_json({"type": "status", **self.status_payload()})
        if self.session is not None and self.session.last_snapshot is not None:
            await websocket.send_json(self.session.last_snapshot)

    async def disconnect(self, websocket: WebSocket) -> None:
        self.websockets.discard(websocket)

    async def broadcast(self, payload: dict[str, Any]) -> None:
        stale: list[Any] = []
        for websocket in list(self.websockets):
            try:
                await websocket.send_json(payload)
            except Exception:
                stale.append(websocket)
        for websocket in stale:
            self.websockets.discard(websocket)


engine = SwmmRuntimeEngine()


if FASTAPI_IMPORT_ERROR is None:
    app = FastAPI(title="SWMM React Runtime Server", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition", "X-Editor-Inp-Warnings"],
    )
else:
    app = None


def require_app() -> Any:
    if FASTAPI_IMPORT_ERROR is not None:
        raise SystemExit(
            "FastAPI is not installed. Install dependencies with "
            "`python3 -m pip install -r requirements.txt`."
        )
    return app


if app is not None:

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "ok": True,
            "service": "swmm-fastapi-engine",
            "modelPath": str(DEFAULT_MODEL),
            "stepSeconds": DEFAULT_STEP_SECONDS,
            "engine": engine.status_payload(),
        }

    @app.get("/engine/status")
    async def engine_status() -> dict[str, Any]:
        return engine.status_payload()

    @app.post("/engine/start")
    async def engine_start(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return await engine.start(payload)
        except ConversionError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except PySwmmUnavailable as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.post("/engine/stop")
    async def engine_stop() -> dict[str, Any]:
        return await engine.stop()

    @app.post("/engine/reset")
    async def engine_reset(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            return await engine.reset(payload or {})
        except PySwmmUnavailable as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @app.post("/engine/control")
    async def engine_control(payload: dict[str, Any]) -> dict[str, Any]:
        return await engine.update_controls(payload)

    @app.get("/engine/snapshot")
    async def engine_snapshot() -> dict[str, Any]:
        if engine.session is None:
            raise HTTPException(status_code=409, detail="SWMM engine is not running.")
        return engine.session.collect_snapshot("snapshot")

    @app.post("/editor/convert/validate")
    async def editor_convert_validate(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            conversion = build_editor_conversion_payload(payload)
        except ConversionError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {
            "ok": conversion["ok"],
            "inpText": conversion["inpText"],
            "report": conversion["report"],
            "mapping": conversion["mapping"],
        }

    @app.post("/editor/convert/download")
    async def editor_convert_download(payload: dict[str, Any]) -> Any:
        try:
            conversion = build_editor_conversion_payload(payload)
        except ConversionError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if not conversion["ok"]:
            raise HTTPException(
                status_code=422,
                detail={
                    "ok": False,
                    "error": "editor_layout_conversion_has_errors",
                    "report": conversion["report"],
                    "mapping": conversion["mapping"],
                },
            )

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("model.inp", conversion["inpText"])
            archive.writestr("conversion-report.json", json.dumps(conversion["report"], ensure_ascii=False, indent=2))
            archive.writestr("swmm-react-mapping.json", json.dumps(conversion["mapping"], ensure_ascii=False, indent=2))
        filename = sanitize_zip_name(payload.get("filename"), "swmm-editor-export.zip")
        return Response(
            content=zip_buffer.getvalue(),
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    @app.post("/editor/export-inp")
    async def editor_export_inp(payload: dict[str, Any]) -> Any:
        try:
            conversion = build_editor_conversion_payload(payload)
        except ConversionError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        filename = sanitize_download_name(payload.get("filename"), "generated_from_editor.inp")
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Editor-Inp-Warnings": json.dumps(conversion["warnings"], ensure_ascii=True),
        }
        status_code = 200 if conversion["ok"] else 422
        return Response(
            content=conversion["inpText"],
            media_type="text/plain; charset=utf-8",
            status_code=status_code,
            headers=headers,
        )

    @app.websocket("/ws/simulation")
    async def simulation_websocket(websocket: WebSocket) -> None:
        await engine.connect(websocket)
        try:
            while True:
                message = await websocket.receive_json()
                message_type = message.get("type")
                if message_type == "control":
                    await engine.update_controls(message)
                elif message_type == "start":
                    await engine.start(message)
                elif message_type == "stop":
                    await engine.stop()
                elif message_type == "status":
                    await websocket.send_json({"type": "status", **engine.status_payload()})
        except WebSocketDisconnect:
            await engine.disconnect(websocket)


def main() -> int:
    require_app()
    try:
        import uvicorn
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Uvicorn is not installed. Install dependencies with "
            "`python3 -m pip install -r requirements.txt`."
        ) from exc

    parser = argparse.ArgumentParser(description="Run the FastAPI SWMM runtime server.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    uvicorn.run(
        "server.swmm_fastapi_server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        factory=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
