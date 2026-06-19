# SWMM 물리 막힘 감사 리포트

- 입력 JSON: `/Users/onseoktae/Downloads/drainage-layout (1).json`
- 산출 디렉터리: `/Users/onseoktae/Documents/swmm/sample-results/physics-audit-20260619-011327`
- 실행 조건: 강수 100%, 600초, SWMM link 전체 1개씩 100% 막힘
- 실행 시간: 258.3초
- 변환 결과: node 71개, link 65개, relation 내부 conduit 24개
- 변환 summary: `{"conduits": 65, "errors": 0, "inflowNodes": 17, "junctions": 61, "outfalls": 3, "pumps": 0, "storages": 7, "warnings": 6, "weirs": 0}`

## 1. 즉시 봐야 할 변환 경고
- Pipe flow direction follows relation click order but conflicts with rotation: 오수 연결관 수평 02 expected ascending station order.
- Pipe flow direction follows relation click order but conflicts with rotation: 우수 연결관 수평 02 expected ascending station order.
- Pipe flow direction follows relation click order but conflicts with rotation: 우수 연결관 수평 04 expected ascending station order.
- Pipe flow direction follows relation click order but conflicts with rotation: 파이프 expected descending station order.
- Pipe flow direction follows relation click order but conflicts with rotation: 파이프 expected descending station order.
- Pipe flow direction follows relation click order but conflicts with rotation: 파이프 expected descending station order.

## 2. 고립 노드 후보
- `CONN_SEWER_08` (오수 커넥터 08)
- `ROAD_02` (도로 02)
- `ROAD_01` (도로 01)
- `terrain_1781772827749_107` (하천 107)

## 3. 전체 막힘 테스트 요약
- inconclusive_no_baseline_flow: 13
- pass: 21
- suspect: 31

## 4. baseline에서 유량이 큰 link
- `pipe_free_1781771885636` / 파이프 / tailAbsFlow=0.011432 CMS / maxFull=26.5%
- `PIPE_STORM_LATERAL_V_02` / 우수 연결관 수직 02 / tailAbsFlow=0.011113 CMS / maxFull=6.7%
- `PIPE_STORM_LATERAL_V_01` / 우수 연결관 수직 01 / tailAbsFlow=0.011111 CMS / maxFull=7.4%
- `PIPE_STORM_LATERAL_V_03` / 우수 연결관 수직 03 / tailAbsFlow=0.011111 CMS / maxFull=8.0%
- `REL_046_CONDUIT` / 관계 046: 빗물받이 03 → 우수 커넥터 03 / tailAbsFlow=0.011111 CMS / maxFull=3.7%
- `REL_085_CONDUIT` / 관계 085: 빗물받이 04 → 우수 커넥터 04 / tailAbsFlow=0.011111 CMS / maxFull=4.0%
- `PIPE_STORM_LATERAL_H_04` / 우수 연결관 수평 04 / tailAbsFlow=0.011111 CMS / maxFull=9.4%
- `PIPE_STORM_LATERAL_H_03` / 우수 연결관 수평 03 / tailAbsFlow=0.011111 CMS / maxFull=8.3%
- `PIPE_STORM_LATERAL_V_04` / 우수 연결관 수직 04 / tailAbsFlow=0.011111 CMS / maxFull=6.2%
- `REL_022_CONDUIT` / 관계 022: 빗물받이 01 → 우수 커넥터 01 / tailAbsFlow=0.011111 CMS / maxFull=3.7%
- `PIPE_STORM_LATERAL_H_01` / 우수 연결관 수평 01 / tailAbsFlow=0.011111 CMS / maxFull=8.5%
- `REL_079_CONDUIT` / 관계 079: 빗물받이 02 → 우수 커넥터 02 / tailAbsFlow=0.011111 CMS / maxFull=3.8%

