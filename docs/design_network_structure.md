# 설계 배수 네트워크 구조

## 전체 기준

- registry 버전: `2026-06-11-control-registry-v1`
- 공통 registry 배관 수: 22개
- 공통 registry 시설 수: 13개
- 공통 registry 지상 유입 객체 수: 4개
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
