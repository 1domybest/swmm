#!/usr/bin/env python3
"""Build SWMM design scenarios that match the HTML drainage diagram IDs.

The generated .inp files are run-ready in EPA SWMM. The CSV files are
controller-ready scenario traces produced from the same network rules so the
browser diagram can be wired before a stable local SWMM engine is available.
"""

from __future__ import annotations

import csv
import json
import math
import shutil
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from network_registry import (
    ASSET_REGISTRY,
    CONTROL_REGISTRY,
    MODEL_ONLY_NODE_REGISTRY,
    PIPE_REGISTRY,
    REGISTRY_VERSION,
    SURFACE_REGISTRY,
    asset_ids,
    pipe_ids,
    surface_ids,
    validate_registry_against_model,
    write_registry_js,
    write_registry_json,
)


ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "viewer" / "overall_drainage_diagram.html"
VIEWER_DATA_PATH = ROOT / "viewer" / "design_scenario_data.js"
VIEWER_REGISTRY_PATH = ROOT / "viewer" / "network_registry.js"
MODEL_DIR = ROOT / "models"
RESULT_DIR = ROOT / "sample-results"
REGISTRY_JSON_PATH = RESULT_DIR / "network_registry.json"
DOC_DIR = ROOT / "docs"


@dataclass(frozen=True)
class NodeSpec:
    node_id: str
    section: str
    elevation: float
    max_depth: float
    init_depth: float = 0.0
    sur_depth: float = 0.5
    ponded_area: float = 0.0
    shape: str = ""
    storage_param: float = 0.0
    x: int = 0
    y: int = 0


@dataclass(frozen=True)
class LinkSpec:
    link_id: str
    link_type: str
    from_node: str
    to_node: str
    length: float
    roughness: float
    diameter: float
    in_offset: float = 0.0
    out_offset: float = 0.0
    max_flow: float = 0.0
    size: str = "medium"
    water_type: str = "storm"


SCENARIOS = {
    "base": {
        "title": "기본 폭우",
        "description": "분류식 우수/오수와 합류식 흐름이 모두 작동하되 월류는 거의 발생하지 않는 기준 시나리오",
        "storm_peak": 0.055,
        "combined_peak": 0.035,
        "sewer_base": 0.045,
        "river_peak": 6.35,
        "backflow": False,
        "overflow_bias": 0.0,
    },
    "overflow": {
        "title": "폭우 월류",
        "description": "합류식 본관과 우수토실 수위가 높아져 유량조절판이 닫히고 월류관이 활성화되는 시나리오",
        "storm_peak": 0.075,
        "combined_peak": 0.115,
        "sewer_base": 0.055,
        "river_peak": 6.55,
        "backflow": False,
        "overflow_bias": 0.25,
    },
    "backflow": {
        "title": "하천 역류",
        "description": "하천 수위가 높아 방류구/토출관 쪽 역방향 유량 후보가 발생하는 시나리오",
        "storm_peak": 0.065,
        "combined_peak": 0.070,
        "sewer_base": 0.050,
        "river_peak": 8.25,
        "backflow": True,
        "overflow_bias": 0.10,
    },
}


NODES = [
    NodeSpec("sep_apartment_1", "JUNCTIONS", 11.30, 1.00, x=120, y=560),
    NodeSpec("sep_apartment_2", "JUNCTIONS", 11.20, 1.00, x=420, y=560),
    NodeSpec("sep_catch_basin_1", "JUNCTIONS", 11.00, 1.20, sur_depth=0.7, ponded_area=12, x=760, y=550),
    NodeSpec("sep_catch_basin_2", "JUNCTIONS", 10.90, 1.20, sur_depth=0.7, ponded_area=12, x=1120, y=550),
    NodeSpec("sep_sewer_upstream", "JUNCTIONS", 8.70, 2.00, x=130, y=300),
    NodeSpec("sep_sewer_manhole", "JUNCTIONS", 8.45, 3.60, sur_depth=1.2, ponded_area=20, x=360, y=300),
    NodeSpec("sep_sewer_downstream", "JUNCTIONS", 8.10, 2.40, x=590, y=300),
    NodeSpec("sep_interceptor_join", "JUNCTIONS", 7.55, 3.00, sur_depth=1.0, ponded_area=20, x=720, y=180),
    NodeSpec("sep_storm_upstream", "JUNCTIONS", 8.95, 2.40, x=700, y=420),
    NodeSpec("sep_storm_manhole", "JUNCTIONS", 8.65, 3.20, sur_depth=1.2, ponded_area=20, x=960, y=420),
    NodeSpec("sep_storm_downstream", "JUNCTIONS", 8.25, 2.80, x=1210, y=420),
    NodeSpec("sep_storm_trunk_inlet", "JUNCTIONS", 7.75, 3.00, x=1350, y=250),
    NodeSpec("comb_house_1", "JUNCTIONS", 11.10, 1.00, x=1580, y=560),
    NodeSpec("comb_house_2", "JUNCTIONS", 11.00, 1.00, x=1810, y=560),
    NodeSpec("comb_catch_basin_1", "JUNCTIONS", 10.90, 1.20, sur_depth=0.7, ponded_area=12, x=2050, y=550),
    NodeSpec("comb_catch_basin_2", "JUNCTIONS", 10.80, 1.20, sur_depth=0.7, ponded_area=12, x=2320, y=550),
    NodeSpec("comb_upstream", "JUNCTIONS", 8.70, 2.60, x=1880, y=395),
    NodeSpec("combined_manhole", "JUNCTIONS", 8.35, 3.50, sur_depth=1.2, ponded_area=20, x=2200, y=395),
    NodeSpec("pump_discharge_node", "JUNCTIONS", 7.15, 2.00, x=1600, y=250),
    NodeSpec("storm_pump_station", "STORAGE", 7.05, 3.30, shape="FUNCTIONAL", storage_param=90, x=1510, y=250),
    NodeSpec("overflow_chamber", "STORAGE", 7.75, 2.80, shape="FUNCTIONAL", storage_param=110, x=2650, y=390),
    NodeSpec("water_reclamation_center", "STORAGE", 6.85, 4.00, init_depth=0.15, shape="FUNCTIONAL", storage_param=360, x=2920, y=160),
    NodeSpec("overflow_outfall", "OUTFALLS", 6.25, 0.0, x=3300, y=395),
    NodeSpec("pump_outfall", "OUTFALLS", 6.20, 0.0, x=3300, y=250),
    NodeSpec("treated_outfall", "OUTFALLS", 6.05, 0.0, x=3300, y=160),
]


LINKS = [
    LinkSpec("sep_sewer_lateral_apartment_1", "CONDUIT", "sep_apartment_1", "sep_sewer_manhole", 55, 0.015, 0.45, size="small", water_type="sewer"),
    LinkSpec("sep_sewer_lateral_apartment_2", "CONDUIT", "sep_apartment_2", "sep_sewer_manhole", 55, 0.015, 0.45, size="small", water_type="sewer"),
    LinkSpec("sep_storm_lateral_catch_basin_1", "CONDUIT", "sep_catch_basin_1", "sep_storm_manhole", 42, 0.018, 0.45, size="small", water_type="storm"),
    LinkSpec("sep_storm_lateral_catch_basin_2", "CONDUIT", "sep_catch_basin_2", "sep_storm_manhole", 42, 0.018, 0.45, size="small", water_type="storm"),
    LinkSpec("sep_storm_trunk", "CONDUIT", "sep_storm_trunk_inlet", "storm_pump_station", 520, 0.015, 1.60, size="large", water_type="storm"),
    LinkSpec("sep_interceptor", "CONDUIT", "sep_interceptor_join", "water_reclamation_center", 620, 0.016, 1.60, max_flow=1.45, size="large", water_type="sewer"),
    LinkSpec("sep_storm_main_1", "CONDUIT", "sep_storm_upstream", "sep_storm_manhole", 260, 0.015, 1.20, size="medium", water_type="storm"),
    LinkSpec("sep_storm_main_2", "CONDUIT", "sep_storm_manhole", "sep_storm_downstream", 310, 0.015, 1.20, size="medium", water_type="storm"),
    LinkSpec("sep_storm_main_to_trunk", "CONDUIT", "sep_storm_downstream", "sep_storm_trunk_inlet", 120, 0.015, 1.20, size="medium", water_type="storm"),
    LinkSpec("sep_sewer_main_1", "CONDUIT", "sep_sewer_upstream", "sep_sewer_manhole", 230, 0.015, 1.05, size="medium", water_type="sewer"),
    LinkSpec("sep_sewer_main_2", "CONDUIT", "sep_sewer_manhole", "sep_sewer_downstream", 260, 0.015, 1.05, size="medium", water_type="sewer"),
    LinkSpec("sep_sewer_main_to_interceptor", "CONDUIT", "sep_sewer_downstream", "sep_interceptor_join", 110, 0.015, 1.05, size="medium", water_type="sewer"),
    LinkSpec("storm_pump_discharge_pipe", "CONDUIT", "pump_discharge_node", "pump_outfall", 240, 0.013, 1.35, size="large", water_type="storm"),
    LinkSpec("treatment_effluent_pipe", "CONDUIT", "water_reclamation_center", "treated_outfall", 360, 0.014, 1.35, max_flow=1.30, size="large", water_type="treated"),
    LinkSpec("comb_sewer_lateral_house_1", "CONDUIT", "comb_house_1", "combined_manhole", 58, 0.015, 0.45, size="small", water_type="sewer"),
    LinkSpec("comb_sewer_lateral_house_2", "CONDUIT", "comb_house_2", "combined_manhole", 58, 0.015, 0.45, size="small", water_type="sewer"),
    LinkSpec("comb_storm_lateral_catch_basin_1", "CONDUIT", "comb_catch_basin_1", "combined_manhole", 48, 0.018, 0.45, size="small", water_type="storm"),
    LinkSpec("comb_main_1", "CONDUIT", "comb_upstream", "combined_manhole", 330, 0.015, 1.20, size="medium", water_type="combined"),
    LinkSpec("comb_main_2", "CONDUIT", "combined_manhole", "overflow_chamber", 360, 0.015, 1.20, size="medium", water_type="combined"),
    LinkSpec("overflow_to_interceptor_drop", "ORIFICE", "overflow_chamber", "sep_interceptor_join", 70, 0.015, 0.95, size="medium", water_type="combined"),
    LinkSpec("overflow_pipe", "CONDUIT", "overflow_chamber", "overflow_outfall", 280, 0.016, 1.35, in_offset=1.05, size="large", water_type="overflow"),
    LinkSpec("comb_storm_lateral_catch_basin_2", "CONDUIT", "comb_catch_basin_2", "combined_manhole", 48, 0.018, 0.45, size="small", water_type="storm"),
]


