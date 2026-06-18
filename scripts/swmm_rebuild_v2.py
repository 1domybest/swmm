#!/usr/bin/env python3
"""Clean SWMM rebuild model.

This file is intentionally separate from design_scenario_builder.py.

Goal:
- keep the existing HTML/SWMM shared IDs as the naming contract
- rebuild the SWMM hydraulic model from first principles
- later replace the old design model only after this model is validated
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from network_registry import ASSET_REGISTRY, PIPE_REGISTRY, SURFACE_REGISTRY


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "seoul_rebuild_v2.inp"
DOC_PATH = ROOT / "docs" / "swmm_rebuild_v2.md"
SWMM_MAP_WIDTH = 5000
SWMM_MAP_HEIGHT = 1900


@dataclass(frozen=True)
class Junction:
    node_id: str
    elevation: float
    max_depth: float
    init_depth: float = 0.0
    sur_depth: float = 0.5
    ponded_area: float = 0.0
    x: int = 0
    y: int = 0


@dataclass(frozen=True)
class Storage:
    node_id: str
    elevation: float
    max_depth: float
    init_depth: float = 0.0
    shape: str = "FUNCTIONAL"
    storage_param: float = 1.0
    evap_factor: float = 0.0
    x: int = 0
    y: int = 0


@dataclass(frozen=True)
class Outfall:
    node_id: str
    elevation: float
    outfall_type: str = "FREE"
    gated: str = "NO"
    x: int = 0
    y: int = 0


@dataclass(frozen=True)
class Conduit:
    link_id: str
    from_node: str
    to_node: str
    length: float
    roughness: float
    diameter: float
    in_offset: float = 0.0
    out_offset: float = 0.0
    init_flow: float = 0.0
    max_flow: float = 0.0
    shape: str = "CIRCULAR"
    geom2: float = 0.0
    geom3: float = 0.0
    geom4: float = 0.0
    barrels: int = 1
    culvert: int = 0
    inlet_loss: float = 0.0
    outlet_loss: float = 0.0
    average_loss: float = 0.0
    flap_gate: str = "NO"
    seepage_rate: float = 0.0


@dataclass(frozen=True)
class Orifice:
    link_id: str
    from_node: str
    to_node: str
    orifice_type: str
    offset: float
    qcoeff: float
    gated: str = "NO"
    close_time: float = 0.0
    shape: str = "CIRCULAR"
    geom1: float = 0.45
    geom2: float = 0.0
    geom3: float = 0.0
    geom4: float = 0.0
    barrels: int = 1
    culvert: int = 0


@dataclass(frozen=True)
class Weir:
    link_id: str
    from_node: str
    to_node: str
    weir_type: str
    crest_height: float
    qcoeff: float
    gated: str = "NO"
    end_contractions: int = 0
    end_coeff: float = 0.0
    surcharge: str = "YES"
    road_width: float = 0.0
    road_surface: str = ""
    shape: str = "RECT_OPEN"
    geom1: float = 1.00
    geom2: float = 2.40
    geom3: float = 0.0
    geom4: float = 0.0
    barrels: int = 1
    culvert: int = 0


@dataclass(frozen=True)
class Pump:
    link_id: str
    from_node: str
    to_node: str
    curve_id: str
    status: str = "OFF"
    startup_depth: float = 0.80
    shutoff_depth: float = 0.25


@dataclass(frozen=True)
class PumpCurve:
    curve_id: str
    curve_type: str
    points: tuple[tuple[float, float], ...]


HTML_ID_CONTRACT = {
    "pipes": [str(item["id"]) for item in PIPE_REGISTRY],
    "assets": [str(item["id"]) for item in ASSET_REGISTRY],
    "surfaces": [str(item["id"]) for item in SURFACE_REGISTRY],
}


# v2 design rules fixed by discussion:
# - horizontal main conduits start with Manning n = 0.015
# - horizontal small storm laterals start with Manning n = 0.018
# - conduit slope is calculated from node invert elevations, offsets, and length
# - SVG x/y coordinates are display-only and do not drive velocity
# - a lateral cannot enter the middle of a SWMM conduit, so the main is split at a join node
# - visually vertical drop pipes are modeled as hydraulic-equivalent drop conduits,
#   not literal 90-degree conduits; this avoids unstable 100% slopes in SWMM.

SMALL_DROP_EQUIVALENT_LENGTH = 30.0
MEDIUM_DROP_EQUIVALENT_LENGTH = 40.0

JUNCTIONS = [
    # Surface/runoff collection node above the grate. Inlet blockage is controlled by the inlet orifice.
    Junction(
        "road_runoff_sep_catch_basin_1",
        elevation=12.20,
        max_depth=0.35,
        sur_depth=0.40,
        ponded_area=18.0,
        x=1195,
        y=246,
    ),
    Junction(
        "road_runoff_sep_catch_basin_2",
        elevation=12.20,
        max_depth=0.35,
        sur_depth=0.40,
        ponded_area=18.0,
        x=1985,
        y=246,
    ),
    # Separate sanitary system: visible apartment sewage sources and model-only upstream sewage.
    Junction(
        "sep_apartment_1",
        elevation=11.35,
        max_depth=1.00,
        sur_depth=0.50,
        ponded_area=0.0,
        x=245,
        y=218,
    ),
    Junction(
        "sep_apartment_2",
        elevation=11.30,
        max_depth=1.00,
        sur_depth=0.50,
        ponded_area=0.0,
        x=847,
        y=218,
    ),
    Junction(
        "sep_sewer_lateral_apartment_1_elbow_connector",
        elevation=11.33,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=365,
        y=218,
    ),
    Junction(
        "sep_sewer_lateral_apartment_2_elbow_connector",
        elevation=11.28,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=727,
        y=218,
    ),
    Junction(
        "sep_sewer_upstream",
        elevation=8.70,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=0.0,
        x=0,
        y=825,
    ),
    Junction(
        "sep_sewer_main_1_apartment_1_connector",
        elevation=8.55,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=0.0,
        x=365,
        y=825,
    ),
    Junction(
        "sep_sewer_manhole",
        elevation=8.45,
        max_depth=3.60,
        sur_depth=1.20,
        ponded_area=20.0,
        x=546,
        y=825,
    ),
    Junction(
        "sep_sewer_main_2_apartment_2_connector",
        elevation=8.35,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=0.0,
        x=727,
        y=825,
    ),
    Junction(
        "sep_sewer_downstream",
        elevation=8.10,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=0.0,
        x=2170,
        y=825,
    ),
    Junction(
        "sep_sewer_main_to_interceptor_elbow_connector",
        elevation=8.07,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=0.0,
        x=2264,
        y=825,
    ),
    Junction(
        "sep_interceptor_upstream",
        elevation=6.55,
        max_depth=3.20,
        sur_depth=0.80,
        ponded_area=0.0,
        x=0,
        y=1669,
    ),
    Junction(
        "sep_interceptor_join",
        elevation=6.20,
        max_depth=3.20,
        sur_depth=1.00,
        ponded_area=20.0,
        x=2264,
        y=1669,
    ),
    Junction(
        "overflow_interceptor_join",
        elevation=5.65,
        max_depth=3.20,
        sur_depth=1.00,
        ponded_area=20.0,
        x=4753,
        y=1669,
    ),
    Junction(
        "sep_interceptor_downstream",
        elevation=5.60,
        max_depth=3.20,
        sur_depth=0.80,
        ponded_area=0.0,
        x=4978,
        y=1669,
    ),
    Junction(
        "treatment_process_outlet_node",
        elevation=4.95,
        max_depth=3.20,
        sur_depth=0.80,
        ponded_area=0.0,
        x=5578,
        y=1677,
    ),
    Junction(
        "treated_outfall_gate_node",
        elevation=4.86,
        max_depth=3.20,
        sur_depth=0.80,
        ponded_area=0.0,
        x=5870,
        y=1677,
    ),
    # Outlet-side node just outside the catch-basin box.
    Junction(
        "sep_storm_lateral_catch_basin_1_start",
        elevation=11.33,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=1250,
        y=314,
    ),
    # 90-degree elbow connector between horizontal and vertical lateral pipes.
    Junction(
        "sep_storm_lateral_catch_basin_1_elbow_connector",
        elevation=11.31,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=1370,
        y=314,
    ),
    Junction(
        "sep_storm_lateral_catch_basin_2_start",
        elevation=11.33,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=2040,
        y=314,
    ),
    Junction(
        "sep_storm_lateral_catch_basin_2_elbow_connector",
        elevation=11.31,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=2160,
        y=314,
    ),
    # Join node where the catch-basin lateral enters storm main 1.
    Junction(
        "sep_storm_main_1_catch_basin_1_connector",
        elevation=8.75,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=30.0,
        x=1370,
        y=530,
    ),
    # Model-only offscreen catch-basin role for stormwater already collected outside the visible screen.
    Junction(
        "offscreen_catch_basin_storm_main_1",
        elevation=8.95,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=0.0,
        x=0,
        y=530,
    ),
    # Visible storm manhole in the separate-system area.
    Junction(
        "sep_storm_manhole",
        elevation=8.65,
        max_depth=3.55,
        sur_depth=0.50,
        ponded_area=50.0,
        x=1704,
        y=530,
    ),
    # Join node where the second catch-basin lateral will enter storm main 2.
    Junction(
        "sep_storm_main_2_catch_basin_2_connector",
        elevation=8.38,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=30.0,
        x=2160,
        y=530,
    ),
    # End of storm main 2 before the medium drop pipe to the storm trunk.
    Junction(
        "sep_storm_main_2_outlet_connector",
        elevation=8.32,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=50.0,
        x=2240,
        y=530,
    ),
    # Elbow connector for the medium drop pipe from storm main 2 to the storm trunk.
    Junction(
        "sep_storm_main_to_trunk_elbow_connector",
        elevation=8.29,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=50.0,
        x=2355,
        y=530,
    ),
    # Large storm trunk nodes. The trunk is split where the drop pipe enters it.
    Junction(
        "sep_storm_trunk_upstream",
        elevation=6.16,
        max_depth=3.00,
        sur_depth=0.50,
        ponded_area=0.0,
        x=0,
        y=1134,
    ),
    Junction(
        "sep_storm_trunk_main_2_drop_connector",
        elevation=5.60,
        max_depth=3.00,
        sur_depth=0.50,
        ponded_area=0.0,
        x=2355,
        y=1134,
    ),
    Junction(
        "sep_storm_trunk_downstream",
        elevation=5.01,
        max_depth=3.00,
        sur_depth=0.50,
        ponded_area=0.0,
        x=4800,
        y=1134,
    ),
    # Controllable inlet gate node before water enters the pump-station wet well.
    Junction(
        "storm_pump_inlet_gate_node",
        elevation=4.95,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=0.0,
        x=4885,
        y=1138,
    ),
    # Pump discharge node just after the pump link and before the discharge pipe.
    Junction(
        "storm_pump_discharge_node",
        elevation=5.20,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=0.0,
        x=5400,
        y=1139,
    ),
    # Controllable outfall gate node at the downstream end of the pump discharge pipe.
    Junction(
        "pump_outfall_gate_node",
        elevation=5.03,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=0.0,
        x=5870,
        y=1139,
    ),
    # Combined system: visible houses/catch basins plus model-only offscreen inflows.
    Junction(
        "road_runoff_offscreen_comb_catch_basin",
        elevation=12.20,
        max_depth=0.35,
        sur_depth=0.40,
        ponded_area=18.0,
        x=2440,
        y=246,
    ),
    Junction(
        "offscreen_comb_sewer_source",
        elevation=8.88,
        max_depth=1.20,
        sur_depth=0.40,
        ponded_area=0.0,
        x=2440,
        y=638,
    ),
    Junction(
        "offscreen_comb_storm_lateral_start",
        elevation=11.33,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=2480,
        y=314,
    ),
    Junction(
        "offscreen_comb_storm_lateral_elbow_connector",
        elevation=11.31,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=2510,
        y=314,
    ),
    Junction(
        "comb_upstream",
        elevation=8.82,
        max_depth=2.60,
        sur_depth=0.50,
        ponded_area=0.0,
        x=2440,
        y=677,
    ),
    Junction(
        "comb_house_1",
        elevation=11.10,
        max_depth=1.00,
        sur_depth=0.50,
        ponded_area=0.0,
        x=2645,
        y=218,
    ),
    Junction(
        "comb_sewer_lateral_house_1_elbow_connector",
        elevation=11.08,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=2850,
        y=218,
    ),
    Junction(
        "comb_main_house_1_connector",
        elevation=8.60,
        max_depth=2.60,
        sur_depth=0.50,
        ponded_area=0.0,
        x=2850,
        y=677,
    ),
    Junction(
        "comb_house_2",
        elevation=11.00,
        max_depth=1.00,
        sur_depth=0.50,
        ponded_area=0.0,
        x=3075,
        y=218,
    ),
    Junction(
        "comb_sewer_lateral_house_2_elbow_connector",
        elevation=10.98,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=3280,
        y=218,
    ),
    Junction(
        "comb_main_house_2_connector",
        elevation=8.54,
        max_depth=2.60,
        sur_depth=0.50,
        ponded_area=0.0,
        x=3280,
        y=677,
    ),
    Junction(
        "road_runoff_comb_catch_basin_1",
        elevation=12.20,
        max_depth=0.35,
        sur_depth=0.40,
        ponded_area=18.0,
        x=3475,
        y=246,
    ),
    Junction(
        "comb_storm_lateral_catch_basin_1_start",
        elevation=11.33,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=3530,
        y=314,
    ),
    Junction(
        "comb_storm_lateral_catch_basin_1_elbow_connector",
        elevation=11.31,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=3650,
        y=314,
    ),
    Junction(
        "comb_main_catch_basin_1_connector",
        elevation=8.43,
        max_depth=2.60,
        sur_depth=0.50,
        ponded_area=0.0,
        x=3650,
        y=677,
    ),
    Junction(
        "combined_manhole",
        elevation=8.35,
        max_depth=3.50,
        sur_depth=1.20,
        ponded_area=20.0,
        x=3900,
        y=677,
    ),
    Junction(
        "road_runoff_comb_catch_basin_2",
        elevation=12.20,
        max_depth=0.35,
        sur_depth=0.40,
        ponded_area=18.0,
        x=4225,
        y=246,
    ),
    Junction(
        "comb_storm_lateral_catch_basin_2_start",
        elevation=11.28,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=4280,
        y=314,
    ),
    Junction(
        "comb_storm_lateral_catch_basin_2_elbow_connector",
        elevation=11.26,
        max_depth=0.80,
        sur_depth=0.30,
        ponded_area=0.0,
        x=4400,
        y=314,
    ),
    Junction(
        "comb_main_catch_basin_2_connector",
        elevation=8.18,
        max_depth=2.60,
        sur_depth=0.50,
        ponded_area=0.0,
        x=4400,
        y=677,
    ),
    Junction(
        "overflow_normal_flow_node",
        elevation=7.62,
        max_depth=2.80,
        sur_depth=0.50,
        ponded_area=0.0,
        x=4753,
        y=846,
    ),
    Junction(
        "overflow_weir_outlet_node",
        elevation=7.70,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=0.0,
        x=5012,
        y=677,
    ),
    Junction(
        "overflow_outfall_gate_node",
        elevation=6.30,
        max_depth=2.40,
        sur_depth=0.50,
        ponded_area=0.0,
        x=5870,
        y=677,
    ),
]


STORAGES = [
    Storage(
        "sep_catch_basin_1",
        elevation=11.00,
        max_depth=1.20,
        init_depth=0.00,
        storage_param=2.0,
        x=1195,
        y=324,
    ),
    Storage(
        "sep_catch_basin_2",
        elevation=11.00,
        max_depth=1.20,
        init_depth=0.00,
        storage_param=2.0,
        x=1985,
        y=324,
    ),
    Storage(
        "offscreen_comb_catch_basin",
        elevation=11.00,
        max_depth=1.20,
        init_depth=0.00,
        storage_param=2.0,
        x=2440,
        y=324,
    ),
    Storage(
        "comb_catch_basin_1",
        elevation=11.00,
        max_depth=1.20,
        init_depth=0.00,
        storage_param=2.0,
        x=3475,
        y=324,
    ),
    Storage(
        "comb_catch_basin_2",
        elevation=10.95,
        max_depth=1.20,
        init_depth=0.00,
        storage_param=2.0,
        x=4225,
        y=324,
    ),
    Storage(
        "overflow_chamber",
        elevation=7.75,
        max_depth=2.80,
        init_depth=0.00,
        storage_param=45.0,
        x=4752,
        y=680,
    ),
    # Visible storm pump station. In SWMM this is the wet well that receives trunk flow.
    Storage(
        "storm_pump_station",
        elevation=4.70,
        max_depth=2.40,
        init_depth=0.00,
        storage_param=25.0,
        x=5092,
        y=1138,
    ),
    # Visible water reclamation center. In this first model it stores incoming sewage
    # and releases it through a limited treatment-capacity link.
    Storage(
        "water_reclamation_center",
        elevation=5.05,
        max_depth=4.00,
        init_depth=0.15,
        storage_param=120.0,
        x=5270,
        y=1672,
    ),
]


OUTFALLS = [
    Outfall("overflow_outfall", 6.25, x=6028, y=677),
    Outfall("pump_outfall", 5.02, x=6054, y=1139),
    Outfall("treated_outfall", 4.85, x=6028, y=1677),
]


ORIFICES = [
    Orifice(
        "sep_catch_basin_1_inlet_connector",
        "road_runoff_sep_catch_basin_1",
        "sep_catch_basin_1",
        orifice_type="BOTTOM",
        offset=0.00,
        qcoeff=0.65,
        shape="RECT_CLOSED",
        geom1=0.60,
        geom2=0.60,
    ),
    Orifice(
        "sep_catch_basin_1_outlet_connector",
        "sep_catch_basin_1",
        "sep_storm_lateral_catch_basin_1_start",
        orifice_type="SIDE",
        offset=0.33,
        qcoeff=0.65,
        shape="CIRCULAR",
        geom1=0.45,
    ),
    Orifice(
        "sep_catch_basin_2_inlet_connector",
        "road_runoff_sep_catch_basin_2",
        "sep_catch_basin_2",
        orifice_type="BOTTOM",
        offset=0.00,
        qcoeff=0.65,
        shape="RECT_CLOSED",
        geom1=0.60,
        geom2=0.60,
    ),
    Orifice(
        "sep_catch_basin_2_outlet_connector",
        "sep_catch_basin_2",
        "sep_storm_lateral_catch_basin_2_start",
        orifice_type="SIDE",
        offset=0.33,
        qcoeff=0.65,
        shape="CIRCULAR",
        geom1=0.45,
    ),
    Orifice(
        "storm_pump_inlet_gate",
        "storm_pump_inlet_gate_node",
        "storm_pump_station",
        orifice_type="SIDE",
        offset=0.00,
        qcoeff=0.75,
        shape="CIRCULAR",
        geom1=1.80,
    ),
    Orifice(
        "pump_outfall_gate",
        "pump_outfall_gate_node",
        "pump_outfall",
        orifice_type="SIDE",
        offset=0.00,
        qcoeff=0.75,
        shape="CIRCULAR",
        geom1=1.80,
    ),
    Orifice(
        "treated_outfall_gate",
        "treated_outfall_gate_node",
        "treated_outfall",
        orifice_type="SIDE",
        offset=0.00,
        qcoeff=0.75,
        shape="CIRCULAR",
        geom1=1.80,
    ),
    Orifice(
        "offscreen_comb_catch_basin_inlet_connector",
        "road_runoff_offscreen_comb_catch_basin",
        "offscreen_comb_catch_basin",
        orifice_type="BOTTOM",
        offset=0.00,
        qcoeff=0.65,
        shape="RECT_CLOSED",
        geom1=0.60,
        geom2=0.60,
    ),
    Orifice(
        "offscreen_comb_catch_basin_outlet_connector",
        "offscreen_comb_catch_basin",
        "offscreen_comb_storm_lateral_start",
        orifice_type="SIDE",
        offset=0.33,
        qcoeff=0.65,
        shape="CIRCULAR",
        geom1=0.45,
    ),
    Orifice(
        "comb_catch_basin_1_inlet_connector",
        "road_runoff_comb_catch_basin_1",
        "comb_catch_basin_1",
        orifice_type="BOTTOM",
        offset=0.00,
        qcoeff=0.65,
        shape="RECT_CLOSED",
        geom1=0.60,
        geom2=0.60,
    ),
    Orifice(
        "comb_catch_basin_1_outlet_connector",
        "comb_catch_basin_1",
        "comb_storm_lateral_catch_basin_1_start",
        orifice_type="SIDE",
        offset=0.33,
        qcoeff=0.65,
        shape="CIRCULAR",
        geom1=0.45,
    ),
    Orifice(
        "comb_catch_basin_2_inlet_connector",
        "road_runoff_comb_catch_basin_2",
        "comb_catch_basin_2",
        orifice_type="BOTTOM",
        offset=0.00,
        qcoeff=0.65,
        shape="RECT_CLOSED",
        geom1=0.60,
        geom2=0.60,
    ),
    Orifice(
        "comb_catch_basin_2_outlet_connector",
        "comb_catch_basin_2",
        "comb_storm_lateral_catch_basin_2_start",
        orifice_type="SIDE",
        offset=0.33,
        qcoeff=0.65,
        shape="CIRCULAR",
        geom1=0.45,
    ),
    Orifice(
        "overflow_normal_flow_gate",
        "overflow_chamber",
        "overflow_normal_flow_node",
        orifice_type="SIDE",
        offset=0.20,
        qcoeff=0.65,
        shape="CIRCULAR",
        geom1=0.95,
    ),
    Orifice(
        "overflow_outfall_gate",
        "overflow_outfall_gate_node",
        "overflow_outfall",
        orifice_type="SIDE",
        offset=0.00,
        qcoeff=0.75,
        shape="CIRCULAR",
        geom1=1.80,
    ),
]


WEIRS = [
    Weir(
        "overflow_excess_weir",
        "overflow_chamber",
        "overflow_weir_outlet_node",
        weir_type="TRANSVERSE",
        crest_height=1.60,
        qcoeff=1.84,
        gated="NO",
        end_contractions=0,
        end_coeff=0.0,
        surcharge="YES",
        shape="RECT_OPEN",
        geom1=1.00,
        geom2=2.40,
    ),
]


CONDUITS = [
    Conduit(
        "sep_sewer_lateral_apartment_1_horizontal",
        "sep_apartment_1",
        "sep_sewer_lateral_apartment_1_elbow_connector",
        length=18.0,
        roughness=0.015,
        diameter=0.45,
    ),
    Conduit(
        "sep_sewer_lateral_apartment_1_vertical",
        "sep_sewer_lateral_apartment_1_elbow_connector",
        "sep_sewer_main_1_apartment_1_connector",
        length=SMALL_DROP_EQUIVALENT_LENGTH,
        roughness=0.015,
        diameter=0.45,
        average_loss=1.20,
    ),
    Conduit(
        "sep_sewer_lateral_apartment_2_horizontal",
        "sep_apartment_2",
        "sep_sewer_lateral_apartment_2_elbow_connector",
        length=18.0,
        roughness=0.015,
        diameter=0.45,
    ),
    Conduit(
        "sep_sewer_lateral_apartment_2_vertical",
        "sep_sewer_lateral_apartment_2_elbow_connector",
        "sep_sewer_main_2_apartment_2_connector",
        length=SMALL_DROP_EQUIVALENT_LENGTH,
        roughness=0.015,
        diameter=0.45,
        average_loss=1.20,
    ),
    Conduit(
        "sep_sewer_main_1_upstream_segment",
        "sep_sewer_upstream",
        "sep_sewer_main_1_apartment_1_connector",
        length=185.0,
        roughness=0.015,
        diameter=1.05,
    ),
    Conduit(
        "sep_sewer_main_1_downstream_segment",
        "sep_sewer_main_1_apartment_1_connector",
        "sep_sewer_manhole",
        length=45.0,
        roughness=0.015,
        diameter=1.05,
    ),
    Conduit(
        "sep_sewer_main_2_upstream_segment",
        "sep_sewer_manhole",
        "sep_sewer_main_2_apartment_2_connector",
        length=60.0,
        roughness=0.015,
        diameter=1.05,
    ),
    Conduit(
        "sep_sewer_main_2_downstream_segment",
        "sep_sewer_main_2_apartment_2_connector",
        "sep_sewer_downstream",
        length=200.0,
        roughness=0.015,
        diameter=1.05,
    ),
    Conduit(
        "sep_sewer_main_to_interceptor_horizontal",
        "sep_sewer_downstream",
        "sep_sewer_main_to_interceptor_elbow_connector",
        length=24.0,
        roughness=0.015,
        diameter=1.05,
    ),
    Conduit(
        "sep_sewer_main_to_interceptor_vertical",
        "sep_sewer_main_to_interceptor_elbow_connector",
        "sep_interceptor_join",
        length=MEDIUM_DROP_EQUIVALENT_LENGTH,
        roughness=0.015,
        diameter=1.05,
        average_loss=1.50,
    ),
    Conduit(
        "sep_interceptor_upstream_segment",
        "sep_interceptor_upstream",
        "sep_interceptor_join",
        length=460.0,
        roughness=0.016,
        diameter=1.80,
    ),
    Conduit(
        "sep_interceptor_join_to_overflow_segment",
        "sep_interceptor_join",
        "overflow_interceptor_join",
        length=570.0,
        roughness=0.016,
        diameter=1.80,
    ),
    Conduit(
        "sep_interceptor_downstream_segment",
        "overflow_interceptor_join",
        "sep_interceptor_downstream",
        length=50.0,
        roughness=0.016,
        diameter=1.80,
    ),
    Conduit(
        "sep_interceptor_to_reclamation_inlet",
        "sep_interceptor_downstream",
        "water_reclamation_center",
        length=45.0,
        roughness=0.016,
        diameter=1.80,
    ),
    Conduit(
        "treatment_process_limited_outlet",
        "water_reclamation_center",
        "treatment_process_outlet_node",
        length=30.0,
        roughness=0.014,
        diameter=1.20,
        max_flow=0.020,
    ),
    Conduit(
        "treatment_effluent_pipe",
        "treatment_process_outlet_node",
        "treated_outfall_gate_node",
        length=300.0,
        roughness=0.014,
        diameter=1.80,
    ),
    Conduit(
        "sep_storm_lateral_catch_basin_1_horizontal",
        "sep_storm_lateral_catch_basin_1_start",
        "sep_storm_lateral_catch_basin_1_elbow_connector",
        length=18.0,
        roughness=0.018,
        diameter=0.45,
    ),
    Conduit(
        "sep_storm_lateral_catch_basin_1_vertical",
        "sep_storm_lateral_catch_basin_1_elbow_connector",
        "sep_storm_main_1_catch_basin_1_connector",
        length=SMALL_DROP_EQUIVALENT_LENGTH,
        roughness=0.018,
        diameter=0.45,
        average_loss=1.20,
    ),
    Conduit(
        "sep_storm_lateral_catch_basin_2_horizontal",
        "sep_storm_lateral_catch_basin_2_start",
        "sep_storm_lateral_catch_basin_2_elbow_connector",
        length=18.0,
        roughness=0.018,
        diameter=0.45,
    ),
    Conduit(
        "sep_storm_lateral_catch_basin_2_vertical",
        "sep_storm_lateral_catch_basin_2_elbow_connector",
        "sep_storm_main_2_catch_basin_2_connector",
        length=SMALL_DROP_EQUIVALENT_LENGTH,
        roughness=0.018,
        diameter=0.45,
        average_loss=1.20,
    ),
    Conduit(
        "sep_storm_main_1_upstream_segment",
        "offscreen_catch_basin_storm_main_1",
        "sep_storm_main_1_catch_basin_1_connector",
        length=175.0,
        roughness=0.015,
        diameter=1.20,
    ),
    Conduit(
        "sep_storm_main_1_downstream_segment",
        "sep_storm_main_1_catch_basin_1_connector",
        "sep_storm_manhole",
        length=85.0,
        roughness=0.015,
        diameter=1.20,
    ),
    Conduit(
        "sep_storm_main_2_upstream_segment",
        "sep_storm_manhole",
        "sep_storm_main_2_catch_basin_2_connector",
        length=233.0,
        roughness=0.015,
        diameter=1.20,
    ),
    Conduit(
        "sep_storm_main_2_downstream_segment",
        "sep_storm_main_2_catch_basin_2_connector",
        "sep_storm_main_2_outlet_connector",
        length=47.0,
        roughness=0.015,
        diameter=1.20,
    ),
    Conduit(
        "sep_storm_main_to_trunk_horizontal",
        "sep_storm_main_2_outlet_connector",
        "sep_storm_main_to_trunk_elbow_connector",
        length=24.0,
        roughness=0.016,
        diameter=0.80,
    ),
    Conduit(
        "sep_storm_main_to_trunk_vertical",
        "sep_storm_main_to_trunk_elbow_connector",
        "sep_storm_trunk_main_2_drop_connector",
        length=MEDIUM_DROP_EQUIVALENT_LENGTH,
        roughness=0.016,
        diameter=0.80,
        average_loss=1.50,
    ),
    Conduit(
        "sep_storm_trunk_upstream_segment",
        "sep_storm_trunk_upstream",
        "sep_storm_trunk_main_2_drop_connector",
        length=490.0,
        roughness=0.015,
        diameter=1.80,
    ),
    Conduit(
        "sep_storm_trunk_downstream_segment",
        "sep_storm_trunk_main_2_drop_connector",
        "sep_storm_trunk_downstream",
        length=510.0,
        roughness=0.015,
        diameter=1.80,
    ),
    Conduit(
        "sep_storm_trunk_to_pump_station",
        "sep_storm_trunk_downstream",
        "storm_pump_inlet_gate_node",
        length=35.0,
        roughness=0.015,
        diameter=1.80,
    ),
    Conduit(
        "storm_pump_discharge_pipe",
        "storm_pump_discharge_node",
        "pump_outfall_gate_node",
        length=145.0,
        roughness=0.015,
        diameter=1.80,
    ),
    Conduit(
        "offscreen_comb_sewer_lateral",
        "offscreen_comb_sewer_source",
        "comb_upstream",
        length=24.0,
        roughness=0.015,
        diameter=0.45,
    ),
    Conduit(
        "offscreen_comb_storm_lateral_horizontal",
        "offscreen_comb_storm_lateral_start",
        "offscreen_comb_storm_lateral_elbow_connector",
        length=18.0,
        roughness=0.018,
        diameter=0.45,
    ),
    Conduit(
        "offscreen_comb_storm_lateral_vertical",
        "offscreen_comb_storm_lateral_elbow_connector",
        "comb_upstream",
        length=SMALL_DROP_EQUIVALENT_LENGTH,
        roughness=0.018,
        diameter=0.45,
        average_loss=1.20,
    ),
    Conduit(
        "comb_sewer_lateral_house_1_horizontal",
        "comb_house_1",
        "comb_sewer_lateral_house_1_elbow_connector",
        length=18.0,
        roughness=0.015,
        diameter=0.45,
    ),
    Conduit(
        "comb_sewer_lateral_house_1_vertical",
        "comb_sewer_lateral_house_1_elbow_connector",
        "comb_main_house_1_connector",
        length=SMALL_DROP_EQUIVALENT_LENGTH,
        roughness=0.015,
        diameter=0.45,
        average_loss=1.20,
    ),
    Conduit(
        "comb_sewer_lateral_house_2_horizontal",
        "comb_house_2",
        "comb_sewer_lateral_house_2_elbow_connector",
        length=18.0,
        roughness=0.015,
        diameter=0.45,
    ),
    Conduit(
        "comb_sewer_lateral_house_2_vertical",
        "comb_sewer_lateral_house_2_elbow_connector",
        "comb_main_house_2_connector",
        length=SMALL_DROP_EQUIVALENT_LENGTH,
        roughness=0.015,
        diameter=0.45,
        average_loss=1.20,
    ),
    Conduit(
        "comb_storm_lateral_catch_basin_1_horizontal",
        "comb_storm_lateral_catch_basin_1_start",
        "comb_storm_lateral_catch_basin_1_elbow_connector",
        length=18.0,
        roughness=0.018,
        diameter=0.45,
    ),
    Conduit(
        "comb_storm_lateral_catch_basin_1_vertical",
        "comb_storm_lateral_catch_basin_1_elbow_connector",
        "comb_main_catch_basin_1_connector",
        length=SMALL_DROP_EQUIVALENT_LENGTH,
        roughness=0.018,
        diameter=0.45,
        average_loss=1.20,
    ),
    Conduit(
        "comb_storm_lateral_catch_basin_2_horizontal",
        "comb_storm_lateral_catch_basin_2_start",
        "comb_storm_lateral_catch_basin_2_elbow_connector",
        length=18.0,
        roughness=0.018,
        diameter=0.45,
    ),
    Conduit(
        "comb_storm_lateral_catch_basin_2_vertical",
        "comb_storm_lateral_catch_basin_2_elbow_connector",
        "comb_main_catch_basin_2_connector",
        length=SMALL_DROP_EQUIVALENT_LENGTH,
        roughness=0.018,
        diameter=0.45,
        average_loss=1.20,
    ),
    Conduit(
        "comb_main_1_upstream_segment",
        "comb_upstream",
        "comb_main_house_1_connector",
        length=220.0,
        roughness=0.015,
        diameter=1.20,
    ),
    Conduit(
        "comb_main_1_house_1_to_house_2_segment",
        "comb_main_house_1_connector",
        "comb_main_house_2_connector",
        length=60.0,
        roughness=0.015,
        diameter=1.20,
    ),
    Conduit(
        "comb_main_1_house_2_to_catch_basin_1_segment",
        "comb_main_house_2_connector",
        "comb_main_catch_basin_1_connector",
        length=110.0,
        roughness=0.015,
        diameter=1.20,
    ),
    Conduit(
        "comb_main_1_to_manhole_segment",
        "comb_main_catch_basin_1_connector",
        "combined_manhole",
        length=80.0,
        roughness=0.015,
        diameter=1.20,
    ),
    Conduit(
        "comb_main_2_manhole_to_catch_basin_2_segment",
        "combined_manhole",
        "comb_main_catch_basin_2_connector",
        length=120.0,
        roughness=0.015,
        diameter=1.20,
    ),
    Conduit(
        "comb_main_2_downstream_segment",
        "comb_main_catch_basin_2_connector",
        "overflow_chamber",
        length=70.0,
        roughness=0.015,
        diameter=1.20,
    ),
    Conduit(
        "overflow_to_interceptor_drop",
        "overflow_normal_flow_node",
        "overflow_interceptor_join",
        length=MEDIUM_DROP_EQUIVALENT_LENGTH,
        roughness=0.016,
        diameter=0.95,
        average_loss=1.50,
    ),
    Conduit(
        "overflow_pipe",
        "overflow_weir_outlet_node",
        "overflow_outfall_gate_node",
        length=280.0,
        roughness=0.016,
        diameter=1.80,
    ),
]


PUMPS = [
    Pump(
        "storm_pump_unit",
        "storm_pump_station",
        "storm_pump_discharge_node",
        "STORM_PUMP_CURVE",
        status="OFF",
        startup_depth=0.80,
        shutoff_depth=0.25,
    ),
]


PUMP_CURVES = [
    PumpCurve(
        "STORM_PUMP_CURVE",
        "PUMP4",
        (
            (0.00, 0.00),
            (0.50, 0.25),
            (0.80, 0.55),
            (1.50, 1.10),
            (2.20, 1.60),
        ),
    ),
]


INFLOWS = [
    ("offscreen_catch_basin_storm_main_1", "FLOW", "TS_STORM_RAIN", "FLOW", 1.20, 1.00, 0.0),
    ("road_runoff_sep_catch_basin_1", "FLOW", "TS_STORM_RAIN", "FLOW", 0.95, 1.00, 0.0),
    ("road_runoff_sep_catch_basin_2", "FLOW", "TS_STORM_RAIN", "FLOW", 1.05, 1.00, 0.0),
    ("sep_sewer_upstream", "FLOW", "TS_SEWER_DWF", "FLOW", 3.00, 1.00, 0.0),
    ("sep_apartment_1", "FLOW", "TS_SEWER_DWF", "FLOW", 1.40, 1.00, 0.0),
    ("sep_apartment_2", "FLOW", "TS_SEWER_DWF", "FLOW", 1.50, 1.00, 0.0),
    ("road_runoff_offscreen_comb_catch_basin", "FLOW", "TS_STORM_RAIN", "FLOW", 0.85, 1.00, 0.0),
    ("road_runoff_comb_catch_basin_1", "FLOW", "TS_STORM_RAIN", "FLOW", 0.90, 1.00, 0.0),
    ("road_runoff_comb_catch_basin_2", "FLOW", "TS_STORM_RAIN", "FLOW", 0.95, 1.00, 0.0),
    ("offscreen_comb_sewer_source", "FLOW", "TS_SEWER_DWF", "FLOW", 1.20, 1.00, 0.0),
    ("comb_house_1", "FLOW", "TS_SEWER_DWF", "FLOW", 1.00, 1.00, 0.0),
    ("comb_house_2", "FLOW", "TS_SEWER_DWF", "FLOW", 1.10, 1.00, 0.0),
]


TIMESERIES = [
    ("TS_STORM_RAIN", "00:00", 0.0000),
    ("TS_STORM_RAIN", "00:20", 0.0055),
    ("TS_STORM_RAIN", "00:40", 0.0248),
    ("TS_STORM_RAIN", "01:00", 0.0451),
    ("TS_STORM_RAIN", "01:15", 0.0550),
    ("TS_STORM_RAIN", "01:35", 0.0473),
    ("TS_STORM_RAIN", "02:00", 0.0220),
    ("TS_STORM_RAIN", "02:30", 0.0066),
    ("TS_STORM_RAIN", "03:00", 0.0000),
    ("TS_SEWER_DWF", "00:00", 0.0100),
    ("TS_SEWER_DWF", "03:00", 0.0100),
]


def junction_by_id(node_id: str) -> Junction | None:
    return next((node for node in JUNCTIONS if node.node_id == node_id), None)


def storage_by_id(node_id: str) -> Storage | None:
    return next((node for node in STORAGES if node.node_id == node_id), None)


def outfall_by_id(node_id: str) -> Outfall | None:
    return next((node for node in OUTFALLS if node.node_id == node_id), None)


def conduit_by_id(link_id: str) -> Conduit:
    return next(link for link in CONDUITS if link.link_id == link_id)


def orifice_by_id(link_id: str) -> Orifice:
    return next(link for link in ORIFICES if link.link_id == link_id)


def weir_by_id(link_id: str) -> Weir:
    return next(link for link in WEIRS if link.link_id == link_id)


def pump_by_id(link_id: str) -> Pump:
    return next(link for link in PUMPS if link.link_id == link_id)


def node_elevation(node_id: str) -> float:
    junction = junction_by_id(node_id)
    if junction:
        return junction.elevation
    storage = storage_by_id(node_id)
    if storage:
        return storage.elevation
    outfall = outfall_by_id(node_id)
    if outfall:
        return outfall.elevation
    raise KeyError(f"Unknown node: {node_id}")


def conduit_slope(conduit: Conduit) -> float:
    upstream_invert = node_elevation(conduit.from_node) + conduit.in_offset
    downstream_invert = node_elevation(conduit.to_node) + conduit.out_offset
    return (upstream_invert - downstream_invert) / conduit.length


def storage_surface_elevation(storage: Storage) -> float:
    return storage.elevation + storage.max_depth


def swmm_y(html_y: int) -> int:
    """Convert HTML/SVG y-down coordinates to SWMM GUI y-up coordinates."""
    return SWMM_MAP_HEIGHT - html_y


def build_inp() -> str:
    lines: list[str] = []
    add = lines.append

    add("[TITLE]")
    add(";; Seoul drainage model rebuild v2")
    add(";; This file is separate from the old design model.")
    add(";; Existing HTML/SWMM IDs are kept only as the naming contract.")
    add("")
    add("[OPTIONS]")
    add("FLOW_UNITS           CMS")
    add("INFILTRATION         HORTON")
    add("FLOW_ROUTING         DYNWAVE")
    add("LINK_OFFSETS         DEPTH")
    add("MIN_SLOPE            0")
    add("ALLOW_PONDING        YES")
    add("START_DATE           06/11/2026")
    add("START_TIME           00:00:00")
    add("REPORT_START_DATE    06/11/2026")
    add("REPORT_START_TIME    00:00:00")
    add("END_DATE             06/11/2026")
    add("END_TIME             03:00:00")
    add("REPORT_STEP          00:00:01")
    add("WET_STEP             00:00:01")
    add("DRY_STEP             00:01:00")
    add("ROUTING_STEP         00:00:01")
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
    for node in JUNCTIONS:
        add(f"{node.node_id:<42} {node.elevation:<8.2f} {node.max_depth:<8.2f} {node.init_depth:<9.2f} {node.sur_depth:<8.2f} {node.ponded_area:.1f}")
    add("")
    add("[STORAGE]")
    add(";;Name                         Elev     MaxDepth InitDepth Shape      Curve/Params          N/A  Fevap Psi Ksat IMD")
    for node in STORAGES:
        add(f"{node.node_id:<42} {node.elevation:<8.2f} {node.max_depth:<8.2f} {node.init_depth:<9.2f} {node.shape:<10} {node.storage_param:<7.1f} 0      {node.evap_factor:.0f}      0    0")
    add("")
    add("[OUTFALLS]")
    add(";;Name                         Elev     Type       Stage Data       Gated")
    for node in OUTFALLS:
        add(f"{node.node_id:<42} {node.elevation:<8.2f} {node.outfall_type:<10} {'':<16} {node.gated}")
    add("")
    add("[ORIFICES]")
    add(";;Name                         From Node                    To Node                      Type   Offset Qcoeff Gated CloseTime")
    for link in ORIFICES:
        add(f"{link.link_id:<42} {link.from_node:<42} {link.to_node:<42} {link.orifice_type:<6} {link.offset:<6.2f} {link.qcoeff:<6.2f} {link.gated:<5} {link.close_time:.0f}")
    add("")
    add("[WEIRS]")
    add(";;Name                         From Node                    To Node                      Type       CrestHt Qcoeff Gated EndCon EndCoeff Surcharge RoadWidth RoadSurf")
    for link in WEIRS:
        add(f"{link.link_id:<42} {link.from_node:<42} {link.to_node:<42} {link.weir_type:<10} {link.crest_height:<7.2f} {link.qcoeff:<6.2f} {link.gated:<5} {link.end_contractions:<6} {link.end_coeff:<8.2f} {link.surcharge:<9} {link.road_width:<9.2f} {link.road_surface}")
    add("")
    add("[PUMPS]")
    add(";;Name                         From Node                    To Node                      Pump Curve        Status Startup Shutoff")
    for link in PUMPS:
        add(f"{link.link_id:<42} {link.from_node:<42} {link.to_node:<42} {link.curve_id:<17} {link.status:<6} {link.startup_depth:<7.2f} {link.shutoff_depth:.2f}")
    add("")
    add("[CONDUITS]")
    add(";;Name                         From Node                    To Node                      Length Roughness InOffset OutOffset InitFlow MaxFlow")
    for link in CONDUITS:
        add(f"{link.link_id:<42} {link.from_node:<42} {link.to_node:<42} {link.length:<6.2f} {link.roughness:<9.3f} {link.in_offset:<8.2f} {link.out_offset:<9.2f} {link.init_flow:<8.2f} {link.max_flow:.2f}")
    add("")
    add("[XSECTIONS]")
    add(";;Link                         Shape      Geom1 Geom2 Geom3 Geom4 Barrels Culvert")
    for link in ORIFICES:
        add(f"{link.link_id:<42} {link.shape:<10} {link.geom1:<5.2f} {link.geom2:<5.2f} {link.geom3:<5.2f} {link.geom4:<5.2f} {link.barrels:<7} {link.culvert}")
    for link in CONDUITS:
        add(f"{link.link_id:<42} {link.shape:<10} {link.diameter:<5.2f} {link.geom2:<5.2f} {link.geom3:<5.2f} {link.geom4:<5.2f} {link.barrels:<7} {link.culvert}")
    for link in WEIRS:
        add(f"{link.link_id:<42} {link.shape:<10} {link.geom1:<5.2f} {link.geom2:<5.2f} {link.geom3:<5.2f} {link.geom4:<5.2f} {link.barrels:<7} {link.culvert}")
    add("")
    add("[LOSSES]")
    add(";;Link                         InletLoss OutletLoss AverageLoss FlapGate SeepageRate")
    for link in CONDUITS:
        add(f"{link.link_id:<42} {link.inlet_loss:<9.2f} {link.outlet_loss:<10.2f} {link.average_loss:<11.2f} {link.flap_gate:<8} {link.seepage_rate:.2f}")
    add("")
    add("[INFLOWS]")
    add(";;Node                         Constituent Time Series       Type   Mfactor Sfactor Baseline Pattern")
    for node_id, constituent, series, inflow_type, mfactor, sfactor, baseline in INFLOWS:
        add(f"{node_id:<42} {constituent:<11} {series:<17} {inflow_type:<6} {mfactor:<7.2f} {sfactor:<8.2f} {baseline:.2f}")
    add("")
    add("[TIMESERIES]")
    add(";;Name                         Time      Value")
    for name, time, value in TIMESERIES:
        add(f"{name:<42} {time:<8} {value:.4f}")
    add("")
    add("[CURVES]")
    add(";;Name                         Type   X-Value  Y-Value")
    for curve in PUMP_CURVES:
        for index, (x_value, y_value) in enumerate(curve.points):
            curve_type = curve.curve_type if index == 0 else ""
            curve_id = curve.curve_id if index == 0 else curve.curve_id
            add(f"{curve_id:<42} {curve_type:<6} {x_value:<8.2f} {y_value:.2f}")
    add("")
    add("[REPORT]")
    add("INPUT      YES")
    add("CONTROLS   YES")
    add("NODES ALL")
    add("LINKS ALL")
    add("")
    add("[MAP]")
    add(f"DIMENSIONS 0 0 {SWMM_MAP_WIDTH} {SWMM_MAP_HEIGHT}")
    add("Units      Meters")
    add("")
    add("[COORDINATES]")
    add(";;Node                         X-Coord          Y-Coord")
    for node in JUNCTIONS:
        add(f"{node.node_id:<42} {node.x:<16} {swmm_y(node.y)}")
    for node in STORAGES:
        add(f"{node.node_id:<42} {node.x:<16} {swmm_y(node.y)}")
    for node in OUTFALLS:
        add(f"{node.node_id:<42} {node.x:<16} {swmm_y(node.y)}")
    add("")
    return "\n".join(lines) + "\n"


def _conduit_doc(link: Conduit) -> str:
    return f"""관 ID: `{link.link_id}`
