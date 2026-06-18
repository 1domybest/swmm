# 작업 로그

최신 작업을 위에 기록한다. 새 작업을 시작하기 전에는 최근 3개 항목을 먼저 확인한다.

## 2026-06-18 KST - 커넥터-맨홀 등 node-node relation을 내부 conduit로 변환

- 작업 요약: SWMM GUI에서 `CONN_SEWER_09`, `CONN_SEWER_10` 사이가 `-o  o-`처럼 끊겨 보이던 문제를 수정했다. 원인은 relation 방향이 아니라, 기존 변환기가 `pipeSegment`만 SWMM `CONDUIT`로 만들고 커넥터-맨홀 같은 node-node relation은 수리 링크로 펼치지 않았기 때문이다. 이제 pipe가 아닌 두 hydraulic node 사이 relation은 최소 길이 1.0m 이상인 짧은 내부 conduit로 변환한다. 맨홀 SWMM 좌표도 시각 중심점이 아니라 relation이 붙는 하단 접속부 y를 기준으로 잡아 SWMM Map에서 연결선이 맨홀 하단부에 붙어 보이도록 했다.
- 주요 파일: `scripts/editor_layout_to_swmm_inp.py`, `docs/work_log.md`
- 검증 결과: `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py server/swmm_engine_server.py` 통과. `/Users/onseoktae/Downloads/drainage-layout (1).json` 변환 결과 error 0개, warning 6개 유지. `REL_006_CONDUIT: CONN_SEWER_09 -> MH_SEWER_01`, `REL_009_CONDUIT: MH_SEWER_01 -> CONN_SEWER_10` 생성 확인. 전체 conduit 수는 내부 relation conduit 포함 65개이고, 막힘 제어 대상은 명시적 pipeSegment 41개로 유지했다. 강우 target은 9개로 유지했다. 수정된 서버를 `127.0.0.1:8765`로 재시작하고 `/editor/convert/validate` 응답에서 동일 결과를 확인했다.
- 계층 영향: JSON -> SWMM INP 변환기의 topology 추론을 변경했다. `relation` 자체를 SWMM 객체로 승격한 것은 아니고, pipe가 생략된 node-node attach를 실제 수리 연결로 펼치기 위한 내부 conduit를 생성한다. React UI와 기존 SWMM 모델 원본은 변경하지 않았다.
- 주의점: relation 방향이 반대면 선은 생성되지만 SWMM `from -> to` 흐름 방향이 반대로 잡힌다. 방향 warning은 기존처럼 별도로 확인해야 한다.

## 2026-06-18 KST - INP 단독 다운로드 warning 헤더 인코딩 수정

- 작업 요약: React의 `INP만 다운로드` 버튼에서 `Failed to fetch`가 뜨던 문제를 수정했다. 변환 자체는 성공했지만 서버가 `X-Editor-Inp-Warnings` 응답 헤더에 한국어 warning 문자열을 그대로 넣으면서 HTTP 헤더가 깨져 브라우저 fetch가 실패했다. warning header를 ASCII JSON escape(`ensure_ascii=True`)로 보내도록 바꿨다.
- 주요 파일: `server/swmm_engine_server.py`, `docs/work_log.md`
- 검증 결과: `python3 -m py_compile server/swmm_engine_server.py` 통과. 수정된 서버를 `127.0.0.1:8765`로 재시작한 뒤 `/editor/export-inp` POST 요청이 200으로 `generated_from_editor.inp` 28919 bytes를 반환하는 것 확인. CORS/preflight와 warning header도 정상 확인.
- 계층 영향: 서버의 INP 텍스트 다운로드 응답 헤더만 변경했다. 변환 규칙, React UI, SWMM 모델 원본은 변경하지 않았다.
- 주의점: warning 내용은 기존처럼 React에서 alert로 표시되며, 헤더 내부에서는 `\\uXXXX` escape 형태로 전송된다.

## 2026-06-18 KST - SWMM MAP 좌표를 React 레이아웃 기준으로 정규화

- 작업 요약: React에서 화면 밖까지 이어지는 긴 관이 SWMM GUI에서는 중간부터 시작하는 것처럼 보이던 문제를 수정했다. 기존 변환기는 conduit `Length`는 React 관 길이 기반으로 계산했지만 `[MAP] DIMENSIONS`를 `0 0 3000 2000`으로 고정했고, y축 반전도 고정 `mapHeight=2000` 기준이라 큰/음수 좌표 레이아웃에서 SWMM GUI 표시가 어긋났다. 이제 전체 React node bounds를 기준으로 좌표를 meter 단위로 정규화하고 y축을 뒤집으며, `[MAP] DIMENSIONS`도 동적으로 출력한다. React 원본 좌표는 mapping JSON의 `reactPoint`에 계속 보존한다.
- 주요 파일: `scripts/editor_layout_to_swmm_inp.py`, `docs/work_log.md`
- 검증 결과: `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py server/swmm_engine_server.py` 통과. `/Users/onseoktae/Downloads/drainage-layout (1).json` 변환에서 error 0개, 기존 방향 warning 6개 유지, `PIPE_COMB_MAIN_01` 길이 2105.31m 유지 확인. 새 `[MAP] DIMENSIONS`는 `0.00 0.00 5036.21 1409.00`으로 출력되고, 합류식 본관 시작점은 SWMM 좌표 x=56.34m로 맵 왼쪽 근처에 배치되는 것 확인.
- 계층 영향: JSON -> SWMM INP 변환기의 지도 좌표/맵 범위 산출만 변경했다. 관 수리 길이 계산은 기존처럼 React 파이프 width/height 및 attach station 기반을 유지하고, 너무 짧은 경우에만 최소 conduit length 1.0m 보정을 적용한다. React UI, 서버 API shape, 기존 SWMM 모델 원본은 변경하지 않았다.
- 주의점: SWMM `[COORDINATES]`는 GUI 표시 안정성을 위해 React 좌표를 그대로 쓰지 않고 전체 레이아웃 bounds 기준으로 양수 좌표로 평행이동한다. 원본 React 좌표가 필요하면 `swmm-react-mapping.json`의 `reactPoint`를 확인한다.

## 2026-06-18 KST - React editor JSON -> SWMM 변환 검증/ZIP 패널 추가

- 작업 요약: React editor JSON을 기준으로 SWMM GUI 확인용 `.inp`, 변환 리포트 JSON, React/SWMM 매핑 JSON을 생성하는 1차 변환 흐름을 확장했다. 선택한 정책(0.5m/px, 지표고 100m, y좌표 기반 invert/max depth, 관경 소/중/대 0.3/0.6/1.0m, Manning n 0.013, 강우 직접 유입 기본 0mm/h, 오수 DWF 0.005 CMS, 방류구 FREE, warning/error 분리)을 변환기에 반영했고, 서버에 검증 JSON API와 ZIP 다운로드 API를 추가했다. React 오른쪽 패널에는 `시뮬레이션` 섹션을 추가해 검증, ZIP 다운로드, report/mapping JSON 다운로드를 실행할 수 있게 했다.
- 주요 파일: `scripts/editor_layout_to_swmm_inp.py`, `server/swmm_engine_server.py`, `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py server/swmm_engine_server.py` 통과, `cd react-viewer && npm run build` 통과. `/Users/onseoktae/Downloads/drainage-layout (1).json` 변환에서 error 0개, warning 6개, conduits 41개, rainfall target 9개, blockage target 41개 확인. 임시 서버 `127.0.0.1:8790`에서 `/editor/convert/validate` 200 응답과 `/editor/convert/download` ZIP 200 응답을 확인했고 ZIP에는 `model.inp`, `conversion-report.json`, `swmm-react-mapping.json` 3개 파일이 포함됐다.
- 계층 영향: React editor JSON -> SWMM INP 변환기, SWMM engine HTTP 서버 API, React editor UI 패널을 변경했다. 기존 HTML viewer contract와 기본 SWMM 모델 원본은 변경하지 않았다. `relation`은 계속 SWMM 객체가 아니라 topology/attach 추론용 UI metadata로만 사용한다.
- 주의점: 월류시설/펌프장/물재생센터는 이번 단계에서 SWMM GUI 비교용 STORAGE 중심 구조와 report/mapping 확장 대상으로 남긴다. 실제 `ORIFICE + WEIR`, `STORAGE + PUMP` 제어 링크와 1초 step 동적 강우/막힘 반영은 다음 FastAPI/PySWMM 엔진 단계에서 명확히 붙이는 것이 안전하다. 변환 warning 6개는 relation 클릭 방향과 pipe rotation 방향 충돌이며, 현재 정책대로 최종 흐름은 relation parent -> child를 따른다.

## 2026-06-18 KST - 파란 relation 포트 해체 메뉴 복원

- 작업 요약: T자 좌표 변경 진입점을 객체 우클릭으로 옮기면서 막혔던 파란 relation 포트 우클릭 메뉴를 복원했다. 파란 포트 우클릭 메뉴에서는 `좌표 변경`만 제거하고 `해체`는 계속 사용할 수 있게 했다. T자 커넥터 객체 우클릭의 `좌표 변경` 메뉴는 유지했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과, `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py` 통과.
- 계층 영향: React editor context menu UX만 변경했다. SWMM 모델, contract, 서버 payload, JSON -> SWMM INP 변환기는 변경하지 않았다.
- 주의점: 파란 포트 우클릭은 relation 해체 전용이고, T자 trunk 좌표 변경은 T자 객체 자체 우클릭 메뉴에서만 시작한다.

## 2026-06-18 KST - T자 좌표변경 진입점을 객체 우클릭으로 이동

- 작업 요약: T자 커넥터 trunk 축 좌표 변경을 기존 파란 relation 포트 우클릭 메뉴가 아니라 T자 객체 자체 우클릭 메뉴에서 시작하도록 바꿨다. T자 객체 우클릭 시 양쪽 trunk 파이프가 모두 연결되어 있으면 `좌표 변경` 버튼이 표시되고, 연결된 파란 포트 우클릭에서는 더 이상 해체/좌표변경 메뉴가 열리지 않는다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과, `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py` 통과.
- 계층 영향: React editor의 context menu 진입 방식만 변경했다. SWMM 모델, contract, 서버 payload, JSON -> SWMM INP 변환기는 변경하지 않았다.
- 주의점: relation 삭제는 파란 포트 우클릭 메뉴 대신 relation 선택 후 삭제/Backspace 흐름을 사용해야 한다.

## 2026-06-18 KST - T자 커넥터 trunk 축 좌표조정 추가

- 작업 요약: 기존 커넥터 parent 포트 우클릭의 `좌표 변경` 기능을 T자 커넥터에 맞게 확장했다. T자 커넥터는 relation 방향이 `T자 -> 파이프`이든 `파이프 -> T자`이든 trunk(`ㅡ`) 포트에서 우클릭하면 좌표 변경이 가능하며, T자와 branch 쪽 연결 객체는 trunk 축을 따라 이동하고 양쪽 trunk 파이프는 최소 길이를 유지하는 범위에서 자동으로 줄거나 늘어난다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `react-viewer/src/components/editor/editorInternalTypes.ts`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과, `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py` 통과. 기존 dev server는 `http://127.0.0.1:5175/`에서 계속 실행 중이다.
- 계층 영향: React editor의 relation 좌표 변경 인터랙션과 내부 타입만 변경했다. SWMM 모델, contract, 서버 payload, JSON -> SWMM INP 변환기는 변경하지 않았다.
- 주의점: T자 좌표 변경은 trunk 양쪽에 `pipeSegment`가 모두 연결되어 있을 때만 표시된다. 한쪽 파이프가 `MIN_PIPE_SEGMENT_LENGTH`에 닿으면 더 이상 그 방향으로 이동하지 않도록 clamp한다.

## 2026-06-18 KST - React editor T자 배관 커넥터 1차 추가

- 작업 요약: 커넥터 세부 종류에 `T자 커넥터`를 추가하고, ㄱ자 커넥터와 같은 방식으로 관 종류/굵기/오른쪽 90도 회전/포트 remap을 지원하게 했다. T자 커넥터는 좌/우/상 열린 끝단 3곳과 중앙 attach 포트를 가지며, 선택 시 해당 포트로 relation을 만들 수 있다.
- 주요 파일: `react-viewer/src/components/editor/editorTypes.ts`, `react-viewer/src/components/editor/editorDefinitions.ts`, `react-viewer/src/components/editor/defaultLayout.ts`, `react-viewer/src/components/editor/editorNodeHelpers.ts`, `react-viewer/src/components/editor/EditorCanvas.tsx`, `scripts/editor_layout_to_swmm_inp.py`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과, `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py` 통과, `teeConnector` 샘플 JSON 변환에서 `CONN_TEE_01`이 `[JUNCTIONS]`로 생성되는 것 확인. dev server는 `http://127.0.0.1:5175/`에서 실행했다.
- 계층 영향: React editor 객체 스키마와 렌더링, 편집 패널, JSON -> SWMM INP 변환기의 노드 타입 인식이 변경됐다. 기존 SWMM 모델/HTML contract/실시간 서버 payload는 변경하지 않았다.
- 주의점: 이번 단계는 T자 커넥터 객체 자체만 추가한 1차 구현이다. 사용자가 말한 `파이프2 + T자 + 파이프3` 가로 범위 안에서 T자/분기 파이프를 슬라이드하고 양쪽 파이프 길이를 자동 보정하는 좌표조정 규칙은 다음 작업으로 남겼다.

