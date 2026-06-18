#!/usr/bin/env python3
"""Build the SWMM-first HTML object contract.

This contract is the migration boundary between the SWMM model and the HTML
viewer. SWMM remains the source of truth; the viewer only groups SWMM nodes and
links into readable visual objects.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "seoul_rebuild_v2.inp"
JSON_PATH = ROOT / "sample-results" / "swmm_html_contract.json"
JS_PATH = ROOT / "viewer" / "swmm_html_contract.js"
DOC_PATH = ROOT / "docs" / "swmm_html_contract.md"

CONTRACT_VERSION = "2026-06-12-swmm-first-contract-v1"


VISUAL_OBJECTS: list[dict[str, Any]] = [
    {
        "htmlId": "sep_apartment_1",
        "label": "분류식 아파트 1",
        "objectType": "surface",
        "system": "separate",
        "waterType": "sewer",
        "swmmNodes": ["sep_apartment_1"],
        "swmmLinks": [],
        "controls": {"rainfall": False, "blockage": False},
    },
    {
        "htmlId": "sep_apartment_2",
        "label": "분류식 아파트 2",
        "objectType": "surface",
        "system": "separate",
        "waterType": "sewer",
        "swmmNodes": ["sep_apartment_2"],
        "swmmLinks": [],
        "controls": {"rainfall": False, "blockage": False},
    },
    {
        "htmlId": "sep_catch_basin_1",
        "label": "분류식 빗물받이 1",
        "objectType": "catch_basin",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": ["road_runoff_sep_catch_basin_1", "sep_catch_basin_1"],
        "swmmLinks": ["sep_catch_basin_1_inlet_connector"],
        "controls": {"rainfall": True, "blockage": True},
    },
    {
        "htmlId": "sep_catch_basin_2",
        "label": "분류식 빗물받이 2",
        "objectType": "catch_basin",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": ["road_runoff_sep_catch_basin_2", "sep_catch_basin_2"],
        "swmmLinks": ["sep_catch_basin_2_inlet_connector"],
        "controls": {"rainfall": True, "blockage": True},
    },
    {
        "htmlId": "sep_storm_lateral_catch_basin_1",
        "label": "분류식 빗물받이 1 우수연결관",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": [
            "sep_catch_basin_1",
            "sep_storm_lateral_catch_basin_1_start",
            "sep_storm_lateral_catch_basin_1_elbow_connector",
            "sep_storm_main_1_catch_basin_1_connector",
        ],
        "swmmLinks": [
            "sep_catch_basin_1_outlet_connector",
            "sep_storm_lateral_catch_basin_1_horizontal",
            "sep_storm_lateral_catch_basin_1_vertical",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_storm_lateral_catch_basin_2",
        "label": "분류식 빗물받이 2 우수연결관",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": [
            "sep_catch_basin_2",
            "sep_storm_lateral_catch_basin_2_start",
            "sep_storm_lateral_catch_basin_2_elbow_connector",
            "sep_storm_main_2_catch_basin_2_connector",
        ],
        "swmmLinks": [
            "sep_catch_basin_2_outlet_connector",
            "sep_storm_lateral_catch_basin_2_horizontal",
            "sep_storm_lateral_catch_basin_2_vertical",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_storm_main_1",
        "label": "우수 본관 1",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": [
            "offscreen_catch_basin_storm_main_1",
            "sep_storm_main_1_catch_basin_1_connector",
            "sep_storm_manhole",
        ],
        "swmmLinks": [
            "sep_storm_main_1_upstream_segment",
            "sep_storm_main_1_downstream_segment",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_storm_manhole",
        "label": "분류식 우수 맨홀",
        "objectType": "manhole",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": ["sep_storm_manhole"],
        "swmmLinks": [],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_storm_main_2",
        "label": "우수 본관 2",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": [
            "sep_storm_manhole",
            "sep_storm_main_2_catch_basin_2_connector",
            "sep_storm_main_2_outlet_connector",
        ],
        "swmmLinks": [
            "sep_storm_main_2_upstream_segment",
            "sep_storm_main_2_downstream_segment",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_storm_main_to_trunk",
        "label": "우수 본관 2에서 우수 간선관거로 내려가는 연결관",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": [
            "sep_storm_main_2_outlet_connector",
            "sep_storm_main_to_trunk_elbow_connector",
            "sep_storm_trunk_main_2_drop_connector",
        ],
        "swmmLinks": [
            "sep_storm_main_to_trunk_horizontal",
            "sep_storm_main_to_trunk_vertical",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_storm_trunk",
        "label": "우수 간선관거",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": [
            "sep_storm_trunk_upstream",
            "sep_storm_trunk_main_2_drop_connector",
            "sep_storm_trunk_downstream",
            "storm_pump_inlet_gate_node",
        ],
        "swmmLinks": [
            "sep_storm_trunk_upstream_segment",
            "sep_storm_trunk_downstream_segment",
            "sep_storm_trunk_to_pump_station",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "storm_pump_station",
        "label": "빗물펌프장",
        "objectType": "pump_station",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": ["storm_pump_inlet_gate_node", "storm_pump_station", "storm_pump_discharge_node"],
        "swmmLinks": ["storm_pump_inlet_gate", "storm_pump_unit"],
        "controls": {"rainfall": False, "blockage": True, "operation": True},
    },
    {
        "htmlId": "storm_pump_discharge_pipe",
        "label": "펌프 토출관",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": ["storm_pump_discharge_node", "pump_outfall_gate_node"],
        "swmmLinks": ["storm_pump_discharge_pipe"],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "pump_outfall",
        "label": "펌프 방류구",
        "objectType": "outfall",
        "system": "separate",
        "waterType": "storm",
        "swmmNodes": ["pump_outfall_gate_node", "pump_outfall"],
        "swmmLinks": ["pump_outfall_gate"],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_sewer_lateral_apartment_1",
        "label": "분류식 아파트 1 오수연결관",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "sewer",
        "swmmNodes": [
            "sep_apartment_1",
            "sep_sewer_lateral_apartment_1_elbow_connector",
            "sep_sewer_main_1_apartment_1_connector",
        ],
        "swmmLinks": [
            "sep_sewer_lateral_apartment_1_horizontal",
            "sep_sewer_lateral_apartment_1_vertical",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_sewer_lateral_apartment_2",
        "label": "분류식 아파트 2 오수연결관",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "sewer",
        "swmmNodes": [
            "sep_apartment_2",
            "sep_sewer_lateral_apartment_2_elbow_connector",
            "sep_sewer_main_2_apartment_2_connector",
        ],
        "swmmLinks": [
            "sep_sewer_lateral_apartment_2_horizontal",
            "sep_sewer_lateral_apartment_2_vertical",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_sewer_main_1",
        "label": "오수 본관 1",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "sewer",
        "swmmNodes": [
            "sep_sewer_upstream",
            "sep_sewer_main_1_apartment_1_connector",
            "sep_sewer_manhole",
        ],
        "swmmLinks": [
            "sep_sewer_main_1_upstream_segment",
            "sep_sewer_main_1_downstream_segment",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_sewer_manhole",
        "label": "분류식 오수 맨홀",
        "objectType": "manhole",
        "system": "separate",
        "waterType": "sewer",
        "swmmNodes": ["sep_sewer_manhole"],
        "swmmLinks": [],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_sewer_main_2",
        "label": "오수 본관 2",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "sewer",
        "swmmNodes": [
            "sep_sewer_manhole",
            "sep_sewer_main_2_apartment_2_connector",
            "sep_sewer_downstream",
        ],
        "swmmLinks": [
            "sep_sewer_main_2_upstream_segment",
            "sep_sewer_main_2_downstream_segment",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_sewer_main_to_interceptor",
        "label": "오수 본관 2에서 차집관거로 내려가는 연결관",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "sewer",
        "swmmNodes": [
            "sep_sewer_downstream",
            "sep_sewer_main_to_interceptor_elbow_connector",
            "sep_interceptor_join",
        ],
        "swmmLinks": [
            "sep_sewer_main_to_interceptor_horizontal",
            "sep_sewer_main_to_interceptor_vertical",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "sep_interceptor",
        "label": "차집관거",
        "objectType": "pipe_group",
        "system": "separate",
        "waterType": "sewer",
        "swmmNodes": [
            "sep_interceptor_upstream",
            "sep_interceptor_join",
            "overflow_interceptor_join",
            "sep_interceptor_downstream",
            "water_reclamation_center",
        ],
        "swmmLinks": [
            "sep_interceptor_upstream_segment",
            "sep_interceptor_join_to_overflow_segment",
            "sep_interceptor_downstream_segment",
            "sep_interceptor_to_reclamation_inlet",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "water_reclamation_center",
        "label": "물재생센터",
        "objectType": "treatment_facility",
        "system": "treatment",
        "waterType": "treated",
        "swmmNodes": ["water_reclamation_center", "treatment_process_outlet_node"],
        "swmmLinks": ["treatment_process_limited_outlet"],
        "controls": {"rainfall": False, "blockage": True, "operation": True},
    },
    {
        "htmlId": "treatment_effluent_pipe",
        "label": "처리수 방류관",
        "objectType": "pipe_group",
        "system": "treatment",
        "waterType": "treated",
        "swmmNodes": ["treatment_process_outlet_node", "treated_outfall_gate_node"],
        "swmmLinks": ["treatment_effluent_pipe"],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "treated_outfall",
        "label": "처리수 방류구",
        "objectType": "outfall",
        "system": "treatment",
        "waterType": "treated",
        "swmmNodes": ["treated_outfall_gate_node", "treated_outfall"],
        "swmmLinks": ["treated_outfall_gate"],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "comb_house_1",
        "label": "합류식 주거지 1",
        "objectType": "surface",
        "system": "combined",
        "waterType": "sewer",
        "swmmNodes": ["comb_house_1"],
        "swmmLinks": [],
        "controls": {"rainfall": False, "blockage": False},
    },
    {
        "htmlId": "comb_house_2",
        "label": "합류식 주거지 2",
        "objectType": "surface",
        "system": "combined",
        "waterType": "sewer",
        "swmmNodes": ["comb_house_2"],
        "swmmLinks": [],
        "controls": {"rainfall": False, "blockage": False},
    },
    {
        "htmlId": "offscreen_comb_catch_basin",
        "label": "합류식 화면밖 빗물받이",
        "objectType": "catch_basin",
        "system": "combined",
        "waterType": "storm",
        "swmmNodes": ["road_runoff_offscreen_comb_catch_basin", "offscreen_comb_catch_basin"],
        "swmmLinks": ["offscreen_comb_catch_basin_inlet_connector"],
        "controls": {"rainfall": True, "blockage": True},
    },
    {
        "htmlId": "comb_catch_basin_1",
        "label": "합류식 빗물받이 1",
        "objectType": "catch_basin",
        "system": "combined",
        "waterType": "storm",
        "swmmNodes": ["road_runoff_comb_catch_basin_1", "comb_catch_basin_1"],
        "swmmLinks": ["comb_catch_basin_1_inlet_connector"],
        "controls": {"rainfall": True, "blockage": True},
    },
    {
        "htmlId": "comb_catch_basin_2",
        "label": "합류식 빗물받이 2",
        "objectType": "catch_basin",
        "system": "combined",
        "waterType": "storm",
        "swmmNodes": ["road_runoff_comb_catch_basin_2", "comb_catch_basin_2"],
        "swmmLinks": ["comb_catch_basin_2_inlet_connector"],
        "controls": {"rainfall": True, "blockage": True},
    },
    {
        "htmlId": "offscreen_comb_storm_lateral",
        "label": "합류식 화면밖 우수연결관",
        "objectType": "pipe_group",
        "system": "combined",
        "waterType": "storm",
        "swmmNodes": [
            "offscreen_comb_catch_basin",
            "offscreen_comb_storm_lateral_start",
            "offscreen_comb_storm_lateral_elbow_connector",
            "comb_upstream",
        ],
        "swmmLinks": [
            "offscreen_comb_catch_basin_outlet_connector",
            "offscreen_comb_storm_lateral_horizontal",
            "offscreen_comb_storm_lateral_vertical",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "offscreen_comb_sewer_lateral",
        "label": "합류식 화면밖 오수연결관",
        "objectType": "pipe_group",
        "system": "combined",
        "waterType": "sewer",
        "swmmNodes": ["offscreen_comb_sewer_source", "comb_upstream"],
        "swmmLinks": ["offscreen_comb_sewer_lateral"],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "comb_sewer_lateral_house_1",
        "label": "합류식 주거지 1 오수연결관",
        "objectType": "pipe_group",
        "system": "combined",
        "waterType": "sewer",
        "swmmNodes": [
            "comb_house_1",
            "comb_sewer_lateral_house_1_elbow_connector",
            "comb_main_house_1_connector",
        ],
        "swmmLinks": [
            "comb_sewer_lateral_house_1_horizontal",
            "comb_sewer_lateral_house_1_vertical",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "comb_sewer_lateral_house_2",
        "label": "합류식 주거지 2 오수연결관",
        "objectType": "pipe_group",
        "system": "combined",
        "waterType": "sewer",
        "swmmNodes": [
            "comb_house_2",
            "comb_sewer_lateral_house_2_elbow_connector",
            "comb_main_house_2_connector",
        ],
        "swmmLinks": [
            "comb_sewer_lateral_house_2_horizontal",
            "comb_sewer_lateral_house_2_vertical",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "comb_storm_lateral_catch_basin_1",
        "label": "합류식 빗물받이 1 우수연결관",
        "objectType": "pipe_group",
        "system": "combined",
        "waterType": "storm",
        "swmmNodes": [
            "comb_catch_basin_1",
            "comb_storm_lateral_catch_basin_1_start",
            "comb_storm_lateral_catch_basin_1_elbow_connector",
            "comb_main_catch_basin_1_connector",
        ],
        "swmmLinks": [
            "comb_catch_basin_1_outlet_connector",
            "comb_storm_lateral_catch_basin_1_horizontal",
            "comb_storm_lateral_catch_basin_1_vertical",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "comb_storm_lateral_catch_basin_2",
        "label": "합류식 빗물받이 2 우수연결관",
        "objectType": "pipe_group",
        "system": "combined",
        "waterType": "storm",
        "swmmNodes": [
            "comb_catch_basin_2",
            "comb_storm_lateral_catch_basin_2_start",
            "comb_storm_lateral_catch_basin_2_elbow_connector",
            "comb_main_catch_basin_2_connector",
        ],
        "swmmLinks": [
            "comb_catch_basin_2_outlet_connector",
            "comb_storm_lateral_catch_basin_2_horizontal",
            "comb_storm_lateral_catch_basin_2_vertical",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "comb_main_1",
        "label": "합류식 본관 1",
        "objectType": "pipe_group",
        "system": "combined",
        "waterType": "combined",
        "swmmNodes": [
            "comb_upstream",
            "comb_main_house_1_connector",
            "comb_main_house_2_connector",
            "comb_main_catch_basin_1_connector",
            "combined_manhole",
        ],
        "swmmLinks": [
            "comb_main_1_upstream_segment",
            "comb_main_1_house_1_to_house_2_segment",
            "comb_main_1_house_2_to_catch_basin_1_segment",
            "comb_main_1_to_manhole_segment",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "combined_manhole",
        "label": "합류식 맨홀",
        "objectType": "manhole",
        "system": "combined",
        "waterType": "combined",
        "swmmNodes": ["combined_manhole"],
        "swmmLinks": [],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "comb_main_2",
        "label": "합류식 본관 2",
        "objectType": "pipe_group",
        "system": "combined",
        "waterType": "combined",
        "swmmNodes": [
            "combined_manhole",
            "comb_main_catch_basin_2_connector",
            "overflow_chamber",
        ],
        "swmmLinks": [
            "comb_main_2_manhole_to_catch_basin_2_segment",
            "comb_main_2_downstream_segment",
        ],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "overflow_chamber",
        "label": "우수토실-월류시설",
        "objectType": "overflow_facility",
        "system": "combined",
        "waterType": "combined",
        "swmmNodes": ["overflow_chamber", "overflow_normal_flow_node", "overflow_weir_outlet_node"],
        "swmmLinks": ["overflow_normal_flow_gate", "overflow_excess_weir"],
        "controls": {"rainfall": False, "blockage": True, "operation": True},
    },
    {
        "htmlId": "overflow_to_interceptor_drop",
        "label": "우수토실 일반 유량에서 차집관거로 내려가는 관",
        "objectType": "pipe_group",
        "system": "combined",
        "waterType": "combined",
        "swmmNodes": ["overflow_chamber", "overflow_normal_flow_node", "overflow_interceptor_join"],
        "swmmLinks": ["overflow_normal_flow_gate", "overflow_to_interceptor_drop"],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "overflow_pipe",
        "label": "월류관",
        "objectType": "pipe_group",
        "system": "combined",
        "waterType": "overflow",
        "swmmNodes": ["overflow_chamber", "overflow_weir_outlet_node", "overflow_outfall_gate_node"],
        "swmmLinks": ["overflow_excess_weir", "overflow_pipe"],
        "controls": {"rainfall": False, "blockage": True},
    },
    {
        "htmlId": "overflow_outfall",
        "label": "월류 방류구",
        "objectType": "outfall",
        "system": "combined",
        "waterType": "overflow",
        "swmmNodes": ["overflow_outfall_gate_node", "overflow_outfall"],
        "swmmLinks": ["overflow_outfall_gate"],
        "controls": {"rainfall": False, "blockage": True},
    },
]


SECTION_NAMES = {
    "JUNCTIONS",
    "STORAGE",
    "OUTFALLS",
    "ORIFICES",
    "WEIRS",
    "PUMPS",
    "CONDUITS",
    "XSECTIONS",
    "LOSSES",
    "INFLOWS",
    "COORDINATES",
}


def parse_sections(model_path: Path) -> dict[str, list[list[str]]]:
    sections: dict[str, list[list[str]]] = {}
    current: str | None = None
    for raw_line in model_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";;"):
            continue
        if line.startswith("[") and line.endswith("]"):
            name = line.strip("[]").upper()
            current = name if name in SECTION_NAMES else None
            if current:
                sections.setdefault(current, [])
            continue
        if current:
            sections[current].append(line.split())
    return sections


def build_indexes(sections: dict[str, list[list[str]]]) -> tuple[dict[str, Any], dict[str, Any]]:
    nodes: dict[str, Any] = {}
    links: dict[str, Any] = {}

    for row in sections.get("JUNCTIONS", []):
        node_id = row[0]
        nodes[node_id] = {
            "id": node_id,
            "nodeType": "JUNCTION",
            "elevationM": float(row[1]),
            "maxDepthM": float(row[2]),
            "initialDepthM": float(row[3]),
            "surchargeDepthM": float(row[4]),
            "pondedAreaM2": float(row[5]),
        }

    for row in sections.get("STORAGE", []):
        node_id = row[0]
        nodes[node_id] = {
            "id": node_id,
            "nodeType": "STORAGE",
            "elevationM": float(row[1]),
            "maxDepthM": float(row[2]),
            "initialDepthM": float(row[3]),
            "shape": row[4],
            "storageParam": float(row[5]),
        }

    for row in sections.get("OUTFALLS", []):
        node_id = row[0]
        nodes[node_id] = {
            "id": node_id,
            "nodeType": "OUTFALL",
            "elevationM": float(row[1]),
            "outfallType": row[2],
            "gated": row[-1],
        }

    for row in sections.get("CONDUITS", []):
        link_id = row[0]
        links[link_id] = {
            "id": link_id,
            "linkType": "CONDUIT",
            "fromNode": row[1],
            "toNode": row[2],
            "lengthM": float(row[3]),
            "roughnessN": float(row[4]),
            "inOffsetM": float(row[5]),
            "outOffsetM": float(row[6]),
            "initialFlowCms": float(row[7]),
            "maxFlowCms": float(row[8]),
        }

    for row in sections.get("ORIFICES", []):
        link_id = row[0]
        links[link_id] = {
            "id": link_id,
            "linkType": "ORIFICE",
            "fromNode": row[1],
            "toNode": row[2],
            "orificeType": row[3],
            "offsetM": float(row[4]),
            "qCoeff": float(row[5]),
            "gated": row[6],
            "closeTimeSec": float(row[7]),
        }

    for row in sections.get("WEIRS", []):
        link_id = row[0]
        links[link_id] = {
            "id": link_id,
            "linkType": "WEIR",
            "fromNode": row[1],
            "toNode": row[2],
            "weirType": row[3],
            "crestHeightM": float(row[4]),
            "qCoeff": float(row[5]),
            "gated": row[6],
        }

    for row in sections.get("PUMPS", []):
        link_id = row[0]
        links[link_id] = {
            "id": link_id,
            "linkType": "PUMP",
            "fromNode": row[1],
            "toNode": row[2],
            "pumpCurve": row[3],
            "initialStatus": row[4],
            "startupDepthM": float(row[5]),
            "shutoffDepthM": float(row[6]),
        }

    for row in sections.get("XSECTIONS", []):
        link = links.get(row[0])
        if not link:
            continue
        link["crossSection"] = {
            "shape": row[1],
            "geom1": float(row[2]),
            "geom2": float(row[3]),
            "geom3": float(row[4]),
            "geom4": float(row[5]),
            "barrels": int(row[6]),
            "culvert": int(row[7]),
        }

    for row in sections.get("LOSSES", []):
        link = links.get(row[0])
        if not link:
            continue
        link["losses"] = {
            "inletLoss": float(row[1]),
            "outletLoss": float(row[2]),
            "averageLoss": float(row[3]),
            "flapGate": row[4],
            "seepageRate": float(row[5]),
        }

    for row in sections.get("COORDINATES", []):
        node = nodes.get(row[0])
        if not node:
            continue
        node["map"] = {"x": float(row[1]), "y": float(row[2])}

    for link in links.values():
        from_node = nodes.get(link.get("fromNode"))
        to_node = nodes.get(link.get("toNode"))
        if not from_node or not to_node:
            continue
        if link["linkType"] == "CONDUIT":
            length = float(link.get("lengthM") or 0)
            if length > 0:
                invert_in = float(from_node.get("elevationM", 0)) + float(link.get("inOffsetM", 0))
                invert_out = float(to_node.get("elevationM", 0)) + float(link.get("outOffsetM", 0))
                link["computedSlope"] = round((invert_in - invert_out) / length, 6)

    return nodes, links


def attach_resolved_elements(nodes: dict[str, Any], links: dict[str, Any]) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    for item in VISUAL_OBJECTS:
        missing_nodes = [node_id for node_id in item["swmmNodes"] if node_id not in nodes]
        missing_links = [link_id for link_id in item["swmmLinks"] if link_id not in links]
        resolved_nodes = [nodes[node_id] for node_id in item["swmmNodes"] if node_id in nodes]
        resolved_links = [links[link_id] for link_id in item["swmmLinks"] if link_id in links]
        objects.append(
            {
                **item,
                "missingNodes": missing_nodes,
                "missingLinks": missing_links,
                "resolvedNodes": resolved_nodes,
                "resolvedLinks": resolved_links,
            }
        )
    return objects


def build_contract() -> dict[str, Any]:
    sections = parse_sections(MODEL_PATH)
    nodes, links = build_indexes(sections)
    visual_objects = attach_resolved_elements(nodes, links)
    return {
        "version": CONTRACT_VERSION,
        "sourceOfTruth": "SWMM",
        "modelPath": str(MODEL_PATH),
        "viewerRole": "render_only_with_controls",
        "controlBoundary": {
            "htmlCanControl": ["rainfall", "object_blockage"],
            "htmlMustNotCalculate": ["hydraulic_flow", "backflow", "fullness", "pump_discharge"],
            "pythonBridgeRole": "advance_pyswmm_step_and_return_state",
        },
        "swmmIndexes": {
            "nodes": nodes,
            "links": links,
        },
        "visualObjects": visual_objects,
    }


def write_json(contract: dict[str, Any]) -> None:
    JSON_PATH.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_js(contract: dict[str, Any]) -> None:
    payload = json.dumps(contract, ensure_ascii=False, indent=2)
    JS_PATH.write_text(f"window.SWMM_HTML_CONTRACT = {payload};\n", encoding="utf-8")


def write_doc(contract: dict[str, Any]) -> None:
    objects = contract["visualObjects"]
    missing = [obj for obj in objects if obj["missingNodes"] or obj["missingLinks"]]
    lines = [
        "# SWMM-HTML 객체 계약",
        "",
        "## 기준",
        "",
        "- SWMM 모델이 원본입니다.",
        "- HTML은 SWMM 상태를 렌더링하고, 강수량과 객체별 막힘정도만 입력합니다.",
        "- 유량, 유속, 만관, 역류, 펌프 배출량은 HTML에서 직접 계산하지 않습니다.",
        "- ㄱ자로 보이는 관은 SWMM에서 `수평 관 + 접합 노드 + 수직 관`으로 나눕니다.",
        "",
        "## 생성 파일",
        "",
        f"- JSON 계약: `{JSON_PATH}`",
        f"- 브라우저 계약: `{JS_PATH}`",
        f"- 기준 모델: `{MODEL_PATH}`",
        "",
        "## HTML이 제어할 수 있는 값",
        "",
        "| 제어값 | 의미 | SWMM 반영 방식 |",
        "| --- | --- | --- |",
        "| 강수량 | 빗물 유입 강도 | PySWMM 브릿지에서 강우/유입 시계열 또는 입력 유량으로 변환 |",
        "| 객체별 막힘정도 | 특정 시설/관의 흐름 제한 | PySWMM 브릿지에서 대응 게이트/오리피스/제어 링크 setting으로 변환 |",
        "",
        "## HTML이 계산하면 안 되는 값",
        "",
        "- 유속",
        "- 유량",
        "- 만관 여부",
        "- 역류 여부",
        "- 펌프 배출량",
        "- 우수토실 월류량",
        "",
        "## 객체 매핑",
        "",
        "| HTML 객체 ID | 이름 | 종류 | SWMM 노드 | SWMM 링크 |",
        "| --- | --- | --- | --- | --- |",
    ]

    for obj in objects:
        nodes = ", ".join(f"`{node}`" for node in obj["swmmNodes"]) or "-"
        links = ", ".join(f"`{link}`" for link in obj["swmmLinks"]) or "-"
        lines.append(
            f"| `{obj['htmlId']}` | {obj['label']} | {obj['objectType']} | {nodes} | {links} |"
        )

    lines.extend(
        [
            "",
            "## 검증 결과",
            "",
            f"- 등록된 HTML 대표 객체: {len(objects)}개",
            f"- SWMM 노드 수: {len(contract['swmmIndexes']['nodes'])}개",
            f"- SWMM 링크 수: {len(contract['swmmIndexes']['links'])}개",
            f"- 누락 매핑 수: {len(missing)}개",
        ]
    )
    if missing:
        lines.extend(["", "### 누락 항목"])
        for obj in missing:
            lines.append(
                f"- `{obj['htmlId']}`: missing nodes={obj['missingNodes']}, missing links={obj['missingLinks']}"
            )

    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    contract = build_contract()
    write_json(contract)
    write_js(contract)
    write_doc(contract)
    missing = [obj for obj in contract["visualObjects"] if obj["missingNodes"] or obj["missingLinks"]]
    print(f"Wrote {JSON_PATH}")
    print(f"Wrote {JS_PATH}")
    print(f"Wrote {DOC_PATH}")
    print(f"visual_objects={len(contract['visualObjects'])}")
    print(f"nodes={len(contract['swmmIndexes']['nodes'])}")
    print(f"links={len(contract['swmmIndexes']['links'])}")
    print(f"missing_mappings={len(missing)}")
    if missing:
        for obj in missing:
            print(f"- {obj['htmlId']}: nodes={obj['missingNodes']} links={obj['missingLinks']}")


if __name__ == "__main__":
    main()