→ 이 관의 고유 이름입니다.

상류 노드, 물이 들어오는 곳: `{link.from_node}`
→ 이 관으로 물이 들어오는 시작 노드입니다.

하류 노드, 물이 빠지는 곳: `{link.to_node}`
→ 이 관을 지난 물이 도착하는 노드입니다.

관 길이: {link.length:.2f} m
→ 이 관을 따라 물이 이동하는 실제 길이입니다.

조도계수: {link.roughness:.3f}
→ 관 내부 마찰값입니다.

상류 연결 높이: {link.in_offset:.2f} m
→ 관 입구가 상류 노드 바닥에서 얼마나 위에 붙는지입니다.

하류 연결 높이: {link.out_offset:.2f} m
→ 관 출구가 하류 노드 바닥에서 얼마나 위에 붙는지입니다.

초기 유량: {link.init_flow:.2f}
→ 시작 시점에는 관에 미리 흐르는 물을 따로 넣지 않습니다.

최대 유량 제한: {link.max_flow:.2f}, 제한 없음
→ 별도 상한을 걸지 않고 SWMM이 단면, 경사, 수위 조건으로 계산합니다.

단면 형태: 원형관
→ 관 단면이 원형입니다.

지름: {link.diameter:.2f} m
→ 원형관의 내부 지름입니다.