## 2026-06-18 KST - React editor 2차 구조 주석/노드 helper 분리

- 작업 요약: `EditorCanvas.tsx`의 노드/포트 순수 계산 helper를 `editorNodeHelpers.ts`로 분리하고, EditorCanvas의 top-level helper, relation 전파 규칙, 사용자 액션 핸들러, 렌더 컴포넌트 흐름에 한국어 주석을 보강했다. 영어 주석이 남아 있던 `editorDefinitions.ts`, `editorGeometry.ts`, `editorInternalTypes.ts`도 한국어로 정리했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `react-viewer/src/components/editor/editorNodeHelpers.ts`, `react-viewer/src/components/editor/editorDefinitions.ts`, `react-viewer/src/components/editor/editorGeometry.ts`, `react-viewer/src/components/editor/editorInternalTypes.ts`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React editor 내부 구조와 주석만 변경했다.
- 주의점: 동작 변경을 의도하지 않은 구조/주석 중심 리팩토링이다. relation 전파 규칙은 아직 `EditorCanvas.tsx`에 남겨 두었고, 다음 단계에서 action hook/propagation module로 분리 가능하다.

## 2026-06-18 KST - React editor 1차 무동작 리팩토링

- 작업 요약: 현재 정상 동작 중인 에디터 코드를 `backups/react-editor-before-refactor-20260618T161444.tar.gz`로 백업한 뒤, `EditorCanvas.tsx`에 몰려 있던 내부 interaction 타입, 에디터 정의/상수, 기초 좌표 helper를 별도 파일로 분리했다. attach/resize/parent-child propagation 계산식 자체는 변경하지 않았다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `react-viewer/src/components/editor/editorDefinitions.ts`, `react-viewer/src/components/editor/editorInternalTypes.ts`, `react-viewer/src/components/editor/editorGeometry.ts`, `docs/work_log.md`, `backups/react-editor-before-refactor-20260618T161444.tar.gz`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 코드 구조와 주석만 정리했다.
- 주의점: 이번 단계는 동작 보존을 우선한 1차 분리다. 관계 전파, 좌표변경, 길이조절 규칙은 아직 `EditorCanvas.tsx` 안에 남겨 두었고 다음 리팩토링에서 별도 rule 모듈로 분리하는 것이 안전하다.

## 2026-06-18 KST - React editor layout JSON 객체 이름/SWMM ID 정리

- 작업 요약: `/Users/onseoktae/Downloads/drainage-layout.json`의 96개 노드와 89개 relation을 기준으로 복사/붙여넣기에서 남은 일반명 객체를 관종류/객체 타입/방향/화면 순서 기반 이름으로 정리했다. `id`는 중복이 없어 유지했고, `swmmId`는 `PIPE_STORM_MAIN_01`, `CONN_SEWER_01`, `MH_STORM_01`, `REL_001`처럼 중복 없는 규칙형 값으로 갱신했다.
- 주요 파일: `/Users/onseoktae/Downloads/drainage-layout.json`, `docs/work_log.md`
- 검증 결과: Node JSON 검증에서 node/link `id`, `name`, `swmmId` 중복 0개, relation 참조 누락 0개 확인. 원본은 `/Users/onseoktae/Downloads/drainage-layout.backup-20260618T070206.json`에 보관했고, 변경 리포트는 `/Users/onseoktae/Downloads/drainage-layout.rename-report-20260618T070428.json`에 남겼다.
- 계층 영향: SWMM 모델, contract, 서버 payload, React UI 코드는 변경하지 않았다. React editor JSON 데이터의 표시명/식별자만 정리했다.
- 주의점: `relation`은 SWMM 객체가 아니라 UI 연결 메타데이터라 `REL_###`로만 정리했다. JSON을 에디터에 불러오면 현재 배치 그대로 이름/식별자만 바뀐다.

## 2026-06-18 KST - z-order 메뉴가 relation depth를 이기도록 수정

- 작업 요약: 객체 우클릭의 앞으로/뒤로 보내기 메뉴가 실제로 맨 앞으로 오지 않던 문제를 수정했다. 기존 렌더 정렬은 `layout.nodes` 순서보다 relation parent/child depth를 먼저 보았기 때문에 z-order 메뉴가 묻혔다. z-order 명령을 받은 노드에 `props.zOrder`를 기록하고, 렌더 정렬에서 layer 다음에 이 값을 우선하도록 바꿨다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 렌더 정렬 우선순위만 변경했다.
- 주의점: terrain/road 같은 기본 layer 우선순위는 유지된다. 같은 일반 객체 레이어 안에서는 사용자가 지정한 z-order가 relation depth보다 우선한다.

## 2026-06-18 KST - 파이프 흐름 화살표와 객체 z-order 메뉴 추가

- 작업 요약: 파이프 내부의 기존 물 차오름/점선 흐름 표현을 제거하고, 파이프 회전값 기준의 반복 화살표로 흐름 방향을 표시하도록 바꿨다. 0도 파이프는 왼쪽에서 오른쪽으로 흐르는 방향으로 보이며, 세로 파이프도 물 높이 대신 화살표 방향만 표시된다. 객체 우클릭 메뉴에는 맨 앞으로/앞으로/뒤로/맨 뒤로 보내기 z-order 조작을 추가했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 시각 표현과 객체 렌더 순서 조작 메뉴만 변경했다.
- 주의점: z-order 조작은 기존 레이어 우선순위와 relation depth 규칙 안에서 `layout.nodes` 순서를 바꾼다. 즉 terrain/road의 하위 레이어 성격과 parent가 child보다 위에 오도록 하는 기존 렌더 규칙은 유지된다.

## 2026-06-18 KST - 파이프 전체 외곽선 resize hover 복원

- 작업 요약: 파이프 길이조절 hover/hit 영역이 파이프의 길이축 끝면에만 표시되던 문제를 수정했다. 파이프 전용 resize handle 렌더링을 분리해, 가로 파이프는 위/아래 긴 변도 좌우 길이조절로 매핑하고 세로 파이프는 좌/우 긴 변도 상하 길이조절로 매핑했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 수동 resize hover/hit 영역만 변경했다.
- 주의점: 파이프의 실제 길이조절 축은 기존과 동일하게 유지된다. 단지 사각형 전체 외곽선에서 잡을 수 있도록 입력 영역을 넓혔다.

## 2026-06-18 KST - 레이아웃 핸들 입력 우선순위 조정

- 작업 요약: 레이아웃 `+` 핸들의 투명 hover/hit 영역이 파이프 가로 길이조절 핸들 위에 렌더링되어 resize hover가 잡히지 않던 문제를 수정했다. terrain 노드와 layout add handle을 먼저 그리고, relation/link와 실제 편집 객체를 그 위에 렌더링하도록 SVG 순서를 조정했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 SVG 렌더/입력 우선순위만 변경했다.
- 주의점: 빈 땅/하천/바다 edge에서는 기존처럼 `+` 메뉴가 동작하고, 파이프/시설이 겹치는 곳에서는 편집 객체의 resize/drag/attach 입력이 우선한다.

## 2026-06-18 KST - 도로 추가 흐름을 시설 선택으로 이동

- 작업 요약: 레이아웃 `+` 메뉴에서 도로 추가를 제거하고, 기존 `시설 추가` 후 오른쪽 편집 패널의 `객체 종류`에서 도로로 변경하는 흐름으로 옮겼다. 타입 변경 시 `snapNodeToGround`를 적용해 도로/지상 고정 객체가 지상선에 맞게 붙도록 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 추가 메뉴와 객체 타입 변경 흐름만 변경했다.
- 주의점: 레이아웃 `+` 메뉴에는 이제 땅/하천/바다만 표시된다. 도로는 `시설 추가`로 생성한 뒤 선택 객체 패널에서 `도로`로 변경한다.

## 2026-06-18 KST - 기본 땅 배경의 terrain 침범 방지

- 작업 요약: 기본 땅 배경이 `canvasWidth/canvasHeight` 전체로 계속 늘어나 하천/바다 terrain 아래에도 갈색 땅이 깔리던 문제를 수정했다. 기본 땅의 실제 표시 bounds를 계산해 오른쪽/하단에 terrain 노드가 붙으면 그 시작 지점까지만 땅 rect, 물결, 지상선, base `+` 핸들이 렌더링되도록 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 기본 땅 배경과 base layout add handle 기준만 변경했다.
- 주의점: 추가된 terrain 노드는 여전히 독립 노드로 렌더링되며, 기본 땅은 첫 side/bottom terrain 시작 지점 전까지만 배경으로 남는다.

## 2026-06-18 KST - 레이아웃 삽입 핸들 hover guide 개선

- 작업 요약: 땅/하천/바다 레이아웃의 좌우/하단 삽입 핸들을 hover 시 검정 50% guide line과 `+` 배지가 함께 나타나는 형태로 바꿨다. 작은 원을 정확히 찍지 않아도 반응하도록 edge hit 영역도 더 넓혔다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 layout add handle UI만 변경했다.
- 주의점: 핸들은 평소에는 숨고, hover 가능한 edge 영역에 마우스를 올릴 때만 표시된다.

## 2026-06-18 KST - terrain 레이아웃 canvas padding 분리

- 작업 요약: 땅/하천/바다 terrain 레이아웃을 추가하면 새 레이아웃 자체가 `canvasHeight + bottom padding` 계산에 다시 들어가 기본 땅만 아래로 더 늘어나던 문제를 수정했다. terrain은 자신의 경계까지만 캔버스를 확장하고, 일반 편집 객체만 기존 bottom/right padding을 만들도록 height/width 계산을 분리했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 canvas 크기 계산만 변경했다.
- 주의점: 도로는 terrain 체인 레이아웃이 아니라 일반 객체로 남아 기존 padding 규칙을 유지한다.

## 2026-06-18 KST - terrain 레이아웃 추가 높이 기준 통일

- 작업 요약: `+` 핸들로 땅/하천/바다 레이아웃을 추가할 때 새 terrain이 작은 블록처럼 생성되지 않고, 현재 기본 ground layer 높이와 같은 높이로 이어붙도록 했다. 좌/우/하단 추가 모두 기준 레이아웃에 체인처럼 인접 배치된다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 terrain 레이아웃 생성 크기만 변경했다.
- 주의점: 도로는 이전 요구대로 땅 위에 고정되는 별도 객체로 유지하고, 이번 체인식 높이 통일은 땅/하천/바다 terrain 레이아웃에만 적용된다.

## 2026-06-18 KST - 레이아웃 + 핸들 표시 안정화

- 작업 요약: 땅/하천/바다 레이아웃의 좌우/하단 `+` 삽입 핸들이 보이지 않던 문제를 수정했다. 핸들을 레이아웃 내부 경계로 넣어 화면 밖 잘림을 줄이고, 노드 렌더 뒤 overlay 레이어에서 그려 다른 객체에 묻히지 않게 했다. edge hit 영역도 넓혀 정확히 작은 원을 찍지 않아도 메뉴가 열리도록 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 레이아웃 추가 핸들 렌더링/입력 영역만 변경했다.
- 주의점: `+` 핸들은 기본적으로 옅게 보이고 hover 시 선명해진다. base soil 핸들과 terrain 노드 핸들은 모두 노드 위 overlay로 렌더링된다.

## 2026-06-18 KST - 맨홀/방류구/도로/레이아웃 편집 보강

- 작업 요약: 맨홀 세부 종류를 우수/오수/합류식으로 고를 수 있게 하고, 방류구 내부 커넥터 장식을 제거했다. 도로/지형 레이아웃 노드와 edge + 삽입 메뉴를 추가해 땅/하천/바다/도로를 확장 배치할 수 있게 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 표현/레이아웃 노드만 변경했다.
- 주의점: `road`/`terrain`은 SWMM 포트가 없는 편집 레이아웃 객체이며, 배경/도로 레이어 우선순위로 relation 객체보다 뒤에 렌더링된다.