## 5. 실패/의심 link 상위 목록
- [suspect] `pipe_free_1781771885636` / 파이프 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.04%p / baseline 0.011432 -> blocked 0.000001 CMS
- [suspect] `PIPE_STORM_LATERAL_V_02` / 우수 연결관 수직 02 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.61%p / baseline 0.011113 -> blocked 0.000001 CMS
- [suspect] `PIPE_STORM_LATERAL_V_01` / 우수 연결관 수직 01 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.66%p / baseline 0.011111 -> blocked 0.000001 CMS
- [suspect] `PIPE_STORM_LATERAL_H_04` / 우수 연결관 수평 04 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 1.69%p / baseline 0.011111 -> blocked 0.000001 CMS
- [suspect] `pipe_free_1781771598332` / 파이프 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.00%p / baseline 0.007645 -> blocked 0.000001 CMS
- [suspect] `PIPE_STORM_MAIN_DROP_01` / 우수 본관 하강관 01 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.02%p / baseline 0.006587 -> blocked 0.000001 CMS
- [suspect] `pipe_free_1781771701381` / 파이프 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.00%p / baseline 0.006428 -> blocked 0.000001 CMS
- [suspect] `pipe_free_1781772019999` / 파이프 / no_upstream_depth_response / flow reduction 100.0% / upstream delta -0.03%p / baseline 0.005708 -> blocked 0.000001 CMS
- [suspect] `PIPE_OVERFLOW_INTERCEPTOR_DROP_01` / 월류 차집 연결관 01 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.01%p / baseline 0.005576 -> blocked 0.000001 CMS
- [suspect] `pipeSegment_copy_1781772027152_1` / 파이프 복사 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.00%p / baseline 0.005403 -> blocked 0.000001 CMS
- [suspect] `REL_061_CONDUIT` / 관계 061: 합류식 커넥터 03 → 우수토실-월류시설 01 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.09%p / baseline 0.005403 -> blocked 0.000001 CMS
- [suspect] `REL_071_CONDUIT` / 관계 071: 우수토실-월류시설 01 → 합류식 커넥터 04 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 1.66%p / baseline 0.005380 -> blocked 0.000001 CMS
- [suspect] `REL_057_CONDUIT` / 관계 057: 합류식 커넥터 01 → 합류식 맨홀 01 / no_upstream_depth_response / flow reduction 100.0% / upstream delta -0.01%p / baseline 0.004666 -> blocked 0.000001 CMS
- [suspect] `PIPE_STORM_MAIN_02` / 우수 본관 02 / no_upstream_depth_response / flow reduction 100.0% / upstream delta -0.01%p / baseline 0.004662 -> blocked 0.000001 CMS
- [suspect] `REL_009_CONDUIT` / 관계 009: 오수 맨홀 01 → 오수 커넥터 10 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.12%p / baseline 0.004320 -> blocked 0.000001 CMS
- [suspect] `REL_058_CONDUIT` / 관계 058: 합류식 맨홀 01 → 합류식 커넥터 02 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.00%p / baseline 0.004197 -> blocked 0.000001 CMS
- [suspect] `REL_029_CONDUIT` / 관계 029: 우수 커넥터 10 → 우수 맨홀 01 / no_upstream_depth_response / flow reduction 100.0% / upstream delta -0.04%p / baseline 0.004190 -> blocked 0.000001 CMS
- [suspect] `REL_030_CONDUIT` / 관계 030: 우수 맨홀 01 → 우수 커넥터 09 / no_upstream_depth_response / flow reduction 100.0% / upstream delta -0.03%p / baseline 0.003692 -> blocked 0.000001 CMS
- [suspect] `pipe_free_1781771452952` / 파이프 / no_upstream_depth_response / flow reduction 100.0% / upstream delta -0.01%p / baseline 0.003173 -> blocked 0.000001 CMS
- [suspect] `pipe_free_1781772198383` / 파이프 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.00%p / baseline 0.002866 -> blocked 0.000001 CMS
- [suspect] `pipe_free_1781771017429` / 파이프 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.00%p / baseline 0.002609 -> blocked 0.000001 CMS
- [suspect] `REL_006_CONDUIT` / 관계 006: 오수 커넥터 09 → 오수 맨홀 01 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.02%p / baseline 0.002606 -> blocked 0.000001 CMS
- [suspect] `PIPE_SEWER_MAIN_01` / 오수 본관 01 / no_upstream_depth_response / flow reduction 100.0% / upstream delta -0.01%p / baseline 0.002376 -> blocked 0.000001 CMS
- [suspect] `pipe_free_1781772135198` / 파이프 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.00%p / baseline 0.002362 -> blocked 0.000001 CMS
- [suspect] `PIPE_STORM_MAIN_01` / 우수 본관 01 / no_upstream_depth_response / flow reduction 100.0% / upstream delta -0.00%p / baseline 0.002281 -> blocked 0.000001 CMS
- [suspect] `REL_019_CONDUIT` / 관계 019: 오수 커넥터 12 → 물재생센터 01 / no_upstream_depth_response / flow reduction 100.0% / upstream delta 0.00%p / baseline 0.002275 -> blocked 0.000001 CMS
- [suspect] `PIPE_SEWER_MAIN_02` / 오수 본관 02 / no_upstream_depth_response / flow reduction 99.9% / upstream delta 0.00%p / baseline 0.001699 -> blocked 0.000001 CMS
- [suspect] `REL_066_CONDUIT` / 관계 066: 빗물펌프장 01 → 우수 커넥터 13 / no_upstream_depth_response / flow reduction 99.9% / upstream delta -0.76%p / baseline 0.001330 -> blocked 0.000001 CMS
- [suspect] `PIPE_SEWER_MAIN_DROP_01` / 오수 본관 하강관 01 / no_upstream_depth_response / flow reduction 99.9% / upstream delta 0.00%p / baseline 0.001304 -> blocked 0.000001 CMS
- [suspect] `PIPE_STORM_TRUNK_01` / 우수 간선관거 01 / no_upstream_depth_response / flow reduction 99.9% / upstream delta -0.00%p / baseline 0.000733 -> blocked 0.000001 CMS

## 6. 수정 준비안
- 방향 warning은 단순 warning이 아니라 변환 audit fail로 승격한다. relation 클릭 순서와 pipe rotation이 충돌한 객체는 UI에서 수정하거나 변환기에서 자동 보정 정책을 명확히 둔다.
- link별 막힘 테스트에서 `blocked_target_still_flows`가 뜬 link는 conduit `flow_limit`/control link setting 적용 여부를 먼저 확인한다.
- `no_upstream_depth_response`는 upstream node가 실제 물을 받지 못하거나, 중간 relation conduit/tee 분할 때문에 막힘 경계가 UI 의도 위치와 다른 경우를 우선 의심한다.
- 시설/맨홀 차오름 판정은 표시용 editor aggregation과 raw SWMM node/link 값을 분리해서 리포트와 UI 상세 패널에 함께 보여준다.
- 이 리포트의 CSV를 기준으로 변환기 수정 후 같은 명령을 재실행해 fail/suspect 수가 줄었는지 비교한다.

## 7. 산출물
- `react_editor_physics_audit.inp`: 테스트에 사용한 변환 INP
- `swmm-react-mapping.json`: UI-SWMM 매핑
- `conversion-report.json`: 변환 report/warning
- `baseline_links.csv`: baseline link 요약
- `blockage_results.csv`: link별 막힘 비교 결과
- `raw-summary.json`: 주요 raw summary
