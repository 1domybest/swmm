#!/usr/bin/env python3
"""Step-by-step PySWMM bridge for the HTML drainage viewer.

The HTML viewer is allowed to send only rainfall and blockage controls. This
bridge applies those inputs to SWMM, advances the simulation, and returns a
viewer-ready state payload. Hydraulic values are read from SWMM, not calculated
by the HTML.
"""

from __future__ import annotations

import argparse
import json
import math
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = ROOT / "models" / "seoul_rebuild_v2.inp"
DEFAULT_CONTRACT = ROOT / "sample-results" / "swmm_html_contract.json"
DEFAULT_OUTPUT = ROOT / "sample-results" / "swmm_html_bridge_preview.jsonl"

FLOW_EPSILON_CMS = 0.0005
MIN_BLOCKED_FLOW_CMS = 0.000001
CONTROL_LINK_TYPES = {"ORIFICE", "WEIR", "PUMP"}


class PySwmmUnavailable(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_sections(inp_text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in inp_text.splitlines():
        line = raw_line.strip()
        if line.startswith("[") and line.endswith("]"):
            current = line[1:-1].upper()
            sections.setdefault(current, [])
            continue
        if current:
            sections[current].append(raw_line)
    return sections


def storm_timeseries_peak(sections: dict[str, list[str]]) -> float:
    peak = 0.0
    for raw_line in sections.get("TIMESERIES", []):
        line = raw_line.strip()
        if not line or line.startswith(";"):
            continue
        parts = line.split()
        if len(parts) >= 3 and parts[0] == "TS_STORM_RAIN":
            peak = max(peak, float(parts[2]))
    return peak


def storm_inflow_peak_by_node(model_path: Path) -> dict[str, float]:
    text = model_path.read_text(encoding="utf-8")
    sections = iter_sections(text)
    storm_peak = storm_timeseries_peak(sections)
    inflows: dict[str, float] = {}
    for raw_line in sections.get("INFLOWS", []):
        line = raw_line.strip()
        if not line or line.startswith(";"):
            continue
        parts = line.split()
        if len(parts) >= 5 and parts[2] == "TS_STORM_RAIN":
            inflows[parts[0]] = float(parts[4]) * storm_peak
    return inflows


def build_runtime_control_model(source_model: Path) -> Path:
    """Create a temporary model where storm time-series inflows are disabled.

    The bridge then injects stormwater with Node.generated_inflow() so the HTML
    rainfall control is the live source of rainfall. Dry-weather sewer inflows
    remain in the model.
    """
    lines = source_model.read_text(encoding="utf-8").splitlines()
    current: str | None = None
    output_lines: list[str] = []
    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            current = stripped[1:-1].upper()
            output_lines.append(raw_line)
            continue
        if current == "INFLOWS" and stripped and not stripped.startswith(";"):
            parts = stripped.split()
            if len(parts) >= 5 and parts[2] == "TS_STORM_RAIN":
                parts[4] = "0.00"
                output_lines.append("{:<40} {:<11} {:<17} {:<6} {:<7} {:<8} {}".format(*parts[:7]))
                continue
        output_lines.append(raw_line)

    temp_dir = Path(tempfile.mkdtemp(prefix="swmm-html-bridge-"))
    runtime_model = temp_dir / source_model.name
    runtime_model.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    return runtime_model


def cross_section_depth(link_meta: dict[str, Any]) -> float:
    xsection = link_meta.get("crossSection") or {}
    shape = str(xsection.get("shape", "")).upper()
    geom1 = float(xsection.get("geom1") or 0)
    geom2 = float(xsection.get("geom2") or 0)
    if shape == "CIRCULAR":
        return geom1
    if shape.startswith("RECT"):
        return geom1
    return max(geom1, geom2, 1.0)


def full_flow_capacity_cms(link_meta: dict[str, Any]) -> float:
    if float(link_meta.get("maxFlowCms") or 0) > 0:
        return float(link_meta["maxFlowCms"])
    if link_meta.get("linkType") != "CONDUIT":
        return 0.0

    xsection = link_meta.get("crossSection") or {}
    shape = str(xsection.get("shape", "")).upper()
    roughness = float(link_meta.get("roughnessN") or 0.015)
    slope = max(abs(float(link_meta.get("computedSlope") or 0.0005)), 0.0001)
    geom1 = float(xsection.get("geom1") or 0)
    geom2 = float(xsection.get("geom2") or 0)

    if shape == "CIRCULAR" and geom1 > 0:
        area = math.pi * geom1 * geom1 / 4
        hydraulic_radius = geom1 / 4
    elif shape.startswith("RECT") and geom1 > 0 and geom2 > 0:
        area = geom1 * geom2
        hydraulic_radius = area / (2 * (geom1 + geom2))
    else:
        return 0.0
    return (1 / roughness) * area * (hydraulic_radius ** (2 / 3)) * math.sqrt(slope)


def full_flow_area_sqm(link_meta: dict[str, Any]) -> float:
    xsection = link_meta.get("crossSection") or {}
    shape = str(xsection.get("shape", "")).upper()
    geom1 = float(xsection.get("geom1") or 0)
    geom2 = float(xsection.get("geom2") or 0)
    barrels = max(int(float(xsection.get("barrels") or 1)), 1)

    if shape == "CIRCULAR" and geom1 > 0:
        return math.pi * geom1 * geom1 / 4 * barrels
    if shape.startswith("RECT") and geom1 > 0 and geom2 > 0:
        return geom1 * geom2 * barrels
    return 0.0


def display_velocity_mps(link_meta: dict[str, Any], flow_cms: float, raw_velocity_mps: float) -> float:
    if raw_velocity_mps > 0:
        return raw_velocity_mps
    if link_meta.get("linkType") != "CONDUIT" or abs(flow_cms) <= FLOW_EPSILON_CMS:
        return 0.0
    area = full_flow_area_sqm(link_meta)
    if area <= 0:
        return 0.0
    return abs(flow_cms) / area


def safe_number(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def safe_attr(obj: Any, name: str, default: float = 0.0) -> float:
    try:
        return safe_number(getattr(obj, name), default)
    except Exception:
        return default


def import_pyswmm() -> tuple[Any, Any, Any]:
    try:
        from pyswmm import Links, Nodes, Simulation
    except ModuleNotFoundError as exc:
        raise PySwmmUnavailable(
            "PySWMM is not installed. Install it first with `python3 -m pip install pyswmm`."
        ) from exc
    return Simulation, Nodes, Links


class SwmmHtmlBridge:
    def __init__(
        self,
        model_path: Path = DEFAULT_MODEL,
        contract_path: Path = DEFAULT_CONTRACT,
        *,
        step_seconds: int = 1,
        disable_model_storm_inflows: bool = True,
    ) -> None:
        self.source_model_path = model_path
        self.model_path = build_runtime_control_model(model_path) if disable_model_storm_inflows else model_path
        self.contract = load_json(contract_path)
        self.step_seconds = step_seconds
        self.storm_inflow_peaks = storm_inflow_peak_by_node(model_path)
        self.node_meta = self.contract["swmmIndexes"]["nodes"]
        self.link_meta = self.contract["swmmIndexes"]["links"]
        self.objects = self.contract["visualObjects"]
        self.object_by_id = {item["htmlId"]: item for item in self.objects}
        self.link_capacity = {
            link_id: full_flow_capacity_cms(meta)
            for link_id, meta in self.link_meta.items()
        }

        Simulation, Nodes, Links = import_pyswmm()
        self.sim = Simulation(str(self.model_path))
        self.sim.__enter__()
        self.sim.step_advance(step_seconds)
        self.nodes = Nodes(self.sim)
        self.links = Links(self.sim)
        self._iterator = iter(self.sim)

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
        self.sim.__exit__(None, None, None)

    def __enter__(self) -> "SwmmHtmlBridge":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def apply_rainfall(self, rainfall_ratio: float) -> None:
        ratio = max(0.0, min(1.0, rainfall_ratio))
        for node_id, peak_cms in self.storm_inflow_peaks.items():
            node = self.get_node(node_id)
            if node is not None:
                node.generated_inflow(ratio * peak_cms)

    def apply_blockage_to_link(self, link_id: str, blockage_ratio: float) -> None:
        link = self.get_link(link_id)
        if link is None:
            return
        meta = self.link_meta.get(link_id, {})
        open_ratio = max(0.0, min(1.0, 1.0 - blockage_ratio))
        if meta.get("linkType") in CONTROL_LINK_TYPES:
            link.target_setting = open_ratio
            return

        capacity = self.link_capacity.get(link_id, 0.0)
        if capacity <= 0:
            return
        try:
            link.flow_limit = 0.0 if open_ratio >= 0.999 else max(capacity * open_ratio, MIN_BLOCKED_FLOW_CMS)
        except Exception:
            # Some SWMM/PySWMM link types do not expose a mutable flow limit.
            return

    def apply_controls(self, payload: dict[str, Any]) -> None:
        self.apply_rainfall(safe_number(payload.get("rainfallRatio", payload.get("rainfall", 0.0))))
        for exception in payload.get("exceptions", []):
            blockage = max(0.0, min(1.0, safe_number(exception.get("blockage"))))
            for link_id in exception.get("swmmLinks", []):
                self.apply_blockage_to_link(link_id, blockage)

    def visual_pipe_state(self, obj: dict[str, Any]) -> dict[str, Any]:
        return self.visual_link_state(obj.get("swmmLinks", []), include_fullness=True)

    def visual_link_state(self, link_ids: list[str], *, include_fullness: bool = False) -> dict[str, Any]:
        states: list[dict[str, Any]] = []
        for link_id in link_ids:
            link = self.get_link(link_id)
            if link is None:
                continue
            meta = self.link_meta.get(link_id, {})
            depth = safe_attr(link, "depth")
            flow = safe_attr(link, "flow")
            raw_velocity = abs(safe_attr(link, "velocity"))
            velocity = display_velocity_mps(meta, flow, raw_velocity)
            full_depth = max(cross_section_depth(meta), 0.001)
            capacity = self.link_capacity.get(link_id, 0.0)
            states.append(
                {
                    "link_type": meta.get("linkType"),
                    "depth": depth,
                    "flow": flow,
                    "velocity": velocity,
                    "raw_velocity": raw_velocity,
                    "fullness": max(0.0, min(1.5, depth / full_depth)),
                    "capacity": capacity,
                }
            )
        if not states:
            base_state = {"flow_cms": 0.0, "velocity_mps": 0.0, "direction": "forward", "active": False}
            if include_fullness:
                base_state.update({"fullness": 0.0, "capacity_cms": 0.0})
            return base_state

        representative = max(states, key=lambda item: abs(item["flow"]))
        conduit_states = [item for item in states if item["link_type"] == "CONDUIT"]
        velocity_source = max(conduit_states, key=lambda item: abs(item["flow"]), default=representative)
        capacity = max((item["capacity"] for item in states), default=0.0)
        summary = {
            "flow_cms": representative["flow"],
            "velocity_mps": velocity_source["velocity"],
            "direction": "reverse" if representative["flow"] < -FLOW_EPSILON_CMS else "forward",
            "active": any(abs(item["flow"]) > FLOW_EPSILON_CMS for item in states),
        }
        if include_fullness:
            summary.update({
                "capacity_cms": capacity,
                "fullness": max(item["fullness"] for item in states),
            })
        return summary

    def connected_link_ids(self, node_ids: list[str], explicit_link_ids: list[str]) -> list[str]:
        connected = set(explicit_link_ids)
        node_set = set(node_ids)
        if node_set:
            for link_id, meta in self.link_meta.items():
                if meta.get("fromNode") in node_set or meta.get("toNode") in node_set:
                    connected.add(link_id)
        return sorted(connected)

    def visual_asset_state(self, obj: dict[str, Any]) -> dict[str, Any]:
        depths: list[float] = []
        ratios: list[float] = []
        inflows: list[float] = []
        for node_id in obj.get("swmmNodes", []):
            node = self.get_node(node_id)
            if node is None:
                continue
            meta = self.node_meta.get(node_id, {})
            depth = safe_attr(node, "depth")
            max_depth = max(float(meta.get("maxDepthM") or 1.0), 0.001)
            depths.append(depth)
            ratios.append(max(0.0, min(1.5, depth / max_depth)))
            inflows.append(safe_attr(node, "total_inflow"))
        link_state = self.visual_link_state(
            self.connected_link_ids(obj.get("swmmNodes", []), obj.get("swmmLinks", [])),
        )
        flow = safe_number(link_state.get("flow_cms"))
        node_inflow = max(inflows, default=0.0)
        return {
            "depth_m": max(depths, default=0.0),
            "depth_ratio": max(ratios, default=0.0),
            "inflow_cms": max(node_inflow, abs(flow)),
            "flow_cms": flow,
            "velocity_mps": safe_number(link_state.get("velocity_mps")),
            "direction": link_state.get("direction", "forward"),
            "active": max(ratios, default=0.0) > 0.01 or bool(link_state.get("active")),
            "status": "normal",
        }

    def visual_outfall_state(self, obj: dict[str, Any]) -> dict[str, Any]:
        asset_state = self.visual_asset_state(obj)
        pipe_state = self.visual_pipe_state(obj)
        flow = safe_number(pipe_state.get("flow_cms"))
        has_flow = abs(flow) > FLOW_EPSILON_CMS
        return {
            **asset_state,
            "flow_cms": flow,
            "velocity_mps": safe_number(pipe_state.get("velocity_mps")),
            "depth_ratio": max(safe_number(asset_state.get("depth_ratio")), 0.08 if has_flow else 0.0),
            "direction": pipe_state.get("direction", "forward"),
            "active": bool(has_flow or asset_state.get("active")),
            "status": "normal" if has_flow else "idle",
        }

    def collect_state_payload(self, control_payload: dict[str, Any]) -> dict[str, Any]:
        pipes: dict[str, Any] = {}
        assets: dict[str, Any] = {}
        for obj in self.objects:
            if obj["objectType"] == "pipe_group":
                pipes[obj["htmlId"]] = self.visual_pipe_state(obj)
            elif obj["objectType"] == "outfall":
                assets[obj["htmlId"]] = self.visual_outfall_state(obj)
            else:
                assets[obj["htmlId"]] = self.visual_asset_state(obj)

        controls = {}
        for link_id in ("storm_pump_unit", "overflow_normal_flow_gate", "pump_outfall_gate", "treated_outfall_gate", "overflow_outfall_gate"):
            link = self.get_link(link_id)
            if link is not None:
                controls[link_id] = {
                    "target_setting": safe_attr(link, "target_setting", 1.0),
                    "flow_cms": safe_attr(link, "flow"),
                    "active": abs(safe_attr(link, "flow")) > FLOW_EPSILON_CMS,
                }
        if "overflow_normal_flow_gate" in controls:
            controls["overflow_to_interceptor_drop"] = dict(controls["overflow_normal_flow_gate"])

        return {
            "contractVersion": self.contract["version"],
            "sourceOfTruth": "SWMM",
            "modelTime": self.sim.current_time.isoformat(),
            "rainfallRatio": safe_number(control_payload.get("rainfallRatio", control_payload.get("rainfall", 0.0))),
            "pipes": pipes,
            "assets": assets,
            "controls": controls,
        }

    def step(self, control_payload: dict[str, Any]) -> dict[str, Any]:
        self.apply_controls(control_payload)
        next(self._iterator)
        return self.collect_state_payload(control_payload)


def sample_control_payload(contract_path: Path = DEFAULT_CONTRACT) -> dict[str, Any]:
    contract = load_json(contract_path)
    return {
        "contractVersion": contract["version"],
        "sourceOfTruth": "SWMM",
        "reason": "sample",
        "stepSeconds": 1,
        "rainfall": 0.75,
        "rainfallRatio": 0.75,
        "exceptions": [],
        "blockagesById": {},
        "physicsMode": "swmm-step",
        "htmlRole": "render_only_with_controls",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the SWMM HTML bridge for a few 1-second steps.")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--control-json", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--sample-control", action="store_true")
    parser.add_argument("--keep-model-storm-inflows", action="store_true")
    args = parser.parse_args()

    if args.sample_control:
        print(json.dumps(sample_control_payload(args.contract), ensure_ascii=False, indent=2))
        return 0

    control_payload = (
        load_json(args.control_json)
        if args.control_json
        else sample_control_payload(args.contract)
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with SwmmHtmlBridge(
            args.model,
            args.contract,
            step_seconds=int(control_payload.get("stepSeconds", 1)),
            disable_model_storm_inflows=not args.keep_model_storm_inflows,
        ) as bridge:
            with args.output.open("w", encoding="utf-8") as out:
                for _ in range(args.steps):
                    out.write(json.dumps(bridge.step(control_payload), ensure_ascii=False) + "\n")
    except PySwmmUnavailable as exc:
        print(str(exc))
        return 2

    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