## 2026-06-18 KST - relation group 기반 다중 선택/복사/붙여넣기

- 작업 요약: 캔버스 빈 영역 드래그로 marquee 다중 선택을 추가하고, 선택된 노드가 relation group 일부라면 그룹 전체가 선택되도록 했다. 다중 선택 상태에서 드래그하면 선택된 그룹 전체가 기존 그룹 이동 규칙을 따라 움직이고, Command/Ctrl+C/V로 내부 클립보드 복사/붙여넣기를 할 수 있게 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `react-viewer/src/components/editor/editorTypes.ts`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 selection 타입과 캔버스 입력 처리만 변경했다.
- 주의점: 복사 시 relation group 내부 노드/링크만 복제하며, 붙여넣은 relation attach 메타데이터는 새 좌표 기준으로 다시 정규화된다.

## 2026-06-18 KST - 맨홀 직접 마우스 높이조절 비활성화

- 작업 요약: 맨홀은 relation 전파/좌표변경 규칙에서 높이조절 가능한 객체로 유지하되, 선택 상태에서 마우스로 직접 높이를 조절하는 resize 핸들은 제거했다. 수동 resize 가능 edge를 별도 helper로 분리해 맨홀은 직접 조작을 시작할 수 없게 막았다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 수동 resize UI/이벤트 가드만 변경했다.
- 주의점: relation 기반 맨홀 높이 보정과 parent/child 전파에서 쓰는 `getAttachResizableEdges()`의 맨홀 bottom 가능 상태는 유지했다.

## 2026-06-18 KST - y축 좌표변경에서 고정객체 포함 parent chain 전파

- 작업 요약: relation 좌표변경 중 parent-side group에 아파트/집/빗물받이 같은 y고정 객체가 있고, 좌표변경 축이 y축인 경우 단순 group y 이동 대신 relation endpoint 보정 경로를 타도록 했다. 선택한 parent endpoint를 먼저 이동시키고, 그 변화가 parent-side relation chain으로 전파되어 기존 길이조절 우선순위가 동작하게 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 좌표변경 y축 처리 분기만 변경했다.
- 주의점: x축 좌표변경과 y고정 객체가 없는 y축 좌표변경은 기존처럼 parent-side group 좌표 이동을 유지한다.

## 2026-06-18 KST - 좌표변경 clamp에 커넥터 clearance 반영

- 작업 요약: relation 좌표변경에서 child 파이프의 단순 x/y 경계만 기준으로 clamp하던 것을, parent 커넥터/ㄱ자 커넥터가 실제로 차지하는 반폭/반높이 clearance를 반영하도록 바꿨다. 같은 파이프 face 위의 다른 attach 지점도 양쪽 커넥터 clearance와 margin을 함께 고려해 중심점 기준 겹침을 줄였다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 좌표변경 드래그 범위 계산만 변경했다.
- 주의점: 좌표변경 가능 조건은 기존 그대로 `connector/elbowConnector parent -> 길이축 조절 가능한 pipe child` relation에만 적용된다.

## 2026-06-18 KST - x축 resize 전파를 좌표 이동 전용으로 제한

- 작업 요약: 가로 파이프 길이변경에서 reverse parent 보정은 좌표 이동만 하더라도, 이후 일반 child/attach 전파가 다시 `applyRelationEndpointDelta`를 타며 가로 파이프 길이를 조절하던 문제를 줄였다. `sourceLengthAxis: 'x'`가 전달된 전파에서는 후속 relation endpoint를 resize하지 않고 x/y delta 모두 좌표 이동으로만 처리하도록 공통 wrapper를 추가하고, 일반 child 전파와 parent-side attach 전파가 이를 사용하게 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 resize 전파의 x축 후속 처리만 변경했다.
- 주의점: y축 길이변경은 기존처럼 길이조절 우선순위 경로를 유지한다. attach 생성 자체는 `sourceLengthAxis`가 없으므로 기존 attach snap 규칙을 유지한다.

## 2026-06-18 KST - reverse parent propagation을 원본 resize 축 기준으로 분리

- 작업 요약: 역방향 parent 보정이 단순 delta 축 기준으로 동작하던 것을 원본 길이변경 축 기준으로 바꿨다. 가로 파이프처럼 x축 길이변경에서 발생한 역방향 parent 보정은 길이조절 우선순위를 타지 않고 좌표 이동만 한다. 세로 파이프/맨홀처럼 y축 길이변경에서 발생한 역방향 parent 보정은 기존 `applyRelationEndpointDelta` 경로를 유지해 길이조절 우선순위 후 잔여 좌표 이동을 적용한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 resize 기반 다중 parent 역방향 보정 기준만 변경했다.
- 주의점: attach/좌표변경/일반 parent->child 전파는 기존 경로를 유지한다. 이번 분기는 길이변경 이벤트가 `sourceLengthAxis`를 넘길 때의 reverse parent propagation에만 적용된다.

## 2026-06-18 KST - reverse parent propagation x/y 동작 분리

- 작업 요약: 임시로 꺼두었던 `ENABLE_REVERSE_PARENT_PROPAGATION_RULE`을 다시 켜고, reverse parent 보정 전용 delta 적용 함수를 분리했다. 역방향 parent 보정에서 x축 변화는 길이조절을 시도하지 않고 좌표 이동으로 처리하며, y축 변화는 기존처럼 길이조절 우선순위 규칙을 탄다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 다중 parent 역방향 보정 축별 동작만 변경했다.
- 주의점: 일반 `parent -> child` 전파는 기존 `applyRelationEndpointDelta`를 계속 사용한다. 이번 분기는 reverse parent 보정에만 적용된다.

## 2026-06-18 KST - reverse parent propagation 임시 비활성화

- 작업 요약: 가로 파이프 길이조절 테스트를 위해 다중 parent 상황에서 자식 변경을 부모 방향으로 거슬러 보정하는 `ENABLE_REVERSE_PARENT_PROPAGATION_RULE`을 임시로 껐다. 일반 `parent -> child` 전파는 유지했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 relation 전파 토글만 변경했다.
- 주의점: 현재 다중 parent의 역방향 parent 보정은 동작하지 않는다. 재활성화하려면 `ENABLE_REVERSE_PARENT_PROPAGATION_RULE`을 다시 `true`로 바꿔야 한다.

## 2026-06-18 KST - 좌표변경을 connector parent -> resizable pipe child로 제한

- 작업 요약: relation 우클릭 메뉴의 `좌표 변경`을 커넥터/ㄱ자 커넥터 parent가 길이축 좌표 조절이 가능한 파이프 child에 붙은 경우에만 표시하도록 제한했다. 좌표변경 중에는 자식 파이프의 해당 face 좌표계를 기준으로 움직이고, 같은 face의 다른 attach 지점을 넘어가지 못하도록 clamp한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 relation 좌표변경 메뉴 표시 조건과 드래그 clamp만 변경했다.
- 주의점: `파이프 -> 커넥터`처럼 child가 커넥터인 relation에는 좌표변경이 뜨지 않는다. 좌표변경 가능 여부는 parent가 connector 계열인지, child가 pipeSegment인지, child attach face가 파이프 길이축과 일치하는지로 판단한다.

## 2026-06-18 KST - attach anchor resize guard를 부모 방향 기준으로 변경

- 작업 요약: attach 지점을 넘지 못하게 하는 resize guard 조건을 relation group 전체 기준에서 현재 노드의 부모/조상 방향 기준으로 좁혔다. 자식 쪽에 맨홀이 붙어 있어도 guard가 꺼지지 않고, 부모 라인에 아파트/집/빗물받이가 있으며 부모 라인에 맨홀이 없는 경우에만 guard가 동작한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기의 resize guard 적용 조건만 변경했다.
- 주의점: 현재 guard 판단은 directed parent chain 기준이다. 자식/후손에 어떤 객체가 붙어 있는지는 guard on/off 판단에 포함하지 않는다.

## 2026-06-18 KST - attach anchor resize guard 적용 대상을 fixed branch로 제한

- 작업 요약: attach 지점을 넘지 못하게 하는 resize guard가 맨홀이 포함된 relation group에서 부작용을 계속 만들 수 있어, guard 적용 대상을 좁혔다. 이제 relation group 안에 아파트/집/빗물받이 중 하나가 있고, 맨홀이 없는 branch에서만 내부 attach anchor guard가 동작한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 길이조절 guard 적용 조건만 변경했다.
- 주의점: 맨홀이 포함된 그룹에서는 guard가 꺼지므로 기존 부모/자식 전파 규칙만 동작한다. 아파트/집/빗물받이 branch에서는 attach 지점을 넘어가는 것을 막는 보호가 유지된다.

## 2026-06-18 KST - 맨홀 side attach 기준 보정 후 resize guard 재활성화

- 작업 요약: attach anchor resize guard를 다시 켜고, 맨홀/집/아파트 같은 lower-side attach 객체가 상대 포트 기준을 계산할 때 가로 파이프의 전체 폭을 세로 반경처럼 쓰던 문제를 수정했다. 상대 포트가 top/bottom이면 상대 객체의 실제 세로 두께 절반을 사용하도록 분리 helper를 추가했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 lower-side attach 좌표/높이 역산과 resize guard 계산만 변경했다.
- 주의점: 직전 진단에서 guard를 껐을 때 증상이 사라졌으므로 guard 자체는 원인이 맞았다. 이번 수정은 guard를 포기하지 않고, 맨홀 side attach가 긴 가로 파이프 폭에 의해 비정상적으로 clamp되는 문제를 줄이는 방향이다.

## 2026-06-18 KST - attach anchor resize guard 진단용 비활성화

- 작업 요약: 파이프/맨홀 길이조절 시 attach 지점을 넘지 못하게 하는 내부 anchor guard가 줄임 동작을 막는 원인인지 분리하기 위해 `ENABLE_ATTACH_ANCHOR_RESIZE_GUARD` 토글을 추가하고 현재 `false`로 비활성화했다. 부모/자식 전파, 역방향 parent 전파, fixed-y vertical top resize 보정은 그대로 유지했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 길이조절 guard 실행 여부만 진단용으로 변경했다.
- 주의점: attach 지점을 넘어가지 못하게 하는 보호 규칙은 현재 꺼져 있다. 줄임/늘림 비대칭이 사라지는지 확인한 뒤, 원인이 맞으면 guard를 다시 설계해야 한다.

## 2026-06-18 KST - relation endpoint resize guard에서 현재 relation 제외

- 작업 요약: relation 전파 중 특정 endpoint를 맞추기 위해 파이프/맨홀 길이를 조절할 때, 그 현재 relation의 이전 attach 좌표까지 내부 anchor guard에 포함되어 줄이기가 막히거나 늘림/줄임 반응이 비대칭으로 보일 수 있던 문제를 줄였다. endpoint pair로 현재 relation id를 찾고, 전파 resize의 anchor bounds 계산에서는 해당 relation만 제외한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 relation 전파 중 길이조절 guard 계산만 변경했다.
- 주의점: 직접 마우스로 길이를 조절할 때의 내부 attach 보호는 유지된다. 제외되는 것은 relation 전파가 현재 맞추고 있는 relation 자신의 과거 좌표뿐이다.

## 2026-06-18 KST - 다중 parent 역방향 보정 parent-side 그룹 전파

- 작업 요약: 다중 parent child 예외에서 다른 incoming parent endpoint는 보정되지만, 그 parent 쪽에 이어진 ㄱ자/파이프/커넥터 체인이 같이 전파되지 않아 연결이 끊겨 보이는 문제를 줄였다. 역방향 보정된 parent를 main queue에 다시 넣지는 않고, `propagateAttachEndpointChanges`로 변경된 parent의 반대편 그룹만 1회 전파한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 relation 전파의 다중 parent 예외 처리만 보완했다.
- 주의점: 변경된 child 자체는 blocked node로 두어, 역방향 parent-side 전파가 다시 child를 끌고 가는 루프를 만들지 않도록 했다.

## 2026-06-18 KST - 다중 parent child 역방향 전파 조건 명시화

- 작업 요약: child 전파의 기본 방향은 `parent -> child`로 유지하되, child가 현재 relation 외의 다른 incoming parent를 가진 경우에만 역방향 parent 보정을 허용하도록 조건을 명시했다. 기존 `depth === 0` 기반 제한을 제거하고, 실제 다중 parent 여부를 `hasOtherIncomingParentRelation`으로 확인한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 relation 전파 조건만 변경했다.
- 주의점: 역방향으로 보정된 parent는 여전히 queue에 다시 넣지 않는다. child-of-child 전파는 기존 queue 경로로 계속 진행된다.

## 2026-06-18 KST - 길이조절 attach 경계 face 기준 보정

