# React Editor JSON - SWMM 모델/결과 연동 분석

작성일: 2026-06-16 KST

## 목적

React 편집모드에서 완성한 JSON을 실제 SWMM 모델로 변환하고, SWMM 계산 결과를 다시 React UI에 표시하려면 중간에 두 계약이 필요하다.

1. Editor -> SWMM 모델링 계약
2. SWMM 결과 -> UI 표시 계약

현재 React 편집기는 화면 객체 배치와 attach 관계를 다루는 수준까지 잘 진행되어 있지만, 이 JSON을 그대로 SWMM `.inp`로 만들기에는 수리 모델 필드와 contract 매핑 정보가 부족하다. 이 문서는 현재 구조를 기준으로 무엇을 유지하고, 무엇을 새로 정의해야 하는지 정리한다.

## 확인한 파일

- `react-viewer/src/components/editor/editorTypes.ts`
- `react-viewer/src/components/editor/layoutStorage.ts`
- `react-viewer/src/components/editor/EditorCanvas.tsx`
- `react-viewer/src/components/editor/defaultLayout.ts`
- `react-viewer/src/services/swmm/client.ts`
- `models/seoul_rebuild_v2.inp`
- `scripts/build_swmm_html_contract.py`
- `scripts/swmm_html_bridge.py`
- `server/swmm_engine_server.py`
- `sample-results/swmm_html_contract.json`
- `viewer/overall_drainage_diagram.html`
- `docs/swmm_html_contract.md`
- `docs/swmm_html_bridge.md`
- `docs/design_network_structure.md`
- `docs/swmm_rebuild_v2.md`
- `scripts/network_registry.py`
- `scripts/design_scenario_builder.py`

## 현재 구조 요약

### React 편집 JSON

현재 `EditorLayout`은 다음 구조다.

```ts
interface EditorLayout {
  version: 1
  groundSurfaceY: number
  nodes: EditorNode[]
  links: EditorLink[]
}
```

`EditorNode`는 `id`, `swmmId`, `name`, `type`, 화면 좌표/크기, 포트, 자유형 `props`를 가진다. `EditorLink`는 `from`, `to`, `size`, `props.route`, `slope`, `length`, `blockage`, `pipeKind` 정도를 가진다.

이 구조는 화면 편집에는 충분하지만 SWMM 모델 생성에는 부족하다. 특히 현재 `relation` 링크는 화면 attach/그룹 이동 관계이며, SWMM의 `CONDUIT`, `ORIFICE`, `WEIR`, `PUMP` 링크와 같은 의미가 아니다.

현재 JSON 저장/내보내기는 다음 상태다.

- localStorage key: `swmm-react-editor-layout-v1`
- 검증: `version === 1`, `nodes` 배열, `links` 배열만 확인
- 내보내기: `drainage-layout.json`으로 `EditorLayout` 원본을 저장
- React SWMM client: `getSwmmEngineStatus()`가 `{ connected: false }`를 반환하는 stub 상태

### 기존 SWMM/HTML 계약

현재 실제 모델의 원본은 `models/seoul_rebuild_v2.inp`이고, 화면과 모델의 연결은 `sample-results/swmm_html_contract.json`이 담당한다.

계약 생성 결과는 다음 상태다.

- contract version: `2026-06-12-swmm-first-contract-v1`
- visualObjects: 42개
- SWMM nodes: 68개
- SWMM links: 66개
- missing mappings: 0개
- objectTypes: `pipe_group` 24개, `catch_basin` 5개, `manhole` 3개, `surface` 4개, `outfall` 3개, `overflow_facility` 1개, `pump_station` 1개, `treatment_facility` 1개

현재 contract는 `scripts/build_swmm_html_contract.py` 안의 `VISUAL_OBJECTS`가 기준이다. 즉, React 편집 JSON에서 contract가 자동 생성되는 구조는 아직 아니다.

### 실제 SWMM 모델이 요구하는 핵심 섹션

`models/seoul_rebuild_v2.inp` 기준 주요 섹션 수는 다음과 같다.