PUMP_LINK = LinkSpec("storm_pump_unit", "PUMP", "storm_pump_station", "pump_discharge_node", 0, 0, 0, water_type="storm")


ASSET_MAX_DEPTH = {
    node.node_id: node.max_depth for node in NODES if node.section in {"JUNCTIONS", "STORAGE"}
}
NODE_BY_ID = {node.node_id: node for node in NODES}
LINK_BY_ID = {link.link_id: link for link in LINKS}


HYDRAULIC_RULES = {
    "pump_on_level": 0.45,
    "pump_off_level": 0.28,
    "pump_capacity_cms": 1.20,
    "overflow_gate_start_level": 0.68,
    "overflow_gate_closed_level": 0.92,
    "overflow_gate_min_setting": 0.12,
    "overflow_weir_start_level": 0.82,
    "water_reclamation_capacity_cms": 1.25,
    "river_backflow_start": 0.30,
    "warning_capacity_ratio": 0.85,
    "surcharge_capacity_ratio": 1.05,
    "blocked_backflow_fullness_ratio": 0.98,
    "blocked_backflow_inflow_cms": 0.002,
    "blocked_backflow_blockage_ratio": 0.85,
}


def extract_diagram_ids() -> tuple[list[str], list[str]]:
    return pipe_ids(), asset_ids()


def timeseries_rows(scenario: str) -> dict[str, list[tuple[str, float]]]:
    config = SCENARIOS[scenario]

    def hydrograph(peak: float, tail: float = 0.0) -> list[tuple[str, float]]:
        return [
            ("00:00", 0.00),
            ("00:20", peak * 0.10),
            ("00:40", peak * 0.45),
            ("01:00", peak * 0.82),
            ("01:15", peak),
            ("01:35", peak * 0.86),
            ("02:00", peak * 0.40),
            ("02:30", peak * 0.12),
            ("03:00", tail),
        ]

    if scenario == "backflow":
        river = [
            ("00:00", 6.10),
            ("00:45", 6.55),
            ("01:10", 7.50),
            ("01:35", config["river_peak"]),
            ("02:05", 8.05),
            ("02:35", 7.10),
            ("03:00", 6.40),
        ]
    else:
        river = [
            ("00:00", 6.00),
            ("00:50", 6.15),
            ("01:20", config["river_peak"]),
            ("02:10", 6.25),
            ("03:00", 6.05),
        ]

    return {
        "TS_STORM_RAIN": hydrograph(config["storm_peak"]),
        "TS_COMBINED_RAIN": hydrograph(config["combined_peak"]),
        "TS_SEWER_DWF": [("00:00", config["sewer_base"]), ("03:00", config["sewer_base"])],
        "TS_RIVER_STAGE": river,
    }


def build_inp(scenario: str) -> str:
    config = SCENARIOS[scenario]
    lines: list[str] = []
    add = lines.append

    add("[TITLE]")
    add(f";; Seoul design-control model - {config['title']}")
    add(";; IDs are aligned with viewer/overall_drainage_diagram.html.")
    add("")
    add("[OPTIONS]")
    add("FLOW_UNITS           CMS")
    add("INFILTRATION         HORTON")
    add("FLOW_ROUTING         DYNWAVE")
    add("LINK_OFFSETS         DEPTH")
    add("MIN_SLOPE            0")
    add("ALLOW_PONDING        YES")
    add("START_DATE           06/10/2026")
    add("START_TIME           00:00:00")
    add("REPORT_START_DATE    06/10/2026")
    add("REPORT_START_TIME    00:00:00")
    add("END_DATE             06/10/2026")
    add("END_TIME             03:00:00")
    add("REPORT_STEP          00:01:00")
    add("WET_STEP             00:01:00")
    add("DRY_STEP             00:05:00")
    add("ROUTING_STEP         00:00:15")
    add("VARIABLE_STEP        0.75")
    add("NORMAL_FLOW_LIMITED  BOTH")
    add("INERTIAL_DAMPING     PARTIAL")
    add("SURCHARGE_METHOD     SLOT")
    add("")
    add("[EVAPORATION]")
    add("CONSTANT             0.0")
    add("")
    add("[JUNCTIONS]")
    add(";;Name                         Elev     MaxDepth InitDepth SurDepth Aponded")
    for node in NODES:
        if node.section == "JUNCTIONS":
            add(f"{node.node_id:<30} {node.elevation:<8.2f} {node.max_depth:<8.2f} {node.init_depth:<9.2f} {node.sur_depth:<8.2f} {node.ponded_area:.1f}")
    add("")
    add("[STORAGE]")
    add(";;Name                         Elev     MaxDepth InitDepth Shape      Curve/Params          N/A  Fevap Psi Ksat IMD")
    for node in NODES:
        if node.section == "STORAGE":
            add(f"{node.node_id:<30} {node.elevation:<8.2f} {node.max_depth:<8.2f} {node.init_depth:<9.2f} {node.shape:<10} {node.storage_param:<7.1f} 0      0      0    0")
    add("")
    add("[OUTFALLS]")
    add(";;Name                         Elev     Type       Stage Data       Gated")
    for node in NODES:
        if node.section == "OUTFALLS":
            add(f"{node.node_id:<30} {node.elevation:<8.2f} TIMESERIES TS_RIVER_STAGE    YES")
    add("")
    add("[CONDUITS]")
    add(";;Name                         From Node                    To Node                      Length Roughness InOffset OutOffset InitFlow MaxFlow")
    for link in LINKS:
        if link.link_type == "CONDUIT":
            add(f"{link.link_id:<30} {link.from_node:<28} {link.to_node:<28} {link.length:<6.1f} {link.roughness:<9.3f} {link.in_offset:<8.2f} {link.out_offset:<9.2f} 0        {link.max_flow:.2f}")
    add("")
    add("[ORIFICES]")
    add(";;Name                         From Node                    To Node                      Type   Offset Qcoeff Gated CloseTime")
    for link in LINKS:
        if link.link_type == "ORIFICE":
            add(f"{link.link_id:<30} {link.from_node:<28} {link.to_node:<28} SIDE   0.00   0.65   NO    0")
    add("")
    add("[PUMPS]")
    add(";;Name                         From Node                    To Node                      Pump Curve     Status Startup Shutoff")
    add(f"{PUMP_LINK.link_id:<30} {PUMP_LINK.from_node:<28} {PUMP_LINK.to_node:<28} PUMP_CURVE     OFF    0.75    0.25")
    add("")
    add("[XSECTIONS]")
    add(";;Link                         Shape      Geom1 Geom2 Geom3 Geom4 Barrels Culvert")
    for link in LINKS:
        if link.link_type == "CONDUIT":
            add(f"{link.link_id:<30} CIRCULAR   {link.diameter:<5.2f} 0     0     0     1")
    for link in LINKS:
        if link.link_type == "ORIFICE":
            add(f"{link.link_id:<30} RECT_CLOSED {link.diameter:<5.2f} {link.diameter:<5.2f} 0     0     1")
    add("")
    add("[CURVES]")
    add(";;Name           Type       X-Value  Y-Value")
    add("PUMP_CURVE       PUMP4      0.00     0.00")
    add("PUMP_CURVE                  0.70     0.35")
    add("PUMP_CURVE                  1.20     0.70")
    add("PUMP_CURVE                  2.00     1.15")
    add("PUMP_CURVE                  3.00     1.45")
    add("")
    add("[INFLOWS]")
    add(";;Node                         Constituent Time Series       Type   Mfactor Sfactor Baseline Pattern")
    for node_id, factor in [
        ("sep_storm_upstream", 1.20),
        ("sep_catch_basin_1", 0.95),
        ("sep_catch_basin_2", 1.05),
        ("comb_upstream", 1.05),
        ("comb_catch_basin_1", 0.95),
        ("comb_catch_basin_2", 1.10),
    ]:
        series = "TS_STORM_RAIN" if node_id.startswith("sep_") else "TS_COMBINED_RAIN"
        add(f"{node_id:<30} FLOW        {series:<17} FLOW   {factor:<7.2f} 1.00    0")
    for node_id, factor in [
        ("sep_sewer_upstream", 1.15),
        ("sep_apartment_1", 1.00),
        ("sep_apartment_2", 0.95),
        ("comb_house_1", 0.90),
        ("comb_house_2", 1.00),
        ("comb_upstream", 0.50),
    ]:
        add(f"{node_id:<30} FLOW        TS_SEWER_DWF      FLOW   {factor:<7.2f} 1.00    0")
    add("")
    add("[TIMESERIES]")
    add(";;Name                         Time      Value")
    for name, rows in timeseries_rows(scenario).items():
        for time, value in rows:
            add(f"{name:<30} {time:<8} {value:.4f}")
    add("")
    add("[CONTROLS]")
    add("RULE PUMP_ON")
    add("IF NODE storm_pump_station DEPTH > 0.75")
    add("THEN PUMP storm_pump_unit STATUS = ON")
    add("PRIORITY 2")
    add("")
    add("RULE PUMP_OFF")
    add("IF NODE storm_pump_station DEPTH < 0.25")
    add("THEN PUMP storm_pump_unit STATUS = OFF")
    add("PRIORITY 2")
    add("")
    add("RULE NORMAL_GATE_CLOSE_FOR_OVERFLOW")
    add("IF NODE overflow_chamber DEPTH > 1.05")
    add("THEN ORIFICE overflow_to_interceptor_drop SETTING = 0.15")
    add("PRIORITY 3")
    add("")
    add("RULE NORMAL_GATE_OPEN")
    add("IF NODE overflow_chamber DEPTH < 0.70")
    add("THEN ORIFICE overflow_to_interceptor_drop SETTING = 1.00")
    add("PRIORITY 3")
    add("")
    add("[REPORT]")
    add("INPUT      NO")
    add("CONTROLS   YES")
    add("NODES ALL")
    add("LINKS ALL")
    add("")
    add("[MAP]")
    add("DIMENSIONS 0 0 3500 650")
    add("Units      Meters")
    add("")
    add("[COORDINATES]")
    add(";;Node                         X-Coord          Y-Coord")
    for node in NODES:
        add(f"{node.node_id:<30} {node.x:<16} {node.y}")
    add("")
    add("[VERTICES]")
    add(";;Link                         X-Coord          Y-Coord")
    add("sep_storm_main_to_trunk        1260             330")
    add("sep_sewer_main_to_interceptor  650              230")
    add("overflow_to_interceptor_drop   2620             210")
    add("")
    add("[TAGS]")
    add("")
    add("[END]")
    return "\n".join(lines) + "\n"


