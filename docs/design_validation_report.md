# 설계 배수도 SWMM 모델 검증

## 기준

- registry 버전: `2026-06-11-control-registry-v1`
- 공통 registry 배관 ID 수: 22
- 공통 registry 시설 ID 수: 13
- 공통 registry 지상 유입 객체 ID 수: 4
- 원칙: registry의 `pipe.id`와 `pipe.swmmId`는 SWMM 링크 ID와 동일하게 둔다.
- 원칙: registry의 `asset.id`와 `asset.swmmId`는 SWMM 노드 ID와 동일하게 둔다.
- 원칙: HTML은 `viewer/network_registry.js`를 먼저 읽고, PySWMM/API는 같은 registry JSON을 읽는다.

## 시나리오 파일

- `models/seoul_design_base.inp`: 기본 폭우 / 구조 검증 통과
  - 이벤트 확인: pump_active 24건
- `models/seoul_design_overflow.inp`: 폭우 월류 / 구조 검증 통과
  - 이벤트 확인: gate_closing 58건, overflow_active 56건, overflow_gate_active 58건, pump_active 102건, surcharge_risk 101건, treatment_over_capacity 32건, warning 117건
- `models/seoul_design_backflow.inp`: 하천 역류 / 구조 검증 통과
  - 이벤트 확인: backflow 711건, pump_active 24건

## 조건 설계

| 조건 | 화면/데이터 반영 |
|---|---|
| 관 용량 계산 | 지름, 길이, 경사, 조도 기준의 간이 Manning 용량을 `capacity_cms`로 저장 |
| 용량 사용률 증가 | `capacity_ratio = abs(flow_cms) / capacity_cms`로 계산 |
| 유속 증가 | 해당 pipe ID의 흐름 점선 속도 증가 |
| 유량/만관비 증가 | 해당 pipe/asset ID의 차오름 증가, 파랑에서 붉은색으로 변화 |
| 우수 간선관거 수위 상승 | 펌프장 수위 0.45 이상이면 `storm_pump_station` 활성화 |
| 합류식 본관 수위 상승 | 우수토실 수위 0.68부터 일반 유량부 제한 시작 |
| 우수토실 만수 접근 | 우수토실 수위 0.92 이상이면 일반 유량부 최소 개도, `overflow_pipe` 활성화 |
| 하천 수위 상승 | `overflow_pipe`, `storm_pump_discharge_pipe`, `treatment_effluent_pipe` 역류 후보 |

## 생성 결과 CSV

- `sample-results/design_sensor_readings.csv`: 시간별 pipe/asset 상태
  - 주요 열: `flow_cms`, `velocity_mps`, `capacity_cms`, `capacity_ratio`, `control_setting`, `backflow`, `risk`
- `sample-results/design_sensor_readings_base.csv`: 기본 폭우 시나리오 상태
- `sample-results/design_sensor_readings_overflow.csv`: 폭우 월류 시나리오 상태
- `sample-results/design_sensor_readings_backflow.csv`: 하천 역류 시나리오 상태
- `sample-results/design_sensor_summary.csv`: ID별 최대/최소 요약
- `sample-results/design_problem_events.csv`: 경고/월류/역류 후보 이벤트
- `sample-results/design_problem_events_base.csv`: 기본 폭우 이벤트
- `sample-results/design_problem_events_overflow.csv`: 폭우 월류 이벤트
- `sample-results/design_problem_events_backflow.csv`: 하천 역류 이벤트
- `sample-results/design_screen_swmm_mapping.csv`: 화면 ID와 SWMM ID 매핑
- `sample-results/network_registry.json`: Python/PySWMM/API가 읽을 공통 ID registry
- `viewer/network_registry.js`: HTML 화면이 읽을 공통 ID registry

## 생성 문서

- `docs/design_network_structure.md`: 화면 구조와 SWMM ID 연결
- `docs/hydraulic_control_rules.md`: 물리 조건과 시설 작동 기준

## Windows 실행 파일

- `Run_SWMM_Design_Base.bat`
- `Run_SWMM_Design_Overflow.bat`
- `Run_SWMM_Design_Backflow.bat`

## 실행 상태

- 현재 Mac PATH에서는 `swmm5` 또는 `runswmm` 실행 파일을 찾지 못했다.
- `.inp` 파일은 EPA SWMM GUI 또는 Windows `runswmm.exe`에서 실행할 수 있게 생성했다.
- CSV는 같은 조건 설계를 기반으로 만든 화면 연결용 시나리오 데이터다. Windows에서 실제 SWMM 실행 결과를 뽑으면 이 CSV 생성부를 실제 결과 파서로 교체하면 된다.