| 섹션 | 개수 | 의미 |
|---|---:|---|
| `JUNCTIONS` | 57 | 계산 노드, 접합점, 건물/맨홀/중간 connector 노드 |
| `STORAGE` | 8 | 빗물받이, 우수토실, 펌프장, 물재생센터 등 저장 노드 |
| `OUTFALLS` | 3 | 월류/펌프/처리수 방류구 |
| `ORIFICES` | 15 | 빗물받이 입출구, 방류구 gate, 우수토실 normal gate |
| `WEIRS` | 1 | 우수토실 초과 월류 weir |
| `PUMPS` | 1 | 빗물펌프 |
| `CONDUITS` | 49 | 관거/연결관/토출관 |
| `XSECTIONS` | 65 | 관/오리피스/위어 단면 |
| `LOSSES` | 49 | 관 손실, ㄱ자/수직부 손실 |
| `INFLOWS` | 12 | 강우/생활오수 유입 |
| `TIMESERIES` | 11 | 강우, 생활오수 유입 패턴 |
| `CURVES` | 5 | 펌프 곡선 |
| `COORDINATES` | 68 | SWMM GUI 표시 좌표 |

SWMM에서는 하나의 화면 객체가 여러 SWMM 객체로 펼쳐질 수 있다. 예를 들어 화면의 우수 본관 하나는 중간 attach 지점 때문에 여러 conduit segment와 connector junction으로 쪼개진다. ㄱ자 연결관도 화면에서는 하나처럼 보이지만 SWMM에서는 수평 conduit, elbow junction, 수직 conduit로 나뉠 수 있다.

## Editor -> SWMM 모델링 계약

### 필요한 원칙

React 편집 JSON을 바로 `.inp`로 저장하지 말고, 중간 산출물로 `EditorLayout`과 별도의 `DrainageModelDocument`를 만들어야 한다.

권장 흐름:

```text
EditorLayout
-> validate layout graph
-> DrainageModelDocument
-> SWMM .inp
-> swmm_html_contract.json
-> React/HTML result mapping
```

`EditorLayout`은 화면 편집 상태를 유지하고, `DrainageModelDocument`는 SWMM 생성에 필요한 의미/수리 필드를 가진다.

### 제안 데이터 구조

```ts
interface DrainageModelDocument {
  version: 1
  sourceLayoutVersion: 1
  units: {
    length: 'm'
    flow: 'CMS'
  }
  visualObjects: DrainageVisualObject[]
  swmmNodes: DrainageSwmmNode[]
  swmmLinks: DrainageSwmmLink[]
  controls: DrainageControl[]
  inflows: DrainageInflow[]
  timeseries: DrainageTimeseries[]
  display: {
    groundSurfaceY: number
    screenToSwmmMap: 'swmmY = mapHeight - screenY'
  }
}
```

`DrainageVisualObject`는 UI 객체와 SWMM 객체 묶음을 이어준다.

```ts
interface DrainageVisualObject {
  editorId: string
  htmlId: string
  swmmId: string
  label: string
  objectType:
    | 'surface'
    | 'catch_basin'
    | 'manhole'
    | 'pipe_group'
    | 'overflow_facility'
    | 'pump_station'
    | 'treatment_facility'
    | 'outfall'
  system: 'separate' | 'combined' | 'treatment'
  waterType: 'storm' | 'sewer' | 'combined' | 'overflow' | 'treated'
  swmmNodes: string[]
  swmmLinks: string[]
  controls: string[]
  editorGeometry: {
    x: number
    y: number
    width: number
    height: number
    attachPorts?: string[]
  }
}
```

`DrainageSwmmNode`는 `.inp`의 `JUNCTIONS`, `STORAGE`, `OUTFALLS`를 만들 수 있어야 한다.

