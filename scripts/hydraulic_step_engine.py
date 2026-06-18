#!/usr/bin/env python3
"""One-step hydraulic control engine for the drainage diagram.

This module is the contract layer that will later be replaced by a live
PySWMM `for step in sim` loop. It intentionally uses the same object IDs as
the HTML diagram and registry.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from network_registry import registry_payload


GRAVITY = 9.81
PUMP_ON_LEVEL = 0.45
PUMP_OFF_LEVEL = 0.28
PUMP_CAPACITY_CMS = 1.20
OVERFLOW_GATE_START_LEVEL = 0.68
OVERFLOW_GATE_CLOSED_LEVEL = 0.92
OVERFLOW_GATE_MIN_SETTING = 0.12
BACKFLOW_FULLNESS_RATIO = 0.98
BACKFLOW_INFLOW_CMS = 0.002
DISCHARGE_FAILURE_RATIO = 0.05

PIPE_FLOW_ORDER = [
    "sep_sewer_lateral_apartment_1",
    "sep_sewer_lateral_apartment_2",
    "sep_sewer_main_1",
    "sep_sewer_main_2",
    "sep_sewer_main_to_interceptor",
    "sep_storm_lateral_catch_basin_1",
    "sep_storm_lateral_catch_basin_2",
    "sep_storm_main_1",
    "sep_storm_main_2",
    "sep_storm_main_to_trunk",
    "sep_storm_trunk",
    "storm_pump_discharge_pipe",
    "comb_sewer_lateral_house_1",
    "comb_sewer_lateral_house_2",
    "comb_storm_lateral_catch_basin_1",
    "comb_storm_lateral_catch_basin_2",
    "comb_main_1",
    "comb_main_2",
    "overflow_to_interceptor_drop",
    "overflow_pipe",
    "sep_interceptor",
    "treatment_effluent_pipe",
]


@dataclass
class PipeState:
    id: str
    inflow_cms: float = 0.0
    outflow_cms: float = 0.0
    storage_m3: float = 0.0
    storage_capacity_m3: float = 0.0
    capacity_cms: float = 0.0
    effective_capacity_cms: float = 0.0
    velocity_mps: float = 0.0
    fullness: float = 0.0
    blockage_ratio: float = 0.0
    direction: str = "forward"
    active: bool = False


@dataclass
class AssetState:
    id: str
    inflow_cms: float = 0.0
    outflow_cms: float = 0.0
    storage_m3: float = 0.0
    storage_capacity_m3: float = 0.0
    depth_ratio: float = 0.0
    blockage_ratio: float = 0.0
    status: str = "normal"
    active: bool = False


@dataclass
class StepResult:
    time_step_sec: int
    rainfall_ratio: float
    pipes: dict[str, PipeState] = field(default_factory=dict)
    assets: dict[str, AssetState] = field(default_factory=dict)
    controls: dict[str, Any] = field(default_factory=dict)
    next_state: dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        return {
            "timeStepSec": self.time_step_sec,
            "rainfallRatio": self.rainfall_ratio,
            "pipes": {
                pipe_id: {
                    "flow_cms": state.outflow_cms,
                    "inflow_cms": state.inflow_cms,
                    "storage_m3": state.storage_m3,
                    "storage_capacity_m3": state.storage_capacity_m3,
                    "capacity_cms": state.capacity_cms,
                    "effective_capacity_cms": state.effective_capacity_cms,
                    "velocity_mps": state.velocity_mps,
                    "fullness": state.fullness,
                    "blockage_ratio": state.blockage_ratio,
                    "direction": state.direction,
                    "active": state.active,
                }
                for pipe_id, state in self.pipes.items()
            },
            "assets": {
                asset_id: {
                    "inflow_cms": state.inflow_cms,
                    "outflow_cms": state.outflow_cms,
                    "storage_m3": state.storage_m3,
                    "storage_capacity_m3": state.storage_capacity_m3,
                    "depth_ratio": state.depth_ratio,
                    "blockage_ratio": state.blockage_ratio,
                    "status": state.status,
                    "active": state.active,
                }
                for asset_id, state in self.assets.items()
            },
            "controls": self.controls,
            "state": self.next_state,
        }


def clamp(value: float, low: float, high: float) -> float:
    return min(high, max(low, value))


def pipe_area(diameter_m: float) -> float:
    return math.pi * (diameter_m / 2) ** 2


def pipe_storage_capacity_m3(pipe: dict[str, Any], blockage_ratio: float = 0.0) -> float:
    physics = pipe.get("physics", {})
    diameter_m = float(physics.get("diameterM") or 0.1)
    length_m = max(float(physics.get("lengthM") or 1), 1.0)
    base_volume = pipe_area(diameter_m) * length_m
    # A clog reduces usable volume, but even a fully blocked pipe can hold water
    # between the inlet and the obstruction before upstream backup begins.
    usable_ratio = clamp(1 - blockage_ratio * 0.70, 0.30, 1.0)
    return max(base_volume * usable_ratio, 0.001)


def node_storage_capacity_m3(item: dict[str, Any]) -> float:
    physics = item.get("physics", {})
    max_depth = max(float(physics.get("maxDepthM") or 0), 0.1)
    ponded_area = float(physics.get("pondedAreaM2") or 0)
    node_type = str(physics.get("nodeType") or "")
    item_type = str(item.get("type") or "")

    if ponded_area > 0:
        return max(ponded_area * max_depth, 0.001)
    if item_type == "overflow_facility":
        return 110.0
    if item_type == "pump_station":
        return 90.0
    if item_type == "treatment_facility":
        return 360.0
    if item_type == "manhole":
        return max(20.0 * max_depth, 0.001)
    if node_type == "OUTFALLS":
        return 1.0
    return max(6.0 * max_depth, 0.001)


def base_capacity_cms(pipe: dict[str, Any]) -> float:
    physics = pipe.get("physics", {})
    diameter_m = float(physics.get("diameterM") or 0)
    if diameter_m <= 0:
        return 0.0

    area = pipe_area(diameter_m)
    link_type = str(physics.get("linkType") or "CONDUIT")
    if link_type == "ORIFICE":
        capacity = 0.65 * area * math.sqrt(2 * GRAVITY * max(diameter_m, 0.1))
    else:
        roughness = float(physics.get("roughnessN") or 0.015)
        slope = max(float(physics.get("slope") or 0.001), 0.0001)
        hydraulic_radius = diameter_m / 4
        capacity = (1 / roughness) * area * (hydraulic_radius ** (2 / 3)) * math.sqrt(slope)

    bend_loss = max(float(physics.get("bendLossK") or 0), 0.0)
    capacity = capacity / (1 + bend_loss)
    max_flow = float(physics.get("maxFlowCms") or 0)
    if max_flow > 0:
        capacity = min(capacity, max_flow)
    return max(capacity, 0.001)


def effective_capacity_cms(pipe: dict[str, Any], blockage_ratio: float, setting: float = 1.0) -> float:
    open_ratio = clamp(1 - blockage_ratio, 0.0, 1.0)
    if open_ratio <= 0:
        return 0.0
    # Capacity falls faster than the visible opening because area and hydraulic
    # radius both shrink when the pipe cross-section is obstructed.
    return base_capacity_cms(pipe) * (open_ratio ** 1.55) * clamp(setting, 0.0, 1.0)


def gate_setting_from_level(level: float) -> float:
    if level <= OVERFLOW_GATE_START_LEVEL:
        return 1.0
    if level >= OVERFLOW_GATE_CLOSED_LEVEL:
        return OVERFLOW_GATE_MIN_SETTING
    ratio = (level - OVERFLOW_GATE_START_LEVEL) / (OVERFLOW_GATE_CLOSED_LEVEL - OVERFLOW_GATE_START_LEVEL)
    return 1.0 - ratio * (1.0 - OVERFLOW_GATE_MIN_SETTING)


def has_discharge_failure(upstream_inflow_cms: float, outflow_cms: float, effective_capacity_cms: float) -> bool:
    """Return true when water is trying to enter but the link cannot release it."""
    if upstream_inflow_cms <= BACKFLOW_INFLOW_CMS:
        return False
    if effective_capacity_cms <= BACKFLOW_INFLOW_CMS:
        return True
    return outflow_cms <= BACKFLOW_INFLOW_CMS or outflow_cms < upstream_inflow_cms * DISCHARGE_FAILURE_RATIO


def should_reverse(
    fullness: float,
    upstream_inflow_cms: float,
    outflow_cms: float,
    effective_capacity_cms: float,
) -> bool:
    return (
        fullness >= BACKFLOW_FULLNESS_RATIO
        and upstream_inflow_cms > BACKFLOW_INFLOW_CMS
        and has_discharge_failure(upstream_inflow_cms, outflow_cms, effective_capacity_cms)
    )


def parse_control_payload(payload: dict[str, Any]) -> tuple[float, int, dict[str, float]]:
    rainfall = clamp(float(payload.get("rainfallRatio", payload.get("rainfall", 0)) or 0), 0, 1)
    step_sec = max(1, int(payload.get("stepSeconds", 1) or 1))
    blockages: dict[str, float] = {}

    for item in payload.get("exceptions", []) or []:
        object_id = str(item.get("id") or item.get("swmmId") or "")
        if not object_id:
            continue
        blockages[object_id] = clamp(float(item.get("blockage", item.get("blockageRatio", 0)) or 0), 0, 1)

    for object_id, item in (payload.get("blockagesById") or {}).items():
        if isinstance(item, dict):
            blockages[str(object_id)] = clamp(float(item.get("blockageRatio", item.get("blockage", 0)) or 0), 0, 1)

    return rainfall, step_sec, blockages


def parse_previous_storage(payload: dict[str, Any]) -> tuple[dict[str, float], dict[str, float]]:
    state = payload.get("state") or payload.get("previousState") or {}
    pipe_storage = {
        str(key): max(float(value or 0), 0.0)
        for key, value in (state.get("pipeStorageM3") or {}).items()
    }
    node_storage = {
        str(key): max(float(value or 0), 0.0)
        for key, value in (state.get("nodeStorageM3") or {}).items()
    }

    for pipe_id, item in (state.get("pipes") or {}).items():
        if isinstance(item, dict) and "storage_m3" in item:
            pipe_storage[str(pipe_id)] = max(float(item.get("storage_m3") or 0), 0.0)
    for node_id, item in (state.get("assets") or state.get("nodes") or {}).items():
        if isinstance(item, dict) and "storage_m3" in item:
            node_storage[str(node_id)] = max(float(item.get("storage_m3") or 0), 0.0)

    return pipe_storage, node_storage


def source_inflows(rainfall_ratio: float) -> dict[str, float]:
    # These are controllable source rates for the one-step preview. Live SWMM
    # will replace them with rain gages, subcatchment runoff, and dry-weather flow.
    return {
        "sep_catch_basin_1": rainfall_ratio * 0.16,
        "sep_catch_basin_2": rainfall_ratio * 0.18,
        "sep_storm_upstream": rainfall_ratio * 0.36,
        "sep_apartment_1": 0.040,
        "sep_apartment_2": 0.038,
        "sep_sewer_upstream": 0.070,
        "comb_catch_basin_1": rainfall_ratio * 0.15,
        "comb_catch_basin_2": rainfall_ratio * 0.17,
        "comb_house_1": 0.034,
        "comb_house_2": 0.037,
        "comb_upstream": rainfall_ratio * 0.35 + 0.050,
    }


def update_asset_state(result: StepResult, node_id: str, *, inflow: float = 0, outflow: float = 0, blockage: float = 0) -> None:
    if node_id not in result.assets:
        return
    state = result.assets[node_id]
    state.inflow_cms += max(inflow, 0)
    state.outflow_cms += max(outflow, 0)
    state.blockage_ratio = max(state.blockage_ratio, blockage)
    net = max(state.inflow_cms - state.outflow_cms, 0)
    state.depth_ratio = clamp(max(state.depth_ratio, net / 1.2), 0, 1.18)
    state.active = state.inflow_cms > 0.002 or state.depth_ratio > 0.02
    if state.depth_ratio >= 0.98:
        state.status = "surcharge"
    elif state.depth_ratio >= 0.75:
        state.status = "warning"


def run_step(control_payload: dict[str, Any]) -> dict[str, Any]:
    registry = registry_payload()
    rainfall, step_sec, blockages = parse_control_payload(control_payload)
    previous_pipe_storage, previous_node_storage = parse_previous_storage(control_payload)
    pipes = registry["pipes"]
    assets = registry["assets"]
    node_items = {
        str(item["id"]): item
        for item in [
            *registry.get("assets", []),
            *registry.get("surfaces", []),
            *registry.get("modelOnlyNodes", []),
        ]
    }

    result = StepResult(time_step_sec=step_sec, rainfall_ratio=rainfall)
    node_storage = {node_id: max(value, 0.0) for node_id, value in previous_node_storage.items()}
    pipe_storage = {pipe_id: max(value, 0.0) for pipe_id, value in previous_pipe_storage.items()}
    node_in_volume: dict[str, float] = {}
    node_out_volume: dict[str, float] = {}
    pump_setting = 0.18
    pump_active = False
    overflow_gate_setting = 1.0

    pipes_by_id = {str(pipe["id"]): pipe for pipe in pipes}
    ordered_pipe_ids = [pipe_id for pipe_id in PIPE_FLOW_ORDER if pipe_id in pipes_by_id]
    ordered_pipe_ids.extend(pipe_id for pipe_id in pipes_by_id if pipe_id not in set(ordered_pipe_ids))

    for node_id, inflow_cms in source_inflows(rainfall).items():
        volume = max(inflow_cms, 0.0) * step_sec
        node_storage[node_id] = node_storage.get(node_id, 0.0) + volume
        node_in_volume[node_id] = node_in_volume.get(node_id, 0.0) + volume

    for pipe_id in ordered_pipe_ids:
        pipe = pipes_by_id[pipe_id]
        physics = pipe.get("physics", {})
        from_node = str(physics.get("fromNode") or "")
        to_node = str(physics.get("toNode") or "")
        blockage = blockages.get(pipe_id, 0.0)
        setting = 1.0

        if pipe_id == "overflow_to_interceptor_drop":
            chamber_capacity = node_storage_capacity_m3(node_items.get("overflow_chamber", {}))
            chamber_level = clamp(node_storage.get("overflow_chamber", 0.0) / chamber_capacity, 0, 1.18)
            overflow_gate_setting = gate_setting_from_level(chamber_level)
            setting = overflow_gate_setting

        if pipe_id == "overflow_pipe":
            chamber_capacity = node_storage_capacity_m3(node_items.get("overflow_chamber", {}))
            chamber_level = clamp(node_storage.get("overflow_chamber", 0.0) / chamber_capacity, 0, 1.18)
            setting = 1.0 if chamber_level >= OVERFLOW_GATE_START_LEVEL else 0.0

        if pipe_id == "storm_pump_discharge_pipe":
            station_capacity = node_storage_capacity_m3(node_items.get("storm_pump_station", {}))
            pump_level = clamp(node_storage.get("storm_pump_station", 0.0) / station_capacity, 0, 1.18)
            pump_active = pump_level >= PUMP_ON_LEVEL
            pump_setting = 1.0 if pump_active else 0.18
            pump_volume = min(node_storage.get("storm_pump_station", 0.0), PUMP_CAPACITY_CMS * pump_setting * step_sec)
            if pump_volume > 0:
                node_storage["storm_pump_station"] = max(node_storage.get("storm_pump_station", 0.0) - pump_volume, 0.0)
                node_storage["pump_discharge_node"] = node_storage.get("pump_discharge_node", 0.0) + pump_volume
                node_out_volume["storm_pump_station"] = node_out_volume.get("storm_pump_station", 0.0) + pump_volume
                node_in_volume["pump_discharge_node"] = node_in_volume.get("pump_discharge_node", 0.0) + pump_volume

        available_volume = max(node_storage.get(from_node, 0.0), 0.0)
        capacity = base_capacity_cms(pipe)
        effective_capacity = effective_capacity_cms(pipe, blockage, setting)
        storage_capacity = pipe_storage_capacity_m3(pipe, blockage)
        current_storage = clamp(pipe_storage.get(pipe_id, 0.0), 0.0, storage_capacity)
        free_volume = max(storage_capacity - current_storage, 0.0)
        node_blockage = blockages.get(from_node, 0.0)
        node_open_ratio = clamp(1 - node_blockage, 0.0, 1.0) ** 1.55
        inlet_setting = setting if pipe_id == "overflow_pipe" else 1.0
        inlet_capacity_volume = capacity * node_open_ratio * inlet_setting * step_sec
        accepted_volume = min(available_volume, inlet_capacity_volume, free_volume)

        if accepted_volume > 0:
            node_storage[from_node] = max(node_storage.get(from_node, 0.0) - accepted_volume, 0.0)
            node_out_volume[from_node] = node_out_volume.get(from_node, 0.0) + accepted_volume
            current_storage += accepted_volume

        discharge_volume = min(current_storage, effective_capacity * step_sec)
        if discharge_volume > 0:
            current_storage = max(current_storage - discharge_volume, 0.0)
            node_storage[to_node] = node_storage.get(to_node, 0.0) + discharge_volume
            node_in_volume[to_node] = node_in_volume.get(to_node, 0.0) + discharge_volume

        pipe_storage[pipe_id] = current_storage
        fullness = clamp(current_storage / storage_capacity if storage_capacity else 0.0, 0.0, 1.18)
        waiting_upstream_cms = max(node_storage.get(from_node, 0.0), 0.0) / step_sec
        outflow = discharge_volume / step_sec
        reverse = should_reverse(fullness, waiting_upstream_cms, outflow, effective_capacity)
        direction = "reverse" if reverse else "forward"

        area = pipe_area(float(physics.get("diameterM") or 0.1)) * max(1 - blockage, 0.05)
        inflow = accepted_volume / step_sec
        velocity = outflow / max(area, 0.001)
        if blockage > 0:
            velocity *= max(0.05, 1 - blockage * 0.82)

        result.pipes[pipe_id] = PipeState(
            id=pipe_id,
            inflow_cms=inflow,
            outflow_cms=outflow,
            storage_m3=current_storage,
            storage_capacity_m3=storage_capacity,
            capacity_cms=capacity,
            effective_capacity_cms=effective_capacity,
            velocity_mps=velocity,
            fullness=fullness,
            blockage_ratio=blockage,
            direction=direction,
            active=inflow > 0.002 or outflow > 0.002 or current_storage > 0.001,
        )

    for asset in assets:
        asset_id = str(asset["id"])
        physics = asset.get("physics", {})
        if str(physics.get("nodeType") or "") == "OUTFALLS":
            released_volume = node_storage.get(asset_id, 0.0)
            if released_volume > 0:
                node_storage[asset_id] = 0.0
                node_out_volume[asset_id] = node_out_volume.get(asset_id, 0.0) + released_volume

    result.assets = {}
    for asset in assets:
        asset_id = str(asset["id"])
        storage_capacity = node_storage_capacity_m3(asset)
        storage = clamp(node_storage.get(asset_id, 0.0), 0.0, storage_capacity)
        node_storage[asset_id] = storage
        depth_ratio = clamp(storage / storage_capacity if storage_capacity else 0.0, 0.0, 1.18)
        inflow_cms = node_in_volume.get(asset_id, 0.0) / step_sec
        outflow_cms = node_out_volume.get(asset_id, 0.0) / step_sec
        active = storage > 0.001 or inflow_cms > 0.002 or outflow_cms > 0.002
        status = "normal"
        if depth_ratio >= 0.98:
            status = "surcharge"
        elif depth_ratio >= 0.75:
            status = "warning"
        result.assets[asset_id] = AssetState(
            id=asset_id,
            inflow_cms=inflow_cms,
            outflow_cms=outflow_cms,
            storage_m3=storage,
            storage_capacity_m3=storage_capacity,
            depth_ratio=depth_ratio,
            blockage_ratio=blockages.get(asset_id, 0.0),
            status=status,
            active=active,
        )

    result.controls = {
        "storm_pump_unit": {
            "active": pump_active,
            "target_setting": pump_setting,
        },
        "overflow_to_interceptor_drop": {
            "active": overflow_gate_setting > 0,
            "target_setting": overflow_gate_setting,
        },
    }
    result.next_state = {
        "pipeStorageM3": {
            pipe_id: round(storage, 6)
            for pipe_id, storage in pipe_storage.items()
            if storage > 0.000001
        },
        "nodeStorageM3": {
            node_id: round(storage, 6)
            for node_id, storage in node_storage.items()
            if storage > 0.000001
        },
    }
    return result.to_payload()


def run_steps(control_payload: dict[str, Any], steps: int) -> dict[str, Any]:
    payload = dict(control_payload)
    result: dict[str, Any] = {}
    for _ in range(max(1, steps)):
        result = run_step(payload)
        payload = {**payload, "state": result.get("state", {})}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one hydraulic preview step from a control payload.")
    parser.add_argument("--payload", help="JSON string or path to a JSON payload file.")
    parser.add_argument("--steps", type=int, default=1, help="Number of one-second steps to run while carrying internal storage state.")
    args = parser.parse_args()

    if args.payload:
        payload_path = Path(args.payload)
        if payload_path.exists():
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
        else:
            payload = json.loads(args.payload)
    else:
        payload = {"rainfallRatio": 0.7, "stepSeconds": 1, "blockagesById": {}}

    json.dump(run_steps(payload, args.steps), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
