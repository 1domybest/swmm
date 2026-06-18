#!/usr/bin/env python3
"""Step-by-step pump backflow control test for rebuild v2.

This script intentionally controls only the pump line:
- close the pump outfall gate for a period,
- stop the pump when the discharge side is full,
- close the pump-station inlet gate when the wet well is near full,
- reopen the outfall and confirm the line drains and the pump restarts.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from pyswmm import Links, Nodes, Simulation


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "seoul_rebuild_v2.inp"
RESULTS_DIR = ROOT / "sample-results"
CSV_PATH = RESULTS_DIR / "rebuild_v2_pump_backflow_control.csv"

OUTFALL_CLOSE_AT = timedelta(hours=1, minutes=30)
OUTFALL_REOPEN_AT = timedelta(hours=2, minutes=50)

PUMP_START_DEPTH_M = 0.80
PUMP_STOP_DEPTH_M = 0.25
DISCHARGE_PIPE_DIAMETER_M = 1.80
DISCHARGE_NODE_MAX_DEPTH_M = 2.40
PUMP_STATION_MAX_DEPTH_M = 2.40

DISCHARGE_FULL_RATIO = 0.92
PUMP_STATION_CLOSE_INLET_DEPTH_M = 0.80
PUMP_STATION_REOPEN_INLET_DEPTH_M = 0.52


@dataclass
class EventFlags:
    outfall_closed: bool = False
    outfall_reopened: bool = False
    discharge_full: bool = False
    pump_stopped_by_discharge: bool = False
    inlet_closed_by_storage: bool = False
    inlet_reopened_after_drain: bool = False
    pump_restarted_after_reopen: bool = False


def elapsed(current_time: datetime, start_time: datetime) -> timedelta:
    return current_time - start_time


def stamp(current_time: datetime, start_time: datetime) -> str:
    total = int(elapsed(current_time, start_time).total_seconds())
    return f"{total // 3600:02d}:{(total % 3600) // 60:02d}:{total % 60:02d}"


def event(events: list[tuple[str, str]], when: str, message: str) -> None:
    events.append((when, message))


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    events: list[tuple[str, str]] = []
    flags = EventFlags()

    pump_command = 0.0
    inlet_gate_command = 1.0
    outfall_gate_command = 1.0

    maxima = {
        "pump_station_depth": 0.0,
        "discharge_pipe_depth": 0.0,
        "discharge_node_depth": 0.0,
        "trunk_downstream_depth": 0.0,
        "trunk_drop_depth": 0.0,
        "pump_flow": 0.0,
        "inlet_gate_flow": 0.0,
        "outfall_gate_flow": 0.0,
    }

    with Simulation(str(MODEL_PATH)) as sim:
        sim.step_advance(1)
        links = Links(sim)
        nodes = Nodes(sim)

        pump = links["storm_pump_unit"]
        inlet_gate = links["storm_pump_inlet_gate"]
        outfall_gate = links["pump_outfall_gate"]
        discharge_pipe = links["storm_pump_discharge_pipe"]

        pump_station = nodes["storm_pump_station"]
        discharge_node = nodes["storm_pump_discharge_node"]
        trunk_downstream = nodes["sep_storm_trunk_downstream"]
        trunk_drop = nodes["sep_storm_trunk_main_2_drop_connector"]

        start_time = sim.start_time

        for _ in sim:
            now = sim.current_time
            t = elapsed(now, start_time)
            time_label = stamp(now, start_time)

            if OUTFALL_CLOSE_AT <= t < OUTFALL_REOPEN_AT:
                outfall_gate_command = 0.0
                if not flags.outfall_closed:
                    flags.outfall_closed = True
                    event(events, time_label, "펌프 방류구 게이트 닫힘")
            else:
                outfall_gate_command = 1.0
                if t >= OUTFALL_REOPEN_AT and not flags.outfall_reopened:
                    flags.outfall_reopened = True
                    event(events, time_label, "펌프 방류구 게이트 재개방")

            discharge_pipe_ratio = (discharge_pipe.depth or 0.0) / DISCHARGE_PIPE_DIAMETER_M
            discharge_node_ratio = discharge_node.depth / DISCHARGE_NODE_MAX_DEPTH_M
            discharge_side_full = (
                discharge_pipe_ratio >= DISCHARGE_FULL_RATIO
                or discharge_node_ratio >= DISCHARGE_FULL_RATIO
            )

            if discharge_side_full and not flags.discharge_full:
                flags.discharge_full = True
                event(events, time_label, "펌프 토출측 만관 감지")

            discharge_side_safe = not discharge_side_full and outfall_gate_command > 0

            if discharge_side_full:
                if pump_command > 0 and not flags.pump_stopped_by_discharge:
                    flags.pump_stopped_by_discharge = True
                    event(events, time_label, "토출측 만관으로 펌프 정지")
                pump_command = 0.0
            elif flags.pump_stopped_by_discharge and discharge_side_safe and pump_station.depth > PUMP_STOP_DEPTH_M:
                if not flags.pump_restarted_after_reopen:
                    flags.pump_restarted_after_reopen = True
                    event(events, time_label, "방류구 재개방 후 펌프 재가동")
                pump_command = 1.0
            elif pump_station.depth >= PUMP_START_DEPTH_M:
                if flags.outfall_reopened and not flags.pump_restarted_after_reopen:
                    flags.pump_restarted_after_reopen = True
                    event(events, time_label, "방류구 재개방 후 펌프 재가동")
                pump_command = 1.0
            elif pump_station.depth <= PUMP_STOP_DEPTH_M:
                pump_command = 0.0

            pump_station_ratio = pump_station.depth / PUMP_STATION_MAX_DEPTH_M
            pump_station_operating_ratio = pump_station.depth / PUMP_STATION_CLOSE_INLET_DEPTH_M
            inlet_should_close = (
                outfall_gate_command == 0.0
                and flags.pump_stopped_by_discharge
                and pump_station.depth >= PUMP_STATION_CLOSE_INLET_DEPTH_M
            )
            if inlet_should_close:
                if inlet_gate_command > 0 and not flags.inlet_closed_by_storage:
                    flags.inlet_closed_by_storage = True
                    event(events, time_label, "빗물펌프장 운영 고수위로 유입 게이트 닫힘")
                inlet_gate_command = 0.0
            elif pump_station.depth <= PUMP_STATION_REOPEN_INLET_DEPTH_M:
                if flags.inlet_closed_by_storage and not flags.inlet_reopened_after_drain:
                    flags.inlet_reopened_after_drain = True
                    event(events, time_label, "빗물펌프장 수위 하강으로 유입 게이트 재개방")
                inlet_gate_command = 1.0

            pump.target_setting = pump_command
            inlet_gate.target_setting = inlet_gate_command
            outfall_gate.target_setting = outfall_gate_command

            maxima["pump_station_depth"] = max(maxima["pump_station_depth"], pump_station.depth)
            maxima["discharge_pipe_depth"] = max(maxima["discharge_pipe_depth"], discharge_pipe.depth or 0.0)
            maxima["discharge_node_depth"] = max(maxima["discharge_node_depth"], discharge_node.depth)
            maxima["trunk_downstream_depth"] = max(maxima["trunk_downstream_depth"], trunk_downstream.depth)
            maxima["trunk_drop_depth"] = max(maxima["trunk_drop_depth"], trunk_drop.depth)
            maxima["pump_flow"] = max(maxima["pump_flow"], pump.flow)
            maxima["inlet_gate_flow"] = max(maxima["inlet_gate_flow"], inlet_gate.flow)
            maxima["outfall_gate_flow"] = max(maxima["outfall_gate_flow"], outfall_gate.flow)

            if now.second == 0:
                rows.append(
                    {
                        "time": time_label,
                        "outfall_gate_setting": outfall_gate.current_setting,
                        "inlet_gate_setting": inlet_gate.current_setting,
                        "pump_setting": pump.current_setting,
                        "pump_station_depth_m": pump_station.depth,
                        "pump_station_full_ratio": pump_station_ratio,
                        "pump_station_operating_ratio": pump_station_operating_ratio,
                        "discharge_pipe_depth_m": discharge_pipe.depth or 0.0,
                        "discharge_pipe_full_ratio": discharge_pipe_ratio,
                        "discharge_node_depth_m": discharge_node.depth,
                        "trunk_downstream_depth_m": trunk_downstream.depth,
                        "trunk_drop_depth_m": trunk_drop.depth,
                        "pump_flow_cms": pump.flow,
                        "inlet_gate_flow_cms": inlet_gate.flow,
                        "outfall_gate_flow_cms": outfall_gate.flow,
                    }
                )

    with CSV_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("CSV", CSV_PATH)
    print("EVENTS")
    for when, message in events:
        print(f"{when} {message}")
    print("MAXIMA")
    for key, value in maxima.items():
        print(f"{key}={value:.6f}")
    print("FINAL")
    if rows:
        for key, value in rows[-1].items():
            if key == "time":
                print(f"{key}={value}")
            elif isinstance(value, float):
                print(f"{key}={value:.6f}")
            else:
                print(f"{key}={value}")


if __name__ == "__main__":
    main()