```ts
interface DrainageSwmmNode {
  id: string
  nodeType: 'JUNCTION' | 'STORAGE' | 'OUTFALL'
  elevationM: number
  maxDepthM?: number
  initialDepthM?: number
  surchargeDepthM?: number
  pondedAreaM2?: number
  storage?: {
    shape: 'FUNCTIONAL' | 'TABULAR'
    curveOrParam: number | string
    evaporationFactor?: number
  }
  outfall?: {
    type: 'FREE' | 'NORMAL' | 'FIXED' | 'TIDAL' | 'TIMESERIES'
    stageData?: string | number
    gated: boolean
  }
  map: {
    x: number
    y: number
  }
}
```

`DrainageSwmmLink`는 `.inp`의 `CONDUITS`, `ORIFICES`, `WEIRS`, `PUMPS`, `XSECTIONS`, `LOSSES`를 만들 수 있어야 한다.

```ts
interface DrainageSwmmLink {
  id: string
  linkType: 'CONDUIT' | 'ORIFICE' | 'WEIR' | 'PUMP'
  fromNode: string
  toNode: string
  lengthM?: number
  roughnessN?: number
  inOffsetM?: number
  outOffsetM?: number
  initialFlowCms?: number
  maxFlowCms?: number
  xsection?: {
    shape: 'CIRCULAR' | 'RECT_CLOSED' | 'RECT_OPEN'
    geom1: number
    geom2?: number
    geom3?: number
    geom4?: number
    barrels?: number
    culvert?: number
  }
  losses?: {
    inletLoss: number
    outletLoss: number
    averageLoss: number
    flapGate: boolean
    seepageRate: number
  }
  orifice?: {
    type: 'BOTTOM' | 'SIDE'
    offsetM: number
    qCoeff: number
    gated: boolean
    closeTimeSeconds: number
  }
  weir?: {
    type: 'TRANSVERSE'
    crestHeightM: number
    qCoeff: number
    gated: boolean
    surcharge: boolean
  }
  pump?: {
    curveId: string
    status: 'ON' | 'OFF'
    startupDepthM: number
    shutoffDepthM: number
  }
}
```

### attach 관계를 SWMM으로 변환하는 규칙

편집기의 `relation`은 SWMM 링크가 아니라 “붙어 함께 움직이는 화면 관계”다. SWMM 변환 단계에서는 다음 규칙으로 해석해야 한다.

1. parent -> child 방향은 편집 의도를 보존하는 관계 방향이다.
2. `relation` 자체를 `.inp` 링크로 만들지 않는다.
3. 실제 SWMM 링크는 pipe/facility/outfall의 의미 필드와 attach endpoint를 보고 생성한다.
4. 파이프 중간 tap에 다른 관이 붙으면, SWMM에서는 대상 파이프를 두 개 이상의 conduit segment로 분할하고 tap 위치에 connector junction을 추가한다.
5. 한 파이프에 부모가 여러 명 붙을 수 있으므로, 파이프 tap은 `portId`와 `offsetRatio`를 모델 문서에 남겨야 한다.
6. ㄱ자 connector는 화면 객체 하나여도 SWMM에서는 최소 `horizontal conduit + elbow junction + vertical conduit`로 펼쳐질 수 있다.
7. facility/outfall의 tap attach도 같은 방식으로 `port side + offsetRatio`를 보존해야 한다. 다만 시설은 직접 conduit를 여러 개 생성하기보다 facility storage/outfall node로 들어오는 접속 링크를 여러 개 허용하는 쪽이 자연스럽다.

### 현재 React JSON에서 부족한 항목

현재 `EditorLayout`에는 다음 정보가 없다.

- SWMM node type: `JUNCTION`, `STORAGE`, `OUTFALL`
- SWMM link type: `CONDUIT`, `ORIFICE`, `WEIR`, `PUMP`
- 각 node의 `elevationM`, `maxDepthM`, `initialDepthM`, `surchargeDepthM`, `pondedAreaM2`
- storage shape/curve
- outfall type/stage/gated
- conduit length/roughness/offset/maxFlow
- xsection shape/geometries/barrels
- losses/flapGate
- pump curve/startup/shutoff
- orifice/weir 계수
- rainfall/sewer inflow 대상과 multiplier
- `system`, `waterType`, `objectType`의 명시 필드
- visual object가 어떤 `swmmNodes`, `swmmLinks`, `controls`에 매핑되는지
- screen 좌표와 SWMM map 좌표 변환 규칙
- 다중 tap attach가 SWMM segment 분할을 일으킨다는 구조적 정보