def parse_inp_objects(inp_text: str) -> dict[str, set[str]]:
    sections: dict[str, set[str]] = {}
    current = ""
    for raw_line in inp_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";;") or line.startswith(";"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current = line.strip("[]")
            sections.setdefault(current, set())
            continue
        if current:
            sections.setdefault(current, set()).add(line.split()[0])
    return sections


def scenario_profile(minute: int) -> float:
    points = [(0, 0.0), (20, 0.10), (40, 0.45), (60, 0.82), (75, 1.0), (95, 0.86), (120, 0.40), (150, 0.12), (180, 0.0)]
    for (m1, v1), (m2, v2) in zip(points, points[1:]):
        if m1 <= minute <= m2:
            ratio = (minute - m1) / (m2 - m1)
            return v1 + (v2 - v1) * ratio
    return 0.0


def scenario_backflow_profile(minute: int) -> float:
    if minute < 60:
        return 0.0
    if minute <= 95:
        return (minute - 60) / 35
    if minute <= 125:
        return 1.0
    if minute <= 160:
        return 1 - (minute - 125) / 35
    return 0.0


def clamp(value: float, minimum: float, maximum: float) -> float:
    return min(maximum, max(minimum, value))


def link_area(link: LinkSpec) -> float:
    return math.pi * (link.diameter / 2) ** 2


def link_capacity(link: LinkSpec, setting: float = 1.0) -> float:
    if link.link_type == "PUMP":
        return HYDRAULIC_RULES["pump_capacity_cms"] * setting

    area = link_area(link)
    if link.link_type == "ORIFICE":
        capacity = 0.65 * area * math.sqrt(2 * 9.81 * max(link.diameter, 0.1))
    else:
        from_node = NODE_BY_ID.get(link.from_node)
        to_node = NODE_BY_ID.get(link.to_node)
        slope = 0.001
        if from_node and to_node and link.length > 0:
            slope = max((from_node.elevation - to_node.elevation) / link.length, 0.0007)
        hydraulic_radius = link.diameter / 4
        capacity = (1 / link.roughness) * area * (hydraulic_radius ** (2 / 3)) * math.sqrt(slope)

    if link.max_flow > 0:
        capacity = min(capacity, link.max_flow)
    return max(0.001, capacity * setting)


def fullness_from_capacity_ratio(capacity_ratio: float, idle_level: float = 0.03) -> float:
    if capacity_ratio <= 0:
        return 0.0
    level = idle_level + 0.88 * (min(capacity_ratio, 1.0) ** 0.58)
    if capacity_ratio > 1.0:
        level += min(0.24, (capacity_ratio - 1.0) * 0.28)
    return clamp(level, 0.0, 1.18)


def risk_from_ratio(capacity_ratio: float, backflow: bool, fallback: str = "normal") -> str:
    if backflow:
        return "backflow"
    if fallback != "normal":
        return fallback
    if capacity_ratio >= HYDRAULIC_RULES["surcharge_capacity_ratio"]:
        return "surcharge_risk"
    if capacity_ratio >= HYDRAULIC_RULES["warning_capacity_ratio"]:
        return "warning"
    return "normal"


def should_trigger_blocked_backflow(fullness_ratio: float, upstream_inflow_cms: float, blockage_ratio: float) -> bool:
    """A blockage creates reverse pressure only after the link is full and upstream inflow continues."""
    return (
        blockage_ratio >= HYDRAULIC_RULES["blocked_backflow_blockage_ratio"]
        and fullness_ratio >= HYDRAULIC_RULES["blocked_backflow_fullness_ratio"]
        and upstream_inflow_cms > HYDRAULIC_RULES["blocked_backflow_inflow_cms"]
    )


def gate_setting_from_chamber_level(chamber_level: float) -> float:
    start = HYDRAULIC_RULES["overflow_gate_start_level"]
    closed = HYDRAULIC_RULES["overflow_gate_closed_level"]
    minimum = HYDRAULIC_RULES["overflow_gate_min_setting"]
    if chamber_level <= start:
        return 1.0
    if chamber_level >= closed:
        return minimum
    ratio = (chamber_level - start) / (closed - start)
    return 1.0 - ratio * (1.0 - minimum)


def make_pipe_measurement(
    pipe_id: str,
    flow: float,
    *,
    setting: float = 1.0,
    backflow: bool = False,
    risk_hint: str = "normal",
) -> dict[str, float | bool | str]:
    link = LINK_BY_ID[pipe_id]
    capacity = link_capacity(link, setting)
    capacity_ratio = abs(flow) / capacity if capacity else 0.0
    level = fullness_from_capacity_ratio(capacity_ratio)
    if pipe_id == "overflow_pipe" and abs(flow) < 0.001:
        level = 0.0

    wet_area = max(link_area(link) * max(level, 0.08), 0.001)
    velocity = flow / wet_area
    velocity = clamp(velocity, -4.5, 4.5)
    risk = risk_from_ratio(capacity_ratio, backflow, risk_hint)

    return {
        "level": level,
        "flow": flow,
        "velocity": velocity,
        "capacity": capacity,
        "capacity_ratio": capacity_ratio,
        "backflow": backflow,
        "risk": risk,
        "setting": setting,
        "status": risk if risk != "normal" else "active" if abs(flow) > 0.002 else "idle",
    }


def make_asset_measurement(
    asset_id: str,
    water_level: float,
    flow: float,
    *,
    backflow: bool = False,
    risk_hint: str = "normal",
    active: bool = True,
    setting: float = 1.0,
) -> dict[str, float | bool | str]:
    level = clamp(water_level, 0.0, 1.18)
    risk = risk_from_ratio(level, backflow, risk_hint)
    return {
        "level": level,
        "flow": flow,
        "velocity": 0.0,
        "capacity": 0.0,
        "capacity_ratio": level,
        "backflow": backflow,
        "risk": risk,
        "active": active,
        "setting": setting,
        "status": risk if risk != "normal" else "active" if active else "idle",
    }


def routed_network_state(scenario: str, minute: int) -> tuple[dict[str, dict[str, float | bool | str]], dict[str, dict[str, float | bool | str]]]:
    config = SCENARIOS[scenario]
    rain = scenario_profile(minute)
    backflow_pressure = scenario_backflow_profile(minute) if scenario == "backflow" else 0.0
    diurnal = 0.92 + 0.08 * math.sin((minute / 180) * math.pi)

    storm_peak = config["storm_peak"]
    combined_peak = config["combined_peak"]
    sewer_base = config["sewer_base"] * diurnal

    sep_storm_upstream = storm_peak * rain * 8.8
    sep_catch_1 = storm_peak * rain * 2.15
    sep_catch_2 = storm_peak * rain * 2.35
    sep_storm_total = sep_storm_upstream + sep_catch_1 + sep_catch_2

    sep_sewer_upstream = sewer_base * 2.25
    sep_apartment_1 = sewer_base * 0.95
    sep_apartment_2 = sewer_base * 0.90
    sep_sewer_total = sep_sewer_upstream + sep_apartment_1 + sep_apartment_2

    combined_rain_scale = 11.0 if scenario == "overflow" else 7.2
    comb_upstream_storm = combined_peak * rain * combined_rain_scale
    comb_upstream_sewer = sewer_base * 0.95
    comb_house_1 = sewer_base * 0.78
    comb_house_2 = sewer_base * 0.86
    comb_catch_1 = combined_peak * rain * 1.85
    comb_catch_2 = combined_peak * rain * 2.05
    comb_total = comb_upstream_storm + comb_upstream_sewer + comb_house_1 + comb_house_2 + comb_catch_1 + comb_catch_2

    pipe_measurements: dict[str, dict[str, float | bool | str]] = {}

    pipe_measurements["sep_storm_lateral_catch_basin_1"] = make_pipe_measurement("sep_storm_lateral_catch_basin_1", sep_catch_1)
    pipe_measurements["sep_storm_lateral_catch_basin_2"] = make_pipe_measurement("sep_storm_lateral_catch_basin_2", sep_catch_2)
    pipe_measurements["sep_storm_main_1"] = make_pipe_measurement("sep_storm_main_1", sep_storm_upstream)
    pipe_measurements["sep_storm_main_2"] = make_pipe_measurement("sep_storm_main_2", sep_storm_total)
    pipe_measurements["sep_storm_main_to_trunk"] = make_pipe_measurement("sep_storm_main_to_trunk", sep_storm_total)
    pipe_measurements["sep_storm_trunk"] = make_pipe_measurement("sep_storm_trunk", sep_storm_total)

    pump_station_level = max(
        pipe_measurements["sep_storm_trunk"]["capacity_ratio"] * 0.72,
        sep_storm_total / HYDRAULIC_RULES["pump_capacity_cms"] * 0.78,
    )
    pump_active = pump_station_level >= HYDRAULIC_RULES["pump_on_level"]
    pump_capacity = HYDRAULIC_RULES["pump_capacity_cms"] if pump_active else HYDRAULIC_RULES["pump_capacity_cms"] * 0.18
    pump_discharge = min(sep_storm_total, pump_capacity)
    pump_backflow = scenario == "backflow" and backflow_pressure >= HYDRAULIC_RULES["river_backflow_start"]
    if pump_backflow:
        pump_discharge = -max(pump_discharge * 0.28, link_capacity(LINK_BY_ID["storm_pump_discharge_pipe"]) * backflow_pressure * 0.12)
    pipe_measurements["storm_pump_discharge_pipe"] = make_pipe_measurement(
        "storm_pump_discharge_pipe",
        pump_discharge,
        backflow=pump_backflow,
        risk_hint="pump_active" if pump_active and not pump_backflow else "normal",
    )

    pipe_measurements["sep_sewer_lateral_apartment_1"] = make_pipe_measurement("sep_sewer_lateral_apartment_1", sep_apartment_1)
    pipe_measurements["sep_sewer_lateral_apartment_2"] = make_pipe_measurement("sep_sewer_lateral_apartment_2", sep_apartment_2)
    pipe_measurements["sep_sewer_main_1"] = make_pipe_measurement("sep_sewer_main_1", sep_sewer_upstream)
    pipe_measurements["sep_sewer_main_2"] = make_pipe_measurement("sep_sewer_main_2", sep_sewer_total)
    pipe_measurements["sep_sewer_main_to_interceptor"] = make_pipe_measurement("sep_sewer_main_to_interceptor", sep_sewer_total)

    pipe_measurements["comb_sewer_lateral_house_1"] = make_pipe_measurement("comb_sewer_lateral_house_1", comb_house_1)
    pipe_measurements["comb_sewer_lateral_house_2"] = make_pipe_measurement("comb_sewer_lateral_house_2", comb_house_2)
    pipe_measurements["comb_storm_lateral_catch_basin_1"] = make_pipe_measurement("comb_storm_lateral_catch_basin_1", comb_catch_1)
    pipe_measurements["comb_storm_lateral_catch_basin_2"] = make_pipe_measurement("comb_storm_lateral_catch_basin_2", comb_catch_2)
    pipe_measurements["comb_main_1"] = make_pipe_measurement("comb_main_1", comb_upstream_storm + comb_upstream_sewer)
    pipe_measurements["comb_main_2"] = make_pipe_measurement("comb_main_2", comb_total)

    chamber_level = max(pipe_measurements["comb_main_2"]["capacity_ratio"] * 0.88, rain * 0.52)
    gate_setting = gate_setting_from_chamber_level(chamber_level)
    drop_capacity = link_capacity(LINK_BY_ID["overflow_to_interceptor_drop"], gate_setting)
    normal_drop = min(comb_total, drop_capacity)
    overflow_flow = max(0.0, comb_total - normal_drop)
    if chamber_level < HYDRAULIC_RULES["overflow_weir_start_level"]:
        overflow_flow *= 0.18

    pipe_measurements["overflow_to_interceptor_drop"] = make_pipe_measurement(
        "overflow_to_interceptor_drop",
        normal_drop,
        setting=gate_setting,
        risk_hint="gate_closing" if gate_setting < 0.65 else "normal",
    )
    overflow_backflow = scenario == "backflow" and backflow_pressure >= HYDRAULIC_RULES["river_backflow_start"]
    if overflow_backflow:
        overflow_flow = -max(overflow_flow * 0.35, link_capacity(LINK_BY_ID["overflow_pipe"]) * backflow_pressure * 0.10)
    pipe_measurements["overflow_pipe"] = make_pipe_measurement(
        "overflow_pipe",
        overflow_flow,
        backflow=overflow_backflow,
        risk_hint="overflow_active" if overflow_flow > 0.01 and not overflow_backflow else "normal",
    )

    interceptor_flow = sep_sewer_total + max(normal_drop, 0)
    pipe_measurements["sep_interceptor"] = make_pipe_measurement("sep_interceptor", interceptor_flow)
    treatment_capacity = HYDRAULIC_RULES["water_reclamation_capacity_cms"]
    treatment_effluent = min(interceptor_flow, treatment_capacity)
    treatment_backflow = scenario == "backflow" and backflow_pressure >= HYDRAULIC_RULES["river_backflow_start"]
    if treatment_backflow:
        treatment_effluent = -max(treatment_effluent * 0.20, link_capacity(LINK_BY_ID["treatment_effluent_pipe"]) * backflow_pressure * 0.08)
    pipe_measurements["treatment_effluent_pipe"] = make_pipe_measurement(
        "treatment_effluent_pipe",
        treatment_effluent,
        backflow=treatment_backflow,
        risk_hint="treatment_over_capacity" if interceptor_flow > treatment_capacity and not treatment_backflow else "normal",
    )

    asset_measurements = {
        "sep_catch_basin_1": make_asset_measurement(
            "sep_catch_basin_1",
            pipe_measurements["sep_storm_lateral_catch_basin_1"]["capacity_ratio"] * 0.82,
            sep_catch_1,
        ),
        "sep_catch_basin_2": make_asset_measurement(
            "sep_catch_basin_2",
            pipe_measurements["sep_storm_lateral_catch_basin_2"]["capacity_ratio"] * 0.82,
            sep_catch_2,
        ),
        "comb_catch_basin_1": make_asset_measurement(
            "comb_catch_basin_1",
            pipe_measurements["comb_storm_lateral_catch_basin_1"]["capacity_ratio"] * 0.82,
            comb_catch_1,
        ),
        "comb_catch_basin_2": make_asset_measurement(
            "comb_catch_basin_2",
            pipe_measurements["comb_storm_lateral_catch_basin_2"]["capacity_ratio"] * 0.82,
            comb_catch_2,
        ),
        "sep_storm_manhole": make_asset_measurement(
            "sep_storm_manhole",
            max(pipe_measurements["sep_storm_main_1"]["capacity_ratio"], pipe_measurements["sep_storm_main_2"]["capacity_ratio"]) * 0.88,
            sep_storm_total,
        ),
        "sep_sewer_manhole": make_asset_measurement(
            "sep_sewer_manhole",
            max(pipe_measurements["sep_sewer_main_1"]["capacity_ratio"], pipe_measurements["sep_sewer_main_2"]["capacity_ratio"]) * 0.88,
            sep_sewer_total,
        ),
        "combined_manhole": make_asset_measurement(
            "combined_manhole",
            max(pipe_measurements["comb_main_1"]["capacity_ratio"], pipe_measurements["comb_main_2"]["capacity_ratio"]) * 0.88,
            comb_total,
        ),
        "storm_pump_station": make_asset_measurement(
            "storm_pump_station",
            pump_station_level,
            pump_discharge,
            backflow=pump_backflow,
            risk_hint="pump_active" if pump_active and not pump_backflow else "normal",
            active=pump_active,
        ),
        "overflow_chamber": make_asset_measurement(
            "overflow_chamber",
            chamber_level,
            comb_total,
            backflow=overflow_backflow,
            risk_hint="overflow_gate_active" if gate_setting < 0.65 and not overflow_backflow else "normal",
            setting=gate_setting,
        ),
        "water_reclamation_center": make_asset_measurement(
            "water_reclamation_center",
            interceptor_flow / treatment_capacity * 0.76,
            treatment_effluent,
            backflow=treatment_backflow,
            risk_hint="treatment_over_capacity" if interceptor_flow > treatment_capacity and not treatment_backflow else "normal",
        ),
        "overflow_outfall": make_asset_measurement(
            "overflow_outfall",
            abs(overflow_flow) / max(link_capacity(LINK_BY_ID["overflow_pipe"]), 0.001),
            overflow_flow,
            backflow=overflow_backflow,
        ),
        "pump_outfall": make_asset_measurement(
            "pump_outfall",
            abs(pump_discharge) / max(link_capacity(LINK_BY_ID["storm_pump_discharge_pipe"]), 0.001),
            pump_discharge,
            backflow=pump_backflow,
        ),
        "treated_outfall": make_asset_measurement(
            "treated_outfall",
            abs(treatment_effluent) / max(link_capacity(LINK_BY_ID["treatment_effluent_pipe"]), 0.001),
            treatment_effluent,
            backflow=treatment_backflow,
        ),
    }

    return pipe_measurements, asset_measurements


def generate_controller_data(pipe_ids: list[str], asset_ids: list[str]) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    summary: dict[tuple[str, str, str], dict[str, float | str]] = {}
    events: list[dict[str, str]] = []
    start = datetime(2026, 6, 10, 0, 0)

    for scenario in SCENARIOS:
        for minute in range(0, 181):
            time = (start + timedelta(minutes=minute)).isoformat()
            pipe_measurements, asset_measurements = routed_network_state(scenario, minute)

            for pipe_id in pipe_ids:
                link = LINK_BY_ID[pipe_id]
                measurement = pipe_measurements[pipe_id]
                level = float(measurement["level"])
                row = {
                    "scenario": scenario,
                    "time": time,
                    "object_type": "pipe",
                    "id": pipe_id,
                    "swmm_id": pipe_id,
                    "depth_m": f"{level * link.diameter:.4f}",
                    "flow_cms": f"{float(measurement['flow']):.4f}",
                    "velocity_mps": f"{float(measurement['velocity']):.4f}",
                    "water_level": f"{level:.4f}",
                    "fullness_ratio": f"{level:.4f}",
                    "capacity_cms": f"{float(measurement['capacity']):.4f}",
                    "capacity_ratio": f"{float(measurement['capacity_ratio']):.4f}",
                    "control_setting": f"{float(measurement['setting']):.4f}",
                    "backflow": str(bool(measurement["backflow"])).lower(),
                    "active": str(abs(float(measurement["flow"])) > 0.002).lower(),
                    "status": str(measurement["status"]),
                    "risk": str(measurement["risk"]),
                }
                rows.append(row)
                update_summary(summary, row)
                if row["risk"] != "normal":
                    events.append(event_from_row(row))

            for asset_id in asset_ids:
                measurement = asset_measurements[asset_id]
                level = float(measurement["level"])
                max_depth = ASSET_MAX_DEPTH.get(asset_id, 1.0)
                row = {
                    "scenario": scenario,
                    "time": time,
                    "object_type": "asset",
                    "id": asset_id,
                    "swmm_id": asset_id,
                    "depth_m": f"{level * max_depth:.4f}",
                    "flow_cms": f"{float(measurement['flow']):.4f}",
                    "velocity_mps": "",
                    "water_level": f"{level:.4f}",
                    "fullness_ratio": f"{level:.4f}",
                    "capacity_cms": f"{float(measurement['capacity']):.4f}",
                    "capacity_ratio": f"{float(measurement['capacity_ratio']):.4f}",
                    "control_setting": f"{float(measurement['setting']):.4f}",
                    "backflow": str(bool(measurement["backflow"])).lower(),
                    "active": str(bool(measurement["active"])).lower(),
                    "status": str(measurement["status"]),
                    "risk": str(measurement["risk"]),
                }
                rows.append(row)
                update_summary(summary, row)
                if row["risk"] != "normal":
                    events.append(event_from_row(row))

    return rows, list(summary.values()), events


def update_summary(summary: dict[tuple[str, str, str], dict[str, float | str]], row: dict[str, str]) -> None:
    key = (row["scenario"], row["object_type"], row["id"])
    depth = float(row["depth_m"] or 0)
    flow = float(row["flow_cms"] or 0)
    velocity = float(row["velocity_mps"] or 0)
    fullness = float(row["fullness_ratio"] or 0)
    capacity_ratio = float(row.get("capacity_ratio") or 0)
    if key not in summary:
        summary[key] = {
            "scenario": row["scenario"],
            "object_type": row["object_type"],
            "id": row["id"],
            "max_depth_m": depth,
            "max_flow_cms": flow,
            "min_flow_cms": flow,
            "max_velocity_mps": velocity,
            "max_abs_velocity_mps": abs(velocity),
            "max_fullness_ratio": fullness,
            "max_capacity_ratio": capacity_ratio,
            "backflow_count": 1 if row["backflow"] == "true" else 0,
        }
        return
    item = summary[key]
    item["max_depth_m"] = max(float(item["max_depth_m"]), depth)
    item["max_flow_cms"] = max(float(item["max_flow_cms"]), flow)
    item["min_flow_cms"] = min(float(item["min_flow_cms"]), flow)
    item["max_velocity_mps"] = max(float(item["max_velocity_mps"]), velocity)
    item["max_abs_velocity_mps"] = max(float(item["max_abs_velocity_mps"]), abs(velocity))
    item["max_fullness_ratio"] = max(float(item["max_fullness_ratio"]), fullness)
    item["max_capacity_ratio"] = max(float(item["max_capacity_ratio"]), capacity_ratio)
    item["backflow_count"] = int(item["backflow_count"]) + (1 if row["backflow"] == "true" else 0)


def event_from_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "scenario": row["scenario"],
        "time": row["time"],
        "object_type": row["object_type"],
        "id": row["id"],
        "risk": row["risk"],
        "water_level": row["water_level"],
        "flow_cms": row["flow_cms"],
        "capacity_ratio": row.get("capacity_ratio", ""),
        "control_setting": row.get("control_setting", ""),
        "backflow": row["backflow"],
    }