단면 보조 치수 2: {link.geom2:.0f}
→ 원형관에서는 사용하지 않습니다.

단면 보조 치수 3: {link.geom3:.0f}
→ 원형관에서는 사용하지 않습니다.

단면 보조 치수 4: {link.geom4:.0f}
→ 원형관에서는 사용하지 않습니다.

병렬 관 개수: {link.barrels}
→ 같은 관이 하나만 있다는 뜻입니다.

암거 코드: {link.culvert}
→ 특수 암거 계산을 사용하지 않습니다.

입구 손실계수: {link.inlet_loss:.2f}
→ 입구 손실입니다.

출구 손실계수: {link.outlet_loss:.2f}
→ 출구 손실입니다.

평균 손실계수: {link.average_loss:.2f}
→ 관 전체 또는 꺾임부 추가 손실입니다.

역류 방지문: {'있음' if link.flap_gate == 'YES' else '없음'}
→ 하류 물이 역류하는 것을 막는 플랩게이트 여부입니다.

침투 손실률: {link.seepage_rate:.2f}
→ 관 안의 물이 지반으로 빠져나가는 손실입니다.

상류 노드 바닥 고도: {node_elevation(link.from_node):.2f} m
→ 물이 들어오는 노드의 바닥 높이입니다.

하류 노드 바닥 고도: {node_elevation(link.to_node):.2f} m
→ 물이 빠지는 노드의 바닥 높이입니다.