따라서 다음 구현 단계에서 raw `EditorLayout` export와 별도로 “모델링 export”를 추가해야 한다.

## SWMM 결과 -> UI 표시 계약

### 현재 Python bridge 결과

`scripts/swmm_html_bridge.py`와 `server/swmm_engine_server.py`는 이미 React가 재사용할 수 있는 결과 구조를 제공한다.

`POST /session/step` 결과 핵심 구조:

```json
{
  "ok": true,
  "stepIndex": 1,
  "contractVersion": "2026-06-12-swmm-first-contract-v1",
  "sourceOfTruth": "SWMM",
  "modelTime": "2026-06-11T00:00:01",
  "rainfallRatio": 0.75,
  "pipes": {
    "sep_storm_main_1": {
      "flow_cms": 0.0,
      "velocity_mps": 0.0,
      "direction": "forward",
      "active": false,
      "capacity_cms": 1.15,
      "fullness": 0.0
    }
  },
  "assets": {
    "sep_catch_basin_1": {
      "depth_m": 0.04,
      "depth_ratio": 0.12,
      "inflow_cms": 0.03,
      "flow_cms": 0.03,
      "velocity_mps": 0.0,
      "direction": "forward",
      "active": true,
      "status": "normal"
    }
  },
  "controls": {
    "storm_pump_unit": {
      "target_setting": 0.0,
      "flow_cms": 0.0,
      "active": false
    }
  }
}
```

React는 이 payload를 계산하지 말고 표시해야 한다. HTML viewer의 `applySwmmStatePayload()`가 현재 참고 구현이다.

### React에 필요한 상태

React 쪽에는 최소 다음 타입이 필요하다.

```ts
interface SwmmStatePayload {
  ok?: boolean
  stepIndex?: number
  contractVersion: string
  sourceOfTruth: 'SWMM'
  modelTime: string
  rainfallRatio: number
  pipes: Record<string, SwmmPipeState>
  assets: Record<string, SwmmAssetState>
  controls: Record<string, SwmmControlState>
}

interface SwmmPipeState {
  flow_cms: number
  velocity_mps: number
  direction: 'forward' | 'reverse'
  active: boolean
  capacity_cms?: number
  fullness: number
}

interface SwmmAssetState {
  depth_m: number
  depth_ratio: number
  inflow_cms: number
  flow_cms: number
  velocity_mps: number
  direction: 'forward' | 'reverse'
  active: boolean
  status: 'normal' | 'warning' | 'surcharge' | 'idle' | string
}

interface SwmmControlState {
  target_setting: number
  flow_cms: number
  active: boolean
}
```

React 표시 규칙:

1. `contractVersion`이 현재 로드한 contract와 다르면 경고를 표시한다.
2. `pipes[htmlId]`는 해당 editor/diagram object의 유량, 유속, 만관율, 역류 방향 표시로만 사용한다.
3. `assets[htmlId]`는 시설 수위, 활성 상태, 경고 상태 표시로만 사용한다.
4. `controls[swmmLinkId]`는 펌프/gate 상태 표시로만 사용한다.
5. React가 임의로 유량, 역류, 만관 여부를 계산하지 않는다.
6. 화면 애니메이션용 보간값은 `sourceOfTruth: 'SWMM'` 결과와 구분되는 UI-only state로 둔다.

### React client 구현 대상

현재 `react-viewer/src/services/swmm/client.ts`는 stub이다. 다음 API가 필요하다.

- `getContract(engineUrl): Promise<SwmmHtmlContract>`
- `startSession(engineUrl, stepSeconds): Promise<ResetResponse>`
- `resetSession(engineUrl, stepSeconds): Promise<ResetResponse>`
- `stepSession(engineUrl, payload): Promise<SwmmStatePayload>`
- `getHealth(engineUrl): Promise<SwmmEngineHealth>`