def write_csv(path: Path, rows: list[dict[str, str | float | int]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def bool_from_csv(value: str) -> bool:
    return str(value).lower() == "true"


def round_float(value: str, digits: int = 4) -> float:
    if value == "":
        return 0.0
    return round(float(value), digits)


def viewer_velocity(value: str) -> float:
    velocity = abs(round_float(value))
    return round(clamp(velocity, 0.2, 4.0), 3)


def viewer_flow_rate(row: dict[str, str]) -> float:
    capacity_ratio = round_float(row.get("capacity_ratio", "0"))
    fullness = round_float(row.get("fullness_ratio", "0"))
    return round(clamp(max(capacity_ratio, fullness), 0.0, 1.5), 3)


def build_viewer_playback_data(rows: list[dict[str, str]]) -> dict[str, object]:
    grouped: dict[tuple[str, str], dict[str, dict[str, dict[str, object]]]] = {}

    for row in rows:
        frame = grouped.setdefault((row["scenario"], row["time"]), {"pipes": {}, "assets": {}})
        if row["object_type"] == "pipe":
            frame["pipes"][row["id"]] = {
                "v": viewer_velocity(row["velocity_mps"]),
                "f": viewer_flow_rate(row),
                "l": round(clamp(round_float(row["fullness_ratio"]), 0.0, 1.0), 3),
                "q": round_float(row["flow_cms"]),
                "c": round_float(row["capacity_ratio"]),
                "g": round_float(row["control_setting"]),
                "b": bool_from_csv(row["backflow"]),
                "a": bool_from_csv(row["active"]),
                "r": row["risk"],
                "s": row["status"],
            }
        elif row["object_type"] == "asset":
            frame["assets"][row["id"]] = {
                "l": round(clamp(round_float(row["water_level"]), 0.0, 1.0), 3),
                "f": viewer_flow_rate(row),
                "q": round_float(row["flow_cms"]),
                "c": round_float(row["capacity_ratio"]),
                "g": round_float(row["control_setting"]),
                "b": bool_from_csv(row["backflow"]),
                "a": bool_from_csv(row["active"]),
                "r": row["risk"],
                "s": row["status"],
            }

    scenarios: dict[str, dict[str, object]] = {}
    for scenario, config in SCENARIOS.items():
        times = sorted(time for current_scenario, time in grouped if current_scenario == scenario)
        frames = []
        for time in times:
            frame = grouped[(scenario, time)]
            frames.append({
                "time": time,
                "pipes": frame["pipes"],
                "assets": frame["assets"],
            })
        scenarios[scenario] = {
            "title": config["title"],
            "description": config["description"],
            "frames": frames,
        }

    return {
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "registryVersion": REGISTRY_VERSION,
        "frameMinutes": 1,
        "scenarioOrder": list(SCENARIOS.keys()),
        "scenarios": scenarios,
    }


def write_viewer_playback_data(rows: list[dict[str, str]]) -> None:
    data = build_viewer_playback_data(rows)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    VIEWER_DATA_PATH.write_text(
        "window.DESIGN_SCENARIO_DATA = " + payload + ";\n",
        encoding="utf-8",
    )


def validate(inp_text: str) -> tuple[bool, list[str]]:
    sections = parse_inp_objects(inp_text)
    swmm_links = set().union(
        sections.get("CONDUITS", set()),
        sections.get("ORIFICES", set()),
        sections.get("WEIRS", set()),
        sections.get("PUMPS", set()),
    )
    swmm_nodes = set().union(
        sections.get("JUNCTIONS", set()),
        sections.get("STORAGE", set()),
        sections.get("OUTFALLS", set()),
    )
    errors = validate_registry_against_model(swmm_links=swmm_links, swmm_nodes=swmm_nodes)
    return not errors, errors


def count_events(events: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {scenario: {} for scenario in SCENARIOS}
    for event in events:
        scenario = event["scenario"]
        risk = event["risk"]
        counts.setdefault(scenario, {})
        counts[scenario][risk] = counts[scenario].get(risk, 0) + 1
    return counts


def format_event_counts(event_counts: dict[str, dict[str, int]], scenario: str) -> str:
    counts = event_counts.get(scenario, {})
    if not counts:
        return "이벤트 없음"
    return ", ".join(f"{risk} {count}건" for risk, count in sorted(counts.items()))


def build_windows_runner(scenario: str) -> str:
    title = SCENARIOS[scenario]["title"]
    model_name = f"seoul_design_{scenario}"
    text = f"""@echo off
setlocal

set "ROOT=%~dp0"
set "MODEL=%ROOT%models\\{model_name}.inp"
set "OUTDIR=%ROOT%run-results"
set "RPT=%OUTDIR%\\{model_name}.rpt"
set "OUT=%OUTDIR%\\{model_name}.out"

if not exist "%OUTDIR%" mkdir "%OUTDIR%"

call :find_swmm
if "%SWMM_EXE%"=="" (
  echo EPA SWMM command-line executable was not found.
  echo.
  echo Install EPA SWMM 5.2, then run this file again.
  echo If runswmm.exe is installed in a custom folder, add that folder to PATH.
  echo.
  pause
  exit /b 1
)

echo Running {title} scenario...
echo Model: %MODEL%
echo SWMM : %SWMM_EXE%
echo.
"%SWMM_EXE%" "%MODEL%" "%RPT%" "%OUT%"
echo.
echo Done.
echo Report: %RPT%
echo Output: %OUT%
echo.
pause
exit /b 0

:find_swmm
set "SWMM_EXE="
where runswmm.exe >nul 2>nul
if not errorlevel 1 (
  for /f "delims=" %%P in ('where runswmm.exe') do (
    set "SWMM_EXE=%%P"
    exit /b 0
  )
)
for %%P in (
  "C:\\Program Files\\EPA SWMM 5.2.4\\runswmm.exe"
  "C:\\Program Files\\EPA SWMM 5.2.3\\runswmm.exe"
  "C:\\Program Files\\EPA SWMM 5.2.2\\runswmm.exe"
  "C:\\Program Files\\EPA SWMM 5.2.1\\runswmm.exe"
  "C:\\Program Files\\EPA SWMM 5.2.0\\runswmm.exe"
  "C:\\Program Files (x86)\\EPA SWMM 5.2.4\\runswmm.exe"
  "C:\\Program Files (x86)\\EPA SWMM 5.2.3\\runswmm.exe"
  "C:\\Program Files (x86)\\EPA SWMM 5.2.2\\runswmm.exe"
  "C:\\Program Files (x86)\\EPA SWMM 5.2.1\\runswmm.exe"
  "C:\\Program Files (x86)\\EPA SWMM 5.2.0\\runswmm.exe"
) do (
  if exist "%%~P" (
    set "SWMM_EXE=%%~P"
    exit /b 0
  )
)
exit /b 0
"""
    return text.replace("\n", "\r\n")


def build_report(
    pipe_ids: list[str],
    asset_ids: list[str],
    scenario_results: dict[str, tuple[bool, list[str]]],
    event_counts: dict[str, dict[str, int]],
    swmm_cli: str | None,
) -> str:
    lines = [
        "# 설계 배수도 SWMM 모델 검증",
        "",
        "## 기준",
        "",
        f"- registry 버전: `{REGISTRY_VERSION}`",
        f"- 공통 registry 배관 ID 수: {len(pipe_ids)}",
        f"- 공통 registry 시설 ID 수: {len(asset_ids)}",
        f"- 공통 registry 지상 유입 객체 ID 수: {len(surface_ids())}",
        "- 원칙: registry의 `pipe.id`와 `pipe.swmmId`는 SWMM 링크 ID와 동일하게 둔다.",
        "- 원칙: registry의 `asset.id`와 `asset.swmmId`는 SWMM 노드 ID와 동일하게 둔다.",
        "- 원칙: HTML은 `viewer/network_registry.js`를 먼저 읽고, PySWMM/API는 같은 registry JSON을 읽는다.",
        "",
        "## 시나리오 파일",
        "",
    ]
    for scenario, config in SCENARIOS.items():
        ok, errors = scenario_results[scenario]
        result = "통과" if ok else "수정 필요"
        lines.append(f"- `models/seoul_design_{scenario}.inp`: {config['title']} / 구조 검증 {result}")
        lines.append(f"  - 이벤트 확인: {format_event_counts(event_counts, scenario)}")
        for error in errors:
            lines.append(f"  - {error}")
    lines.extend([
        "",
        "## 조건 설계",
        "",
        "| 조건 | 화면/데이터 반영 |",
        "|---|---|",
        "| 관 용량 계산 | 지름, 길이, 경사, 조도 기준의 간이 Manning 용량을 `capacity_cms`로 저장 |",
        "| 용량 사용률 증가 | `capacity_ratio = abs(flow_cms) / capacity_cms`로 계산 |",
        "| 유속 증가 | 해당 pipe ID의 흐름 점선 속도 증가 |",
        "| 유량/만관비 증가 | 해당 pipe/asset ID의 차오름 증가, 파랑에서 붉은색으로 변화 |",
        f"| 우수 간선관거 수위 상승 | 펌프장 수위 {HYDRAULIC_RULES['pump_on_level']:.2f} 이상이면 `storm_pump_station` 활성화 |",
        f"| 합류식 본관 수위 상승 | 우수토실 수위 {HYDRAULIC_RULES['overflow_gate_start_level']:.2f}부터 일반 유량부 제한 시작 |",
        f"| 우수토실 만수 접근 | 우수토실 수위 {HYDRAULIC_RULES['overflow_gate_closed_level']:.2f} 이상이면 일반 유량부 최소 개도, `overflow_pipe` 활성화 |",
        "| 하천 수위 상승 | `overflow_pipe`, `storm_pump_discharge_pipe`, `treatment_effluent_pipe` 역류 후보 |",
        "",
        "## 생성 결과 CSV",
        "",
        "- `sample-results/design_sensor_readings.csv`: 시간별 pipe/asset 상태",
        "  - 주요 열: `flow_cms`, `velocity_mps`, `capacity_cms`, `capacity_ratio`, `control_setting`, `backflow`, `risk`",
        "- `sample-results/design_sensor_readings_base.csv`: 기본 폭우 시나리오 상태",
        "- `sample-results/design_sensor_readings_overflow.csv`: 폭우 월류 시나리오 상태",
        "- `sample-results/design_sensor_readings_backflow.csv`: 하천 역류 시나리오 상태",
        "- `sample-results/design_sensor_summary.csv`: ID별 최대/최소 요약",
        "- `sample-results/design_problem_events.csv`: 경고/월류/역류 후보 이벤트",
        "- `sample-results/design_problem_events_base.csv`: 기본 폭우 이벤트",
        "- `sample-results/design_problem_events_overflow.csv`: 폭우 월류 이벤트",
        "- `sample-results/design_problem_events_backflow.csv`: 하천 역류 이벤트",
        "- `sample-results/design_screen_swmm_mapping.csv`: 화면 ID와 SWMM ID 매핑",
        "- `sample-results/network_registry.json`: Python/PySWMM/API가 읽을 공통 ID registry",
        "- `viewer/network_registry.js`: HTML 화면이 읽을 공통 ID registry",
        "",
        "## 생성 문서",
        "",
        "- `docs/design_network_structure.md`: 화면 구조와 SWMM ID 연결",
        "- `docs/hydraulic_control_rules.md`: 물리 조건과 시설 작동 기준",
        "",
        "## Windows 실행 파일",
        "",
        "- `Run_SWMM_Design_Base.bat`",
        "- `Run_SWMM_Design_Overflow.bat`",
        "- `Run_SWMM_Design_Backflow.bat`",
        "",
        "## 실행 상태",
        "",
    ])
    if swmm_cli:
        lines.append(f"- 현재 Mac에서 감지된 SWMM 실행 파일: `{swmm_cli}`")
    else:
        lines.append("- 현재 Mac PATH에서는 `swmm5` 또는 `runswmm` 실행 파일을 찾지 못했다.")
    lines.append("- `.inp` 파일은 EPA SWMM GUI 또는 Windows `runswmm.exe`에서 실행할 수 있게 생성했다.")
    lines.append("- CSV는 같은 조건 설계를 기반으로 만든 화면 연결용 시나리오 데이터다. Windows에서 실제 SWMM 실행 결과를 뽑으면 이 CSV 생성부를 실제 결과 파서로 교체하면 된다.")
    return "\n".join(lines) + "\n"


def build_structure_doc(pipe_ids: list[str], asset_ids: list[str]) -> str:
    return f"""# 설계 배수 네트워크 구조

## 전체 기준

- registry 버전: `{REGISTRY_VERSION}`
- 공통 registry 배관 수: {len(pipe_ids)}개
- 공통 registry 시설 수: {len(asset_ids)}개
- 공통 registry 지상 유입 객체 수: {len(surface_ids())}개
- 화면 ID와 SWMM ID를 동일하게 맞췄다.
- 방향 기준은 화면과 동일하게 `왼쪽 -> 오른쪽`, `위 -> 아래` 흐름이다.

## 분류식 우수 흐름

```text
분류식 빗물받이
-> 우수연결관
-> 우수 맨홀 / 우수 본관 1, 2
-> 우수 간선관거
-> 빗물펌프장
-> 펌프 토출관
-> 펌프 방류구
-> 하천
```

핵심 ID:

- `sep_catch_basin_1`, `sep_catch_basin_2`
- `sep_storm_lateral_catch_basin_1`, `sep_storm_lateral_catch_basin_2`
- `sep_storm_manhole`
- `sep_storm_main_1`, `sep_storm_main_2`, `sep_storm_main_to_trunk`
- `sep_storm_trunk`
- `storm_pump_station`
- `storm_pump_discharge_pipe`
- `pump_outfall`

## 분류식 오수 흐름

```text
아파트 생활오수
-> 오수연결관
-> 오수 맨홀 / 오수 본관 1, 2
-> 차집관거
-> 물재생센터
-> 처리수 방류관
-> 처리수 방류구
-> 하천
```

핵심 ID:

- `sep_sewer_lateral_apartment_1`, `sep_sewer_lateral_apartment_2`
- `sep_sewer_manhole`
- `sep_sewer_main_1`, `sep_sewer_main_2`, `sep_sewer_main_to_interceptor`
- `sep_interceptor`
- `water_reclamation_center`
- `treatment_effluent_pipe`
- `treated_outfall`

## 합류식 흐름

```text
주거지 생활오수 + 빗물받이 우수
-> 합류식 맨홀 / 합류식 본관 1, 2
-> 우수토실-월류시설
```

정상 유량:

```text
우수토실-월류시설
-> 일반 유량 연결부
-> 차집관거
-> 물재생센터
-> 처리수 방류구
```

폭우 초과 유량:

```text
우수토실-월류시설
-> 월류관
-> 월류 방류구
-> 하천
```

핵심 ID:

- `comb_sewer_lateral_house_1`, `comb_sewer_lateral_house_2`
- `comb_storm_lateral_catch_basin_1`, `comb_storm_lateral_catch_basin_2`
- `combined_manhole`
- `comb_main_1`, `comb_main_2`
- `overflow_chamber`
- `overflow_to_interceptor_drop`
- `overflow_pipe`
- `overflow_outfall`

## 조건 설계

- 우수 간선관거 수위가 높아지면 `storm_pump_station`이 활성화되고 `storm_pump_discharge_pipe` 유량이 증가한다.
- `overflow_chamber` 수위가 높아지면 일반 유량 쪽 `overflow_to_interceptor_drop`은 제한되고, `overflow_pipe`가 활성화된다.
- 하천 수위가 높아지는 역류 시나리오에서는 `overflow_pipe`, `storm_pump_discharge_pipe`, `treatment_effluent_pipe`가 역류 후보가 된다.

## 생성된 시나리오

- `base`: 기본 폭우. 월류 없이 펌프 중심으로 우수 배제.
- `overflow`: 폭우 월류. 합류식 본관과 우수토실이 높아져 월류관 활성화.
- `backflow`: 하천 역류. 방류구 3종과 연결 방류관에서 역방향 후보 발생.
"""


def build_hydraulic_rules_doc() -> str:
    return f"""# 배수도 물리 조건 및 시설 작동 규칙

## 목적

이 문서는 화면 배수도와 SWMM 설계 모델 사이에서 사용하는 간이 물리 규칙을 정리한다.
실제 서울 전역 관망을 완전히 대체하는 정밀 해석은 아니지만, 발표용 시뮬레이션에서
`유속`, `유량`, `만관비`, `역류`, `펌프 작동`, `월류시설 작동`을 일관되게 제어하기 위한 기준이다.

## 공통 배관 계산

| 항목 | 계산 방식 | 화면 반영 |
|---|---|---|
| 배관 용량 | 관 지름, 길이, 상하류 고도차, 조도계수로 간이 Manning 용량 계산 | `capacity_cms` |
| 현재 유량 | 상류 유입량과 시설 제어 조건을 따라 네트워크 방향으로 전달 | `flow_cms` |
| 용량 사용률 | `abs(flow_cms) / capacity_cms` | `capacity_ratio` |
| 만관비 | 용량 사용률을 수위처럼 변환 | `fullness_ratio`, `water_level` |
| 유속 | `flow / 젖은 단면적`으로 간이 계산 | `velocity_mps` |
| 위험도 | 용량 사용률이 높거나 역류이면 상태 변경 | `risk` |

## 위험도 기준

| 상태 | 기준 |
|---|---|
| `normal` | 용량 사용률이 낮고 역류 없음 |
| `warning` | 용량 사용률 {HYDRAULIC_RULES['warning_capacity_ratio']:.2f} 이상 |
| `surcharge_risk` | 용량 사용률 {HYDRAULIC_RULES['surcharge_capacity_ratio']:.2f} 이상 |
| `backflow` | 하천 수위 조건 또는 막힘 관 만관 조건으로 역방향 흐름 발생 |

## 빗물펌프장 조건

```text
우수본관 -> 우수 간선관거 -> 빗물펌프장 -> 펌프 토출관 -> 펌프 방류구
```

| 조건 | 동작 |
|---|---|
| 펌프장 수위 {HYDRAULIC_RULES['pump_on_level']:.2f} 이상 | `storm_pump_station` 상태를 `pump_active`로 변경 |
| 펌프장 수위 {HYDRAULIC_RULES['pump_off_level']:.2f} 이하 | 펌프 대기 상태 |
| 펌프 용량 | {HYDRAULIC_RULES['pump_capacity_cms']:.2f} CMS |
| 하천 역류 압력 발생 | `storm_pump_discharge_pipe`, `pump_outfall`을 역류 후보로 표시 |

## 우수토실-월류시설 조건

```text
합류식 본관 -> 우수토실
정상 유량 -> 차집관거
초과 유량 -> 월류관 -> 월류 방류구
```

| 조건 | 동작 |
|---|---|
| 우수토실 수위 {HYDRAULIC_RULES['overflow_gate_start_level']:.2f} 이하 | 일반 유량부 완전 개방 |
| 우수토실 수위 {HYDRAULIC_RULES['overflow_gate_start_level']:.2f} 초과 | 유량조절판이 닫히기 시작 |
| 우수토실 수위 {HYDRAULIC_RULES['overflow_gate_closed_level']:.2f} 이상 | 일반 유량부 최소 개도 {HYDRAULIC_RULES['overflow_gate_min_setting']:.2f} |
| 일반 유량부 용량 초과 | 남는 유량이 `overflow_pipe`로 이동 |
| 하천 역류 압력 발생 | `overflow_pipe`, `overflow_outfall`을 역류 후보로 표시 |

## 물재생센터 조건

```text
차집관거 -> 물재생센터 -> 처리수 방류관 -> 처리수 방류구
```

| 조건 | 동작 |
|---|---|
| 차집관거 유입이 처리 용량 이하 | 처리수 방류관으로 정상 방류 |
| 차집관거 유입이 {HYDRAULIC_RULES['water_reclamation_capacity_cms']:.2f} CMS 초과 | `treatment_over_capacity` 표시 |
| 하천 역류 압력 발생 | `treatment_effluent_pipe`, `treated_outfall`을 역류 후보로 표시 |

## 역류 조건

하천 역류 시나리오에서는 하천 수위가 상승하는 시간대에만 역류 압력을 만든다.
역류 압력이 {HYDRAULIC_RULES['river_backflow_start']:.2f} 이상이면 다음 경로가 역류 후보가 된다.

- `overflow_pipe` -> `overflow_outfall`
- `storm_pump_discharge_pipe` -> `pump_outfall`
- `treatment_effluent_pipe` -> `treated_outfall`

막힘 기반 역류는 막힘 자체만으로 발생하지 않는다. 다음 조건이 동시에 맞을 때만 상류 노드/시설의 수위와 유량을 증가시킨다.

| 조건 | 기준 |
|---|---|
| 막힌 관이 사실상 만관 | fullness ratio {HYDRAULIC_RULES['blocked_backflow_fullness_ratio']:.2f} 이상 |
| 전 노드에서 유입 지속 | upstream inflow {HYDRAULIC_RULES['blocked_backflow_inflow_cms']:.3f} CMS 초과 |
| 배출 제한이 충분히 큼 | blockage ratio {HYDRAULIC_RULES['blocked_backflow_blockage_ratio']:.2f} 이상 |

## 화면 연결 방식

CSV의 `id`는 화면 객체 ID와 동일하다.

```text
design_sensor_readings.csv
-> id로 화면 pipe/asset 찾기
-> velocity_mps로 점선 애니메이션 속도 제어
-> fullness_ratio로 차오름 제어
-> backflow=true면 역방향 흐름 표시
-> status/risk로 시설 작동 상태 표시
```
"""


def main() -> int:
    pipe_ids, asset_ids = extract_diagram_ids()
    scenario_results: dict[str, tuple[bool, list[str]]] = {}
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_DIR.mkdir(parents=True, exist_ok=True)
    write_registry_json(REGISTRY_JSON_PATH)
    write_registry_js(VIEWER_REGISTRY_PATH)

    for scenario in SCENARIOS:
        inp_text = build_inp(scenario)
        path = MODEL_DIR / f"seoul_design_{scenario}.inp"
        path.write_text(inp_text, encoding="utf-8")
        scenario_results[scenario] = validate(inp_text)

    mapping_rows = []
    for pipe in PIPE_REGISTRY:
        pipe_id = pipe["id"]
        link = LINK_BY_ID[pipe_id]
        mapping_rows.append({
            "object_type": "pipe",
            "screen_id": pipe_id,
            "swmm_id": pipe["swmmId"],
            "swmm_object_type": link.link_type.lower(),
            "size": pipe["size"],
            "water_type": pipe["waterType"],
        })
    for asset in ASSET_REGISTRY:
        asset_id = asset["id"]
        node = next((item for item in NODES if item.node_id == asset_id), None)
        mapping_rows.append({
            "object_type": "asset",
            "screen_id": asset_id,
            "swmm_id": asset["swmmId"],
            "swmm_object_type": node.section.lower() if node else "",
            "size": "",
            "water_type": asset["waterType"],
        })
    for surface in SURFACE_REGISTRY:
        surface_id = surface["id"]
        node = next((item for item in NODES if item.node_id == surface_id), None)
        mapping_rows.append({
            "object_type": "surface",
            "screen_id": surface_id,
            "swmm_id": surface["swmmId"],
            "swmm_object_type": node.section.lower() if node else "",
            "size": "",
            "water_type": surface["waterType"],
        })
    for hidden_node in MODEL_ONLY_NODE_REGISTRY:
        node_id = hidden_node["id"]
        node = next((item for item in NODES if item.node_id == node_id), None)
        mapping_rows.append({
            "object_type": "model_only_node",
            "screen_id": "",
            "swmm_id": hidden_node["swmmId"],
            "swmm_object_type": node.section.lower() if node else "",
            "size": "",
            "water_type": "",
        })
    for control in CONTROL_REGISTRY:
        control_id = control["id"]
        link = PUMP_LINK if control_id == PUMP_LINK.link_id else LINK_BY_ID.get(control_id)
        mapping_rows.append({
            "object_type": "control",
            "screen_id": control["targetId"],
            "swmm_id": control["swmmId"],
            "swmm_object_type": link.link_type.lower() if link else control["type"],
            "size": "",
            "water_type": link.water_type if link else "",
        })

    rows, summary, events = generate_controller_data(pipe_ids, asset_ids)
    write_csv(RESULT_DIR / "design_screen_swmm_mapping.csv", mapping_rows)
    write_csv(RESULT_DIR / "design_sensor_readings.csv", rows)
    write_csv(RESULT_DIR / "design_sensor_summary.csv", summary)
    write_csv(RESULT_DIR / "design_problem_events.csv", events)
    write_viewer_playback_data(rows)
    for scenario in SCENARIOS:
        write_csv(
            RESULT_DIR / f"design_sensor_readings_{scenario}.csv",
            [row for row in rows if row["scenario"] == scenario],
        )
        write_csv(
            RESULT_DIR / f"design_problem_events_{scenario}.csv",
            [row for row in events if row["scenario"] == scenario],
        )
        (ROOT / f"Run_SWMM_Design_{scenario.title()}.bat").write_text(build_windows_runner(scenario), encoding="utf-8")

    swmm_cli = shutil.which("swmm5") or shutil.which("runswmm")
    event_counts = count_events(events)
    (DOC_DIR / "design_validation_report.md").write_text(
        build_report(pipe_ids, asset_ids, scenario_results, event_counts, swmm_cli),
        encoding="utf-8",
    )
    (DOC_DIR / "design_network_structure.md").write_text(
        build_structure_doc(pipe_ids, asset_ids),
        encoding="utf-8",
    )
    (DOC_DIR / "hydraulic_control_rules.md").write_text(
        build_hydraulic_rules_doc(),
        encoding="utf-8",
    )

    ok = all(result for result, _ in scenario_results.values())
    print(f"diagram_pipe_count={len(pipe_ids)}")
    print(f"diagram_asset_count={len(asset_ids)}")
    print(f"generated_scenarios={','.join(SCENARIOS)}")
    print(f"validation={'ok' if ok else 'failed'}")
    for scenario, (result, errors) in scenario_results.items():
        print(f"{scenario}: {'ok' if result else 'failed'}")
        for error in errors:
            print(f"  {error}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