- 작업 요약: 길이조절 중 내부 attach anchor를 통과하지 못하게 하는 guard가 점 좌표만 기준으로 동작해, 상대 객체의 중앙선까지 파고들 수 있던 문제를 보정했다. 상대 포트가 top/bottom이면 x축 경계에서 상대 객체의 좌우 외곽까지, left/right이면 y축 경계에서 상대 객체의 상하 외곽까지 clearance를 더해 실제 면 기준으로 clamp한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 길이조절 guard의 UI geometry 계산만 변경했다.
- 주의점: resize 시작 시점의 anchor snapshot 구조는 유지했다. 이번 변경은 snapshot anchor 좌표를 상대 객체의 실제 외곽면 기준으로 확장하는 보정이다.

## 2026-06-18 KST - 길이조절 attach anchor 경계 snapshot 고정

- 작업 요약: 길이조절 중 attach anchor 좌표가 relation 전파로 계속 바뀌면서 clamp 기준도 흔들리는 문제를 줄였다. resize 시작 시점에 edge별 내부 attach 경계를 `ResizeState.anchorBounds`로 저장하고, 마우스 이동 중에는 이 snapshot을 사용한다. relation 전파 중 endpoint resize도 현재 전파 layout이 아니라 전파 시작 전 `baseLayout` 기준 anchor를 사용하도록 연결했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 길이조절 중 attach anchor clamp 기준만 안정화했다.
- 주의점: 목적은 움직이는 edge가 내부 attach 지점을 통과하지 못하게 하는 것이다. moving edge 위에 있는 attach point는 함께 움직이는 지점으로 보고 경계 계산에서 제외한다.

## 2026-06-18 KST - 길이조절 내부 attach anchor 경계 보정 재적용

- 작업 요약: 이전 anchor boundary guard가 움직이는 edge 자체의 relation까지 경계로 삼아 줄이기를 막던 문제를 피해서 다시 적용했다. 이번에는 resize 중인 edge 위에 있는 attach point는 같이 움직이는 점으로 보고 제외하고, edge 안쪽에 남아 있는 relation attach point만 통과하지 못하도록 clamp한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 길이조절/전파 resize의 geometry guard만 추가했다.
- 주의점: 직접 파이프/맨홀 길이조절, relation 전파 중 endpoint resize, 우측 속성 패널 길이 변경 경로에 같은 guard를 적용했다. 길이로 흡수 가능한 범위가 내부 attach anchor에 막히면 기존 규칙대로 남은 delta는 좌표 이동 경로에서 처리된다.

## 2026-06-18 KST - 역방향 parent 전파 depth 제한

- 작업 요약: 길이조절 중 역방향 parent 보정이 하위 child chain의 각 depth에서 반복 실행되어 가로 파이프 축소 시 downstream 본관/맨홀 쪽 geometry가 꼬일 수 있는 문제를 줄였다. `propagateChildEndpointChanges` queue에 depth를 추가하고, 역방향 parent 보정은 직접 변경된 parent의 바로 child 단계에서만 실행되도록 제한했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 relation 전파 중 reverse parent 보정 실행 범위만 제한했다.
- 주의점: 자식 방향 전파는 여전히 child-of-child로 계속 내려간다. 좌표 맞춤은 기존처럼 길이조절 가능 edge가 있으면 길이로 먼저 흡수하고, 남은 delta는 좌표 이동으로 처리한다.

## 2026-06-18 KST - 길이조절 relation anchor 경계 보정 롤백

- 작업 요약: 직전 추가한 anchor boundary guard가 길이 늘리기는 허용하지만 줄이기를 막는 부작용을 내서 해당 코드만 롤백했다. 맨홀 side attach 높이 역산 보정과 역방향 parent 전파 재활성화는 유지했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 길이조절 UI 제약 추가분만 되돌렸다.
- 주의점: attach 지점을 지나가지 못하게 하는 규칙은 다시 설계가 필요하다. 특히 움직이는 edge 자체에 붙은 relation을 경계로 삼으면 줄이기가 막히므로, 다음 시도에서는 moving edge endpoint와 내부 tap/반대쪽 parent anchor를 구분해야 한다.

## 2026-06-18 KST - 길이조절 relation anchor 경계 보정

- 작업 요약: 파이프/맨홀 길이조절 중 움직이는 edge가 해당 객체 위의 relation attach 지점을 지나가지 못하도록 anchor boundary guard를 추가했다. relation이 붙어 있는 좌표를 수집한 뒤, right/left/top/bottom edge별로 attach point를 넘지 않도록 resize 결과를 clamp한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 길이조절 UI의 geometry 제약만 추가했다.
- 주의점: 경계는 부모/자식 방향과 무관하게 해당 객체 위에 존재하는 모든 relation attach point를 기준으로 한다. 전파 로직보다 앞단의 resize 결과를 제한하므로 child 전파와 역방향 parent 보정은 기존 순서를 유지한다.

## 2026-06-18 KST - 역방향 parent 전파 재활성화

- 작업 요약: 맨홀 side attach 높이 역산 보정 후 정상 동작을 확인했으므로, 다중 parent child 상황에서 다른 incoming parent endpoint를 1단계 보정하는 `ENABLE_REVERSE_PARENT_PROPAGATION_RULE`를 다시 `true`로 켰다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 resize 전파의 역방향 parent 보정 플래그만 재활성화했다.
- 주의점: 역방향 보정은 여전히 보정된 parent를 queue에 다시 넣지 않는 1단계 구조다. child-of-child 전파는 기존 `queue.push(childAfter.id)` 경로가 담당한다.

## 2026-06-18 KST - 맨홀 side attach 높이 역산 보정

- 작업 요약: 맨홀 left/right attach가 실제 렌더링 위치와 다른 단순 `LOWER_SIDE_PORT_BOTTOM_GAP` 역산식을 쓰던 문제를 수정했다. lower-side attach offset 계산을 공통 helper로 분리하고, 맨홀 side 포트 높이 조절은 같은 공식의 역계산을 사용하도록 바꿨다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기에서 길이변경 전파가 맨홀 side 포트에 도달했을 때의 UI geometry 계산만 보정했다.
- 주의점: 역방향 parent 전파는 계속 `ENABLE_REVERSE_PARENT_PROPAGATION_RULE = false` 상태다. 이번 수정은 child 전파 중 맨홀 side attach 높이 비율이 틀어지는 문제를 겨냥한다.

## 2026-06-18 KST - 역방향 parent 전파 임시 비활성화

- 작업 요약: 파이프 길이 변경 후 맨홀 높이가 늘릴 때 과하게, 줄일 때 덜 반응하는 현상을 비교하기 위해 최근 추가한 역방향 parent 보정을 `ENABLE_REVERSE_PARENT_PROPAGATION_RULE = false` 플래그로 임시 비활성화했다. 기존 `parent -> child` 전파와 child-of-child queue 전파는 유지했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 resize 전파 중 다중 parent 역방향 보정만 껐다.
- 주의점: 이 변경은 원인 확인용 임시 차단이다. 문제가 사라지면 역방향 보정의 delta 계산/중복 적용 조건을 다시 설계해야 한다.

## 2026-06-18 KST - 역방향 parent 보정을 1단계로 제한

- 작업 요약: 다중 parent child 역방향 보정이 자체 queue와 main queue 재삽입으로 child-of-child 전파와 겹칠 수 있던 문제를 수정했다. 이제 역방향 보정은 변경된 child의 다른 incoming parent endpoint만 1단계로 맞추고, 보정된 parent를 다시 전파 queue에 넣지 않는다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 relation 전파 중 중복 child 전파 가능성만 줄였다.
- 주의점: child-of-child 전파는 기존 `propagateChildEndpointChanges`의 `queue.push(childAfter.id)` 경로에서만 유지된다. 역방향 보정은 현재 parent relation을 제외한 다른 incoming parent만 직접 보정한다.

## 2026-06-18 KST - 다중 parent child의 조건부 역방향 보정 복원

- 작업 요약: 길이변경 후 기본 전파는 계속 `parent -> child` 방향으로 유지하되, 변경된 child가 현재 relation 외의 incoming parent를 가지고 있으면 해당 parent endpoint도 같은 delta로 보정하도록 `propagateIncomingParentEndpointChanges`를 추가했다. 이 보정이 실행돼도 기존 child-of-child queue 전파는 계속 실행되도록 유지했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 relation 전파에서 다중 parent child의 upstream endpoint 보정만 복원했다.
- 주의점: 새 feature flag는 추가하지 않았다. 조건부 역방향 보정은 `ENABLE_PARENT_CHILD_PROPAGATION_RULE` 내부에서만 동작하며, 현재 parent relation은 제외하고 다른 incoming parent만 보정한다.

## 2026-06-17 KST - 비활성 resize 보정 규칙 제거

- 작업 요약: 더 이상 필요하지 않은 false 상태의 resize 보정 규칙 `ENABLE_CONNECTED_PORT_RESIZE_FOLLOW_RULE`, `ENABLE_PIPE_TAP_ANCHOR_RETARGET_RULE`, `ENABLE_FIXED_ANCHOR_BRANCH_SYNC_RULE`와 전용 helper들을 제거했다. 현재 `ENABLE_*` 플래그는 basic pipe/manhole resize, parent-child propagation, fixed-y vertical top resize 보정 세 개만 남았다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. 삭제 대상 규칙/전용 helper 문자열 검색 결과 0건 확인.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부의 비활성 resize 보정 잔재만 정리했다.
- 주의점: 현재 길이변경 연결 반응은 `propagateChildEndpointChanges`와 child 방향 edge 선택 규칙이 담당한다. `resizeBranchNodeToEndpointY`와 `moveNodeIdsBy`는 active 경로에서 사용되므로 유지했다.

## 2026-06-17 KST - 길이조절 edge를 child 방향으로 우선 적용

- 작업 요약: 파이프/맨홀 길이를 줄이거나 늘릴 때 사용자가 잡은 resize edge가 아니라 relation `from(parent) -> to(child)` 기준 child가 붙어 있는 parent-side edge를 우선 움직이도록 보정했다. 길이 변화량은 그대로 유지하되, child relation endpoint가 붙은 resizable edge가 있으면 그 edge 방향으로 적용한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 길이조절 시 실제로 움직이는 edge 선택 규칙만 child 방향 우선으로 바꿨다.
- 주의점: relation child edge가 없거나 해당 축에서 조절 가능한 edge가 아니면 기존 resize edge를 그대로 사용한다. 길이변경 후 relation 전파는 직전 작업처럼 child 방향으로만 진행한다.

## 2026-06-17 KST - 길이변경 전파를 child 방향으로 제한

- 작업 요약: 길이변경 시 attach용 양방향 endpoint-chain을 사용하던 흐름을 분리해, resize 이벤트에서는 relation `from(parent) -> to(child)` 방향으로만 전파되도록 `propagateChildEndpointChanges`를 추가했다. 이제 하위 child 객체의 길이를 줄여도 parent / parent의 parent 쪽으로 역전파되지 않고, 해당 객체의 child chain에만 좌표/길이 변경이 전파된다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 길이변경 후 relation 전파 방향만 child 방향으로 제한했다.
- 주의점: attach 시에는 여전히 `propagateAttachEndpointChanges` 양방향 endpoint-chain을 사용한다. `ENABLE_CONNECTED_PORT_RESIZE_FOLLOW_RULE`는 false로 유지하며, `ENABLE_FIXED_Y_VERTICAL_TOP_RESIZE_AS_BOTTOM_RULE`는 true 상태다.

## 2026-06-17 KST - 길이변경 전파를 attach endpoint-chain으로 통합

- 작업 요약: 파이프/맨홀 길이변경 시 기존 방향성 `parent -> child` 전파 helper 대신 attach에서 사용하는 `propagateAttachEndpointChanges`를 호출하도록 바꿨다. 길이변경으로 움직인 endpoint가 relation chain을 한 번씩 따라가며, 대상 endpoint가 길이 조절 가능한 면이면 resize하고 아니면 좌표 이동한다. 기존 방향성 전파 helper와 그 전용 보조 함수들은 제거했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 길이변경 후 relation 전파 방식만 attach와 같은 endpoint-chain으로 통일했다.
- 주의점: `ENABLE_CONNECTED_PORT_RESIZE_FOLLOW_RULE`는 false로 유지한다. 이제 길이변경 연결 보정은 endpoint-chain 전파가 담당하므로, 이 옛 follow 규칙을 다시 켜면 중복 이동이 날 수 있다.

## 2026-06-17 KST - 옛 attach stretch 규칙 제거