React editor/diagram에서 보낼 control payload는 HTML viewer와 같은 필드를 유지해야 한다.

```json
{
  "contractVersion": "2026-06-12-swmm-first-contract-v1",
  "sourceOfTruth": "SWMM",
  "stepSeconds": 1,
  "rainfallRatio": 0.75,
  "exceptions": [],
  "blockagesById": {},
  "physicsMode": "swmm-step",
  "htmlRole": "render_only_with_controls"
}
```

## 수정이 필요한 위치

### 1. React editor 타입

파일: `react-viewer/src/components/editor/editorTypes.ts`

필요 작업:

- `EditorLayout`은 화면 편집 상태로 유지
- 새 `DrainageModelDocument` 타입 추가
- `EditorNode.props` 자유형 값에 숨겨두던 `facilityKind`, `outfallKind`, `pipeKind`를 모델링 변환에서 해석 가능한 명시 enum으로 정리
- endpoint에 `tap offsetRatio`, `side`, `isCenterGuide` 같은 정보를 얻을 수 있는 helper 추가

### 2. JSON 저장/검증

파일: `react-viewer/src/components/editor/layoutStorage.ts`

필요 작업:

- 현재는 배열 여부만 검사하므로, 모델링 export에는 별도 validator가 필요
- layout schema version과 model document schema version을 분리
- 깨진 localStorage 복원/마이그레이션 규칙 유지

### 3. 모델링 export

파일: `react-viewer/src/components/editor/EditorCanvas.tsx` 또는 별도 모듈

필요 작업:

- 기존 `drainage-layout.json` export는 유지
- 새 `SWMM 모델링 JSON 내보내기` 추가
- `relation` 링크를 직접 SWMM 링크로 쓰지 않고, attach graph를 해석해 `visualObjects`, `swmmNodes`, `swmmLinks`를 만드는 변환 함수 추가
- 변환 전 validation 오류 표시:
  - SWMM ID 중복
  - dangling relation
  - pipe/facility에 필수 수리 필드 누락
  - 다중 tap offset 충돌
  - outfall 없는 방류 흐름
  - pump/weir/orifice control 누락

### 4. SWMM 모델 생성 스크립트

새 파일 후보:

- `scripts/editor_model_document_to_inp.py`
- `scripts/editor_model_document_to_contract.py`

필요 작업:

- `DrainageModelDocument`를 입력으로 받아 `.inp` 생성
- 생성한 `.inp`를 다시 `scripts/build_swmm_html_contract.py` 또는 후속 generator로 넘겨 contract 생성
- 생성 후 missing mapping이 0개인지 검사
- SWMM에서는 중간 접속이 직접 불가능하므로, pipe tap마다 junction과 conduit segment를 자동 생성

### 5. contract generator

파일: `scripts/build_swmm_html_contract.py`

필요 작업:

- 현재 하드코딩 `VISUAL_OBJECTS` 유지 가능
- 다음 단계에서는 editor-generated `visualObjects`를 입력으로 받을 수 있게 옵션 추가
- 기존 HTML viewer와 React가 같은 contract 형식을 읽도록 유지

### 6. React SWMM client

파일: `react-viewer/src/services/swmm/client.ts`

필요 작업:

- 실제 HTTP client 구현
- `/health`, `/contract`, `/session/start`, `/session/reset`, `/session/step` 연결
- payload/result 타입 정의
- engine unavailable, PySWMM unavailable, contract mismatch를 UI에서 구분

### 7. React 결과 렌더링

대상: React diagram/viewer 계층

필요 작업:

- `swmmState.pipes[htmlId]`를 pipe visual에 반영
- `swmmState.assets[htmlId]`를 시설/노드 visual에 반영
- `swmmState.controls[id]`를 pump/gate 상태에 반영
- blockage slider 값은 UI 입력이고, flow/fullness/backflow는 SWMM 결과임을 상태명에서 분리

## 단계별 구현 권장안

### 1단계: 계약 타입 고정

