# SWMM-HTML 객체 계약

## 기준

- SWMM 모델이 원본입니다.
- HTML은 SWMM 상태를 렌더링하고, 강수량과 객체별 막힘정도만 입력합니다.
- 유량, 유속, 만관, 역류, 펌프 배출량은 HTML에서 직접 계산하지 않습니다.
- ㄱ자로 보이는 관은 SWMM에서 `수평 관 + 접합 노드 + 수직 관`으로 나눕니다.

## 생성 파일

- JSON 계약: `/Users/onseoktae/Documents/swmm/sample-results/swmm_html_contract.json`
- 브라우저 계약: `/Users/onseoktae/Documents/swmm/viewer/swmm_html_contract.js`
- 기준 모델: `/Users/onseoktae/Documents/swmm/models/seoul_rebuild_v2.inp`

## HTML이 제어할 수 있는 값

| 제어값 | 의미 | SWMM 반영 방식 |
| --- | --- | --- |
| 강수량 | 빗물 유입 강도 | PySWMM 브릿지에서 강우/유입 시계열 또는 입력 유량으로 변환 |
| 객체별 막힘정도 | 특정 시설/관의 흐름 제한 | PySWMM 브릿지에서 대응 게이트/오리피스/제어 링크 setting으로 변환 |

## HTML이 계산하면 안 되는 값

- 유속
- 유량
- 만관 여부
- 역류 여부
- 펌프 배출량
- 우수토실 월류량

## 객체 매핑

