#!/usr/bin/env python3
"""Shared object registry for the drainage diagram and SWMM model.

The IDs in this file are the contract between:

- viewer/overall_drainage_diagram.html
- scripts/design_scenario_builder.py
- the upcoming step-by-step PySWMM controller
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


REGISTRY_VERSION = "2026-06-11-control-registry-v1"


PIPE_REGISTRY = [
    {
        "id": "sep_sewer_lateral_apartment_1",
        "swmmId": "sep_sewer_lateral_apartment_1",
        "htmlId": "sep_sewer_lateral_apartment_1",
        "label": "분류식 아파트 1 오수연결관",
        "system": "separate",
        "waterType": "sewer",
        "size": "small",
        "direction": "right-down",
    },
    {
        "id": "sep_sewer_lateral_apartment_2",
        "swmmId": "sep_sewer_lateral_apartment_2",
        "htmlId": "sep_sewer_lateral_apartment_2",
        "label": "분류식 아파트 2 오수연결관",
        "system": "separate",
        "waterType": "sewer",
        "size": "small",
        "direction": "left-down",
    },
    {
        "id": "sep_storm_lateral_catch_basin_1",
        "swmmId": "sep_storm_lateral_catch_basin_1",
        "htmlId": "sep_storm_lateral_catch_basin_1",
        "label": "분류식 빗물받이 1 우수연결관",
        "system": "separate",
        "waterType": "storm",
        "size": "small",
        "direction": "right-down",
    },
    {
        "id": "sep_storm_lateral_catch_basin_2",
        "swmmId": "sep_storm_lateral_catch_basin_2",
        "htmlId": "sep_storm_lateral_catch_basin_2",
        "label": "분류식 빗물받이 2 우수연결관",
        "system": "separate",
        "waterType": "storm",
        "size": "small",
        "direction": "right-down",
    },
    {
        "id": "sep_storm_trunk",
        "swmmId": "sep_storm_trunk",
        "htmlId": "sep_storm_trunk",
        "label": "우수 간선관거",
        "system": "separate",
        "waterType": "storm",
        "size": "large",
        "direction": "right",
        "alwaysFlow": True,
    },
    {
        "id": "sep_interceptor",
        "swmmId": "sep_interceptor",
        "htmlId": "sep_interceptor",
        "label": "차집관거",
        "system": "separate",
        "waterType": "sewer",
        "size": "large",
        "direction": "right",
        "alwaysFlow": True,
    },
    {
        "id": "sep_storm_main_1",
        "swmmId": "sep_storm_main_1",
        "htmlId": "sep_storm_main_1",
        "label": "우수 본관 1",
        "system": "separate",
        "waterType": "storm",
        "size": "medium",
        "direction": "right",
        "alwaysFlow": True,
    },
    {
        "id": "sep_storm_main_2",
        "swmmId": "sep_storm_main_2",
        "htmlId": "sep_storm_main_2",
        "label": "우수 본관 2",
        "system": "separate",
        "waterType": "storm",
        "size": "medium",
        "direction": "right",
        "alwaysFlow": True,
    },
    {
        "id": "sep_storm_main_to_trunk",
        "swmmId": "sep_storm_main_to_trunk",
        "htmlId": "sep_storm_main_to_trunk",
        "label": "우수 본관 2에서 우수 간선관거로 내려가는 연결관",
        "system": "separate",
        "waterType": "storm",
        "size": "medium",
        "direction": "right-down",
        "alwaysFlow": True,
    },
    {
        "id": "sep_sewer_main_1",
        "swmmId": "sep_sewer_main_1",
        "htmlId": "sep_sewer_main_1",
        "label": "오수 본관 1",
        "system": "separate",
        "waterType": "sewer",
        "size": "medium",
        "direction": "right",
        "alwaysFlow": True,
    },
    {
        "id": "sep_sewer_main_2",
        "swmmId": "sep_sewer_main_2",
        "htmlId": "sep_sewer_main_2",
        "label": "오수 본관 2",
        "system": "separate",
        "waterType": "sewer",
        "size": "medium",
        "direction": "right",
        "alwaysFlow": True,
    },
    {
        "id": "sep_sewer_main_to_interceptor",
        "swmmId": "sep_sewer_main_to_interceptor",
        "htmlId": "sep_sewer_main_to_interceptor",
        "label": "오수 본관 2에서 차집관거로 내려가는 연결관",
        "system": "separate",
        "waterType": "sewer",
        "size": "medium",
        "direction": "right-down",
        "alwaysFlow": True,
    },
    {
        "id": "storm_pump_discharge_pipe",
        "swmmId": "storm_pump_discharge_pipe",
        "htmlId": "storm_pump_discharge_pipe",
        "label": "펌프 토출관",
        "system": "separate",
        "waterType": "storm",
        "size": "large",
        "direction": "right",
        "alwaysFlow": True,
    },
    {
        "id": "treatment_effluent_pipe",
        "swmmId": "treatment_effluent_pipe",
        "htmlId": "treatment_effluent_pipe",
        "label": "처리수 방류관",
        "system": "treatment",
        "waterType": "treated",
        "size": "large",
        "direction": "right",
        "alwaysFlow": True,
    },
    {
        "id": "comb_sewer_lateral_house_1",
        "swmmId": "comb_sewer_lateral_house_1",
        "htmlId": "comb_sewer_lateral_house_1",
        "label": "합류식 주거지 1 오수연결관",
        "system": "combined",
        "waterType": "sewer",
        "size": "small",
        "direction": "right-down",
    },
    {
        "id": "comb_sewer_lateral_house_2",
        "swmmId": "comb_sewer_lateral_house_2",
        "htmlId": "comb_sewer_lateral_house_2",
        "label": "합류식 주거지 2 오수연결관",
        "system": "combined",
        "waterType": "sewer",
        "size": "small",
        "direction": "right-down",
    },
    {
        "id": "comb_storm_lateral_catch_basin_1",
        "swmmId": "comb_storm_lateral_catch_basin_1",
        "htmlId": "comb_storm_lateral_catch_basin_1",
        "label": "합류식 빗물받이 1 우수연결관",
        "system": "combined",
        "waterType": "storm",
        "size": "small",
        "direction": "right-down",
    },
    {
        "id": "comb_main_1",
        "swmmId": "comb_main_1",
        "htmlId": "comb_main_1",
        "label": "합류식 본관 1",
        "system": "combined",
        "waterType": "combined",
        "size": "medium",
        "direction": "right",
        "alwaysFlow": True,
    },
    {
        "id": "comb_main_2",
        "swmmId": "comb_main_2",
        "htmlId": "comb_main_2",
        "label": "합류식 본관 2",
        "system": "combined",
        "waterType": "combined",
        "size": "medium",
        "direction": "right",
        "alwaysFlow": True,
    },
    {
        "id": "overflow_to_interceptor_drop",
        "swmmId": "overflow_to_interceptor_drop",
        "htmlId": "overflow_to_interceptor_drop",
        "label": "우수토실 일반 유량에서 차집관거로 내려가는 관",
        "system": "combined",
        "waterType": "combined",
        "size": "medium",
        "direction": "down",
        "alwaysFlow": True,
    },
    {
        "id": "overflow_pipe",
        "swmmId": "overflow_pipe",
        "htmlId": "overflow_pipe",
        "label": "월류관",
        "system": "combined",
        "waterType": "overflow",
        "size": "large",
        "direction": "right",
    },
    {
        "id": "comb_storm_lateral_catch_basin_2",
        "swmmId": "comb_storm_lateral_catch_basin_2",
        "htmlId": "comb_storm_lateral_catch_basin_2",
        "label": "합류식 빗물받이 2 우수연결관",
        "system": "combined",
        "waterType": "storm",
        "size": "small",
        "direction": "right-down",
    },
]


ASSET_REGISTRY = [
    {
        "id": "sep_catch_basin_1",
        "swmmId": "sep_catch_basin_1",
        "htmlId": "asset-sep-catch-basin-1",
        "label": "분류식 빗물받이 1",
        "type": "catch_basin",
        "system": "separate",
        "waterType": "storm",
        "domId": "asset-sep-catch-basin-1",
    },
    {
        "id": "sep_catch_basin_2",
        "swmmId": "sep_catch_basin_2",
        "htmlId": "asset-sep-catch-basin-2",
        "label": "분류식 빗물받이 2",
        "type": "catch_basin",
        "system": "separate",
        "waterType": "storm",
        "domId": "asset-sep-catch-basin-2",
    },
    {
        "id": "comb_catch_basin_1",
        "swmmId": "comb_catch_basin_1",
        "htmlId": "asset-comb-catch-basin-1",
        "label": "합류식 빗물받이 1",
        "type": "catch_basin",
        "system": "combined",
        "waterType": "storm",
        "domId": "asset-comb-catch-basin-1",
    },
    {
        "id": "comb_catch_basin_2",
        "swmmId": "comb_catch_basin_2",
        "htmlId": "asset-comb-catch-basin-2",
        "label": "합류식 빗물받이 2",
        "type": "catch_basin",
        "system": "combined",
        "waterType": "storm",
        "domId": "asset-comb-catch-basin-2",
    },
    {
        "id": "sep_sewer_manhole",
        "swmmId": "sep_sewer_manhole",
        "htmlId": "asset-sep-sewer-manhole",
        "label": "분류식 오수 맨홀",
        "type": "manhole",
        "system": "separate",
        "waterType": "sewer",
        "domId": "asset-sep-sewer-manhole",
    },
    {
        "id": "sep_storm_manhole",
        "swmmId": "sep_storm_manhole",
        "htmlId": "asset-sep-storm-manhole",
        "label": "분류식 우수 맨홀",
        "type": "manhole",
        "system": "separate",
        "waterType": "storm",
        "domId": "asset-sep-storm-manhole",
    },
    {
        "id": "combined_manhole",
        "swmmId": "combined_manhole",
        "htmlId": "asset-combined-manhole",
        "label": "합류식 맨홀",
        "type": "manhole",
        "system": "combined",
        "waterType": "combined",
        "domId": "asset-combined-manhole",
    },
    {
        "id": "overflow_chamber",
        "swmmId": "overflow_chamber",
        "htmlId": "asset-overflow-chamber",
        "label": "우수토실-월류시설",
        "type": "overflow_facility",
        "system": "combined",
        "waterType": "combined",
        "domId": "asset-overflow-chamber",
    },
    {
        "id": "storm_pump_station",
        "swmmId": "storm_pump_station",
        "htmlId": "asset-storm-pump-station",
        "label": "빗물펌프장",
        "type": "pump_station",
        "system": "separate",
        "waterType": "storm",
        "domId": "asset-storm-pump-station",
    },
    {
        "id": "water_reclamation_center",
        "swmmId": "water_reclamation_center",
        "htmlId": "asset-water-reclamation-center",
        "label": "물재생센터",
        "type": "treatment_facility",
        "system": "treatment",
        "waterType": "treated",
        "domId": "asset-water-reclamation-center",
    },
    {
        "id": "overflow_outfall",
        "swmmId": "overflow_outfall",
        "htmlId": "asset-overflow-outfall",
        "label": "월류 방류구",
        "type": "outfall",
        "system": "combined",
        "waterType": "overflow",
        "domId": "asset-overflow-outfall",
    },
    {
        "id": "pump_outfall",
        "swmmId": "pump_outfall",
        "htmlId": "asset-pump-outfall",
        "label": "펌프 방류구",
        "type": "outfall",
        "system": "separate",
        "waterType": "storm",
        "domId": "asset-pump-outfall",
    },
    {
        "id": "treated_outfall",
        "swmmId": "treated_outfall",
        "htmlId": "asset-treated-outfall",
        "label": "처리수 방류구",
        "type": "outfall",
        "system": "treatment",
        "waterType": "treated",
        "domId": "asset-treated-outfall",
    },
]


SURFACE_REGISTRY = [
    {
        "id": "sep_apartment_1",
        "swmmId": "sep_apartment_1",
        "label": "분류식 아파트 1",
        "type": "apartment",
        "system": "separate",
        "waterType": "sewer",
    },
    {
        "id": "sep_apartment_2",
        "swmmId": "sep_apartment_2",
        "label": "분류식 아파트 2",
        "type": "apartment",
        "system": "separate",
        "waterType": "sewer",
    },
    {
        "id": "comb_house_1",
        "swmmId": "comb_house_1",
        "label": "합류식 주거지 1",
        "type": "house",
        "system": "combined",
        "waterType": "sewer",
    },
    {
        "id": "comb_house_2",
        "swmmId": "comb_house_2",
        "label": "합류식 주거지 2",
        "type": "house",
        "system": "combined",
        "waterType": "sewer",
    },
]


MODEL_ONLY_NODE_REGISTRY = [
    {"id": "sep_sewer_upstream", "swmmId": "sep_sewer_upstream", "label": "분류식 오수 상류 계산 노드"},
    {"id": "sep_sewer_downstream", "swmmId": "sep_sewer_downstream", "label": "분류식 오수 하류 계산 노드"},
    {"id": "sep_interceptor_join", "swmmId": "sep_interceptor_join", "label": "차집관거 합류 계산 노드"},
    {"id": "sep_storm_upstream", "swmmId": "sep_storm_upstream", "label": "분류식 우수 상류 계산 노드"},
    {"id": "sep_storm_downstream", "swmmId": "sep_storm_downstream", "label": "분류식 우수 하류 계산 노드"},
    {"id": "sep_storm_trunk_inlet", "swmmId": "sep_storm_trunk_inlet", "label": "우수 간선관거 유입 계산 노드"},
    {"id": "comb_upstream", "swmmId": "comb_upstream", "label": "합류식 상류 계산 노드"},
    {"id": "pump_discharge_node", "swmmId": "pump_discharge_node", "label": "펌프 토출 계산 노드"},
]


CONTROL_REGISTRY = [
    {
        "id": "storm_pump_unit",
        "swmmId": "storm_pump_unit",
        "label": "빗물펌프 가동 제어",
        "type": "pump",
        "targetId": "storm_pump_station",
        "settingKey": "target_setting",
        "min": 0.0,
        "max": 1.0,
    },
    {
        "id": "overflow_to_interceptor_drop",
        "swmmId": "overflow_to_interceptor_drop",
        "label": "우수토실 일반 유량부 개도 제어",
        "type": "orifice",
        "targetId": "overflow_chamber",
        "settingKey": "target_setting",
        "min": 0.0,
        "max": 1.0,
    },
]


PIPE_PHYSICS_BY_ID = {
    "sep_sewer_lateral_apartment_1": {"linkType": "CONDUIT", "fromNode": "sep_apartment_1", "toNode": "sep_sewer_manhole", "lengthM": 55, "diameterM": 0.45, "roughnessN": 0.015, "slope": 0.051818, "bendLossK": 0.35, "maxFlowCms": 0},
    "sep_sewer_lateral_apartment_2": {"linkType": "CONDUIT", "fromNode": "sep_apartment_2", "toNode": "sep_sewer_manhole", "lengthM": 55, "diameterM": 0.45, "roughnessN": 0.015, "slope": 0.050000, "bendLossK": 0.35, "maxFlowCms": 0},
    "sep_storm_lateral_catch_basin_1": {"linkType": "CONDUIT", "fromNode": "sep_catch_basin_1", "toNode": "sep_storm_manhole", "lengthM": 42, "diameterM": 0.45, "roughnessN": 0.018, "slope": 0.055952, "bendLossK": 0.35, "maxFlowCms": 0},
    "sep_storm_lateral_catch_basin_2": {"linkType": "CONDUIT", "fromNode": "sep_catch_basin_2", "toNode": "sep_storm_manhole", "lengthM": 42, "diameterM": 0.45, "roughnessN": 0.018, "slope": 0.053571, "bendLossK": 0.35, "maxFlowCms": 0},
    "sep_storm_trunk": {"linkType": "CONDUIT", "fromNode": "sep_storm_trunk_inlet", "toNode": "storm_pump_station", "lengthM": 520, "diameterM": 1.60, "roughnessN": 0.015, "slope": 0.001346, "bendLossK": 0, "maxFlowCms": 0},
    "sep_interceptor": {"linkType": "CONDUIT", "fromNode": "sep_interceptor_join", "toNode": "water_reclamation_center", "lengthM": 620, "diameterM": 1.60, "roughnessN": 0.016, "slope": 0.001129, "bendLossK": 0, "maxFlowCms": 1.45},
    "sep_storm_main_1": {"linkType": "CONDUIT", "fromNode": "sep_storm_upstream", "toNode": "sep_storm_manhole", "lengthM": 260, "diameterM": 1.20, "roughnessN": 0.015, "slope": 0.001154, "bendLossK": 0, "maxFlowCms": 0},
    "sep_storm_main_2": {"linkType": "CONDUIT", "fromNode": "sep_storm_manhole", "toNode": "sep_storm_downstream", "lengthM": 310, "diameterM": 1.20, "roughnessN": 0.015, "slope": 0.001290, "bendLossK": 0, "maxFlowCms": 0},
    "sep_storm_main_to_trunk": {"linkType": "CONDUIT", "fromNode": "sep_storm_downstream", "toNode": "sep_storm_trunk_inlet", "lengthM": 120, "diameterM": 1.20, "roughnessN": 0.015, "slope": 0.004167, "bendLossK": 0.35, "maxFlowCms": 0},
    "sep_sewer_main_1": {"linkType": "CONDUIT", "fromNode": "sep_sewer_upstream", "toNode": "sep_sewer_manhole", "lengthM": 230, "diameterM": 1.05, "roughnessN": 0.015, "slope": 0.001087, "bendLossK": 0, "maxFlowCms": 0},
    "sep_sewer_main_2": {"linkType": "CONDUIT", "fromNode": "sep_sewer_manhole", "toNode": "sep_sewer_downstream", "lengthM": 260, "diameterM": 1.05, "roughnessN": 0.015, "slope": 0.001346, "bendLossK": 0, "maxFlowCms": 0},
    "sep_sewer_main_to_interceptor": {"linkType": "CONDUIT", "fromNode": "sep_sewer_downstream", "toNode": "sep_interceptor_join", "lengthM": 110, "diameterM": 1.05, "roughnessN": 0.015, "slope": 0.005000, "bendLossK": 0.35, "maxFlowCms": 0},
    "storm_pump_discharge_pipe": {"linkType": "CONDUIT", "fromNode": "pump_discharge_node", "toNode": "pump_outfall", "lengthM": 240, "diameterM": 1.35, "roughnessN": 0.013, "slope": 0.003958, "bendLossK": 0, "maxFlowCms": 0},
    "treatment_effluent_pipe": {"linkType": "CONDUIT", "fromNode": "water_reclamation_center", "toNode": "treated_outfall", "lengthM": 360, "diameterM": 1.35, "roughnessN": 0.014, "slope": 0.002222, "bendLossK": 0, "maxFlowCms": 1.30},
    "comb_sewer_lateral_house_1": {"linkType": "CONDUIT", "fromNode": "comb_house_1", "toNode": "combined_manhole", "lengthM": 58, "diameterM": 0.45, "roughnessN": 0.015, "slope": 0.047414, "bendLossK": 0.35, "maxFlowCms": 0},
    "comb_sewer_lateral_house_2": {"linkType": "CONDUIT", "fromNode": "comb_house_2", "toNode": "combined_manhole", "lengthM": 58, "diameterM": 0.45, "roughnessN": 0.015, "slope": 0.045690, "bendLossK": 0.35, "maxFlowCms": 0},
    "comb_storm_lateral_catch_basin_1": {"linkType": "CONDUIT", "fromNode": "comb_catch_basin_1", "toNode": "combined_manhole", "lengthM": 48, "diameterM": 0.45, "roughnessN": 0.018, "slope": 0.053125, "bendLossK": 0.35, "maxFlowCms": 0},
    "comb_main_1": {"linkType": "CONDUIT", "fromNode": "comb_upstream", "toNode": "combined_manhole", "lengthM": 330, "diameterM": 1.20, "roughnessN": 0.015, "slope": 0.001061, "bendLossK": 0, "maxFlowCms": 0},
    "comb_main_2": {"linkType": "CONDUIT", "fromNode": "combined_manhole", "toNode": "overflow_chamber", "lengthM": 360, "diameterM": 1.20, "roughnessN": 0.015, "slope": 0.001667, "bendLossK": 0, "maxFlowCms": 0},
    "overflow_to_interceptor_drop": {"linkType": "ORIFICE", "fromNode": "overflow_chamber", "toNode": "sep_interceptor_join", "lengthM": 70, "diameterM": 0.95, "roughnessN": 0.015, "slope": 0.002857, "bendLossK": 0.65, "maxFlowCms": 0},
    "overflow_pipe": {"linkType": "CONDUIT", "fromNode": "overflow_chamber", "toNode": "overflow_outfall", "lengthM": 280, "diameterM": 1.35, "roughnessN": 0.016, "slope": 0.005357, "bendLossK": 0, "maxFlowCms": 0},
    "comb_storm_lateral_catch_basin_2": {"linkType": "CONDUIT", "fromNode": "comb_catch_basin_2", "toNode": "combined_manhole", "lengthM": 48, "diameterM": 0.45, "roughnessN": 0.018, "slope": 0.051042, "bendLossK": 0.35, "maxFlowCms": 0},
}


NODE_PHYSICS_BY_ID = {
    "sep_apartment_1": {"nodeType": "JUNCTIONS", "elevationM": 11.30, "maxDepthM": 1.00, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "sep_apartment_2": {"nodeType": "JUNCTIONS", "elevationM": 11.20, "maxDepthM": 1.00, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "sep_catch_basin_1": {"nodeType": "JUNCTIONS", "elevationM": 11.00, "maxDepthM": 1.20, "initialDepthM": 0, "surchargeDepthM": 0.70, "pondedAreaM2": 12},
    "sep_catch_basin_2": {"nodeType": "JUNCTIONS", "elevationM": 10.90, "maxDepthM": 1.20, "initialDepthM": 0, "surchargeDepthM": 0.70, "pondedAreaM2": 12},
    "sep_sewer_upstream": {"nodeType": "JUNCTIONS", "elevationM": 8.70, "maxDepthM": 2.00, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "sep_sewer_manhole": {"nodeType": "JUNCTIONS", "elevationM": 8.45, "maxDepthM": 3.60, "initialDepthM": 0, "surchargeDepthM": 1.20, "pondedAreaM2": 20},
    "sep_sewer_downstream": {"nodeType": "JUNCTIONS", "elevationM": 8.10, "maxDepthM": 2.40, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "sep_interceptor_join": {"nodeType": "JUNCTIONS", "elevationM": 7.55, "maxDepthM": 3.00, "initialDepthM": 0, "surchargeDepthM": 1.00, "pondedAreaM2": 20},
    "sep_storm_upstream": {"nodeType": "JUNCTIONS", "elevationM": 8.95, "maxDepthM": 2.40, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "sep_storm_manhole": {"nodeType": "JUNCTIONS", "elevationM": 8.65, "maxDepthM": 3.20, "initialDepthM": 0, "surchargeDepthM": 1.20, "pondedAreaM2": 20},
    "sep_storm_downstream": {"nodeType": "JUNCTIONS", "elevationM": 8.25, "maxDepthM": 2.80, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "sep_storm_trunk_inlet": {"nodeType": "JUNCTIONS", "elevationM": 7.75, "maxDepthM": 3.00, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "comb_house_1": {"nodeType": "JUNCTIONS", "elevationM": 11.10, "maxDepthM": 1.00, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "comb_house_2": {"nodeType": "JUNCTIONS", "elevationM": 11.00, "maxDepthM": 1.00, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "comb_catch_basin_1": {"nodeType": "JUNCTIONS", "elevationM": 10.90, "maxDepthM": 1.20, "initialDepthM": 0, "surchargeDepthM": 0.70, "pondedAreaM2": 12},
    "comb_catch_basin_2": {"nodeType": "JUNCTIONS", "elevationM": 10.80, "maxDepthM": 1.20, "initialDepthM": 0, "surchargeDepthM": 0.70, "pondedAreaM2": 12},
    "comb_upstream": {"nodeType": "JUNCTIONS", "elevationM": 8.70, "maxDepthM": 2.60, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "combined_manhole": {"nodeType": "JUNCTIONS", "elevationM": 8.35, "maxDepthM": 3.50, "initialDepthM": 0, "surchargeDepthM": 1.20, "pondedAreaM2": 20},
    "pump_discharge_node": {"nodeType": "JUNCTIONS", "elevationM": 7.15, "maxDepthM": 2.00, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "storm_pump_station": {"nodeType": "STORAGE", "elevationM": 7.05, "maxDepthM": 3.30, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "overflow_chamber": {"nodeType": "STORAGE", "elevationM": 7.75, "maxDepthM": 2.80, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "water_reclamation_center": {"nodeType": "STORAGE", "elevationM": 6.85, "maxDepthM": 4.00, "initialDepthM": 0.15, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "overflow_outfall": {"nodeType": "OUTFALLS", "elevationM": 6.25, "maxDepthM": 0, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "pump_outfall": {"nodeType": "OUTFALLS", "elevationM": 6.20, "maxDepthM": 0, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
    "treated_outfall": {"nodeType": "OUTFALLS", "elevationM": 6.05, "maxDepthM": 0, "initialDepthM": 0, "surchargeDepthM": 0.50, "pondedAreaM2": 0},
}


def _with_pipe_physics(pipe: dict[str, object]) -> dict[str, object]:
    pipe_id = str(pipe["id"])
    return {
        **pipe,
        "physics": PIPE_PHYSICS_BY_ID.get(pipe_id, {}),
        "blockageControl": {
            "id": f"{pipe_id}__blockage",
            "type": "blockage",
            "targetKind": "pipe",
            "targetId": pipe_id,
            "settingKey": "blockage_ratio",
            "min": 0.0,
            "max": 1.0,
            "implementation": "effective_capacity_scale",
        },
    }


def _with_node_physics(item: dict[str, object]) -> dict[str, object]:
    item_id = str(item["id"])
    swmm_id = str(item.get("swmmId", item_id))
    return {**item, "physics": NODE_PHYSICS_BY_ID.get(swmm_id, {})}


def blockage_controls() -> list[dict[str, object]]:
    controls: list[dict[str, object]] = []
    for pipe in PIPE_REGISTRY:
        enriched = _with_pipe_physics(pipe)
        controls.append(enriched["blockageControl"])
    for asset in ASSET_REGISTRY:
        asset_id = str(asset["id"])
        controls.append({
            "id": f"{asset_id}__blockage",
            "type": "blockage",
            "targetKind": "asset",
            "targetId": asset_id,
            "settingKey": "blockage_ratio",
            "min": 0.0,
            "max": 1.0,
            "implementation": "inlet_or_storage_resistance",
        })
    return controls


def registry_payload() -> dict[str, object]:
    return {
        "version": REGISTRY_VERSION,
        "pipes": [_with_pipe_physics(pipe) for pipe in PIPE_REGISTRY],
        "assets": [_with_node_physics(asset) for asset in ASSET_REGISTRY],
        "surfaces": [_with_node_physics(surface) for surface in SURFACE_REGISTRY],
        "modelOnlyNodes": [_with_node_physics(node) for node in MODEL_ONLY_NODE_REGISTRY],
        "controls": CONTROL_REGISTRY,
        "blockageControls": blockage_controls(),
        "physics": {
            "pipeCapacityRule": "manning_with_effective_capacity_scale",
            "flowTransferRule": "previous_node_outflow_becomes_next_node_inflow",
            "backflowRule": "full_link_plus_upstream_inflow_plus_blockage",
        },
    }


def pipe_ids() -> list[str]:
    return [item["id"] for item in PIPE_REGISTRY]


def asset_ids() -> list[str]:
    return [item["id"] for item in ASSET_REGISTRY]


def surface_ids() -> list[str]:
    return [item["id"] for item in SURFACE_REGISTRY]


def control_ids() -> list[str]:
    return [item["id"] for item in CONTROL_REGISTRY]


def _find_duplicate_ids(items: Iterable[dict[str, object]], group_name: str) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        item_id = str(item["id"])
        if item_id in seen:
            duplicates.add(item_id)
        seen.add(item_id)
    return [f"Duplicate {group_name} id: {item_id}" for item_id in sorted(duplicates)]


def validate_registry_against_model(
    *,
    swmm_links: set[str],
    swmm_nodes: set[str],
) -> list[str]:
    errors: list[str] = []
    errors.extend(_find_duplicate_ids(PIPE_REGISTRY, "pipe"))
    errors.extend(_find_duplicate_ids(ASSET_REGISTRY, "asset"))
    errors.extend(_find_duplicate_ids(SURFACE_REGISTRY, "surface"))
    errors.extend(_find_duplicate_ids(MODEL_ONLY_NODE_REGISTRY, "model-only node"))
    errors.extend(_find_duplicate_ids(CONTROL_REGISTRY, "control"))

    all_node_items = ASSET_REGISTRY + SURFACE_REGISTRY + MODEL_ONLY_NODE_REGISTRY
    missing_pipes = sorted(str(item["swmmId"]) for item in PIPE_REGISTRY if item["swmmId"] not in swmm_links)
    missing_nodes = sorted(str(item["swmmId"]) for item in all_node_items if item["swmmId"] not in swmm_nodes)
    missing_controls = sorted(str(item["swmmId"]) for item in CONTROL_REGISTRY if item["swmmId"] not in swmm_links)

    if missing_pipes:
        errors.append(f"Missing SWMM links for registry pipes: {', '.join(missing_pipes)}")
    if missing_nodes:
        errors.append(f"Missing SWMM nodes for registry nodes: {', '.join(missing_nodes)}")
    if missing_controls:
        errors.append(f"Missing SWMM links for registry controls: {', '.join(missing_controls)}")

    return errors


def write_registry_json(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(registry_payload(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_registry_js(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(registry_payload(), ensure_ascii=False, separators=(",", ":"))
    path.write_text(f"window.NETWORK_REGISTRY = {payload};\n", encoding="utf-8")
