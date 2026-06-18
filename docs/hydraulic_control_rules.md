# 배수도 물리 조건 및 시설 작동 규칙

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
| `warning` | 용량 사용률 0.85 이상 |
| `surcharge_risk` | 용량 사용률 1.05 이상 |
| `backflow` | 하천 수위 조건 또는 막힘 관 만관 조건으로 역방향 흐름 발생 |

## 빗물펌프장 조건

```text
우수본관 -> 우수 간선관거 -> 빗물펌프장 -> 펌프 토출관 -> 펌프 방류구
```

| 조건 | 동작 |
|---|---|
| 펌프장 수위 0.45 이상 | `storm_pump_station` 상태를 `pump_active`로 변경 |
| 펌프장 수위 0.28 이하 | 펌프 대기 상태 |
| 펌프 용량 | 1.20 CMS |
| 하천 역류 압력 발생 | `storm_pump_discharge_pipe`, `pump_outfall`을 역류 후보로 표시 |

## 우수토실-월류시설 조건

```text
합류식 본관 -> 우수토실
정상 유량 -> 차집관거
초과 유량 -> 월류관 -> 월류 방류구
```

| 조건 | 동작 |
|---|---|
| 우수토실 수위 0.68 이하 | 일반 유량부 완전 개방 |
| 우수토실 수위 0.68 초과 | 유량조절판이 닫히기 시작 |
| 우수토실 수위 0.92 이상 | 일반 유량부 최소 개도 0.12 |
| 일반 유량부 용량 초과 | 남는 유량이 `overflow_pipe`로 이동 |
| 하천 역류 압력 발생 | `overflow_pipe`, `overflow_outfall`을 역류 후보로 표시 |

## 물재생센터 조건

```text
차집관거 -> 물재생센터 -> 처리수 방류관 -> 처리수 방류구
```

| 조건 | 동작 |
|---|---|
| 차집관거 유입이 처리 용량 이하 | 처리수 방류관으로 정상 방류 |
| 차집관거 유입이 1.25 CMS 초과 | `treatment_over_capacity` 표시 |
| 하천 역류 압력 발생 | `treatment_effluent_pipe`, `treated_outfall`을 역류 후보로 표시 |

## 역류 조건

하천 역류 시나리오에서는 하천 수위가 상승하는 시간대에만 역류 압력을 만든다.
역류 압력이 0.30 이상이면 다음 경로가 역류 후보가 된다.

- `overflow_pipe` -> `overflow_outfall`
- `storm_pump_discharge_pipe` -> `pump_outfall`
- `treatment_effluent_pipe` -> `treated_outfall`

막힘 기반 역류는 막힘 자체만으로 발생하지 않는다. 다음 조건이 동시에 맞을 때만 상류 노드/시설의 수위와 유량을 증가시킨다.

| 조건 | 기준 |
|---|---|
| 막힌 관이 사실상 만관 | fullness ratio 0.98 이상 |
| 전 노드에서 유입 지속 | upstream inflow 0.002 CMS 초과 |
| 배출 제한이 충분히 큼 | blockage ratio 0.85 이상 |

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