계산 경사: 약 {conduit_slope(link):.6f}
→ `(상류 고도 + 상류 연결 높이 - 하류 고도 - 하류 연결 높이) / 관 길이`로 계산합니다.

좌표: 표시용, 유속 계산에 직접 영향 없음
→ x, y 좌표는 SWMM GUI 배치용이며 실제 유속은 길이, 고도, 단면, 조도 등으로 계산됩니다.
"""


def _orifice_doc(link: Orifice) -> str:
    shape_desc = "직사각형 입구" if link.shape == "RECT_CLOSED" else "원형 구멍"
    return f"""링크 ID: `{link.link_id}`
→ 이 제어 링크의 고유 이름입니다.

상류 노드, 물이 들어오는 곳: `{link.from_node}`
→ 이 링크로 물이 들어오는 시작 노드입니다.

하류 노드, 물이 빠지는 곳: `{link.to_node}`
→ 이 링크를 지난 물이 도착하는 노드입니다.

링크 종류: ORIFICE
→ 관이라기보다는 입구, 출구, 개구부처럼 물이 통과하는 구멍입니다.

오리피스 타입: {link.orifice_type}
→ `BOTTOM`은 바닥 방향 입구, `SIDE`는 벽면 방향 출구로 봅니다.

연결 높이: {link.offset:.2f} m
→ 상류 노드 바닥에서 이 구멍이 붙는 높이입니다.

유량 계수: {link.qcoeff:.2f}
→ 구멍을 통과하는 유량 계산에 쓰는 계수입니다.

단면 형태: {shape_desc}
→ 이 오리피스의 개구부 형태입니다.

주요 치수 1: {link.geom1:.2f} m
→ 원형이면 지름, 직사각형이면 높이로 봅니다.

주요 치수 2: {link.geom2:.2f} m
→ 직사각형이면 폭입니다. 원형에서는 사용하지 않습니다.

개폐 시간: {link.close_time:.0f}
→ 현재는 닫힘 지연 시간을 두지 않았습니다.

역류 방지문: {'있음' if link.gated == 'YES' else '없음'}
→ 하류 물이 역류하는 것을 막는 게이트 여부입니다.
"""


def _weir_doc(link: Weir) -> str:
    return f"""링크 ID: `{link.link_id}`
→ 이 월류 링크의 고유 이름입니다.

상류 노드, 물이 들어오는 곳: `{link.from_node}`
→ 수위가 올라가는 우수토실 본체입니다.

하류 노드, 물이 빠지는 곳: `{link.to_node}`
→ 월류턱을 넘은 물이 도착하는 월류관 입구 노드입니다.

링크 종류: WEIR
→ 관이 아니라 물이 일정 높이를 넘으면 넘어가는 월류턱입니다.

위어 타입: {link.weir_type}
→ 횡월류 형태로, 수위가 월류턱보다 높아지면 초과 유량이 넘어갑니다.

월류턱 높이: {link.crest_height:.2f} m
→ 우수토실 바닥에서 이 높이까지는 월류가 발생하지 않습니다.