| HTML 객체 ID | 이름 | 종류 | SWMM 노드 | SWMM 링크 |
| --- | --- | --- | --- | --- |
| `sep_apartment_1` | 분류식 아파트 1 | surface | `sep_apartment_1` | - |
| `sep_apartment_2` | 분류식 아파트 2 | surface | `sep_apartment_2` | - |
| `sep_catch_basin_1` | 분류식 빗물받이 1 | catch_basin | `road_runoff_sep_catch_basin_1`, `sep_catch_basin_1` | `sep_catch_basin_1_inlet_connector` |
| `sep_catch_basin_2` | 분류식 빗물받이 2 | catch_basin | `road_runoff_sep_catch_basin_2`, `sep_catch_basin_2` | `sep_catch_basin_2_inlet_connector` |
| `sep_storm_lateral_catch_basin_1` | 분류식 빗물받이 1 우수연결관 | pipe_group | `sep_catch_basin_1`, `sep_storm_lateral_catch_basin_1_start`, `sep_storm_lateral_catch_basin_1_elbow_connector`, `sep_storm_main_1_catch_basin_1_connector` | `sep_catch_basin_1_outlet_connector`, `sep_storm_lateral_catch_basin_1_horizontal`, `sep_storm_lateral_catch_basin_1_vertical` |
| `sep_storm_lateral_catch_basin_2` | 분류식 빗물받이 2 우수연결관 | pipe_group | `sep_catch_basin_2`, `sep_storm_lateral_catch_basin_2_start`, `sep_storm_lateral_catch_basin_2_elbow_connector`, `sep_storm_main_2_catch_basin_2_connector` | `sep_catch_basin_2_outlet_connector`, `sep_storm_lateral_catch_basin_2_horizontal`, `sep_storm_lateral_catch_basin_2_vertical` |
| `sep_storm_main_1` | 우수 본관 1 | pipe_group | `offscreen_catch_basin_storm_main_1`, `sep_storm_main_1_catch_basin_1_connector`, `sep_storm_manhole` | `sep_storm_main_1_upstream_segment`, `sep_storm_main_1_downstream_segment` |
| `sep_storm_manhole` | 분류식 우수 맨홀 | manhole | `sep_storm_manhole` | - |
| `sep_storm_main_2` | 우수 본관 2 | pipe_group | `sep_storm_manhole`, `sep_storm_main_2_catch_basin_2_connector`, `sep_storm_main_2_outlet_connector` | `sep_storm_main_2_upstream_segment`, `sep_storm_main_2_downstream_segment` |
| `sep_storm_main_to_trunk` | 우수 본관 2에서 우수 간선관거로 내려가는 연결관 | pipe_group | `sep_storm_main_2_outlet_connector`, `sep_storm_main_to_trunk_elbow_connector`, `sep_storm_trunk_main_2_drop_connector` | `sep_storm_main_to_trunk_horizontal`, `sep_storm_main_to_trunk_vertical` |
| `sep_storm_trunk` | 우수 간선관거 | pipe_group | `sep_storm_trunk_upstream`, `sep_storm_trunk_main_2_drop_connector`, `sep_storm_trunk_downstream`, `storm_pump_inlet_gate_node` | `sep_storm_trunk_upstream_segment`, `sep_storm_trunk_downstream_segment`, `sep_storm_trunk_to_pump_station` |
| `storm_pump_station` | 빗물펌프장 | pump_station | `storm_pump_inlet_gate_node`, `storm_pump_station`, `storm_pump_discharge_node` | `storm_pump_inlet_gate`, `storm_pump_unit` |
| `storm_pump_discharge_pipe` | 펌프 토출관 | pipe_group | `storm_pump_discharge_node`, `pump_outfall_gate_node` | `storm_pump_discharge_pipe` |
| `pump_outfall` | 펌프 방류구 | outfall | `pump_outfall_gate_node`, `pump_outfall` | `pump_outfall_gate` |
| `sep_sewer_lateral_apartment_1` | 분류식 아파트 1 오수연결관 | pipe_group | `sep_apartment_1`, `sep_sewer_lateral_apartment_1_elbow_connector`, `sep_sewer_main_1_apartment_1_connector` | `sep_sewer_lateral_apartment_1_horizontal`, `sep_sewer_lateral_apartment_1_vertical` |
| `sep_sewer_lateral_apartment_2` | 분류식 아파트 2 오수연결관 | pipe_group | `sep_apartment_2`, `sep_sewer_lateral_apartment_2_elbow_connector`, `sep_sewer_main_2_apartment_2_connector` | `sep_sewer_lateral_apartment_2_horizontal`, `sep_sewer_lateral_apartment_2_vertical` |
| `sep_sewer_main_1` | 오수 본관 1 | pipe_group | `sep_sewer_upstream`, `sep_sewer_main_1_apartment_1_connector`, `sep_sewer_manhole` | `sep_sewer_main_1_upstream_segment`, `sep_sewer_main_1_downstream_segment` |
| `sep_sewer_manhole` | 분류식 오수 맨홀 | manhole | `sep_sewer_manhole` | - |
| `sep_sewer_main_2` | 오수 본관 2 | pipe_group | `sep_sewer_manhole`, `sep_sewer_main_2_apartment_2_connector`, `sep_sewer_downstream` | `sep_sewer_main_2_upstream_segment`, `sep_sewer_main_2_downstream_segment` |
| `sep_sewer_main_to_interceptor` | 오수 본관 2에서 차집관거로 내려가는 연결관 | pipe_group | `sep_sewer_downstream`, `sep_sewer_main_to_interceptor_elbow_connector`, `sep_interceptor_join` | `sep_sewer_main_to_interceptor_horizontal`, `sep_sewer_main_to_interceptor_vertical` |
| `sep_interceptor` | 차집관거 | pipe_group | `sep_interceptor_upstream`, `sep_interceptor_join`, `overflow_interceptor_join`, `sep_interceptor_downstream`, `water_reclamation_center` | `sep_interceptor_upstream_segment`, `sep_interceptor_join_to_overflow_segment`, `sep_interceptor_downstream_segment`, `sep_interceptor_to_reclamation_inlet` |
| `water_reclamation_center` | 물재생센터 | treatment_facility | `water_reclamation_center`, `treatment_process_outlet_node` | `treatment_process_limited_outlet` |
| `treatment_effluent_pipe` | 처리수 방류관 | pipe_group | `treatment_process_outlet_node`, `treated_outfall_gate_node` | `treatment_effluent_pipe` |
| `treated_outfall` | 처리수 방류구 | outfall | `treated_outfall_gate_node`, `treated_outfall` | `treated_outfall_gate` |
| `comb_house_1` | 합류식 주거지 1 | surface | `comb_house_1` | - |
| `comb_house_2` | 합류식 주거지 2 | surface | `comb_house_2` | - |
| `offscreen_comb_catch_basin` | 합류식 화면밖 빗물받이 | catch_basin | `road_runoff_offscreen_comb_catch_basin`, `offscreen_comb_catch_basin` | `offscreen_comb_catch_basin_inlet_connector` |
| `comb_catch_basin_1` | 합류식 빗물받이 1 | catch_basin | `road_runoff_comb_catch_basin_1`, `comb_catch_basin_1` | `comb_catch_basin_1_inlet_connector` |
| `comb_catch_basin_2` | 합류식 빗물받이 2 | catch_basin | `road_runoff_comb_catch_basin_2`, `comb_catch_basin_2` | `comb_catch_basin_2_inlet_connector` |
| `offscreen_comb_storm_lateral` | 합류식 화면밖 우수연결관 | pipe_group | `offscreen_comb_catch_basin`, `offscreen_comb_storm_lateral_start`, `offscreen_comb_storm_lateral_elbow_connector`, `comb_upstream` | `offscreen_comb_catch_basin_outlet_connector`, `offscreen_comb_storm_lateral_horizontal`, `offscreen_comb_storm_lateral_vertical` |
| `offscreen_comb_sewer_lateral` | 합류식 화면밖 오수연결관 | pipe_group | `offscreen_comb_sewer_source`, `comb_upstream` | `offscreen_comb_sewer_lateral` |
| `comb_sewer_lateral_house_1` | 합류식 주거지 1 오수연결관 | pipe_group | `comb_house_1`, `comb_sewer_lateral_house_1_elbow_connector`, `comb_main_house_1_connector` | `comb_sewer_lateral_house_1_horizontal`, `comb_sewer_lateral_house_1_vertical` |
| `comb_sewer_lateral_house_2` | 합류식 주거지 2 오수연결관 | pipe_group | `comb_house_2`, `comb_sewer_lateral_house_2_elbow_connector`, `comb_main_house_2_connector` | `comb_sewer_lateral_house_2_horizontal`, `comb_sewer_lateral_house_2_vertical` |
| `comb_storm_lateral_catch_basin_1` | 합류식 빗물받이 1 우수연결관 | pipe_group | `comb_catch_basin_1`, `comb_storm_lateral_catch_basin_1_start`, `comb_storm_lateral_catch_basin_1_elbow_connector`, `comb_main_catch_basin_1_connector` | `comb_catch_basin_1_outlet_connector`, `comb_storm_lateral_catch_basin_1_horizontal`, `comb_storm_lateral_catch_basin_1_vertical` |
| `comb_storm_lateral_catch_basin_2` | 합류식 빗물받이 2 우수연결관 | pipe_group | `comb_catch_basin_2`, `comb_storm_lateral_catch_basin_2_start`, `comb_storm_lateral_catch_basin_2_elbow_connector`, `comb_main_catch_basin_2_connector` | `comb_catch_basin_2_outlet_connector`, `comb_storm_lateral_catch_basin_2_horizontal`, `comb_storm_lateral_catch_basin_2_vertical` |
| `comb_main_1` | 합류식 본관 1 | pipe_group | `comb_upstream`, `comb_main_house_1_connector`, `comb_main_house_2_connector`, `comb_main_catch_basin_1_connector`, `combined_manhole` | `comb_main_1_upstream_segment`, `comb_main_1_house_1_to_house_2_segment`, `comb_main_1_house_2_to_catch_basin_1_segment`, `comb_main_1_to_manhole_segment` |
| `combined_manhole` | 합류식 맨홀 | manhole | `combined_manhole` | - |
| `comb_main_2` | 합류식 본관 2 | pipe_group | `combined_manhole`, `comb_main_catch_basin_2_connector`, `overflow_chamber` | `comb_main_2_manhole_to_catch_basin_2_segment`, `comb_main_2_downstream_segment` |
| `overflow_chamber` | 우수토실-월류시설 | overflow_facility | `overflow_chamber`, `overflow_normal_flow_node`, `overflow_weir_outlet_node` | `overflow_normal_flow_gate`, `overflow_excess_weir` |
| `overflow_to_interceptor_drop` | 우수토실 일반 유량에서 차집관거로 내려가는 관 | pipe_group | `overflow_chamber`, `overflow_normal_flow_node`, `overflow_interceptor_join` | `overflow_normal_flow_gate`, `overflow_to_interceptor_drop` |
| `overflow_pipe` | 월류관 | pipe_group | `overflow_chamber`, `overflow_weir_outlet_node`, `overflow_outfall_gate_node` | `overflow_excess_weir`, `overflow_pipe` |
| `overflow_outfall` | 월류 방류구 | outfall | `overflow_outfall_gate_node`, `overflow_outfall` | `overflow_outfall_gate` |

## 검증 결과

- 등록된 HTML 대표 객체: 42개
- SWMM 노드 수: 68개
- SWMM 링크 수: 66개
- 누락 매핑 수: 0개