- `DrainageModelDocument` 타입/JSON schema 작성
- 기존 `EditorLayout`에서 model document로 변환하는 read-only 함수 작성
- 아직 `.inp` 생성은 하지 않고 validation report만 만든다.

### 2단계: default layout golden 변환

- 현재 `defaultLayout.ts`를 입력으로 model document를 생성하는 테스트 추가
- 기대 결과:
  - visual object 수
  - SWMM node/link 후보 수
  - pipe tap 분할 지점
  - missing required field 목록

### 3단계: `.inp` 생성기 작성

- model document -> `.inp`
- 생성된 `.inp`를 대상으로 contract 생성
- missing mapping 0개 검사

### 4단계: React SWMM client 연결

- `/contract` 로드
- `/session/step` 호출
- `pipes/assets/controls` 결과를 UI state에 저장
- HTML viewer의 `applySwmmStatePayload()`와 같은 의미로 렌더링

### 5단계: round-trip 검증

```text
React editor layout
-> model document
-> SWMM .inp
-> contract
-> server step
-> React render state
```

이 흐름을 최소 1개 fixture로 자동화한다.

## 검증 결과

### contract 생성

명령:

```bash
python3 scripts/build_swmm_html_contract.py
```

결과:

```text
visual_objects=42
nodes=68
links=66
missing_mappings=0
```

판단: 현재 SWMM 모델과 HTML contract는 일관성이 있다.

### React build

명령:

```bash
cd react-viewer && npm run build
```

결과:

```text
tsc -b && vite build
✓ built
```

판단: 현재 React 편집기 타입/빌드는 통과한다.

### PySWMM bridge

명령:

```bash
python3 scripts/swmm_html_bridge.py --steps 3
```

결과:

```text
PySWMM is not installed. Install it first with `python3 -m pip install pyswmm`.
```

판단: 시스템 `python3`에는 PySWMM이 없다.

재실행:

```bash
.venv/bin/python scripts/swmm_html_bridge.py --steps 3
```

결과:

```text
Wrote sample-results/swmm_html_bridge_preview.jsonl
```

판단: 프로젝트 `.venv` 기준으로는 PySWMM bridge 3 step이 정상 실행된다.

### HTTP server smoke

`8765`는 이미 기존 엔진 서버가 사용 중이었다.

확인 결과:

- `GET http://127.0.0.1:8765/health` 응답 OK
- `GET http://127.0.0.1:8765/contract` 응답 OK
- 새 서버를 같은 포트로 띄우면 `Address already in use`

다른 포트 검증:

```bash
.venv/bin/python server/swmm_engine_server.py --port 8766
```

결과:

- `GET /health` OK
- `GET /contract` OK
- `POST /session/step` OK

`POST /session/step` 요약:

```text
ok=True
stepIndex=1
contractVersion=2026-06-12-swmm-first-contract-v1
pipes=24
assets=18
controls=6
```

판단: 서버 API는 React가 붙을 최소 표면을 이미 제공한다.

## 2026-06-16 추가 진행: 에디터 JSON -> SWMM `.inp` 1차 변환기

사용자가 기존 `viewer/overall_drainage_diagram.html` 기반 전체배수도는 지금 단계에서 사용하지 않고, React 에디터에서 제작된 JSON만 기준으로 SWMM 모델링을 진행하겠다고 방향을 좁혔다.

이에 따라 기존 HTML contract 재사용은 뒤로 미루고, 다음 독립 변환기를 추가했다.

```text
scripts/editor_layout_to_swmm_inp.py
```

### 변환기 역할

- 입력: React 편집모드에서 내보낸 `EditorLayout` JSON
- 출력: SWMM이 읽을 수 있는 `.inp` skeleton
- 기본 출력 경로: `models/generated_from_editor.inp`
- 기존 HTML viewer/contract에는 의존하지 않음
- `relation` 링크는 화면 attach 관계로 해석하고, 직접 SWMM 링크로 쓰지 않음

### 현재 변환 규칙