유량 계수: {link.qcoeff:.2f}
→ 월류 유량 계산에 쓰는 계수입니다.

역류 방지문: {'있음' if link.gated == 'YES' else '없음'}
→ 하류 물이 역류하는 것을 막는 게이트 여부입니다.

말단 수축 개수: {link.end_contractions}
→ 월류턱 양끝 수축 효과입니다.

말단 수축 계수: {link.end_coeff:.2f}
→ 말단 수축이 있을 때 쓰는 보정 계수입니다.

잠김 월류 보정: {link.surcharge}
→ 하류 수위 영향으로 월류가 잠기는 상황을 보정할지 여부입니다.

단면 형태: {link.shape}
→ 월류부를 열린 직사각형 단면으로 봅니다.

월류부 깊이: {link.geom1:.2f} m
→ 월류턱을 넘은 뒤 물이 통과할 수 있는 단면의 세로 치수입니다.

월류부 폭: {link.geom2:.2f} m
→ 월류턱을 따라 물이 넘어갈 수 있는 가로 폭입니다.
"""


def _pump_doc(link: Pump) -> str:
    return f"""펌프 ID: `{link.link_id}`
→ 이 펌프의 고유 이름입니다.

상류 노드, 물이 모이는 곳: `{link.from_node}`
→ 펌프가 빨아들이는 빗물펌프장 수조입니다.

하류 노드, 물을 밀어내는 곳: `{link.to_node}`
→ 펌프가 물을 밀어낸 뒤 도착하는 토출 노드입니다.

펌프 곡선: `{link.curve_id}`
→ 펌프장 수위가 높아질수록 펌프 유량이 커지도록 정의한 곡선입니다.

초기 상태: {link.status}
→ 시작 시점에는 펌프를 꺼둡니다. 수위 조건에 따라 켜집니다.

가동 수위: {link.startup_depth:.2f} m
→ 펌프장 수조 수심이 이 값 이상이 되면 펌프가 켜집니다.

정지 수위: {link.shutoff_depth:.2f} m
→ 수조 수심이 이 값 이하로 내려가면 펌프가 꺼집니다.

중요:
→ 펌프는 일반 관처럼 길이와 경사를 가진 배관이 아닙니다. 수조의 물을 토출 노드 쪽으로 강제로 이동시키는 SWMM PUMP 링크입니다.
"""


def build_doc() -> str:
    storage = storage_by_id("sep_catch_basin_1")
    assert storage is not None
    storage2 = storage_by_id("sep_catch_basin_2")
    assert storage2 is not None
    inlet = orifice_by_id("sep_catch_basin_1_inlet_connector")
    outlet = orifice_by_id("sep_catch_basin_1_outlet_connector")
    inlet2 = orifice_by_id("sep_catch_basin_2_inlet_connector")
    outlet2 = orifice_by_id("sep_catch_basin_2_outlet_connector")
    lateral_h = conduit_by_id("sep_storm_lateral_catch_basin_1_horizontal")
    lateral_v = conduit_by_id("sep_storm_lateral_catch_basin_1_vertical")
    lateral2_h = conduit_by_id("sep_storm_lateral_catch_basin_2_horizontal")
    lateral2_v = conduit_by_id("sep_storm_lateral_catch_basin_2_vertical")
    main_up = conduit_by_id("sep_storm_main_1_upstream_segment")
    main_down = conduit_by_id("sep_storm_main_1_downstream_segment")
    main2_up = conduit_by_id("sep_storm_main_2_upstream_segment")
    main2_down = conduit_by_id("sep_storm_main_2_downstream_segment")
    main2_to_trunk_h = conduit_by_id("sep_storm_main_to_trunk_horizontal")
    main2_to_trunk_v = conduit_by_id("sep_storm_main_to_trunk_vertical")
    storm_trunk_up = conduit_by_id("sep_storm_trunk_upstream_segment")
    storm_trunk_down = conduit_by_id("sep_storm_trunk_downstream_segment")
    trunk_to_pump = conduit_by_id("sep_storm_trunk_to_pump_station")
    pump = pump_by_id("storm_pump_unit")
    pump_discharge = conduit_by_id("storm_pump_discharge_pipe")
    pump_storage = storage_by_id("storm_pump_station")
    assert pump_storage is not None
    pump_outfall = outfall_by_id("pump_outfall")
    assert pump_outfall is not None
    sewer_lateral1_h = conduit_by_id("sep_sewer_lateral_apartment_1_horizontal")
    sewer_lateral1_v = conduit_by_id("sep_sewer_lateral_apartment_1_vertical")
    sewer_lateral2_h = conduit_by_id("sep_sewer_lateral_apartment_2_horizontal")
    sewer_lateral2_v = conduit_by_id("sep_sewer_lateral_apartment_2_vertical")
    sewer_main1_up = conduit_by_id("sep_sewer_main_1_upstream_segment")
    sewer_main1_down = conduit_by_id("sep_sewer_main_1_downstream_segment")
    sewer_main2_up = conduit_by_id("sep_sewer_main_2_upstream_segment")
    sewer_main2_down = conduit_by_id("sep_sewer_main_2_downstream_segment")
    sewer_to_interceptor_h = conduit_by_id("sep_sewer_main_to_interceptor_horizontal")
    sewer_to_interceptor_v = conduit_by_id("sep_sewer_main_to_interceptor_vertical")
    interceptor_up = conduit_by_id("sep_interceptor_upstream_segment")
    interceptor_to_overflow_join = conduit_by_id("sep_interceptor_join_to_overflow_segment")
    interceptor_down = conduit_by_id("sep_interceptor_downstream_segment")
    interceptor_to_center = conduit_by_id("sep_interceptor_to_reclamation_inlet")
    treatment_process = conduit_by_id("treatment_process_limited_outlet")
    treatment_effluent = conduit_by_id("treatment_effluent_pipe")
    water_reclamation = storage_by_id("water_reclamation_center")
    assert water_reclamation is not None
    treated_gate = orifice_by_id("treated_outfall_gate")
    treated_outfall = outfall_by_id("treated_outfall")
    assert treated_outfall is not None
    offscreen_comb_cb = storage_by_id("offscreen_comb_catch_basin")
    comb_cb1 = storage_by_id("comb_catch_basin_1")
    comb_cb2 = storage_by_id("comb_catch_basin_2")
    assert offscreen_comb_cb is not None
    assert comb_cb1 is not None
    assert comb_cb2 is not None
    offscreen_comb_cb_inlet = orifice_by_id("offscreen_comb_catch_basin_inlet_connector")
    offscreen_comb_cb_outlet = orifice_by_id("offscreen_comb_catch_basin_outlet_connector")
    comb_cb1_inlet = orifice_by_id("comb_catch_basin_1_inlet_connector")
    comb_cb1_outlet = orifice_by_id("comb_catch_basin_1_outlet_connector")
    comb_cb2_inlet = orifice_by_id("comb_catch_basin_2_inlet_connector")
    comb_cb2_outlet = orifice_by_id("comb_catch_basin_2_outlet_connector")
    offscreen_comb_sewer_lateral = conduit_by_id("offscreen_comb_sewer_lateral")
    offscreen_comb_storm_h = conduit_by_id("offscreen_comb_storm_lateral_horizontal")
    offscreen_comb_storm_v = conduit_by_id("offscreen_comb_storm_lateral_vertical")
    comb_sewer1_h = conduit_by_id("comb_sewer_lateral_house_1_horizontal")
    comb_sewer1_v = conduit_by_id("comb_sewer_lateral_house_1_vertical")
    comb_sewer2_h = conduit_by_id("comb_sewer_lateral_house_2_horizontal")
    comb_sewer2_v = conduit_by_id("comb_sewer_lateral_house_2_vertical")
    comb_storm1_h = conduit_by_id("comb_storm_lateral_catch_basin_1_horizontal")
    comb_storm1_v = conduit_by_id("comb_storm_lateral_catch_basin_1_vertical")
    comb_storm2_h = conduit_by_id("comb_storm_lateral_catch_basin_2_horizontal")
    comb_storm2_v = conduit_by_id("comb_storm_lateral_catch_basin_2_vertical")
    comb_main1_up = conduit_by_id("comb_main_1_upstream_segment")
    comb_main1_h1_h2 = conduit_by_id("comb_main_1_house_1_to_house_2_segment")
    comb_main1_h2_cb1 = conduit_by_id("comb_main_1_house_2_to_catch_basin_1_segment")
    comb_main1_to_manhole = conduit_by_id("comb_main_1_to_manhole_segment")
    comb_main2_to_cb2 = conduit_by_id("comb_main_2_manhole_to_catch_basin_2_segment")
    comb_main2_down = conduit_by_id("comb_main_2_downstream_segment")
    overflow_chamber = storage_by_id("overflow_chamber")
    assert overflow_chamber is not None
    overflow_normal_gate = orifice_by_id("overflow_normal_flow_gate")
    overflow_normal_drop = conduit_by_id("overflow_to_interceptor_drop")
    overflow_excess_weir = weir_by_id("overflow_excess_weir")
    overflow_pipe = conduit_by_id("overflow_pipe")
    overflow_gate = orifice_by_id("overflow_outfall_gate")
    overflow_outfall = outfall_by_id("overflow_outfall")
    assert overflow_outfall is not None

    return f"""# SWMM 모델 재설계 v2

## 방향

- 기존 `design_scenario_builder.py` 모델은 바로 수정하지 않는다.
- 새 모델은 `models/seoul_rebuild_v2.inp`로 따로 만든다.
- 기존 HTML과 맞춘 ID 계약은 유지한다.
- 물리 구조가 검증되면 나중에 기존 모델과 교체한다.

## 유지하는 이름 계약

- HTML 배관 ID 수: {len(HTML_ID_CONTRACT["pipes"])}개
- HTML 시설 ID 수: {len(HTML_ID_CONTRACT["assets"])}개
- HTML 지상 객체 ID 수: {len(HTML_ID_CONTRACT["surfaces"])}개

## 화면 기준 좌표

- 좌표 기준 파일: `viewer/overall_drainage_diagram.html`
- 분류식 첫 빗물받이: `transform="translate(1120,232)"`
- 우수본관1 중심선: `y=530`
- 첫 빗물받이 우수연결관 수평부: 대략 `x=1250 -> 1370`, `y=314`
- 첫 빗물받이 우수연결관 수직부: 대략 `x=1370`, `y=314 -> 530`
- 우수맨홀 축: 대략 `x=1704`, `y=530`
- 우수본관2 중심선: `x=1761 -> 2240`, `y=530`
- 분류식 두 번째 빗물받이: `transform="translate(1910,232)"`
- 두 번째 빗물받이 우수연결관 수평부: 대략 `x=2040 -> 2160`, `y=314`
- 두 번째 빗물받이 우수연결관 수직부: 대략 `x=2160`, `y=314 -> 530`
- 우수본관2 빗물받이2 접합 지점: 대략 `x=2160`, `y=530`
- 우수본관2 하류 끝: 대략 `x=2240`, `y=530`
- 우수본관2에서 우수간선관거로 내려가는 연결관 시작: 대략 `x=2240`, `y=530`
- 우수본관2에서 우수간선관거로 내려가는 ㄱ자 커넥터: 대략 `x=2355`, `y=530`
- 우수간선관거 중심선: `y=1134`
- 우수간선관거: `x=0 -> 4800`, `y=1134`
- 우수간선관거 접합 지점: 대략 `x=2355`, `y=1134`
- 빗물펌프장: `x=4842 -> 5342`, `y=1035 -> 1240`, 중심 대략 `x=5092`, `y=1138`
- 펌프 토출관: 대략 `x=5400 -> 5870`, 중심선 `y=1139`
- 펌프 방류구: `x=5928 -> 6180`, 중심 대략 `x=6054`, `y=1139`
- 물재생센터: `x=5020 -> 5520`, `y=1587 -> 1757`, 중심 대략 `x=5270`, `y=1672`
- 처리수 방류관: `x=5578 -> 5870`, 중심선 `y=1677`
- 처리수 방류구: `x=5928 -> 6180`, 중심 대략 `x=6028`, `y=1677`

주의: 이 x/y는 SWMM GUI 표시용입니다. 유속 계산은 좌표가 아니라 길이, 고도, 단면, 조도, 손실계수로 계산됩니다.

좌표계 주의:
→ `overall_drainage_diagram.html`은 y가 커질수록 화면 아래로 내려갑니다.
→ SWMM GUI는 지도 좌표처럼 y가 커질수록 위로 올라가는 방식으로 표시될 수 있습니다.
→ 그래서 `.inp`에 기록할 때는 `SWMM_Y = {SWMM_MAP_HEIGHT} - HTML_Y`로 변환합니다.
→ 예를 들어 HTML에서 빗물받이 y=324, 우수본관 중심 y=530이면 SWMM에는 빗물받이 y={swmm_y(324)}, 우수본관 y={swmm_y(530)}로 들어가서 빗물받이가 본관 위에 표시됩니다.

## 우수본관1 정의

HTML ID: `sep_storm_main_1`
→ 화면에서는 하나의 우수본관1로 보입니다.

SWMM 계산 구조:
→ SWMM에서는 관 중간에 우수연결관을 바로 꽂을 수 없으므로, 우수본관1을 아래 두 관으로 나눕니다.