- 작업 요약: 이미 비활성화되어 있던 `파이프 parent -> 커넥터 child stretch` 규칙과 `multi-parent pipe/tap attach stretch` 규칙을 코드에서 제거했다. 해당 규칙만 사용하던 stretch helper들과 남은 dead flag/helper도 함께 삭제해 attach 실행 경로를 endpoint-chain 스냅/전파로 단순화했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. 삭제 대상 문자열 검색 결과 0건 확인.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부의 비활성 attach stretch 잔재만 정리했다.
- 주의점: 현재 비슷한 attach 결과가 유지되는 이유는 `snapChildToParentByAttachRule -> applyRelationEndpointDelta -> resizeRelationEndpointOnAxisByDelta` 흐름이 child endpoint를 맞추면서 pipe/manhole의 조절 가능한 면은 길이 변경으로 처리하기 때문이다.

## 2026-06-17 KST - relation parent 노드 렌더 우선순위 보정

- 작업 요약: 커넥터가 파이프 사이에 끼어 있을 때 parent 커넥터의 포트/우클릭 hit 영역이 child 파이프에 가려져 `해체` 메뉴가 뜨지 않던 문제를 보정했다. relation 방향을 기준으로 child를 먼저, parent를 나중에 렌더하도록 node draw order를 계산하고, 포트 우클릭 relation 탐색도 `from`뿐 아니라 `to` endpoint exact match까지 허용했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 SVG z-order와 context menu endpoint 탐색만 변경했다.
- 주의점: parent가 child 위에 그려지는 렌더 순서 보정이다. relation cycle은 기존 attach 차단 로직을 전제로 하며, 같은 depth 노드는 기존 node 배열 순서를 유지한다.

## 2026-06-17 KST - attach fallback resize 규칙 제거

- 작업 요약: 현재 attach 실행 경로가 endpoint-chain 전파로 고정된 상태에서 더 이상 도달하지 않는 옛 fallback 규칙 `ENABLE_ATTACH_CHILD_RESIZE_SNAP_RULE`, `ENABLE_ATTACH_FIXED_Y_HEIGHT_ADJUST_RULE`와 전용 helper를 제거했다. 남은 규칙은 현재 `ENABLE_*` 플래그와 무조건 실행되는 attach/normalizer 경로로 다시 확인했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 attach fallback 코드만 정리했다.
- 주의점: `getAttachResizableEdges`, `resizeNodeEdgeToCoordinate`는 현재 endpoint-chain 전파에서 계속 사용하므로 제거하지 않았다.

## 2026-06-17 KST - attach endpoint-chain 되돌아타기 방지

- 작업 요약: attach endpoint-chain 전파에서 같은 relation을 한 방향으로 처리한 뒤 큐에 들어온 상대 노드가 같은 relation을 반대 방향으로 다시 처리할 수 있던 문제를 수정했다. relation 단위로 한 번만 전파하도록 바꿔 `파이프 -> 커넥터 -> 파이프` 같은 연결에서 delta가 같은 edge를 타고 되돌아가 중복 적용되는 계산 오류를 막았다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/` 새로고침 후 브라우저 console error 0건 확인.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 attach 전파의 중복 적용 방지만 변경했다.
- 주의점: 새 relation graph 자체를 재설계한 것은 아니고, 직전 endpoint-chain 방식에서 같은 relation을 되돌아타는 feedback만 차단한 좁은 수정이다. 실제 화면에서 커넥터21/22와 하단 파이프 attach 케이스를 다시 테스트해야 한다.

## 2026-06-17 KST - attach endpoint-chain 전파로 전환

- 작업 요약: `propagateAttachMovedNodeChanges`가 child-side group에 이미 포함된 relation child를 전부 스킵해 후속 전파가 일어나지 않는 구조적 문제를 확인했다. attach 순간에 child-side group을 먼저 통째로 이동하는 방식 대신, 선택된 child endpoint를 parent endpoint에 맞춘 뒤 그 endpoint 변화량을 기존 relation 체인으로 전파하는 `propagateAttachEndpointChanges` 흐름으로 전환했다. y축 endpoint 조정은 맨홀/수직 파이프처럼 길이 조절 가능한 branch 객체면 우선 height/length 변경으로 처리하고, 남는 delta만 좌표 이동으로 처리한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 attach 스냅/전파 규칙만 변경했다.
- 주의점: 기존 `ENABLE_ATTACH_CHILD_RESIZE_SNAP_RULE=false`, `ENABLE_ATTACH_FIXED_Y_HEIGHT_ADJUST_RULE=false` 상태는 유지했다. 새 핵심 경로는 `ENABLE_ATTACH_ENDPOINT_CHAIN_RULE=true`이며, 이전 `movedNodeIdSet` 기반 attach 후속 전파 플래그는 제거했다. 실제 UI에서 커넥터21 -> 파이프 -> 커넥터22 -> 파이프 -> 맨홀 체인 케이스를 추가 확인해야 한다.

## 2026-06-17 KST - attach 후속 child 전파 단독 검증 모드

- 작업 요약: attach 동작 원인 분리를 위해 attach child resize snap과 attach 전용 fixed-y 맨홀 height 보정을 실행 경로에서 껐다. child-side group 이동 뒤, 이동 그룹 밖에 남은 후속 child만 `propagateAttachMovedNodeChanges`로 따라오는지 확인할 수 있도록 실험 플래그를 정리했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 attach 실험용 feature flag만 변경했다.
- 주의점: 현재 `ENABLE_ATTACH_CHILD_RESIZE_SNAP_RULE=false`, `ENABLE_ATTACH_FIXED_Y_HEIGHT_ADJUST_RULE=false`, `ENABLE_ATTACH_MOVED_CHILD_PROPAGATION_RULE=true` 상태다. 이 상태는 원인 분리용이며 최종 동작 확정 전까지 테스트 결과를 보고 다시 정리해야 한다.

## 2026-06-17 KST - attach child group 내 맨홀/후속 child 보정

- 작업 요약: React 편집모드에서 attach 시 child side group이 이동할 때, 그룹 안의 맨홀이 고정 y 스냅 때문에 세로 길이를 줄이지 못하고 제자리에 남는 문제를 보정했다. attach 전용 이동 함수 `moveAttachNodeIdsBy`를 추가해, 맨홀은 y 이동을 직접 적용하지 않고 이동 delta를 height 변화로 반영하도록 했다. 또한 attach로 이동된 child-side node들을 parent 후보로 보고, 이동 그룹 밖에 남아 있는 후속 child가 있으면 `propagateAttachMovedNodeChanges`로 한 번 더 체인 전파하도록 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 attach 순간의 child side group 이동 중 맨홀 높이 반응만 좁게 변경했다.
- 주의점: 일반 그룹 이동/좌표 변경에서 사용하는 `moveNodeIdsBy`는 그대로 두었다. 이번 보정은 attach 스냅에서만 적용되므로 기존 드래그 동작에는 영향을 주지 않는다. 후속 child 전파는 이미 attach 이동 그룹에 포함된 node는 중복 적용하지 않도록 건너뛴다.

## 2026-06-17 KST - attach 시 child side group 이동 보정

- 작업 요약: React 편집모드에서 새 parent -> child attach 후 child 자체만 parent에 맞춰지고 기존 연결 덩어리 일부가 따라오지 않던 문제를 수정했다. attach 순간에는 relation 방향이 완전히 정리돼 있지 않은 기존 구조도 고려해야 하므로, child 하나만 이동하지 않고 `getAttachMovingNodeIds`로 parent 쪽 그룹을 제외한 child side group 전체를 같이 이동하도록 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py` 통과. 기존 dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 attach 직후 child side group 이동 방식만 보정했다.
- 주의점: parent -> child chain 전파 규칙은 계속 길이/좌표 변경 후속 전파용으로 유지한다. attach 순간에는 방향성 전파만으로 부족한 케이스가 있어 우선 child side group을 이동한다.

## 2026-06-17 KST - parent -> child 체인 전파 규칙 도입

- 작업 요약: React 편집모드에서 attach/길이변경별로 흩어져 있던 relation 보정을 줄이고, `relation.from -> relation.to`를 parent -> child 방향으로 보는 공통 전파 규칙을 추가했다. parent endpoint가 이동하면 직계 child endpoint에 같은 delta를 적용하고, child 면이 해당 축으로 길이 조절 가능하면 resize, 아니면 좌표 이동을 적용한다. child가 실제로 바뀌면 다시 그 child의 child로 queue 전파한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py` 통과. 기존 dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 relation 전파 규칙만 변경했다. `relation`은 계속 UI metadata이며, 저장/export 경로에서는 기존 `normalizeRelationAttachments`가 최신 attach metadata와 tap `portId`를 정규화한다.
- 주의점: 예전 `length resize relation` / `attach ancestor branch` 보정 함수는 새 parent -> child 전파와 충돌하지 않도록 실행 경로에서 제거했다. 현재 전파는 relation 방향 기준으로 child chain만 따라가며, 다른 parent branch를 역방향으로 움직이지 않는다.

## 2026-06-17 KST - relation tap portId를 최신 attach 위치에 동기화

- 작업 요약: React 편집모드에서 relation `attach` metadata는 최신 geometry로 갱신되지만 `from/to.portId`가 예전 `tap-*` 비율을 유지해 화살표와 JSON endpoint가 낡은 위치를 가리키던 문제를 보정했다. `normalizeRelationAttachments`가 relation metadata를 계산할 때 tap endpoint의 `portId`도 현재 `parentOnChild` / `childOnParent` ratio 기준으로 재작성하도록 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py` 통과. 기존 dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 JSON relation endpoint와 attach metadata가 같은 최신 tap 위치를 보도록 정규화했다. SWMM INP 변환은 기존처럼 attach metadata를 우선 사용한다.
- 주의점: 이 변경은 객체 위치나 크기를 움직이지 않는다. 저장/undo/redo/export 경로에서 relation endpoint 이름과 metadata를 최신 geometry에 맞춰 정규화하는 보정이다.

## 2026-06-17 KST - relation attach metadata normalizer 도입

- 작업 요약: React 편집모드의 relation에 `attach` metadata를 추가하고, layout 변경이 저장되기 전 `normalizeRelationAttachments`를 통과해 parent/child endpoint 및 `parentOnChild`, `childOnParent` 위치/비율을 자동 갱신하도록 했다. 이 normalizer는 객체 위치나 크기를 바꾸지 않고, 현재 geometry를 기준으로 metadata만 재계산한다.
- 주요 파일: `react-viewer/src/components/editor/editorTypes.ts`, `react-viewer/src/components/editor/EditorCanvas.tsx`, `scripts/editor_layout_to_swmm_inp.py`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py` 통과. 기존 dev server `http://127.0.0.1:5173/`에서 in-app Browser로 앱/편집 모드 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델과 서버 payload는 변경하지 않았다. React 편집기 JSON relation metadata가 확장됐고, SWMM INP 변환은 relation attach metadata가 있으면 pipe station 계산에 우선 사용하며 없으면 기존 `portId` 파싱으로 fallback한다.
- 주의점: in-app Browser는 다운로드 파일 저장을 지원하지 않아 내보낸 JSON 파일 내용까지는 직접 확인하지 못했다. 사용자가 테스트 후 JSON 또는 localStorage 데이터를 제공하면 `attach.parentOnChild`/`attach.childOnParent` 값이 실제 이동/resize 후 갱신됐는지 확인해야 한다.

## 2026-06-16 KST - 좌표 변경 이동 대상을 parent side로 수정

- 작업 요약: React 편집모드의 `좌표 변경`이 마우스 이동을 따라가되 child 쪽 branch를 움직이던 문제를 수정했다. 이제 relation의 `to(child)` 쪽을 막고 반대편 `from(parent)` side node들을 찾아, 마우스 축 좌표에 맞춰 parent 쪽 그룹을 이동한다. 이전 tap port 재계산 helper는 더 이상 사용하지 않아 제거했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. 기존 dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 좌표 변경 중 relation branch 이동 대상만 child side에서 parent side로 바꿨다.
- 주의점: 좌표 변경은 여전히 child 포트 면 기준으로 x축 또는 y축을 결정한다. 이동되는 객체 집합만 relation의 parent 쪽 그룹이다.

## 2026-06-16 KST - 좌표 변경을 마우스 이동 추적 방식으로 전환

