#!/usr/bin/env python3
"""Run physics-oriented blockage audits against a React editor SWMM layout.

The audit treats the React editor layout as the intended physical pipe layout.
It converts that layout to SWMM, runs a baseline rainfall scenario, then blocks
each SWMM link one at a time and compares the hydraulic response.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.swmm_fastapi_server import (  # noqa: E402
    RealtimeSwmmSession,
    RuntimeModelSpec,
    build_editor_conversion_payload,
    safe_number,
)


FLOW_EPS_CMS = 0.0005
UI_REVERSE_EPS_CMS = 0.02
UPSTREAM_DEPTH_DELTA_PASS = 0.02
UPSTREAM_DEPTH_M_DELTA_PASS = 0.02
BLOCKED_FLOW_REDUCTION_PASS = 0.80
TAIL_WINDOW_DEFAULT = 120


@dataclass
class LinkSeries:
    flow_sum: float = 0.0
    abs_flow_sum: float = 0.0
    tail_flow_values: list[float] = field(default_factory=list)
    max_abs_flow: float = 0.0
    max_fullness: float = 0.0
    max_capacity_ratio: float = 0.0
    final_flow: float = 0.0
    final_fullness: float = 0.0
    reverse_count: int = 0
    ui_reverse_count: int = 0
    steps: int = 0

    def add(self, state: dict[str, Any], tail_window: int) -> None:
        flow = safe_number(state.get("flowCms"), 0.0)
        fullness = safe_number(state.get("fullness"), 0.0)
        capacity_ratio = safe_number(state.get("capacityRatio"), 0.0)
        self.steps += 1
        self.flow_sum += flow
        self.abs_flow_sum += abs(flow)
        self.max_abs_flow = max(self.max_abs_flow, abs(flow))
        self.max_fullness = max(self.max_fullness, fullness)
        self.max_capacity_ratio = max(self.max_capacity_ratio, capacity_ratio)
        self.final_flow = flow
        self.final_fullness = fullness
        if flow < -FLOW_EPS_CMS:
            self.reverse_count += 1
        if flow < -UI_REVERSE_EPS_CMS:
            self.ui_reverse_count += 1
        self.tail_flow_values.append(flow)
        if len(self.tail_flow_values) > tail_window:
            self.tail_flow_values.pop(0)

    def summary(self) -> dict[str, float | int]:
        tail_len = max(1, len(self.tail_flow_values))
        return {
            "meanFlowCms": self.flow_sum / max(1, self.steps),
            "meanAbsFlowCms": self.abs_flow_sum / max(1, self.steps),
            "tailMeanFlowCms": sum(self.tail_flow_values) / tail_len,
            "tailMeanAbsFlowCms": sum(abs(value) for value in self.tail_flow_values) / tail_len,
            "maxAbsFlowCms": self.max_abs_flow,
            "maxFullness": self.max_fullness,
            "maxCapacityRatio": self.max_capacity_ratio,
            "finalFlowCms": self.final_flow,
            "finalFullness": self.final_fullness,
            "reverseCount": self.reverse_count,
            "uiReverseCount": self.ui_reverse_count,
        }


@dataclass
class NodeSeries:
    max_depth_m: float = 0.0
    max_depth_ratio: float = 0.0
    max_head_m: float = -math.inf
    max_total_inflow: float = 0.0
    max_flooding: float = 0.0
    final_depth_m: float = 0.0
    final_depth_ratio: float = 0.0
    final_head_m: float = 0.0
    final_total_inflow: float = 0.0

    def add(self, state: dict[str, Any]) -> None:
        depth_m = safe_number(state.get("depthM"), 0.0)
        depth_ratio = safe_number(state.get("depthRatio"), 0.0)
        head_m = safe_number(state.get("headM"), 0.0)
        total_inflow = safe_number(state.get("totalInflowCms"), 0.0)
        flooding = safe_number(state.get("floodingCms"), 0.0)
        self.max_depth_m = max(self.max_depth_m, depth_m)
        self.max_depth_ratio = max(self.max_depth_ratio, depth_ratio)
        self.max_head_m = max(self.max_head_m, head_m)
        self.max_total_inflow = max(self.max_total_inflow, total_inflow)
        self.max_flooding = max(self.max_flooding, flooding)
        self.final_depth_m = depth_m
        self.final_depth_ratio = depth_ratio
        self.final_head_m = head_m
        self.final_total_inflow = total_inflow

    def summary(self) -> dict[str, float]:
        return {
            "maxDepthM": self.max_depth_m,
            "finalDepthM": self.final_depth_m,
            "maxDepthRatio": self.max_depth_ratio,
            "finalDepthRatio": self.final_depth_ratio,
            "maxHeadM": self.max_head_m if math.isfinite(self.max_head_m) else 0.0,
            "finalHeadM": self.final_head_m,
            "maxTotalInflowCms": self.max_total_inflow,
            "finalTotalInflowCms": self.final_total_inflow,
            "maxFloodingCms": self.max_flooding,
        }


def load_layout(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_persistent_spec(layout: dict[str, Any], output_dir: Path, title: str) -> RuntimeModelSpec:
    conversion = build_editor_conversion_payload({"layout": layout, "title": title})
    if not conversion["ok"]:
        raise SystemExit(f"conversion failed: {conversion['errors']}")
    model_path = output_dir / "react_editor_physics_audit.inp"
    mapping_path = output_dir / "swmm-react-mapping.json"
    report_path = output_dir / "conversion-report.json"
    model_path.write_text(conversion["inpText"], encoding="utf-8")
    mapping_path.write_text(json.dumps(conversion["mapping"], ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(json.dumps(conversion["report"], ensure_ascii=False, indent=2), encoding="utf-8")
    return RuntimeModelSpec(
        model_path=model_path,
        mapping=conversion["mapping"],
        report=conversion["report"],
        source="react-editor-json",
        temp_dir=None,
    )


def run_scenario(
    spec: RuntimeModelSpec,
    *,
    steps: int,
    rainfall_ratio: float,
    max_rainfall: float,
    blockage_link_id: str | None,
    tail_window: int,
) -> dict[str, Any]:
    session = RealtimeSwmmSession(spec, step_seconds=1, max_rainfall_mm_per_hour=max_rainfall)
    link_ids = sorted((spec.mapping.get("swmmLinks") or {}).keys())
    node_ids = sorted((spec.mapping.get("swmmNodes") or {}).keys())
    session.control_link_ids = set(link_ids)
    controls: dict[str, Any] = {"rainfallRatio": rainfall_ratio, "blockagesById": {}}
    if blockage_link_id:
        controls["blockagesById"] = {blockage_link_id: 1.0}
    session.update_controls(controls)
    link_series = {link_id: LinkSeries() for link_id in link_ids}
    node_series = {node_id: NodeSeries() for node_id in node_ids}
    final_snapshot: dict[str, Any] | None = None
    try:
        for _ in range(steps):
            final_snapshot = session.step()
            for link_id, state in (final_snapshot.get("links") or {}).items():
                link_series.setdefault(link_id, LinkSeries()).add(state, tail_window)
            for node_id, state in (final_snapshot.get("nodes") or {}).items():
                node_series.setdefault(node_id, NodeSeries()).add(state)
    finally:
        session.close()
    return {
        "snapshot": final_snapshot,
        "links": {link_id: series.summary() for link_id, series in link_series.items()},
        "nodes": {node_id: series.summary() for node_id, series in node_series.items()},
    }


def node_degrees(mapping: dict[str, Any]) -> dict[str, int]:
    degrees = {node_id: 0 for node_id in (mapping.get("swmmNodes") or {})}
    for meta in (mapping.get("swmmLinks") or {}).values():
        for endpoint in (meta.get("fromNode"), meta.get("toNode")):
            if endpoint:
                degrees[str(endpoint)] = degrees.get(str(endpoint), 0) + 1
    return degrees


def relation_link_count(mapping: dict[str, Any]) -> int:
    return sum(
        1
        for meta in (mapping.get("swmmLinks") or {}).values()
        if str(meta.get("sourceEditorType") or "") == "relation"
    )


def classify_result(
    link_id: str,
    link_meta: dict[str, Any],
    baseline: dict[str, Any],
    scenario: dict[str, Any],
) -> dict[str, Any]:
    base_link = baseline["links"].get(link_id) or {}
    blocked_link = scenario["links"].get(link_id) or {}
    base_tail_abs = safe_number(base_link.get("tailMeanAbsFlowCms"), 0.0)
    blocked_tail_abs = safe_number(blocked_link.get("tailMeanAbsFlowCms"), 0.0)
    flow_reduction = None
    if base_tail_abs > FLOW_EPS_CMS:
        flow_reduction = max(0.0, min(1.0, 1.0 - blocked_tail_abs / base_tail_abs))

    from_node = str(link_meta.get("fromNode") or "")
    to_node = str(link_meta.get("toNode") or "")
    base_from = baseline["nodes"].get(from_node) or {}
    scen_from = scenario["nodes"].get(from_node) or {}
    base_to = baseline["nodes"].get(to_node) or {}
    scen_to = scenario["nodes"].get(to_node) or {}
    upstream_depth_delta = safe_number(scen_from.get("maxDepthRatio"), 0.0) - safe_number(base_from.get("maxDepthRatio"), 0.0)
    upstream_depth_m_delta = safe_number(scen_from.get("maxDepthM"), 0.0) - safe_number(base_from.get("maxDepthM"), 0.0)
    upstream_head_delta = safe_number(scen_from.get("maxHeadM"), 0.0) - safe_number(base_from.get("maxHeadM"), 0.0)
    downstream_depth_delta = safe_number(scen_to.get("maxDepthRatio"), 0.0) - safe_number(base_to.get("maxDepthRatio"), 0.0)

    issues: list[str] = []
    status = "pass"
    if flow_reduction is None:
        status = "inconclusive_no_baseline_flow"
    elif flow_reduction < BLOCKED_FLOW_REDUCTION_PASS and blocked_tail_abs > FLOW_EPS_CMS:
        status = "fail"
        issues.append("blocked_target_still_flows")

    if flow_reduction is not None and base_tail_abs > FLOW_EPS_CMS:
        if (
            upstream_depth_delta < UPSTREAM_DEPTH_DELTA_PASS
            and upstream_depth_m_delta < UPSTREAM_DEPTH_M_DELTA_PASS
            and upstream_head_delta < UPSTREAM_DEPTH_M_DELTA_PASS
        ):
            if status == "pass":
                status = "suspect"
            issues.append("no_upstream_depth_response")

    if safe_number(blocked_link.get("uiReverseCount"), 0.0) >= 3:
        if status == "pass":
            status = "suspect"
        issues.append("target_ui_reverse_when_blocked")

    return {
        "linkId": link_id,
        "sourceEditorId": link_meta.get("sourceEditorId") or "",
        "sourceEditorType": link_meta.get("sourceEditorType") or "",
        "sourceEditorName": link_meta.get("sourceEditorName") or "",
        "pipeKind": link_meta.get("pipeKind") or "",
        "kind": link_meta.get("kind") or "",
        "fromNode": from_node,
        "toNode": to_node,
        "lengthM": safe_number(link_meta.get("length"), 0.0),
        "diameterM": safe_number(link_meta.get("diameter"), 0.0),
        "baselineTailAbsFlowCms": base_tail_abs,
        "blockedTailAbsFlowCms": blocked_tail_abs,
        "flowReduction": "" if flow_reduction is None else flow_reduction,
        "baselineMaxFullness": safe_number(base_link.get("maxFullness"), 0.0),
        "blockedMaxFullness": safe_number(blocked_link.get("maxFullness"), 0.0),
        "upstreamDepthDelta": upstream_depth_delta,
        "upstreamDepthMDelta": upstream_depth_m_delta,
        "upstreamHeadDelta": upstream_head_delta,
        "downstreamDepthDelta": downstream_depth_delta,
        "reverseCount": int(safe_number(blocked_link.get("reverseCount"), 0.0)),
        "uiReverseCount": int(safe_number(blocked_link.get("uiReverseCount"), 0.0)),
        "status": status,
        "issues": ";".join(issues),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fmt_percent(value: Any) -> str:
    if value == "":
        return "-"
    parsed = safe_number(value, 0.0)
    return f"{parsed * 100:.1f}%"


def build_markdown_report(
    *,
    input_path: Path,
    output_dir: Path,
    spec: RuntimeModelSpec,
    steps: int,
    rainfall_ratio: float,
    elapsed_seconds: float,
    baseline: dict[str, Any],
    results: list[dict[str, Any]],
) -> str:
    warnings = spec.report.get("warnings") or []
    counts = spec.report.get("summary") or spec.report.get("counts") or {}
    degrees = node_degrees(spec.mapping)
    isolated_nodes = [
        node_id
        for node_id, degree in degrees.items()
        if degree == 0 and ((spec.mapping.get("swmmNodes") or {}).get(node_id) or {}).get("section") != "OUTFALL"
    ]
    result_counts: dict[str, int] = {}
    for row in results:
        result_counts[str(row["status"])] = result_counts.get(str(row["status"]), 0) + 1

    fail_like = [row for row in results if row["status"] in {"fail", "suspect"}]
    fail_like.sort(key=lambda row: (
        0 if row["status"] == "fail" else 1,
        -safe_number(row.get("baselineTailAbsFlowCms"), 0.0),
    ))
    strongest_flows = sorted(
        baseline["links"].items(),
        key=lambda item: safe_number(item[1].get("tailMeanAbsFlowCms"), 0.0),
        reverse=True,
    )[:12]

    lines: list[str] = []
    lines.append("# SWMM 물리 막힘 감사 리포트")
    lines.append("")
    lines.append(f"- 입력 JSON: `{input_path}`")
    lines.append(f"- 산출 디렉터리: `{output_dir}`")
    lines.append(f"- 실행 조건: 강수 {rainfall_ratio * 100:.0f}%, {steps}초, SWMM link 전체 1개씩 100% 막힘")
    lines.append(f"- 실행 시간: {elapsed_seconds:.1f}초")
    lines.append(f"- 변환 결과: node {len(spec.mapping.get('swmmNodes') or {})}개, link {len(spec.mapping.get('swmmLinks') or {})}개, relation 내부 conduit {relation_link_count(spec.mapping)}개")
    if counts:
        lines.append(f"- 변환 summary: `{json.dumps(counts, ensure_ascii=False, sort_keys=True)}`")
    lines.append("")
    lines.append("## 1. 즉시 봐야 할 변환 경고")
    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- 변환 경고 없음")
    if isolated_nodes:
        lines.append("")
        lines.append("## 2. 고립 노드 후보")
        for node_id in isolated_nodes:
            node_meta = (spec.mapping.get("swmmNodes") or {}).get(node_id) or {}
            lines.append(f"- `{node_id}` ({node_meta.get('sourceEditorName') or node_meta.get('sourceEditorType')})")
    lines.append("")
    lines.append("## 3. 전체 막힘 테스트 요약")
    for status, count in sorted(result_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.append("")
    lines.append("## 4. baseline에서 유량이 큰 link")
    for link_id, summary in strongest_flows:
        meta = (spec.mapping.get("swmmLinks") or {}).get(link_id) or {}
        lines.append(
            f"- `{link_id}` / {meta.get('sourceEditorName') or meta.get('sourceEditorId')} "
            f"/ tailAbsFlow={safe_number(summary.get('tailMeanAbsFlowCms'), 0.0):.6f} CMS "
            f"/ maxFull={safe_number(summary.get('maxFullness'), 0.0) * 100:.1f}%"
        )
    lines.append("")
    lines.append("## 5. 실패/의심 link 상위 목록")
    if fail_like:
        for row in fail_like[:30]:
            lines.append(
                f"- [{row['status']}] `{row['linkId']}` / {row['sourceEditorName']} / {row['issues']} "
                f"/ flow reduction {fmt_percent(row['flowReduction'])} "
                f"/ upstream delta {safe_number(row['upstreamDepthDelta'], 0.0) * 100:.2f}%p "
                f"/ upstream depth {safe_number(row.get('upstreamDepthMDelta'), 0.0):.3f}m "
                f"/ baseline {safe_number(row['baselineTailAbsFlowCms'], 0.0):.6f} -> blocked {safe_number(row['blockedTailAbsFlowCms'], 0.0):.6f} CMS"
            )
    else:
        lines.append("- fail/suspect 없음")
    lines.append("")
    lines.append("## 6. 수정 준비안")
    lines.append("- 방향 warning은 단순 warning이 아니라 변환 audit fail로 승격한다. relation 클릭 순서와 pipe rotation이 충돌한 객체는 UI에서 수정하거나 변환기에서 자동 보정 정책을 명확히 둔다.")
    lines.append("- link별 막힘 테스트에서 `blocked_target_still_flows`가 뜬 link는 conduit `flow_limit`/control link setting 적용 여부를 먼저 확인한다.")
    lines.append("- `no_upstream_depth_response`는 upstream node가 실제 물을 받지 못하거나, 중간 relation conduit/tee 분할 때문에 막힘 경계가 UI 의도 위치와 다른 경우를 우선 의심한다.")
    lines.append("- 시설/맨홀 차오름 판정은 표시용 editor aggregation과 raw SWMM node/link 값을 분리해서 리포트와 UI 상세 패널에 함께 보여준다.")
    lines.append("- 이 리포트의 CSV를 기준으로 변환기 수정 후 같은 명령을 재실행해 fail/suspect 수가 줄었는지 비교한다.")
    lines.append("")
    lines.append("## 7. 산출물")
    lines.append("- `react_editor_physics_audit.inp`: 테스트에 사용한 변환 INP")
    lines.append("- `swmm-react-mapping.json`: UI-SWMM 매핑")
    lines.append("- `conversion-report.json`: 변환 report/warning")
    lines.append("- `baseline_links.csv`: baseline link 요약")
    lines.append("- `blockage_results.csv`: link별 막힘 비교 결과")
    lines.append("- `raw-summary.json`: 주요 raw summary")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a per-link SWMM blockage physics audit for a React editor layout.")
    parser.add_argument("--input", required=True, type=Path, help="React editor layout JSON path.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory for audit outputs.")
    parser.add_argument("--steps", type=int, default=600, help="Seconds/steps to run per scenario.")
    parser.add_argument("--tail-window", type=int, default=TAIL_WINDOW_DEFAULT, help="Tail window for steady comparison.")
    parser.add_argument("--rainfall-ratio", type=float, default=1.0, help="0-1 rainfall ratio.")
    parser.add_argument("--max-rainfall-mm-per-hour", type=float, default=100.0)
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = args.output_dir or (ROOT / "sample-results" / f"physics-audit-{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)

    started = time.monotonic()
    layout = load_layout(args.input)
    spec = build_persistent_spec(layout, output_dir, "SWMM physics audit generated from React editor layout")
    link_metas = spec.mapping.get("swmmLinks") or {}
    link_ids = sorted(link_metas)

    print(f"[audit] input={args.input}")
    print(f"[audit] output={output_dir}")
    print(f"[audit] swmm links={len(link_ids)} nodes={len(spec.mapping.get('swmmNodes') or {})}")
    print(f"[audit] warnings={len(spec.report.get('warnings') or [])}")

    baseline = run_scenario(
        spec,
        steps=args.steps,
        rainfall_ratio=args.rainfall_ratio,
        max_rainfall=args.max_rainfall_mm_per_hour,
        blockage_link_id=None,
        tail_window=args.tail_window,
    )
    baseline_rows = []
    for link_id, summary in sorted(baseline["links"].items()):
        meta = link_metas.get(link_id) or {}
        baseline_rows.append({
            "linkId": link_id,
            "sourceEditorId": meta.get("sourceEditorId") or "",
            "sourceEditorType": meta.get("sourceEditorType") or "",
            "sourceEditorName": meta.get("sourceEditorName") or "",
            "pipeKind": meta.get("pipeKind") or "",
            **summary,
        })
    write_csv(output_dir / "baseline_links.csv", baseline_rows)
    print("[audit] baseline complete")

    results: list[dict[str, Any]] = []
    for index, link_id in enumerate(link_ids, start=1):
        meta = link_metas.get(link_id) or {}
        print(f"[audit] {index:03d}/{len(link_ids):03d} block {link_id} ({meta.get('sourceEditorName') or meta.get('sourceEditorType')})", flush=True)
        scenario = run_scenario(
            spec,
            steps=args.steps,
            rainfall_ratio=args.rainfall_ratio,
            max_rainfall=args.max_rainfall_mm_per_hour,
            blockage_link_id=link_id,
            tail_window=args.tail_window,
        )
        results.append(classify_result(link_id, meta, baseline, scenario))

    write_csv(output_dir / "blockage_results.csv", results)
    raw_summary = {
        "input": str(args.input),
        "outputDir": str(output_dir),
        "steps": args.steps,
        "tailWindow": args.tail_window,
        "rainfallRatio": args.rainfall_ratio,
        "maxRainfallMmPerHour": args.max_rainfall_mm_per_hour,
        "linkCount": len(link_ids),
        "nodeCount": len(spec.mapping.get("swmmNodes") or {}),
        "warnings": spec.report.get("warnings") or [],
        "baselineLinks": baseline["links"],
        "baselineNodes": baseline["nodes"],
        "results": results,
    }
    (output_dir / "raw-summary.json").write_text(json.dumps(raw_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    elapsed = time.monotonic() - started
    report = build_markdown_report(
        input_path=args.input,
        output_dir=output_dir,
        spec=spec,
        steps=args.steps,
        rainfall_ratio=args.rainfall_ratio,
        elapsed_seconds=elapsed,
        baseline=baseline,
        results=results,
    )
    (output_dir / "physics-audit-report.md").write_text(report, encoding="utf-8")
    print(f"[audit] complete in {elapsed:.1f}s")
    print(f"[audit] report={output_dir / 'physics-audit-report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