1. `sep_storm_main_1_upstream_segment`
2. `sep_storm_main_1_downstream_segment`

중간 접합 노드:
`sep_storm_main_1_catch_basin_1_connector`
→ 빗물받이1 우수연결관이 우수본관1에 들어오는 지점입니다.

### 우수본관1 상류 구간

{_conduit_doc(main_up)}

### 우수본관1 하류 구간

{_conduit_doc(main_down)}

## 우수맨홀 정의

노드 ID: `sep_storm_manhole`
→ 우수본관1에서 온 물을 받고 우수본관2로 넘기는 분류식 우수 맨홀입니다.

SWMM 노드 종류: JUNCTION
→ 관과 관이 만나는 접합 노드입니다. 맨홀 내부 수위, 만관, 월류, 역류 판단 기준점으로 사용합니다.

유입되는 관:
→ `sep_storm_main_1_downstream_segment`

배출되는 관:
→ `sep_storm_main_2_upstream_segment`

바닥 고도: {node_elevation("sep_storm_manhole"):.2f} m
→ 우수맨홀 바닥 높이입니다.

최대 수심: 3.55 m
→ 도로/빗물받이 지표 높이 12.20m와 맨홀 바닥 고도 8.65m를 맞춘 값입니다.

초기 수심: 0.00 m
→ 시작 시점에는 비어 있다고 봅니다.

월류/압력 여유 수심: 0.50 m
→ 맨홀이 꽉 찬 뒤 압력 상태를 조금 허용하는 여유값입니다.

지상 저류 면적: 20.0 m2
→ 맨홀에서 물이 넘쳤을 때 주변 도로에 고일 수 있는 간이 면적입니다.

좌표: x=1704, y=530
→ HTML에서는 맨홀뚜껑 중심이 y=258에 있지만, SWMM GUI에서는 우수본관1/2가 접속되는 중심선 y=530에 맞춥니다.

## 우수본관2 정의

HTML ID: `sep_storm_main_2`
→ 화면에서는 하나의 우수본관2로 보입니다.

SWMM 계산 구조:
→ 우수본관2에도 빗물받이2 우수연결관이 들어올 예정이므로, SWMM에서는 두 개의 관으로 나눕니다.

1. `sep_storm_main_2_upstream_segment`
2. `sep_storm_main_2_downstream_segment`

중간 접합 노드:
`sep_storm_main_2_catch_basin_2_connector`
→ 빗물받이2 우수연결관이 우수본관2에 들어오는 지점입니다.

하류 끝 노드:
`sep_storm_main_2_outlet_connector`
→ 우수본관2가 끝나고, 이후 우수 간선관거로 내려가는 중형 ㄱ자 연결관이 시작될 지점입니다.

### 우수본관2 상류 구간

{_conduit_doc(main2_up)}

### 우수본관2 하류 구간

{_conduit_doc(main2_down)}

이후 흐름:
→ `sep_storm_main_2_outlet_connector`에서 중형 ㄱ자 연결관을 통해 우수간선관거로 내려갑니다.

## 우수본관2에서 우수간선관거로 내려가는 ㄱ자 연결관 정의

HTML ID: `sep_storm_main_to_trunk`
→ 화면에서는 하나의 ㄱ자 연결관처럼 보입니다.

SWMM 계산 구조:
→ SWMM에서는 이 ㄱ자 연결관을 하나의 꺾인 관으로 계산하지 않고, 수평 직관과 수직 직관 2개로 나눕니다.

1. `sep_storm_main_to_trunk_horizontal`
2. `sep_storm_main_to_trunk_vertical`

중간 ㄱ자 커넥터:
`sep_storm_main_to_trunk_elbow_connector`
→ 수평 관과 수직 관이 만나는 꺾임 지점입니다.

하류 접합 노드:
`sep_storm_trunk_main_2_drop_connector`
→ 우수본관2에서 내려온 물이 우수간선관거에 합류하는 지점입니다.

### 우수본관2-우수간선관거 수평 연결관

{_conduit_doc(main2_to_trunk_h)}

### 우수본관2-우수간선관거 수직 연결관

{_conduit_doc(main2_to_trunk_v)}

수직관 해석:
→ SWMM에 “90도 세로관”이라는 별도 옵션이 있는 것은 아닙니다. 대신 상류 고도 8.29m, 하류 고도 5.60m, 길이 2.69m로 두어 거의 수직 낙차에 가까운 흐름으로 계산하게 했습니다.

## 우수간선관거 정의

HTML ID: `sep_storm_trunk`
→ 화면에서는 하나의 큰 우수간선관거로 보입니다.

SWMM 계산 구조:
→ 우수본관2에서 내려오는 연결관이 우수간선관거 중간으로 들어오므로, 우수간선관거도 접합 노드를 기준으로 두 구간으로 나눕니다.

1. `sep_storm_trunk_upstream_segment`
2. `sep_storm_trunk_downstream_segment`

중간 접합 노드:
`sep_storm_trunk_main_2_drop_connector`
→ 우수본관2에서 내려온 물이 우수간선관거에 들어오는 지점입니다.

### 우수간선관거 상류 구간

{_conduit_doc(storm_trunk_up)}

### 우수간선관거 하류 구간

{_conduit_doc(storm_trunk_down)}

이후 흐름:
→ `sep_storm_trunk_downstream`에서 빗물펌프장 수조로 자연 유입됩니다.

## 빗물펌프장 정의

HTML ID: `storm_pump_station`
→ 화면에서는 하나의 빗물펌프장 상자로 보입니다.

SWMM 계산 구조:
→ 빗물펌프장은 단순 관이 아니라 물을 모으는 수조이므로 STORAGE로 정의합니다.

수조 ID: `storm_pump_station`
→ 우수간선관거 하류에서 들어온 물이 잠시 모이는 펌프장 습정/수조입니다.

바닥 고도: {pump_storage.elevation:.2f} m
→ 우수간선관거 하류 노드보다 낮게 두어 자연 유입이 가능하게 했습니다.

최대 수심: {pump_storage.max_depth:.2f} m
→ 펌프장 수조에 물이 찰 수 있는 최대 깊이입니다.

초기 수심: {pump_storage.init_depth:.2f} m
→ 시작 시점에는 비어 있다고 봅니다.

저류 면적 계수: {pump_storage.storage_param:.1f}
→ 펌프장 내부 수조의 간이 저장 용량입니다.

좌표: HTML x={pump_storage.x}, y={pump_storage.y} / SWMM x={pump_storage.x}, y={swmm_y(pump_storage.y)}
→ HTML의 빗물펌프장 중심에 맞춘 뒤, SWMM GUI에 넣을 때는 y축을 뒤집습니다.

## 우수간선관거에서 빗물펌프장으로 들어가는 유입관

{_conduit_doc(trunk_to_pump)}

해석:
→ 이 관은 우수간선관거 바로 옆에 있는 짧은 대형 자연유입관입니다.
→ 상류 관저고는 `sep_storm_trunk_downstream` 고도 {node_elevation("sep_storm_trunk_downstream"):.2f}m입니다.
→ 하류 관저고는 `storm_pump_station` 바닥 고도 {node_elevation("storm_pump_station"):.2f}m + 하류 연결 높이 {trunk_to_pump.out_offset:.2f}m = {node_elevation("storm_pump_station") + trunk_to_pump.out_offset:.2f}m입니다.
→ 따라서 우수간선관거에서 펌프장 쪽으로 아주 완만하게 내려가는 자연유입 구조입니다.

## 펌프 링크 정의

{_pump_doc(pump)}

펌프 곡선:
→ `STORM_PUMP_CURVE`는 수위에 따라 펌프 유량이 증가하는 곡선입니다.
→ 수심 0.00m에서는 유량 0.00 m3/s입니다.
→ 수심 0.80m 부근부터 실제 가동 유량이 커집니다.
→ 수심 2.20m에서는 약 1.60 m3/s까지 배출할 수 있는 간이 펌프로 둡니다.

## 펌프 토출관 정의

HTML ID: `storm_pump_discharge_pipe`
→ 화면에서는 빗물펌프장에서 펌프 방류구로 이어지는 큰 관입니다.

{_conduit_doc(pump_discharge)}

## 펌프 방류구 정의

노드 ID: `pump_outfall`
→ 펌프 토출관의 물이 하천으로 빠지는 방류구입니다.

SWMM 노드 종류: OUTFALL
→ 모델의 최종 배출구입니다.

바닥 고도: {pump_outfall.elevation:.2f} m
→ 펌프 토출관 끝의 방류구 높이입니다.

방류 조건: {pump_outfall.outfall_type}
→ 현재는 자유 방류로 두었습니다. 이후 하천 수위 역류를 반영할 때는 고정 수위 또는 시계열 수위 방류구로 바꿀 수 있습니다.

좌표: HTML x={pump_outfall.x}, y={pump_outfall.y} / SWMM x={pump_outfall.x}, y={swmm_y(pump_outfall.y)}
→ HTML의 펌프 방류구 중심에 맞췄습니다.

## 빗물받이1 정의

노드 ID: `sep_catch_basin_1`
→ 분류식 첫 번째 빗물받이 박스입니다.

SWMM 노드 종류: STORAGE
→ 단순 접합점이 아니라 물이 잠깐 저장되고 차오를 수 있는 박스로 봅니다.

바닥 고도: {storage.elevation:.2f} m
→ 빗물받이 내부 바닥 높이입니다.

최대 수심: {storage.max_depth:.2f} m
→ 빗물받이 내부에서 물이 찰 수 있는 깊이입니다.

지표면/덮개 높이: {storage_surface_elevation(storage):.2f} m
→ 바닥 고도 + 최대 수심입니다.

초기 수심: {storage.init_depth:.2f} m
→ 시작 시점에는 비어 있다고 봅니다.

저류 면적 계수: {storage.storage_param:.1f}
→ 간이 모델이므로 깊이에 따라 저장량을 계산하는 FUNCTIONAL 저장소 계수로 둡니다.

좌표: HTML x={storage.x}, y={storage.y} / SWMM x={storage.x}, y={swmm_y(storage.y)}
→ HTML 빗물받이 박스 중심에 가깝게 맞춘 뒤, SWMM GUI에 넣을 때는 y축을 뒤집습니다.

막힘 표현:
→ 빗물받이 자체가 막히는 상황은 `sep_catch_basin_1_inlet_connector`의 개도/막힘률로 표현합니다.

배출구 막힘 표현:
→ 빗물받이에서 우수연결관으로 빠지는 출구 막힘은 `sep_catch_basin_1_outlet_connector`의 개도/막힘률로 표현합니다.

## 빗물받이1 입구 커넥터

{_orifice_doc(inlet)}

## 빗물받이1 출구 커넥터

{_orifice_doc(outlet)}

중요:
→ 빗물받이 출구는 박스 하단이 아니라 중간 벽면에 붙은 것으로 정의했습니다.

출구 중심 높이: 0.55 m
→ 빗물받이 바닥에서 파이프 중심까지의 높이입니다.

출구 관 지름: 0.45 m
→ 우수연결관 지름입니다.

출구 하단 높이: 약 0.33 m
→ 0.55m - 0.45m / 2 입니다. 이 값이 SIDE 오리피스 offset으로 들어갑니다.

## ㄱ자 우수연결관 정의

구성:
`빗물받이 -> 출구 커넥터 -> 수평 우수연결관 -> ㄱ자 커넥터 -> 수직 우수연결관 -> 본관 접합 커넥터 -> 우수본관1`

### 수평 우수연결관

{_conduit_doc(lateral_h)}

### ㄱ자 커넥터

노드 ID: `sep_storm_lateral_catch_basin_1_elbow_connector`
→ 화면의 ㄱ자 꺾임부를 SWMM에서는 중간 접합 노드로 둡니다.

역할:
→ 수평 관과 수직 관을 연결합니다. 꺾임 손실은 수직 우수연결관의 평균 손실계수에 반영했습니다.

좌표:
→ x=1370, y=314 입니다. HTML의 ㄱ자 꺾임 위치에 맞춘 표시용 좌표입니다.

### 수직 우수연결관

{_conduit_doc(lateral_v)}

수직관 해석:
→ SWMM에 “90도 세로관”이라는 별도 옵션이 있는 것은 아닙니다. 대신 상류 고도 11.31m, 하류 고도 8.75m, 길이 2.56m로 두어 거의 수직 낙차에 가까운 흐름으로 계산하게 했습니다.

## 빗물받이2 정의

노드 ID: `sep_catch_basin_2`
→ 분류식 두 번째 빗물받이 박스입니다.

SWMM 노드 종류: STORAGE
→ 빗물받이1과 같은 방식으로, 물이 저장되고 차오를 수 있는 박스로 봅니다.

바닥 고도: {storage2.elevation:.2f} m
→ 빗물받이 내부 바닥 높이입니다.

최대 수심: {storage2.max_depth:.2f} m
→ 빗물받이 내부에서 물이 찰 수 있는 깊이입니다.

지표면/덮개 높이: {storage_surface_elevation(storage2):.2f} m
→ 바닥 고도 + 최대 수심입니다.

초기 수심: {storage2.init_depth:.2f} m
→ 시작 시점에는 비어 있다고 봅니다.

저류 면적 계수: {storage2.storage_param:.1f}
→ 빗물받이1과 같은 간이 저장소 계수를 사용합니다.

