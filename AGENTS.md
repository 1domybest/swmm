# AGENTS.md

이 파일은 `/Users/onseoktae/Documents/swmm` 전용 규칙이다. 전역 Codex 작업 규칙을 반복하지 말고, 이 프로젝트의 SWMM/React/실시간 시뮬레이션 계약을 지키는 데 집중한다.

## 프로젝트 정체성

- 이 프로젝트는 SWMM 기반 도시 배수/침수 시뮬레이션을 시각화하고, UI에서 SWMM 모델링과 실시간 제어를 쉽게 만들기 위한 도구다.
- 단순 정적 뷰어가 아니라 React UI, HTML viewer, Python/PySWMM 브릿지, SWMM `.inp` 모델이 서로 같은 객체와 상태를 공유해야 한다.
- 목표 동작은 사용자가 UI에서 강수량과 각 배관/시설의 막힘 정도를 바꾸면, SWMM 상태가 1초 단위로 진행되고 그 결과가 화면에 반영되는 구조다.

## Source Of Truth

- SWMM 모델이 원본이다. 기본 라이브 모델은 `models/seoul_rebuild_v2.inp`를 우선 확인한다.
- 화면 객체와 SWMM 객체의 연결은 `sample-results/swmm_html_contract.json`이 기준이다.
- 브라우저용 계약 파일은 `viewer/swmm_html_contract.js`이며, 설명 문서는 `docs/swmm_html_contract.md`다.
- 계약을 바꿀 때는 `scripts/build_swmm_html_contract.py`에서 생성되는 JSON/JS/문서가 함께 맞아야 한다.
- React 쪽 객체 ID, HTML 객체 ID, contract의 `htmlId`, SWMM node/link ID를 따로따로 임의 변경하지 않는다.

## React ↔ SWMM 계약

- UI가 SWMM에 보낼 수 있는 입력은 기본적으로 강수량과 객체별 막힘 정도다.
- 현재 브릿지 입력 이름은 `stepSeconds`, `rainfall`, `rainfallRatio`, `exceptions`, `blockagesById`, `contractVersion`, `sourceOfTruth`를 기준으로 확인한다.
- UI에서 유량, 유속, 만관 여부, 역류 여부, 펌프 배출량, 월류량을 직접 계산한 값을 SWMM 결과처럼 취급하지 않는다.
- 라이브 시뮬레이션 값은 `scripts/swmm_html_bridge.py`와 `server/swmm_engine_server.py`의 응답을 기준으로 렌더링한다.
- 데모/플레이백/보정용 화면 로직이 필요하면, 그것이 SWMM 계산 결과가 아니라는 경계를 코드와 UI 상태명에서 분명히 한다.

## 1초 스텝 규칙

- 기본 시뮬레이션 진행 단위는 1초다. `stepSeconds: 1` 흐름을 기본값으로 취급한다.
- tick 주기를 바꾸는 작업은 SWMM 엔진, 서버 세션, React 상태 갱신, 애니메이션 속도, CSV/샘플 결과 해석을 함께 확인해야 한다.
- UI 애니메이션을 부드럽게 하기 위한 보간과 SWMM의 1초 계산 스텝을 혼동하지 않는다.
- React에서 빠른 입력 변경이 발생해도 서버에는 현재 제어 상태가 일관된 payload로 전달되어야 한다.

## SWMM 도메인 규칙

- node/link/conduit/orifice/weir/pump/outfall/subcatchment 의미를 UI 편의상 바꾸지 않는다.
- 화면에서 ㄱ자로 보이는 관은 SWMM에서 `수평 관 + 접합 노드 + 수직 관`으로 나뉠 수 있다. 시각 객체 1개가 SWMM link 여러 개에 매핑될 수 있음을 항상 고려한다.
- 분류식 우수, 분류식 오수, 합류식, 차집관거, 우수토실/월류시설, 물재생센터, 펌프장, 방류구의 흐름 방향과 역할을 유지한다.
- 막힘은 단순 CSS 효과가 아니라 SWMM 제어 링크 setting, 게이트/오리피스/위어/펌프 상태와 연결될 수 있는 입력값이다.
- 역류는 막힘 하나만으로 단정하지 않는다. 하천 수위, 만관 조건, 상류 유입, 배출 제한 조건을 함께 본다.

## 주요 파일 역할

- `models/*.inp`: SWMM 모델 원본. 구조, 노드, 링크, 제어시설 변경의 최종 기준이다.
- `scripts/build_swmm_html_contract.py`: SWMM 모델과 화면 객체 사이의 계약 생성기다.
- `scripts/swmm_html_bridge.py`: PySWMM으로 1초 step을 진행하고 화면용 상태 payload를 만든다.
- `server/swmm_engine_server.py`: 브라우저/React가 호출하는 SWMM 엔진 HTTP 서버다.
- `docs/swmm_html_contract.md`: 화면 객체와 SWMM node/link 매핑 설명이다.
- `docs/hydraulic_control_rules.md`: 발표용/간이 물리 조건과 시설 작동 규칙이다.
- `docs/work_log.md`: 작업 내용, 판단, 검증 결과를 누적하는 단일 작업 로그다.
- `viewer/overall_drainage_diagram.html`: 기존 HTML 기반 제어/시각화 화면이다.
- `react-viewer/src`: React 기반 모델링/시각화 UI다.

## 작업 로그 규칙

- 모든 의미 있는 변경 작업은 `docs/work_log.md` 한 파일에 누적해서 기록한다.
- 새 작업을 시작하기 전에는 `docs/work_log.md`의 최근 작업 3개를 먼저 확인하고, 현재 작업과 충돌하거나 이어지는 맥락이 있는지 반영한다.
- 로그는 최신 항목이 위로 오도록 작성한다.
- 각 항목에는 날짜, 작업 요약, 수정한 주요 파일, 검증 결과, 다음 작업자가 알아야 할 주의점을 짧게 남긴다.
- SWMM 모델, contract, 서버 payload, React 상태 구조 중 하나라도 바뀌면 어떤 계층까지 맞췄는지 로그에 명시한다.

## 변경 시 확인할 것

- 새 UI 객체를 추가하면 contract에 `htmlId`, `objectType`, `swmmNodes`, `swmmLinks`, `controls`가 맞게 반영되어야 한다.
- SWMM node/link를 추가, 삭제, rename하면 contract 생성 결과에서 누락 매핑이 0개인지 확인한다.
- React 타입이나 상태 구조를 바꾸면 서버 payload와 HTML contract의 필드명이 함께 맞는지 확인한다.
- 강수량/막힘 slider 값은 0~1 비율과 0~100 표시값을 혼동하지 않는다.
- 샘플 CSV 기반 플레이백과 라이브 SWMM step 모드를 섞을 때는 `sourceOfTruth`와 mode 이름으로 구분한다.

## 권장 검증

- 계약 변경 후: `python3 scripts/build_swmm_html_contract.py`
- 브릿지 샘플 확인: `python3 scripts/swmm_html_bridge.py --steps 3`
- 서버 확인: `python3 server/swmm_engine_server.py --port 8765`
- React 확인: `cd react-viewer && npm run build`

PySWMM 설치나 macOS 동적 라이브러리 문제로 검증이 실패하면, 실패를 숨기지 말고 어떤 계층에서 막혔는지 구분해서 보고한다.