- 작업 요약: React 편집모드의 `좌표 변경`이 클릭해도 변화가 없거나 SVG/포트 이벤트에 따라 불안정하게 종료되던 문제를 다시 수정했다. 좌표 변경 모드가 켜지면 `window.pointermove`로 마우스 위치를 전역 추적해 실시간으로 relation 좌표를 갱신하고, 클릭/마우스 업은 변경 고정 및 history batch 종료 역할만 하도록 분리했다. parent가 tap 좌표를 지원하지 않는 relation도 무반응으로 끝나지 않도록 child branch를 선택 축으로 이동하는 fallback을 추가했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. 기존 dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 좌표 변경 이벤트/입력 처리만 변경했다.
- 주의점: 좌표 변경 중에는 캔버스 밖으로 살짝 나가도 `pointerleave`만으로 모드가 풀리지 않는다. 마우스 이동으로 preview/update가 계속 되고, 클릭 또는 마우스 업으로 고정된다.

## 2026-06-16 KST - 좌표 변경 클릭 종료 타이밍 보정

- 작업 요약: React 편집모드의 `좌표 변경`에서 마우스 커서가 바뀐 뒤 클릭하면 좌표 반영 없이 모드가 풀리는 문제를 수정했다. 좌표 변경 중 캔버스/객체를 누르는 순간 먼저 `updateCoordinateEditEndpoint`를 적용하고, 포트 hit 영역은 좌표 변경 모드에서 pointerdown을 막지 않게 했다. 또한 pointerup 뒤 들어오는 후속 click이 새 attach 클릭으로 처리되지 않도록 짧은 suppress guard를 추가했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. 기존 dev server `http://127.0.0.1:5173/`에서 in-app Browser 새 탭 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 좌표 변경 입력 이벤트만 수정했다.
- 주의점: 좌표 변경 모드는 클릭/드래그 시작 시점의 pointerdown에서 좌표를 먼저 반영하고, pointerup/leave에서 history batch를 종료한다.

## 2026-06-16 KST - 좌표 변경을 branch 이동 방식으로 재구성

- 작업 요약: React 편집모드의 `좌표 변경`이 parent 포트 id만 바꾸고 실제 branch가 안 움직이던 문제를 수정했다. 이제 좌표 변경 중에는 child가 붙은 면 기준으로 x축 또는 y축만 허용하고, 선택된 relation의 child 쪽 그룹 전체를 그 축으로 함께 이동시키면서 parent attach 좌표(`link.from.portId`)도 같이 갱신한다. 세로 파이프의 `bottom` 같은 면도 synthetic tap port로 해석되도록 보강해, 이전처럼 아무 변화가 없는 케이스를 줄였다. 일반 클릭 해체는 계속 비활성 상태를 유지한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 다시 띄운 뒤 in-app Browser 새 탭에서 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 relation 좌표 변경 interaction과 JSON/localStorage에 저장되는 relation endpoint 좌표 표현만 변경했다.
- 주의점: 좌표 변경 모드가 켜지면 우측 패널에 현재 축(`x축` 또는 `y축`)이 표시되고, 마우스를 움직이면 child branch가 따라 움직인다. 원하는 위치에서 한 번 클릭하면 좌표 변경이 종료된다.

## 2026-06-16 KST - attach 포트 즉시 해체 제거와 좌표 변경 드래그화

- 작업 요약: React 편집모드에서 attach된 파란 포트를 일반 클릭했을 때 relation이 바로 해체되던 동작을 제거했다. 이제 일반 클릭은 객체 선택만 수행하고, 해체는 parent 객체 선택 후 파란 포트 우클릭 메뉴의 `해체` 버튼으로만 가능하다. 또한 `좌표 변경` 메뉴를 누른 뒤 마우스를 이동하면 child가 붙은 면 기준으로 parent attach 좌표가 x축 또는 y축 방향으로 실시간 갱신되도록 수정했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser 새 탭에서 로딩했고 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 relation endpoint UI/interaction과 JSON/localStorage에 저장되는 `link.from.portId` 갱신 방식만 변경했다.
- 주의점: 좌표 변경은 history batch로 묶이며, top/bottom child 면은 parent tap의 x좌표를, left/right child 면은 parent tap의 y좌표를 바꾼다. child 위치는 그대로 유지된다.

## 2026-06-16 KST - parent attach 포트 우클릭 해체/좌표 변경 메뉴

- 작업 요약: React 편집모드에서 parent 객체를 선택했을 때 해당 parent에서 attach된 relation 포트만 파란 원으로 표시되도록 수정했다. 선택된 parent의 파란 attach 포트를 우클릭하면 우측 메뉴 최상단에 `해체`와 `좌표 변경`이 뜨며, `해체`는 해당 relation을 삭제하고 `좌표 변경`은 자식 위치를 유지한 채 parent 쪽 attach 좌표를 새 클릭 위치로 갱신한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 띄운 뒤 in-app Browser 새 탭에서 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 relation endpoint 표시/우클릭 메뉴/JSON 저장 대상인 `link.from.portId` 갱신만 변경했다.
- 주의점: 좌표 변경은 현재 tap 포트를 지원하는 parent 객체에서 동작하며, child endpoint 면 기준으로 top/bottom이면 x축 tap 위치를, left/right이면 y축 tap 위치를 갱신한다. child 객체 자체는 움직이지 않는다.

## 2026-06-16 KST - attach 클릭 모드와 resize 모드 분리

- 작업 요약: React 편집모드에서 부모 포트 선택 후 자식 객체를 선택하는 attach 흐름과 객체 사이즈 변경 흐름이 겹치지 않도록 마우스 입력 상태를 분리했다. 부모 포트가 선택된 상태에서는 객체 드래그/리사이즈가 시작되지 않고 attach 후보 객체로 처리된다. 후보 객체 위에 올라가면 edge attach 후보가 `|` 막대로 표시되며, 막대를 직접 누르지 않아도 객체 내부 아무 곳을 클릭하면 클릭 위치에서 가장 가까운 attach 후보 포트로 parent -> child 관계가 생성된다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. in-app Browser에서 `http://127.0.0.1:5173/` 새로고침 후 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 마우스 입력/포트 표시/attach 선택 UI만 변경했다.
- 주의점: `|` 표시는 클릭 대상이 아니라 attach 후보 위치 힌트다. 부모 포트가 없는 일반 선택 상태에서는 선택된 pipe/manhole에만 resize border handle이 활성화된다.

## 2026-06-16 KST - 변경탐색 기반 attach/length 전파 도입

- 작업 요약: React 편집모드에서 attach 또는 length 변경으로 relation endpoint 좌표 보정이 필요할 때, 즉시 대상 branch를 이동하지 않고 `변경탐색`으로 parent/child relation 라인을 축별로 탐색하도록 수정했다. x/y 각각 첫 번째 길이 조절 가능 edge를 우선 적용하고, 축소 중 최소 길이에 걸려 delta를 모두 흡수하지 못하면 같은 방향의 다음 조절 가능 후보를 계속 찾는다. 후보가 없거나 남은 delta가 있으면 해당 relation branch를 좌표 이동한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. in-app Browser에서 `http://127.0.0.1:5173/` 새로고침 후 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 attach/length relation 전파 규칙만 변경했다.
- 주의점: 변경탐색은 relation 방향 기준으로 ancestors 또는 descendants를 훑는다. 길이 조절 후보가 적용되면 그 후보까지의 중간 branch는 같은 축 delta만큼 따라가고, 후보가 없거나 남은 delta가 있으면 기존처럼 branch 이동으로 보정한다.

## 2026-06-16 KST - 기존 parent attach 보정에 y축 2단계 추가

- 작업 요약: React 편집모드에서 기존 parent가 있는 child를 attach할 때, 기존 parent branch 보정을 x축 처리 후 y축 처리까지 이어지도록 수정했다. x축은 기존처럼 가로 길이 조절 가능한 edge이면 길이를 조정하고 아니면 x좌표를 이동한다. 그 다음 y축도 세로 길이 조절 가능한 edge이면 길이를 조정하고 아니면 y좌표를 이동한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 attach 기존 parent branch 보정만 변경했다.
- 주의점: child의 기존 자식 branch는 계속 group 이동만 수행한다. 이번 변경은 기존 parent branch에만 `x 보정 -> y 보정` 순서를 추가한 것이다.

## 2026-06-16 KST - 기존 parent가 있는 child attach를 x축 기준으로 단순화

- 작업 요약: React 편집모드의 attach 전파 중 child에 기존 parent가 있는 경우를 단순화했다. child의 기존 자식들은 더 이상 길이조절 후보로 보지 않고 branch/group 이동만 수행한다. child의 기존 parent 쪽은 x축 delta만 보고, 해당 parent endpoint가 가로 길이 조절 가능한 edge이면 길이를 조정하고 그렇지 않으면 parent branch를 x좌표로 이동한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 attach 전파 규칙만 변경했다.
- 주의점: 이번 변경은 attach 이벤트의 기존 parent branch 처리에만 적용된다. `length resize relation` 규칙은 별도로 유지된다.

## 2026-06-16 KST - attach child 기존 parent 유무 기반 전파 규칙 수정

- 작업 요약: React 편집모드의 attach 스냅 규칙을 `parent -> child` 방향 기준으로 재정리했다. attach 시 새 parent는 제자리에 두고 child 자체를 먼저 길이 조절 또는 좌표 이동으로 맞춘다. child에 기존 parent가 없으면 child의 기존 자식 방향만 전파하고, child에 기존 parent가 1개 이상 있으면 기존 자식 방향과 기존 parent 방향을 모두 확인한다. 전파 대상 endpoint가 길이 조절 가능한 edge이면 길이를 조정하고, 아니면 해당 방향 relation branch를 x/y delta만큼 이동한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 attach 스냅/전파 규칙만 변경했다.
- 주의점: attach 전파는 기존 relation만 대상으로 하며, 새로 클릭한 parent는 움직이지 않는다. 길이 조절 가능 edge 판정은 기존 기준대로 horizontal pipe `left/right`, vertical pipe `top/bottom`, manhole `bottom`이다.

## 2026-06-16 KST - length resize relation 전파 규칙 재구성

- 작업 요약: React 편집모드에서 객체 길이를 조절할 때 relation 방향(`from -> to`)을 기준으로 child 쪽을 먼저 맞추는 새 length 변경 규칙을 추가했다. parent의 움직인 포트에 연결된 child endpoint가 길이 조절 가능한 edge이면 child 길이를 늘리거나 줄이고, 그렇지 않으면 child와 그 하위 relation 객체를 같은 x/y delta로 이동한다. child가 2개 이상의 parent를 가진 경우에는 현재 resize 중인 parent를 제외한 다른 parent endpoint도 같은 방식으로 길이 조절 가능 edge이면 길이를 조정하고, 아니면 parent 상위 relation 객체를 이동한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 length resize relation 전파 규칙만 변경했다.
- 주의점: 기본 pipe/manhole border resize 핸들을 다시 활성화했다. 길이 조절 가능 edge는 horizontal pipe의 `left/right`, vertical pipe의 `top/bottom`, manhole의 `bottom`이다. 이전에 끈 자동 stretch/follow 보정 규칙들은 계속 꺼져 있고 새 length 규칙이 별도로 실행된다.

## 2026-06-16 KST - attach resizable pipe edge를 방향 기준으로 수정

- 작업 요약: React 편집모드의 새 attach 규칙에서 길이 조절 가능한 pipe edge를 세로 파이프만 보던 문제를 수정했다. 이제 `pipeSegment`가 horizontal이면 `left/right`, vertical이면 `top/bottom` edge를 attach 중 길이 조절 가능 대상으로 본다. `manhole`은 기존처럼 height 방향의 `bottom` edge만 유지했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 attach resize edge 판정만 변경했다.
- 주의점: 이 변경은 attach 이벤트에만 적용된다. 이전에 비활성화한 수동 border resize 및 자동 보정 규칙들은 계속 꺼져 있다.

## 2026-06-16 KST - 새 attach parent-anchor/child-resize 규칙 적용

- 작업 요약: React 편집모드의 attach 기본 동작을 다시 정리했다. 관계 생성 시 첫 번째 클릭 객체를 parent anchor로 유지하고, 두 번째 클릭 객체(child) 쪽 relation group을 이동시킨다. 단 child의 선택 포트가 길이 조절 가능한 edge이면 먼저 그 edge를 parent anchor 좌표까지 늘리거나 줄인 뒤, 남은 오차만 child group 이동으로 맞춘다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 attach 스냅 규칙만 변경했다.
- 주의점: 현재 attach에서 길이 조절 가능한 edge는 vertical `pipeSegment`의 `top/bottom`, `manhole`의 `bottom`이다. 이전에 임시 비활성화한 자동 stretch/follow 보정 규칙들은 계속 꺼져 있고, attach helper만 독립적으로 child edge resize를 수행한다.

## 2026-06-16 KST - attach anchor와 기본 resize 규칙 임시 비활성화