좌표: HTML x={storage2.x}, y={storage2.y} / SWMM x={storage2.x}, y={swmm_y(storage2.y)}
→ HTML의 두 번째 빗물받이 박스 중심에 맞춘 뒤, SWMM GUI에 넣을 때는 y축을 뒤집습니다.

막힘 표현:
→ 빗물받이 자체가 막히는 상황은 `sep_catch_basin_2_inlet_connector`의 개도/막힘률로 표현합니다.

배출구 막힘 표현:
→ 빗물받이에서 우수연결관으로 빠지는 출구 막힘은 `sep_catch_basin_2_outlet_connector`의 개도/막힘률로 표현합니다.

## 빗물받이2 입구 커넥터

{_orifice_doc(inlet2)}

## 빗물받이2 출구 커넥터

{_orifice_doc(outlet2)}

중요:
→ 빗물받이2 출구도 빗물받이1과 동일하게 박스 하단이 아니라 중간 벽면에 붙은 것으로 정의했습니다.

출구 중심 높이: 0.55 m
→ 빗물받이 바닥에서 파이프 중심까지의 높이입니다.

출구 관 지름: 0.45 m
→ 우수연결관 지름입니다.

출구 하단 높이: 약 0.33 m
→ 0.55m - 0.45m / 2 입니다. 이 값이 SIDE 오리피스 offset으로 들어갑니다.

## ㄱ자 우수연결관2 정의

구성:
`빗물받이2 -> 출구 커넥터 -> 수평 우수연결관2 -> ㄱ자 커넥터2 -> 수직 우수연결관2 -> 본관2 접합 커넥터 -> 우수본관2`

### 수평 우수연결관2

{_conduit_doc(lateral2_h)}

### ㄱ자 커넥터2

노드 ID: `sep_storm_lateral_catch_basin_2_elbow_connector`
→ 화면의 두 번째 ㄱ자 꺾임부를 SWMM에서는 중간 접합 노드로 둡니다.

역할:
→ 수평 관과 수직 관을 연결합니다. 꺾임 손실은 수직 우수연결관2의 평균 손실계수에 반영했습니다.

좌표:
→ x=2160, y=314 입니다. HTML의 두 번째 ㄱ자 꺾임 위치에 맞춘 표시용 좌표입니다.

### 수직 우수연결관2

{_conduit_doc(lateral2_v)}

수직관 해석:
→ 우수본관2 접합 노드가 x=2160, y=530에 있으므로, 화면의 두 번째 빗물받이 수직 연결관과 같은 위치에 맞습니다. 상류 고도 11.31m, 하류 고도 8.38m, 길이 2.93m로 두어 거의 수직 낙차에 가까운 흐름으로 계산하게 했습니다.

## 현재 v2 모델의 물 흐름

1. 화면밖 빗물받이, 우수본관1 상류 유입: `offscreen_catch_basin_storm_main_1`
2. 우수본관1 상류 구간: `sep_storm_main_1_upstream_segment`
3. 우수본관1 빗물받이1 접합부: `sep_storm_main_1_catch_basin_1_connector`
4. 우수본관1 하류 구간: `sep_storm_main_1_downstream_segment`
5. 우수맨홀: `sep_storm_manhole`
6. 우수본관2 상류 구간: `sep_storm_main_2_upstream_segment`
7. 우수본관2 빗물받이2 접합 노드: `sep_storm_main_2_catch_basin_2_connector`
8. 우수본관2 하류 구간: `sep_storm_main_2_downstream_segment`
9. 우수본관2 하류 끝 노드: `sep_storm_main_2_outlet_connector`
10. 우수본관2-우수간선관거 수평 연결관: `sep_storm_main_to_trunk_horizontal`
11. 우수본관2-우수간선관거 ㄱ자 커넥터: `sep_storm_main_to_trunk_elbow_connector`
12. 우수본관2-우수간선관거 수직 연결관: `sep_storm_main_to_trunk_vertical`
13. 우수간선관거 접합 노드: `sep_storm_trunk_main_2_drop_connector`
14. 우수간선관거 상류 구간: `sep_storm_trunk_upstream_segment`
15. 우수간선관거 하류 구간: `sep_storm_trunk_downstream_segment`
16. 우수간선관거에서 빗물펌프장으로 들어가는 유입관: `sep_storm_trunk_to_pump_station`
17. 빗물펌프장 수조: `storm_pump_station`
18. 펌프 링크: `storm_pump_unit`
19. 펌프 토출 노드: `storm_pump_discharge_node`
20. 펌프 토출관: `storm_pump_discharge_pipe`
21. 펌프 방류구: `pump_outfall`

### 우수본관1 빗물받이1 유입 분기

1. 우수본관1 빗물받이1 도로 유입: `road_runoff_sep_catch_basin_1`
2. 우수본관1 빗물받이1 박스: `sep_catch_basin_1`
3. 우수연결관1 수평부: `sep_storm_lateral_catch_basin_1_horizontal`
4. ㄱ자 커넥터1: `sep_storm_lateral_catch_basin_1_elbow_connector`
5. 우수연결관1 수직부: `sep_storm_lateral_catch_basin_1_vertical`
6. 우수본관1 접합부: `sep_storm_main_1_catch_basin_1_connector`

### 우수본관2 빗물받이2 유입 분기

1. 우수본관2 빗물받이2 도로 유입: `road_runoff_sep_catch_basin_2`
2. 우수본관2 빗물받이2 박스: `sep_catch_basin_2`
3. 우수연결관2 수평부: `sep_storm_lateral_catch_basin_2_horizontal`
4. ㄱ자 커넥터2: `sep_storm_lateral_catch_basin_2_elbow_connector`
5. 우수연결관2 수직부: `sep_storm_lateral_catch_basin_2_vertical`
6. 우수본관2 접합부: `sep_storm_main_2_catch_basin_2_connector`

## 분류식 오수본관, 차집관거, 물재생센터 1차 정의

오수본관2 하류는 중형 ㄱ자 연결관을 통해 차집관거로 내려가고, 차집관거 하류는 물재생센터로 들어갑니다.
물재생센터는 들어온 물을 즉시 그대로 내보내는 관이 아니라, STORAGE에 저장한 뒤 처리 가능량 제한 링크를 통해 처리수 방류관으로 내보내게 했습니다.

화면 기준:

- 아파트1 오수연결관: `M245 218 H365 V790`
- 아파트2 오수연결관: `M847 218 H727 V790`
- 오수본관1 중심선: `y=825`, `x=0 -> 489`
- 오수맨홀 축: `x=546`
- 오수본관2 중심선: `y=825`, `x=603 -> 2170`
- 오수본관2에서 차집관거로 내려가는 연결관: `M2170 825 H2242 Q2264 825 2264 984 V1620`
- 차집관거 중심선: `y=1669`, `x=0 -> 4978`
- 물재생센터: `x=5020 -> 5520`, `y=1587 -> 1757`
- 처리수 방류관 중심선: `y=1677`, `x=5578 -> 5870`
- 처리수 방류구: `x=5928 -> 6180`, 중심 대략 `x=6028`, `y=1677`

생활오수 유입원:

1. 화면밖 오수연결관 역할: `sep_sewer_upstream`
2. 분류식 아파트1: `sep_apartment_1`
3. 분류식 아파트2: `sep_apartment_2`

생활오수 시계열:

- 시계열 ID: `TS_SEWER_DWF`
- 값: 0.0100 CMS 기준의 단순 상시 유입
- 목적: 폭우와 무관하게 생활오수가 계속 들어오는 기본 흐름 확인

### 아파트1 오수연결관 수평부

{_conduit_doc(sewer_lateral1_h)}

### 아파트1 오수연결관 수직부

{_conduit_doc(sewer_lateral1_v)}

### 오수본관1 상류 구간

{_conduit_doc(sewer_main1_up)}

### 오수본관1 하류 구간

{_conduit_doc(sewer_main1_down)}

### 아파트2 오수연결관 수평부

{_conduit_doc(sewer_lateral2_h)}

### 아파트2 오수연결관 수직부

{_conduit_doc(sewer_lateral2_v)}

### 오수본관2 상류 구간

{_conduit_doc(sewer_main2_up)}

### 오수본관2 하류 구간

{_conduit_doc(sewer_main2_down)}

### 오수본관2-차집관거 수평 연결관

{_conduit_doc(sewer_to_interceptor_h)}

### 오수본관2-차집관거 수직 연결관

{_conduit_doc(sewer_to_interceptor_v)}

수직관 해석:
→ 화면에서는 ㄱ자로 꺾여 아래 차집관거로 내려가는 관입니다.
→ SWMM에서는 90도 꺾인 한 관으로 계산하지 않고, 수평 연결관과 수직 낙차 연결관으로 나누었습니다.
→ 이 수직 연결관은 중형 연결관이므로 오수본관과 같은 1.05m 원형관으로 두고, 꺾임/낙차 손실은 평균 손실계수에 반영했습니다.

### 차집관거 상류 표시 구간

{_conduit_doc(interceptor_up)}

### 차집관거 중간 구간

{_conduit_doc(interceptor_to_overflow_join)}

### 우수토실 일반유량 접합 이후 차집관거 구간

{_conduit_doc(interceptor_down)}

### 차집관거에서 물재생센터로 들어가는 유입관

{_conduit_doc(interceptor_to_center)}

해석:
→ 차집관거 하류의 물이 물재생센터 STORAGE로 들어가는 짧은 대형 유입관입니다.
→ 이 관까지는 차집관거의 연장으로 보고, 이후부터 물재생센터 내부 처리 제한이 적용됩니다.

### 물재생센터

노드 ID: `water_reclamation_center`
→ 물재생센터 시설의 고유 이름입니다.

SWMM 노드 종류: STORAGE
→ 관이 아니라 물이 잠시 모이고 수위가 변할 수 있는 저장/처리 시설로 둡니다.

역할:
→ 차집관거에서 들어온 오수를 바로 내보내지 않고, 처리 가능량에 따라 천천히 처리수 방류관으로 넘깁니다.

바닥 고도: {water_reclamation.elevation:.2f} m
→ 물재생센터 수조의 기준 바닥 높이입니다.

최대 수심: {water_reclamation.max_depth:.2f} m
→ 물재생센터에 물이 찰 수 있는 최대 깊이입니다.

초기 수심: {water_reclamation.init_depth:.2f} m
→ 시작 시점에는 약간의 기본 수위를 둡니다.

저류 면적 계수: {water_reclamation.storage_param:.1f}
→ 물재생센터가 차집관거보다 큰 저장/완충 용량을 가진 시설임을 표현합니다.

좌표: HTML x={water_reclamation.x}, y={water_reclamation.y} / SWMM x={water_reclamation.x}, y={swmm_y(water_reclamation.y)}
→ HTML 물재생센터 중심에 맞춘 뒤, SWMM GUI에 넣을 때는 y축을 뒤집습니다.

역류/정체 해석:
→ 차집관거 유입량이 물재생센터 처리 가능량보다 크면 물재생센터 수위가 올라갑니다.
→ 물재생센터 수위가 높아지면 하류로 빨리 빠지지 못하는 상태가 되고, 차집관거 쪽 정체/만관 가능성이 커집니다.
→ 처리수 방류구가 막히거나 하천 수위가 높아지는 조건을 추가하면 처리수 방류관과 물재생센터 수위 상승을 통해 상류 정체를 볼 수 있습니다.

### 물재생센터 처리 가능량 제한 링크

{_conduit_doc(treatment_process)}

중요:
→ 이 링크의 `최대 유량 제한`을 {treatment_process.max_flow:.3f} m3/s로 두었습니다.
→ 그래서 차집관거에서 더 많은 물이 들어와도 물재생센터가 처리수 방류관으로 즉시 내보낼 수 있는 양은 제한됩니다.
→ 이 차이가 물재생센터 내부 수위 상승으로 쌓이고, 필요하면 차집관거 정체로 이어질 수 있습니다.

### 처리수 방류관

{_conduit_doc(treatment_effluent)}

### 처리수 방류구 게이트

{_orifice_doc(treated_gate)}

해석:
→ 현재는 열려 있는 상태의 방류구 커넥터입니다.
→ 이후 하천 수위 상승 또는 방류구 막힘 테스트를 할 때 이 링크의 개도를 낮추면 처리수 방류관이 막히는 상황을 만들 수 있습니다.

### 처리수 방류구

노드 ID: `treated_outfall`
→ 처리수가 최종적으로 하천으로 빠지는 방류구입니다.

SWMM 노드 종류: OUTFALL
→ 모델의 최종 배출구입니다.

바닥 고도: {treated_outfall.elevation:.2f} m
→ 처리수 방류구의 기준 높이입니다.

방류 조건: {treated_outfall.outfall_type}
→ 현재는 자유 방류로 두었습니다. 이후 하천 수위 역류를 반영할 때는 고정 수위 또는 시계열 수위 방류구로 바꿀 수 있습니다.

좌표: HTML x={treated_outfall.x}, y={treated_outfall.y} / SWMM x={treated_outfall.x}, y={swmm_y(treated_outfall.y)}
→ HTML의 처리수 방류구 중심에 맞췄습니다.

## 합류식 본관 1차 정의