- `apartment`, `house`, `manhole`, `connector`, `elbowConnector`는 SWMM `JUNCTIONS`로 변환한다.
- `catchBasin`, `facility`는 SWMM `STORAGE`로 변환한다.
- `outfall`은 SWMM `OUTFALLS`로 변환한다.
- `pipeSegment`는 SWMM `CONDUIT`로 변환한다.
- `pipeSegment`의 `left/right/top/bottom` 또는 `tap-*` relation endpoint를 보고 시작/끝/tap junction을 결정한다.
- `tap-top-25` 같은 tap 관계가 있으면 station 비율을 해석해 파이프를 여러 segment로 나눌 수 있다.
- 직접 `pipe`, `elbowPipe`, `connector`, `outfall` 링크는 SWMM `CONDUIT`로 변환한다.
- 직접 `pump` 링크는 SWMM `PUMP`와 기본 pump curve로 변환한다.
- 직접 `weir` 링크는 SWMM `WEIR`로 변환한다.
- 수리 필드가 아직 에디터 JSON에 없으므로, 관경/조도/저류면적/수위/유입 시계열은 보수적인 기본값을 부여한다.

### 사용법

```bash
python3 scripts/editor_layout_to_swmm_inp.py \
  --input path/to/drainage-layout.json \
  --output models/generated_from_editor.inp
```

stdin도 지원한다.

```bash
python3 scripts/editor_layout_to_swmm_inp.py --input - --output /tmp/generated_from_editor.inp
```

### 이번 검증 결과

검증:

```bash
python3 -m py_compile scripts/editor_layout_to_swmm_inp.py
```

결과: 통과

pipeSegment + relation 기반 샘플 변환:

```bash
python3 scripts/editor_layout_to_swmm_inp.py --input - --output /tmp/generated_from_editor_smoke.inp
```

결과:

```text
summary={"conduits": 3, "inflows": 1, "junctions": 2, "outfalls": 1, "pumps": 0, "storages": 1, "warnings": 0, "weirs": 0}
```

PySWMM 실행:

```bash
.venv/bin/python -c "from pyswmm import Simulation; ..."
```

결과:

```text
{'steps': 3}
```

직접 `pipe/elbowPipe/pump` 링크 기반 샘플도 별도로 변환했고, PySWMM 3 step 실행을 통과했다.

### 현재 한계

- 아직 React UI에서 “SWMM 모델 내보내기” 버튼으로 연결되지는 않았다.
- 에디터 JSON에 실제 수리 입력 필드가 없어서 elevation, maxDepth, roughness, diameter, storage factor 등은 기본값이다.
- 생성된 `.inp`는 첫 실행 가능한 skeleton이며, 실제 설계 정확도를 보장하는 최종 수리 모델은 아니다.
- 기존 `swmm_html_contract.json` 생성과는 아직 연결하지 않았다.
- SWMM 결과를 React UI에 다시 표시하는 작업도 아직 별도 단계다.

## 결론

현재 가장 큰 간극은 React editor JSON이 “화면 편집 상태”라는 점이다. 이 JSON을 직접 SWMM `.inp`로 취급하면 attach 관계, 다중 tap, facility/outfall 종류, 수리 계산 필드가 섞여서 장기적으로 깨지기 쉽다.

다음 작업은 새 중간 계약 `DrainageModelDocument`를 세우는 것이 가장 안전하다. 이 문서는 React 편집기의 화면 좌표/관계와 SWMM의 node/link/control/result contract를 분리해준다. 그 뒤 `.inp` 생성기와 React SWMM client를 붙이면 다음 흐름이 명확해진다.

```text
EditorLayout = 화면 편집/attach 상태
DrainageModelDocument = SWMM 생성 가능한 의미 모델
swmm_html_contract.json = 화면 객체와 SWMM 결과 매핑
SwmmStatePayload = SWMM 계산 결과 표시용 payload
```

이 구조로 가면 편집모드에서 만든 배수도는 SWMM 모델로 변환 가능해지고, PySWMM 결과도 React UI에 같은 ID 체계로 다시 표시할 수 있다.