- 작업 요약: React 편집모드의 새 attach/length/position 규칙 재설계를 위해 아직 남아 있던 `child pipe/tap anchor attach` 규칙과 `pipe/manhole 기본 resize` 규칙을 삭제하지 않고 `ENABLE_*` 플래그로 비활성화했다. 이제 attach에서 child pipe tap 또는 이미 parent가 있는 pipe를 자동 anchor로 보지 않으며, 파이프/맨홀 border resize는 현재 실행되지 않는다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 attach anchor 판단과 기본 길이 변경 실행 조건만 변경했다.
- 주의점: 구현 함수는 남아 있고 상단 플래그만 꺼져 있다. 새 규칙을 넣을 때는 `ENABLE_CHILD_PIPE_OR_TAP_ANCHOR_ATTACH_RULE`, `ENABLE_BASIC_PIPE_MANHOLE_RESIZE_RULE`를 기준으로 기존 동작을 비교할 수 있다.

## 2026-06-16 KST - UI 자동 보정 규칙 6개 임시 비활성화

- 작업 요약: React 편집모드에서 attach/resize 중 자동으로 파이프를 늘리거나 연결 객체를 이동시키는 UI 보정 규칙 6개를 삭제하지 않고 `ENABLE_*` 플래그로 비활성화했다. 비활성화 대상은 `pipe -> connector` parent pipe stretch, 다중 parent tap attach stretch, fixed-y vertical pipe top resize를 bottom resize처럼 처리하는 규칙, 리사이즈된 포트에 붙은 객체 follow 이동, 본관 tap anchor retarget, fixed-anchor branch 길이 동기화다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 UI 자동 보정 실행 조건만 변경했다.
- 주의점: 규칙 구현 함수는 남겨두었고 실행 플래그만 꺼져 있다. 이후 필요한 규칙만 하나씩 되살릴 때는 상단 `ENABLE_*` 플래그를 기준으로 켜면 된다.

## 2026-06-16 KST - 본관 tap 고정 예외 범위 축소

- 작업 요약: React 편집모드에서 파이프 리사이즈 시 tap 포트에 붙은 커넥터를 움직이지 않고 tap 퍼센트만 재계산하는 예외를 추가했지만, 초기 구현이 모든 pipe tap 관계에 적용되어 단순 `맨홀 - 커넥터 - 파이프` 그룹까지 y 이동이 끊길 수 있었다. 예외 조건을 “같은 target pipe에 fixed-y anchor branch가 2개 이상 붙고, 해당 terminal connector가 그 branch cohort에 속한 경우”로 좁혔다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 pipe tap relation 리사이즈 예외 조건만 변경했다.
- 주의점: 단순 relation group은 다시 기존 side 이동 규칙을 탄다. 본관 tap 고정 예외는 fixed-anchor branch cohort가 실제로 존재하는 다중 branch 본관에만 적용된다.

## 2026-06-16 KST - fixed-anchor 본관 접속 branch 길이 동기화

- 작업 요약: React 편집모드에서 같은 child pipe에 붙은 여러 branch가 모두 고정 y 객체를 anchor로 가진 경우, 한 branch의 세로 길이를 조절하면 같은 본관 접속 레벨의 다른 branch들도 통째로 이동하지 않고 세로 길이만 같이 조정되도록 solver를 추가했다. 대상은 terminal connector 바로 위에 vertical `pipeSegment` 또는 `manhole`이 있고, 그 위쪽 relation 경로에 아파트/집/맨홀/빗물받이 같은 fixed-y anchor가 있는 branch로 제한했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 relation 그래프 기반 resize 보정만 변경했다.
- 주의점: 같은 x좌표가 아니라 “같은 child pipe에 붙고 fixed-y anchor를 가진 branch cohort”가 기준이다. 제거했던 광범위한 parent-pipe 전파를 되살린 것이 아니라, terminal connector와 target pipe가 실제로 이동한 resize 상황에서만 branch 길이를 맞춘다.

## 2026-06-16 KST - 파이프 리사이즈 간 parent-pipe 전파 제거

- 작업 요약: React 편집모드에서 하나의 파이프 길이/높이를 조절할 때, 그 파이프에 붙어 이동한 connector를 매개로 다른 parent pipe까지 자동으로 stretch되던 전파 로직을 제거했다. 이제 파이프 리사이즈는 해당 파이프의 직접 연결 side/tap 관계만 이동시키고, 같은 본관에 붙은 다른 가지 파이프의 높이를 함께 바꾸지 않는다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 pipe resize 전파 규칙만 변경했다.
- 주의점: `pipe -> connector` 관계를 새로 생성할 때 parent pipe 또는 relation group을 connector 쪽으로 맞춘 뒤 파이프 길이를 늘리는 규칙은 유지했다. 제거한 것은 “이미 연결된 상태에서 한 파이프를 리사이즈했을 때 다른 파이프까지 따라 stretch되는” 후속 전파다.

## 2026-06-16 KST - 파이프 tap 포트 밀도 동적화와 pipe->connector stretch/x 보정

- 작업 요약: React 편집모드의 파이프 tap 포트가 고정 10% 단위로만 표시되던 것을 파이프 길이에 비례해 동적으로 생성하도록 바꿨다. 짧은 파이프는 포트가 덜 촘촘하게 보이고, 긴 파이프는 더 촘촘한 간격으로 포트를 제공한다. 또한 직전의 본관 sibling branch 추론 방식은 이상한 공중 분리 형태를 만들 수 있어, `pipe -> connector` 관계에서 child connector가 이동하면 parent pipe 끝단이 connector 위치에 맞춰 늘거나 줄어드는 규칙으로 전환했다. 관계 생성 시점에도 parent가 pipe이고 child가 connector이면 connector를 pipe 쪽으로 당기지 않고 parent pipe 끝단을 connector 위치까지 먼저 맞춘다. 이때 x/y 직교축 오차 때문에 direct stretch가 실패하면 parent pipe가 속한 relation group을 connector 좌표 쪽으로 먼저 이동한 뒤 파이프 길이를 늘리도록 보정했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 포트 렌더링 밀도와 relation resize 보정 규칙만 변경했다.
- 주의점: 기존 JSON/localStorage에 저장된 `tap-top-10` 같은 포트 ID는 계속 해석 가능하다. 새로 표시되는 파이프 tap 포트 목록만 길이에 따라 달라진다. connector가 parent이고 pipe가 child인 `connector -> pipe` 관계는 기존 attach/resize 흐름을 유지한다. `pipe -> connector`에서 x/y가 어긋난 경우만 parent pipe 또는 그 relation group이 먼저 직교축으로 맞춰진 뒤 축 방향 길이가 조정된다.

## 2026-06-16 KST - sibling branch 리사이즈 재귀 루프 차단

- 작업 요약: 직전 본관 다중 parent 가지 리사이즈 동기화에서 내부 sibling branch 보정이 다시 `applyPipeResizeToLayout`을 호출하며 `Maximum call stack size exceeded`를 일으키던 문제를 수정했다. 내부 보정용 파이프 리사이즈에는 sibling 동기화를 재실행하지 않는 옵션을 추가해 1회 보정 후 멈추도록 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 pipe resize 보정 호출 흐름만 변경했다.
- 주의점: 일반 사용자 리사이즈와 숫자 길이 입력은 sibling branch 동기화를 계속 수행한다. sibling 동기화 내부에서 파생된 보정 리사이즈만 재귀 방지를 위해 동기화를 끈다.

## 2026-06-16 KST - 본관 다중 parent 가지 리사이즈 동기화

- 작업 요약: React 편집모드에서 하나의 본관 파이프에 여러 parent 가지가 붙은 상태에서, 한쪽 vertical parent 파이프 길이를 줄이거나 늘릴 때 다른 parent 가지가 rigid하게 밀려가지 않도록 보정했다. 본관에 incoming parent가 2개 이상이면, 움직인 본관 쪽에 함께 밀린 sibling branch를 원위치로 되돌린 뒤 그 sibling branch의 parent 파이프 끝단을 같은 delta만큼 리사이즈한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 pipe resize/relation attach 보정만 변경했다.
- 주의점: 오른쪽 패널 숫자 입력으로 파이프의 축 방향 길이(`가로`/`세로`)를 바꾸는 경우도 캔버스 리사이즈와 같은 `applyPipeResizeToLayout` 경로를 타도록 했다. 굵기 변경처럼 축 길이가 아닌 변경은 기존 단순 업데이트를 유지한다.

## 2026-06-16 KST - x 오차가 있는 부모 파이프 자동 연장 보정

- 작업 요약: React 편집모드에서 이미 parent를 가진 본관 파이프에 다른 커넥터-파이프 가지를 붙일 때, target 본관과 parent 가지의 x좌표가 다르면 자동 연장이 중단되던 조건을 보정했다. 기존 stretch 규칙은 파이프 축과 직교하는 오차가 8px을 넘으면 실패했는데, 수직 parent 파이프의 경우 parent 가지를 먼저 x방향으로 맞춘 뒤 세로 길이만 늘리도록 했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 relation attach/파이프 자동 연장 규칙만 변경했다.
- 주의점: 자동 연장은 여전히 “child 대상 파이프에 이미 incoming parent가 있는 경우”에만 동작한다. 이번 보정은 parent 쪽에 실제로 늘릴 수 있는 파이프 끝단이 있을 때 그 parent 가지를 x로 먼저 맞추는 제한된 처리이며, y고정 객체가 포함된 수평 가지를 y방향으로 강제 이동시키지는 않는다.

## 2026-06-16 KST - 부모 있는 파이프 attach 자동 연장 조건 확대

- 작업 요약: React 편집모드에서 이미 incoming parent를 가진 파이프에 새 커넥터를 연결할 때, 클릭한 포트가 `tap-*`일 때만 자동 연장되던 조건을 수정했다. 이제 child가 파이프이고 이미 parent가 있으면 기본 `top/right/bottom/left` 포트로 연결해도 대상 파이프를 고정 anchor로 보고, parent 쪽 파이프 끝단 자동 연장을 먼저 시도한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 관계 스냅 규칙만 변경했다.
- 주의점: 첫 부모 연결 전에는 대상 파이프가 parent 커넥터 쪽으로 이동하는 이전 규칙을 유지한다. 대상 파이프에 parent가 생긴 이후부터만 자동 연장 후보가 된다.

## 2026-06-16 KST - pipe tap 첫 부모 연결과 다중 부모 연장 조건 분리

- 작업 요약: React 편집모드의 attach 스냅에서 child가 파이프 tap일 때 무조건 대상 파이프를 고정 anchor로 보던 동작을 수정했다. 이제 붙이려는 대상 파이프에 기존 incoming parent가 없으면 대상 파이프가 parent 커넥터 쪽으로 이동하고, 기존 incoming parent가 있을 때만 다중 부모 attach로 판단해 parent 쪽 파이프 자동 연장 규칙을 시도한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 관계 스냅 규칙만 변경했다.
- 주의점: `관 종류(pipeKind)`는 여전히 색상/렌더링 및 선택 UI에만 사용하며 attach 분기 조건에 들어가지 않는다. 자동 연장은 “대상 파이프에 이미 부모가 있는 경우”에만 동작한다.

## 2026-06-16 KST - React 버튼으로 SWMM INP 내보내기 연결

- 작업 요약: React 편집 화면 상단에 `SWMM INP 내보내기` 버튼을 추가하고, 기존 SWMM 엔진 서버에 `POST /editor/export-inp` 엔드포인트를 추가했다. 브라우저는 현재 `EditorLayout`을 서버로 보내고, 서버는 `scripts/editor_layout_to_swmm_inp.py` 변환 로직으로 `.inp` 텍스트를 만들어 다운로드 응답으로 반환한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `server/swmm_engine_server.py`, `docs/work_log.md`
- 검증 결과: `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py server/swmm_engine_server.py` 통과. `cd react-viewer && npm run build` 통과. `server/swmm_engine_server.py --port 8767` smoke test에서 `/editor/export-inp`가 `HTTP/1.0 200 OK`, `Content-Disposition: attachment; filename="smoke_editor_export.inp"`와 INP 본문을 반환하는 것을 확인했다. dev server `http://127.0.0.1:5175/` 응답과 production bundle 내 `SWMM INP`/`editor/export-inp` 포함도 확인했다.
- 계층 영향: 기존 기준 SWMM 모델과 HTML contract는 변경하지 않았다. 서버 payload 표면에는 editor export 전용 endpoint가 추가됐고, React 편집기에는 해당 endpoint를 호출하는 버튼이 추가됐다.
- 주의점: 버튼은 기본적으로 `http://127.0.0.1:8765/editor/export-inp`를 호출한다. 다른 엔진 URL을 쓰려면 React 실행 시 `VITE_SWMM_ENGINE_URL`을 설정해야 한다. 서버가 꺼져 있으면 버튼 클릭 시 실패 alert가 뜬다.