이번 단계에서는 합류식 본관 끝에 우수토실-월류시설을 붙입니다.
우수토실은 하나의 SWMM 타입으로 존재하지 않으므로 STORAGE, ORIFICE, WEIR, CONDUIT, OUTFALL 조합으로 표현합니다.

화면 기준:

- 화면밖 합류식 상류 시작점: 대략 `x=2440`, `y=677`
- 주거지1 오수연결관: `M2730 218 H2850 V642`
- 주거지2 오수연결관: `M3160 218 H3280 V642`
- 빗물받이1 우수연결관: `M3530 314 H3650 V642`
- 합류식 맨홀 축: `x=3900`
- 빗물받이2 우수연결관: `M4280 314 H4400 V642`
- 합류식 본관 중심선: `y=677`
- 우수토실-월류시설: 대략 `x=4492 -> 5012`, 중심 `x=4752`, `y=680`
- 일반 유량 차집관거 하강 경로: 대략 `x=4753`, `y=846 -> 1620`
- 월류관: 대략 `x=5070 -> 5870`, 중심선 `y=677`
- 월류 방류구: 대략 `x=5928 -> 6180`, 중심 `x=6028`, `y=677`

중요:
→ 합류식 본관은 화면에서는 하나의 관처럼 보이지만, SWMM에서는 유입 지점마다 본관을 끊었습니다.
→ 그래야 주거지 오수와 빗물받이 우수가 본관 중간으로 들어오는 구조를 물리적으로 계산할 수 있습니다.

### 화면밖 합류식 오수 유입

{_conduit_doc(offscreen_comb_sewer_lateral)}

해석:
→ 화면 왼쪽 밖에서 이미 모여 들어오는 생활오수 연결관 역할입니다.
→ 화면에는 보이지 않지만, SWMM에서는 `offscreen_comb_sewer_source`에 생활오수 시계열을 넣고 `comb_upstream`으로 합류시킵니다.

### 화면밖 합류식 빗물받이

노드 ID: `offscreen_comb_catch_basin`
→ 화면 밖에 있는 대표 빗물받이 박스입니다.

SWMM 노드 종류: STORAGE
→ 화면에는 보이지 않지만, 빗물받이처럼 물이 잠깐 저장되고 차오를 수 있습니다.

바닥 고도: {offscreen_comb_cb.elevation:.2f} m
→ 화면에 보이는 빗물받이들과 같은 기준으로 둡니다.

최대 수심: {offscreen_comb_cb.max_depth:.2f} m
→ 빗물받이 내부에서 물이 찰 수 있는 깊이입니다.

좌표: HTML x={offscreen_comb_cb.x}, y={offscreen_comb_cb.y} / SWMM x={offscreen_comb_cb.x}, y={swmm_y(offscreen_comb_cb.y)}
→ 표시용 좌표입니다.

#### 화면밖 빗물받이 입구

{_orifice_doc(offscreen_comb_cb_inlet)}

#### 화면밖 빗물받이 출구

{_orifice_doc(offscreen_comb_cb_outlet)}

#### 화면밖 우수연결관 수평부

{_conduit_doc(offscreen_comb_storm_h)}

#### 화면밖 우수연결관 수직부

{_conduit_doc(offscreen_comb_storm_v)}

### 합류식 주거지1 오수연결관

{_conduit_doc(comb_sewer1_h)}

{_conduit_doc(comb_sewer1_v)}

### 합류식 주거지2 오수연결관

{_conduit_doc(comb_sewer2_h)}

{_conduit_doc(comb_sewer2_v)}

### 합류식 빗물받이1

노드 ID: `comb_catch_basin_1`
→ 합류식 구역의 첫 번째 빗물받이 박스입니다.

SWMM 노드 종류: STORAGE
→ 도로 빗물이 들어와 잠시 저장되고, 중간 벽면 출구를 통해 우수연결관으로 빠집니다.

바닥 고도: {comb_cb1.elevation:.2f} m
→ 빗물받이 내부 바닥 높이입니다.

최대 수심: {comb_cb1.max_depth:.2f} m
→ 빗물받이가 차오를 수 있는 깊이입니다.

좌표: HTML x={comb_cb1.x}, y={comb_cb1.y} / SWMM x={comb_cb1.x}, y={swmm_y(comb_cb1.y)}
→ HTML의 빗물받이1 위치에 맞췄습니다.

#### 합류식 빗물받이1 입구

{_orifice_doc(comb_cb1_inlet)}

#### 합류식 빗물받이1 출구

{_orifice_doc(comb_cb1_outlet)}

#### 합류식 빗물받이1 우수연결관 수평부

{_conduit_doc(comb_storm1_h)}

#### 합류식 빗물받이1 우수연결관 수직부

{_conduit_doc(comb_storm1_v)}

### 합류식 본관1 분할 구간

HTML ID: `comb_main_1`
→ 화면에서는 합류식 본관1로 보입니다.

SWMM 계산 구조:

1. `comb_main_1_upstream_segment`
2. `comb_main_1_house_1_to_house_2_segment`
3. `comb_main_1_house_2_to_catch_basin_1_segment`
4. `comb_main_1_to_manhole_segment`

#### 합류식 본관1 상류 구간

{_conduit_doc(comb_main1_up)}

#### 합류식 본관1 주거지1-주거지2 사이 구간

{_conduit_doc(comb_main1_h1_h2)}

#### 합류식 본관1 주거지2-빗물받이1 사이 구간

{_conduit_doc(comb_main1_h2_cb1)}

#### 합류식 본관1 빗물받이1-합류식 맨홀 사이 구간

{_conduit_doc(comb_main1_to_manhole)}

### 합류식 맨홀

노드 ID: `combined_manhole`
→ 합류식 본관1에서 온 물을 받아 합류식 본관2로 넘기는 대표 맨홀입니다.

SWMM 노드 종류: JUNCTION
→ 합류식 본관1, 합류식 본관2가 만나는 접합 노드입니다.

바닥 고도: {node_elevation("combined_manhole"):.2f} m
→ 합류식 맨홀 바닥 높이입니다.

최대 수심: 3.50 m
→ 지표면까지의 여유를 반영한 맨홀 깊이입니다.

좌표: x=3900, y=677
→ HTML에서는 맨홀뚜껑이 지상에 있지만, SWMM GUI에서는 본관이 접속되는 중심선에 맞춥니다.

### 합류식 빗물받이2

노드 ID: `comb_catch_basin_2`
→ 합류식 구역의 두 번째 빗물받이 박스입니다.

SWMM 노드 종류: STORAGE
→ 빗물받이1과 동일하게 도로 빗물이 저장되고 우수연결관으로 빠집니다.

바닥 고도: {comb_cb2.elevation:.2f} m
→ 빗물받이 내부 바닥 높이입니다.

최대 수심: {comb_cb2.max_depth:.2f} m
→ 빗물받이가 차오를 수 있는 깊이입니다.

좌표: HTML x={comb_cb2.x}, y={comb_cb2.y} / SWMM x={comb_cb2.x}, y={swmm_y(comb_cb2.y)}
→ HTML의 빗물받이2 위치에 맞췄습니다.

#### 합류식 빗물받이2 입구

{_orifice_doc(comb_cb2_inlet)}

#### 합류식 빗물받이2 출구

{_orifice_doc(comb_cb2_outlet)}

#### 합류식 빗물받이2 우수연결관 수평부

{_conduit_doc(comb_storm2_h)}

#### 합류식 빗물받이2 우수연결관 수직부

{_conduit_doc(comb_storm2_v)}

### 합류식 본관2 분할 구간

HTML ID: `comb_main_2`
→ 화면에서는 합류식 본관2로 보입니다.

SWMM 계산 구조:

1. `comb_main_2_manhole_to_catch_basin_2_segment`
2. `comb_main_2_downstream_segment`

#### 합류식 본관2 맨홀-빗물받이2 사이 구간

{_conduit_doc(comb_main2_to_cb2)}

#### 합류식 본관2 하류 구간

{_conduit_doc(comb_main2_down)}

### 우수토실-월류시설 본체

노드 ID: `overflow_chamber`
→ 합류식 본관2에서 들어온 물을 받아 일반 유량과 폭우 초과분을 나누는 시설입니다.

SWMM 노드 종류: STORAGE
→ 관이 아니라 물이 차오를 수 있는 저장/분기 시설로 둡니다.

바닥 고도: {overflow_chamber.elevation:.2f} m
→ 우수토실 내부 바닥 높이입니다.

최대 수심: {overflow_chamber.max_depth:.2f} m
→ 우수토실 내부에서 물이 찰 수 있는 최대 깊이입니다.

초기 수심: {overflow_chamber.init_depth:.2f} m
→ 시작 시점에는 비어 있다고 봅니다.

저류 면적 계수: {overflow_chamber.storage_param:.1f}
→ 우수토실 내부의 간이 저장 용량입니다.

좌표: HTML x={overflow_chamber.x}, y={overflow_chamber.y} / SWMM x={overflow_chamber.x}, y={swmm_y(overflow_chamber.y)}
→ HTML 우수토실-월류시설 위치에 맞춘 표시용 좌표입니다.

### 일반 유량부 제어 링크

{_orifice_doc(overflow_normal_gate)}

해석:
→ 우수토실에서 차집관거로 내려가는 일반 유량의 입구입니다.
→ 유량조절판 또는 일반 유량 개구부 역할을 합니다.
→ 이후 PySWMM 제어에서는 이 링크의 개도값을 조절할 수 있습니다.

### 우수토실에서 차집관거로 내려가는 관

{_conduit_doc(overflow_normal_drop)}

해석:
→ 화면에서는 우수토실 아래에서 차집관거로 내려가는 세로 관입니다.
→ SWMM에서는 일반 유량부 ORIFICE를 지난 뒤, 실제 관인 CONDUIT로 차집관거 접합부에 연결합니다.

### 폭우 초과분 월류 기준

{_weir_doc(overflow_excess_weir)}

해석:
→ 폭우 초과분 기준은 강수량 자체가 아니라 우수토실 내부 수위입니다.
→ 우수토실 수심이 {overflow_excess_weir.crest_height:.2f}m보다 낮으면 월류관으로 빠지지 않습니다.
→ 우수토실 수심이 {overflow_excess_weir.crest_height:.2f}m를 넘으면 초과 물이 월류턱을 넘어 월류관 방향으로 빠집니다.

### 월류관

{_conduit_doc(overflow_pipe)}

### 월류 방류구 게이트

{_orifice_doc(overflow_gate)}

해석:
→ 현재는 열려 있는 방류구 커넥터입니다.
→ 이후 하천 수위 상승이나 방류구 막힘을 테스트할 때 이 링크의 개도를 낮추면 월류관 하류가 막히는 상황을 만들 수 있습니다.

### 월류 방류구

노드 ID: `overflow_outfall`
→ 월류수가 최종적으로 하천으로 빠지는 방류구입니다.

SWMM 노드 종류: OUTFALL
→ 모델의 최종 배출구입니다.

바닥 고도: {overflow_outfall.elevation:.2f} m
→ 월류 방류구의 기준 높이입니다.

방류 조건: {overflow_outfall.outfall_type}
→ 현재는 자유 방류로 두었습니다. 이후 하천 수위 역류를 반영할 때는 고정 수위 또는 시계열 수위 방류구로 바꿀 수 있습니다.

좌표: HTML x={overflow_outfall.x}, y={overflow_outfall.y} / SWMM x={overflow_outfall.x}, y={swmm_y(overflow_outfall.y)}
→ HTML의 월류 방류구 위치에 맞췄습니다.

### 합류식 현재 흐름

```text
화면밖 오수 + 화면밖 빗물받이
→ comb_upstream
→ 합류식 본관1 상류 구간
→ 주거지1 오수 합류
→ 주거지2 오수 합류
→ 빗물받이1 우수 합류
→ 합류식 맨홀
→ 빗물받이2 우수 합류
→ 합류식 본관2
→ 우수토실-월류시설
   ├─ 일반 유량: 차집관거
   └─ 폭우 초과분: 월류관 → 월류 방류구
```

### 분류식 오수 흐름

```text
화면밖 오수연결관
→ 오수본관1 상류 구간
→ 아파트1 오수 유입 접합부
→ 오수본관1 하류 구간
→ 오수맨홀
→ 오수본관2 상류 구간
→ 아파트2 오수 유입 접합부
→ 오수본관2 하류 구간
→ 오수본관2-차집관거 수평 연결관
→ 오수본관2-차집관거 수직 연결관
→ 차집관거 접합부
→ 차집관거 하류 구간
→ 물재생센터 유입관
→ 물재생센터
→ 처리 가능량 제한 링크
→ 처리수 방류관
→ 처리수 방류구
```

## 다음 작업 후보

1. 처리수 방류구 막힘 또는 하천 수위 상승 조건 테스트
2. 우수토실 일반 유량부 개도와 월류 방류구 막힘 테스트
3. HTML 컨트롤러의 막힘률을 `ORIFICE target_setting` 또는 PySWMM 제어값에 연결
4. 물재생센터 처리 가능량을 화면 컨트롤러에서 조절하는 구조 추가
"""


def main() -> int:
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    MODEL_PATH.write_text(build_inp(), encoding="utf-8")
    DOC_PATH.write_text(build_doc(), encoding="utf-8")
    print(f"wrote {MODEL_PATH}")
    print(f"wrote {DOC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