## 2026-06-16 KST - 에디터 JSON 기반 SWMM INP 1차 변환기 추가

- 작업 요약: 기존 `viewer/overall_drainage_diagram.html`/HTML contract 흐름은 건드리지 않고, React 편집모드에서 내보낸 `EditorLayout` JSON만 기준으로 SWMM `.inp` skeleton을 생성하는 독립 변환기 `scripts/editor_layout_to_swmm_inp.py`를 추가했다. `relation`은 SWMM 링크가 아니라 attach 관계로 해석하고, `pipeSegment`는 relation endpoint/tap station에 따라 SWMM conduit segment로 변환한다.
- 주요 파일: `scripts/editor_layout_to_swmm_inp.py`, `docs/editor_swmm_integration_analysis.md`, `docs/work_log.md`
- 검증 결과: `python3 -m py_compile scripts/editor_layout_to_swmm_inp.py` 통과. stdin 샘플 EditorLayout을 `/tmp/generated_from_editor_smoke.inp`로 변환했고 `summary={"conduits": 3, "inflows": 1, "junctions": 2, "outfalls": 1, "pumps": 0, "storages": 1, "warnings": 0, "weirs": 0}` 확인. `.venv/bin/python` + PySWMM으로 생성 `.inp` 3 step 실행 통과. 직접 `pipe/elbowPipe/pump` 링크 기반 샘플도 별도로 변환 후 PySWMM 3 step 통과.
- 계층 영향: SWMM 기존 기준 모델, HTML contract, 서버 payload, React UI는 변경하지 않았다. 에디터 JSON에서 신규 SWMM `.inp`를 만드는 별도 script와 문서만 추가했다.
- 주의점: 생성 `.inp`는 첫 실행 가능한 skeleton이다. 에디터 JSON에 실제 수리 필드가 아직 없기 때문에 elevation, maxDepth, diameter, roughness, storage factor 등은 기본값으로 추정한다. 다음 단계는 React UI에서 이 변환기를 호출할 수 있도록 모델 내보내기 JSON/버튼을 연결하거나, 에디터에 수리 필드 입력을 추가하는 것이다.

## 2026-06-16 KST - React 편집 JSON과 SWMM 연동 계약 분석

- 작업 요약: React 편집모드의 `EditorLayout` JSON이 실제 SWMM `.inp` 모델과 PySWMM 결과 payload에 연결되려면 어떤 중간 계약이 필요한지 조사하고, `EditorLayout -> DrainageModelDocument -> SWMM .inp -> contract -> SwmmStatePayload -> UI` 흐름으로 정리했다. 현재 `relation` 링크는 화면 attach/그룹 이동 관계이며 SWMM `CONDUIT/ORIFICE/WEIR/PUMP` 링크와 직접 동일시하면 안 된다는 점을 명확히 했다.
- 주요 파일: `docs/editor_swmm_integration_analysis.md`, `docs/work_log.md`, 참고 파일 `react-viewer/src/components/editor/editorTypes.ts`, `react-viewer/src/components/editor/EditorCanvas.tsx`, `react-viewer/src/services/swmm/client.ts`, `models/seoul_rebuild_v2.inp`, `scripts/build_swmm_html_contract.py`, `scripts/swmm_html_bridge.py`, `server/swmm_engine_server.py`, `sample-results/swmm_html_contract.json`
- 검증 결과: `python3 scripts/build_swmm_html_contract.py` 통과(`visual_objects=42`, `nodes=68`, `links=66`, `missing_mappings=0`). `cd react-viewer && npm run build` 통과. 시스템 `python3 scripts/swmm_html_bridge.py --steps 3`는 PySWMM 미설치로 실패했지만, `.venv/bin/python scripts/swmm_html_bridge.py --steps 3`는 통과했다. `server/swmm_engine_server.py --port 8766`로 `/health`, `/contract`, `/session/step` smoke test를 통과했고 step 결과는 `pipes=24`, `assets=18`, `controls=6`이었다.
- 계층 영향: SWMM 모델, contract, 서버 payload, React runtime 코드는 변경하지 않았다. 분석 문서와 작업 로그만 추가/수정했다.
- 주의점: `8765` 포트에는 이미 SWMM 엔진 서버가 떠 있어 새 서버 실행은 포트 충돌이 났다. React 연동 구현 시 raw 편집 JSON을 바로 `.inp`로 변환하지 말고, 수리 필드와 visual mapping을 갖는 중간 모델 문서를 먼저 정의하는 방향이 안전하다.

## 2026-06-16 KST - 시설/방류구 attach 포트 표시 개수 축소

- 작업 요약: 시설/방류구 선택 시 상하좌우 10% 단위로 표시되던 tap 포트가 너무 많아, 시설 계열은 각 변 25%/50%/75% 3개만 기본 표시되도록 줄였다. 파이프는 기존 10% 단위 tap 포트를 유지한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5175/`에서 in-app Browser로 편집 모드 초기화 후 우수토실-월류시설을 선택했고, 시설 tap dot 12개와 중심 가이드 tap 4개, 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부의 가상 포트 렌더링 밀도만 바꿨다.
- 주의점: 기존 localStorage나 JSON에 이미 저장된 `tap-top-10` 같은 시설 관계가 있더라도 포트 해석은 계속 가능하게 두었다. 새로 선택할 때 기본으로 노출되는 시설/방류구 tap만 줄어든다.

## 2026-06-16 01:03 KST - HTML 기반 시설 객체와 시설 다중 attach 포트 추가

- 작업 요약: `viewer/overall_drainage_diagram.html`의 대표 시설물을 React 편집모드 시설 객체로 옮겼다. `facility`는 `facilityKind`로 일반 시설, 우수토실-월류시설, 빗물펌프장, 물재생센터를 선택할 수 있고, `outfall`은 `outfallKind`로 일반 방류구, 월류 방류구, 펌프 방류구, 처리수 방류구를 선택할 수 있다. 방류구는 HTML 화면처럼 좌측 연결관과 우측 그릴 패널이 보이도록 디자인을 조정했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `react-viewer/src/components/editor/defaultLayout.ts`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. dev server `http://127.0.0.1:5175/`에서 in-app Browser로 편집 모드를 열고, 초기화 후 우수토실/빗물펌프장/물재생센터/월류 방류구/펌프 방류구/처리수 방류구가 모두 렌더링되는 것과 콘솔 error 0건을 확인했다. 우수토실 선택 시 `시설 세부 종류`, 방류구 선택 시 `방류구 종류` 셀렉트와 사방 tap 포트 렌더링도 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 node props에 `facilityKind`, `outfallKind`를 추가로 정규화하고, relation endpoint에는 기존과 같은 `tap-top-50` 형식의 가상 포트 ID가 저장될 수 있다.
- 주의점: 파이프 전용이던 tap 포트 해석을 `facility`/`outfall`에도 확장했다. 파이프는 기존처럼 방향에 따라 상하 또는 좌우 tap만 보여주고, 시설/방류구는 상하좌우 모든 변에 10% 단위 tap을 보여준다. 기존 localStorage가 있으면 새 기본 시설 예시는 바로 보이지 않을 수 있으며, 편집 모드의 `초기화`를 누르면 새 기본 레이아웃이 반영된다.

## 2026-06-16 KST - 다중 부모 pipe tap attach 자동 연장 규칙 추가

- 작업 요약: React 편집모드에서 이미 parent 관계를 가진 파이프의 tap 포트에 새 커넥터를 parent로 붙일 때, 기존처럼 새 parent 그룹 전체를 y 방향으로 이동시키지 않고 parent 쪽에 이미 붙어 있는 파이프 끝단을 축 방향으로 자동 연장하도록 좁은 규칙을 추가했다. 조건은 child가 pipe tap이고, 대상 파이프가 기존 incoming parent를 가지며, 새 parent가 커넥터/ㄱ자 커넥터이고, 그 parent가 다른 파이프의 실제 끝단에 붙어 있는 경우로 제한했다. 기존에 들어와 있던 시설/방류구 세부종류 helper가 빌드를 깨지 않도록 오른쪽 선택 패널과 렌더링에 연결했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: `cd react-viewer && npm run build` 통과. 기존 dev server `http://127.0.0.1:5173/`를 in-app Browser에서 새로고침했고, 앱 로딩 및 콘솔 error 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 관계 스냅/파이프 리사이즈 동작에만 영향이 있다.
- 주의점: 예전에 제거한 광범위한 스트레칭 규칙을 되살린 것이 아니라, 다중 부모가 되는 pipe tap attach에서만 동작한다. 축과 직교하는 오차가 큰 경우나 parent 커넥터가 늘릴 수 있는 파이프 끝단을 찾지 못하는 경우에는 기존 그룹 이동 fallback을 사용한다. 시설/방류구 세부종류는 React 편집기 내부 props(`facilityKind`, `outfallKind`)만 다루며 SWMM contract에는 아직 연결하지 않았다.

## 2026-06-16 KST - React 편집모드 히스토리/undo-redo 확인

- 작업 요약: `AGENTS.md` 최신 규칙을 다시 읽고, 직전 React 편집모드 히스토리 작업이 실제 코드에 반영됐는지 확인했다. `useReducer` 기반 레이아웃 히스토리, `Command/Ctrl + Z` 되돌리기, `Command/Ctrl + Shift + Z` 다시 실행, 상단 `되돌리기`/`다시 실행` 버튼, 드래그/리사이즈 배치 저장이 `EditorCanvas.tsx`에 들어가 있음을 확인했다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `AGENTS.md`, `docs/work_log.md`
- 검증 결과: 직전 구현 후 `cd react-viewer && npm run build` 통과 및 in-app Browser 로딩/콘솔 오류 0건 확인 기록이 있다. 이번 확인에서는 `AGENTS.md`와 최근 작업 로그를 다시 읽고, 관련 코드 위치를 재확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부 레이아웃 상태 관리와 키보드/버튼 UI에만 영향이 있다.
- 주의점: 히스토리는 현재 브라우저 편집 세션 안에서 유지된다. 레이아웃 자체는 기존처럼 localStorage에 저장되지만 undo/redo 스택은 새로고침 후 복원 대상이 아니다. 드래그/리사이즈 중간 프레임은 히스토리에 쌓지 않고 포인터 종료 시 1회 커밋한다.

## 2026-06-16 00:35 KST - 파이프 다중 부착 포트 구조 추가

- 작업 요약: React 편집모드에서 커넥터/ㄱ자 커넥터를 파이프의 중앙뿐 아니라 관 길이 중 여러 지점에 붙일 수 있도록, 파이프 전용 가상 tap 포트 구조를 추가했다. 수평 파이프는 상/하단, 수직 파이프는 좌/우측에 10% 단위 부착점을 표시하며, 50% 중심점은 가이드라인 역할을 하도록 다른 색으로 표시한다.
- 주요 파일: `react-viewer/src/components/editor/EditorCanvas.tsx`, `docs/work_log.md`
- 검증 결과: 직전 변경 후 `cd react-viewer && npm run build`를 통과했고, dev server를 띄운 뒤 in-app Browser에서 편집모드 로딩 및 콘솔 오류 0건을 확인했다.
- 계층 영향: SWMM 모델, contract, 서버 payload는 변경하지 않았다. React 편집기 내부에서만 `tap-top-10` 같은 가상 포트 ID를 해석하며, 링크 endpoint에는 해당 포트 ID가 저장될 수 있다.
- 주의점: 기존 `node.ports` 배열을 대량 확장하지 않고 렌더링/스냅 시점에만 가상 포트를 계산한다. 선택된 파이프 또는 관계 생성 대기 중인 파이프에 tap 포트가 보이며, 파이프 길이를 조절하면 tap 포트에 연결된 쪽 그룹도 새 위치로 따라가도록 처리했다. 기존 HTML식 선형 링크 객체는 파이프 노드가 아니므로 이 tap 포트 대상이 아니다.

## 2026-06-16 00:31 KST - AGENTS 프로젝트 전용 규칙 정리

- 작업 요약: 전역 규칙과 중복되던 `AGENTS.md`를 SWMM/React/실시간 시뮬레이션 계약 중심의 프로젝트 전용 규칙으로 재작성하고, 작업 로그 운영 규칙을 추가했다.
- 주요 파일: `AGENTS.md`, `docs/work_log.md`
- 검증 결과: `AGENTS.md` 내용을 다시 읽어 규칙 반영을 확인했다.
- 주의점: 이후 작업자는 이 파일의 최근 3개 항목을 먼저 확인한 뒤, SWMM 모델/contract/server payload/React 상태 구조 중 어떤 계층에 영향이 있는지 기록해야 한다.
