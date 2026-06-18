# 도시침수 SWMM / React 편집기 작업 인수인계 요약

작성일: 2026-06-15

## 1. 전체 목표

서울 도시 배수 시스템을 SWMM 기반으로 모델링하고, React 화면은 SWMM의 노드/링크 구조를 시각화하고 편집하는 도구로 만드는 것이 목표다.

최종 구조는 다음 방향이다.

```text
React 편집기
→ 배수 객체 배치
→ 노드/링크 관계 JSON 생성
→ Python / PySWMM 엔진 서버로 전달
→ 1초 단위 step-by-step 시뮬레이션
→ 현재 수위, 유량, 유속, 역류, 시설 작동 상태 반환
→ React 화면에 렌더링
```

React는 최종적으로 다음 역할을 맡는다.

- 배수도 렌더링
- 강수량 조절
- 각 객체별 막힘 정도 조절
- SWMM에서 반환된 상태값 표시

SWMM / Python은 다음 역할을 맡는다.

- 실제 수리 계산
- 관 기울기, 관경, 조도, 노드 고도 기반 흐름 계산
- 펌프, 월류, 방류, 역류 조건 처리
- 1초 단위 상태 반환

## 2. 주요 저장 위치

프로젝트 루트:

```text
/Users/onseoktae/Documents/swmm
```

React 편집기:

```text
/Users/onseoktae/Documents/swmm/react-viewer
```

React 편집기 핵심 파일:

```text
/Users/onseoktae/Documents/swmm/react-viewer/src/components/editor/EditorCanvas.tsx
/Users/onseoktae/Documents/swmm/react-viewer/src/components/editor/editorTypes.ts
/Users/onseoktae/Documents/swmm/react-viewer/src/components/editor/defaultLayout.ts
/Users/onseoktae/Documents/swmm/react-viewer/src/components/editor/layoutStorage.ts
```

기존 HTML 배수도:

```text
/Users/onseoktae/Documents/swmm/viewer/overall_drainage_diagram.html
```

SWMM 모델:

```text
/Users/onseoktae/Documents/swmm/models/seoul_rebuild_v2.inp
```

SWMM 모델 생성 스크립트:

```text
/Users/onseoktae/Documents/swmm/scripts/swmm_rebuild_v2.py
```

SWMM / HTML 계약 JSON:

```text
/Users/onseoktae/Documents/swmm/sample-results/swmm_html_contract.json
```

PySWMM 엔진 서버:

```text
/Users/onseoktae/Documents/swmm/server/swmm_engine_server.py
```

엔진 서버 실행 파일:

```text
/Users/onseoktae/Documents/swmm/Start_SWMM_Engine_Server.command
```

## 3. 지금까지의 큰 결정

### 3.1 SWMM 기준으로 간다

처음에는 HTML에서 시각적 배수도를 직접 만들었지만, 이후 방향을 바꿨다.

현재 방향은 다음과 같다.

```text
SWMM의 노드 / 링크 구조
→ React 데이터 모델
→ React 렌더링
```

즉 화면이 먼저가 아니라, SWMM에서 쓸 수 있는 구조가 먼저다.

### 3.2 React는 편집기 역할

React 화면은 단순한 그림이 아니라, 배수 네트워크를 직접 배치하고 연결하는 편집기다.

편집 결과는 JSON으로 저장되고, 이 JSON이 이후 SWMM 모델 생성 또는 SWMM ID 매핑에 사용된다.

### 3.3 관계는 시각선이 아니라 실제 스냅 관계

객체끼리 관계를 맺으면 단순히 `관계`라는 점선으로 보이는 것이 아니라, 실제 객체가 서로 붙어야 한다.

예:

```text
빗물받이 오른쪽 포트
→ 커넥터 왼쪽 포트
```

이 관계가 생기면 커넥터가 빗물받이 오른쪽에 붙어야 한다.

### 3.4 첫 번째 클릭은 부모, 두 번째 클릭은 자식

관계를 맺을 때 다음 개념을 도입하려고 했다.

```text
첫 번째 클릭 객체 = 부모
두 번째 클릭 객체 = 자식
```

일반적으로 자식이 부모에 붙는다.

단, 자식이 y좌표 고정 객체라면 부모가 자식 위치에 맞춰 움직여야 한다.

## 4. 객체 종류

현재 React 편집기에서 다루는 주요 객체는 다음과 같다.

### 지상 / 고정 성격 객체

- 빗물받이
- 집
- 아파트
- 맨홀

이 객체들은 기본적으로 지면 기준 위치가 중요하다.

### 배관 / 연결 객체

- 파이프
- 커넥터
- ㄱ자 커넥터
- 시설
- 방류구

### 시설 객체

- 우수토실-월류시설
- 빗물펌프장
- 물재생센터
- 방류구

## 5. 파이프 크기 기준

파이프는 소 / 중 / 대 크기 기준을 사용한다.

현재 기준 예시는 다음과 같다.

```ts
small: {
  innerThickness: 34,
  borderThickness: 6,
  labelSize: 16,
}

medium: {
  innerThickness: 70,
  borderThickness: 5,
  labelSize: 24,
}

large: {
  innerThickness: 98,
  borderThickness: 6,
  labelSize: 30,
}
```

커넥터는 연결되는 파이프 굵기를 기준으로 계산되어야 한다.

원칙:

```text
커넥터 긴 방향 길이 = 파이프 전체 굵기 기준 약 1.1배
커넥터 짧은 방향 길이 = 별도 비율로 조절 가능
```

파이프 전체 굵기는 내부 굵기뿐 아니라 border까지 포함해야 한다.

## 6. 기존 HTML에서 만든 것

기존 HTML 파일:

```text
/Users/onseoktae/Documents/swmm/viewer/overall_drainage_diagram.html
```

여기에는 다음이 구현되었다.

- 전체 도시 배수도
- 분류식 / 합류식 / 하천 구역
- 우수본관, 오수본관, 합류식 본관
- 우수간선관거, 차집관거
- 우수토실-월류시설
- 빗물펌프장
- 물재생센터
- 방류구 3종
- 물 흐름 점선 애니메이션
- 차오름 애니메이션
- 역류 방향 표현
- 비 / 구름 애니메이션
- SWMM 엔진 연결 시도
- UI 모드 / 디버그 모드 전환

다만 HTML은 구조가 커지고 복잡해져서 React로 옮기기로 했다.

## 7. React 편집기 현재 방향

React 편집기는 다음 구조로 가고 있다.

```text
보기 모드
편집 모드
```

보기 모드는 기존 배수도를 보는 용도다.

편집 모드는 객체를 직접 배치하고, 포트끼리 관계를 맺는 용도다.

편집 모드 기능:

- 객체 추가
- 객체 선택
- 객체 드래그
- 포트 클릭으로 관계 생성
- JSON 내보내기
- JSON 불러오기
- localStorage 임시 저장
- Backspace / Delete 삭제
- 우클릭 메뉴
- 선택 객체 우측 정보 패널

## 8. 편집 모드에서 이미 들어간 요구사항

### 8.1 우클릭 메뉴

상단에 모든 추가 버튼을 나열하는 방식은 줄이고, 다음 추가 작업들은 우클릭 메뉴에서 선택하도록 바꾸는 중이다.

- 빗물받이 추가
- 아파트 추가
- 집 추가
- 맨홀 추가
- 커넥터 추가
- ㄱ자 커넥터 추가
- 시설 추가
- 방류구 추가
- 독립 파이프 추가

상단에는 다음만 남기는 방향이다.

- JSON 내보내기
- JSON 불러오기
- 초기화

### 8.2 선택 해제

객체가 아닌 빈 캔버스를 클릭하면 선택이 풀려야 한다.

선택된 객체가 없으면 오른쪽 편집 정보 패널도 보이지 않아야 한다.

### 8.3 포트 표시

원하는 동작:

```text
선택 전: 포트 O 표시 안 보임
선택 후: 상 / 하 / 좌 / 우 포트 O 표시
관계가 있는 포트: 파란색 활성 표시
```

### 8.4 관계 표시

관계가 맺어진 포트는 시각적으로 확인 가능해야 한다.

예:

```text
빗물받이 오른쪽 ↔ 커넥터 왼쪽
```

빗물받이를 선택하면 오른쪽 포트가 파란색으로 표시되어야 한다.

커넥터를 선택하면 왼쪽 포트가 파란색으로 표시되어야 한다.

둘 중 하나라도 연결을 끊으면 관계가 삭제되어야 한다.

## 9. 최근 해결해야 하는 핵심 이슈

현재 가장 마지막으로 다루던 문제는 관계 스냅 규칙이다.

### 9.1 맨홀 포트 위치 문제

현재 맨홀의 좌 / 우 포트가 맨홀 몸통 중앙에 있어서 커넥터를 붙이면 중앙에 붙는다.

사용자가 원하는 것은 다음이다.

```text
맨홀의 좌 / 우 포트는 몸통 중앙이 아니라 하단부 쪽에 있어야 한다.
```

즉 맨홀만 특수하게 포트 위치를 아래쪽으로 내려야 한다.

특히 커넥터 크기가 소 / 중 / 대로 달라지므로, 커넥터 크기를 고려해서 붙어야 한다.

수정 후보 함수:

```text
getNodePortPoint
getEndpointPoint
renderSelectionHandles
snapRelationEndpoints
```

### 9.2 고정 y 객체가 자식일 때 부모가 따라가야 함

현재 문제:

```text
파이프 → 아파트
커넥터 → 맨홀
```

이런 순서로 관계를 맺으면, 아파트 / 맨홀은 y가 고정되어 있어서 움직이지 않는다.

그래서 커넥터 또는 파이프가 맞춰져야 한다.

원하는 규칙:

```text
첫 번째 클릭 = 부모
두 번째 클릭 = 자식

자식이 y 고정 객체라면
→ 자식을 움직이지 말고
→ 부모가 자식 위치에 맞춰 이동
```

### 9.3 자기 자신과 관계 금지

같은 객체의 포트끼리 관계가 생기면 안 된다.

예:

```text
커넥터 왼쪽 ↔ 같은 커넥터 오른쪽
```

이런 관계는 금지해야 한다.

### 9.4 ㄱ자 커넥터 포트 문제

ㄱ자 커넥터는 현재 포트 위치 때문에 원하는 모양으로 붙지 않는다.

원하는 모양은 다음이다.

```text
가로 파이프
→ 커넥터
→ ㄱ자 커넥터
→ 커넥터
→ 세로 파이프
```

ㄱ자 커넥터의 포트는 실제 커넥터 cap의 면을 기준으로 잡혀야 한다.

### 9.5 그룹 이동 규칙

관계가 형성된 객체들은 그룹처럼 움직여야 한다.

예:

```text
빗물받이 - 커넥터 - 파이프 - 커넥터
```

이 중 하나를 드래그하면 전체가 같이 움직여야 한다.

단, 그룹 안에 y 고정 객체가 있으면 그룹 전체는 x축만 움직여야 한다.

중요:

```text
y 고정 객체가 포함된 그룹만 x축 이동 제한
일반 객체만 있는 그룹은 x/y 자유 이동
```

## 10. SWMM 모델링 쪽 진행 상황

SWMM v2 모델 파일:

```text
/Users/onseoktae/Documents/swmm/models/seoul_rebuild_v2.inp
```

모델 생성 스크립트:

```text
/Users/onseoktae/Documents/swmm/scripts/swmm_rebuild_v2.py
```

진행했던 모델링:

- 우수본관 1
- 우수본관 2
- 우수맨홀
- 빗물받이 STORAGE
- 우수연결관을 ㄱ자 1개가 아니라 가로관 + 세로관 + 중간 노드로 분리
- 우수간선관거
- 빗물펌프장
- 펌프 토출관
- 펌프 방류구
- 오수본관
- 차집관거
- 물재생센터
- 처리수 방류관
- 합류식 본관
- 우수토실-월류시설
- 월류관
- 방류구

단, React 편집기와 SWMM 구조의 완전 매칭은 아직 진행 중이다.

## 11. PySWMM 엔진 서버

실행:

```bash
cd /Users/onseoktae/Documents/swmm
./Start_SWMM_Engine_Server.command
```

과거 이슈:

```text
PySWMM is not installed.
OSError: [Errno 48] Address already in use
```

`Address already in use`는 보통 이미 서버가 떠 있다는 뜻이다.

PySWMM macOS 바이너리 서명 복구 스크립트:

```bash
/Users/onseoktae/Documents/swmm/scripts/repair_pyswmm_macos_codesign.sh
```

## 12. React 실행

React 개발 서버 실행:

```bash
cd /Users/onseoktae/Documents/swmm/react-viewer
npm run dev
```

검증:

```bash
npm run build
npm run lint
```

## 13. 현재 git 상태 요약

최근 확인한 변경 상태:

```text
 M .gitignore
 M docs/swmm_rebuild_v2.md
 M models/seoul_rebuild_v2.inp
 M scripts/hydraulic_step_engine.py
 M scripts/swmm_rebuild_v2.py
 M viewer/overall_drainage_diagram.html
?? Start_SWMM_Engine_Server.command
?? backups/
?? docs/swmm_html_bridge.md
?? docs/swmm_html_contract.md
?? react-viewer/
?? requirements.txt
?? sample-results/swmm_html_contract.json
?? scripts/build_swmm_html_contract.py
?? scripts/repair_pyswmm_macos_codesign.sh
?? scripts/swmm_html_bridge.py
?? server/
?? viewer/swmm_html_contract.js
?? viewer/swmm_model_debug_viewer.html
```

주의:

```text
작업 트리에 이미 많은 변경이 있으므로,
무작정 reset / checkout 하지 말 것.
```

## 14. 다음 세션에서 바로 할 일

다음 세션에서는 구현을 이어가기 전에 아래 순서로 진행하는 것이 좋다.

### 1단계: React 편집기 관계 스냅 고치기

파일:

```text
/Users/onseoktae/Documents/swmm/react-viewer/src/components/editor/EditorCanvas.tsx
```

우선 확인할 함수:

```text
snapRelationEndpoints
moveNodeBy
getEndpointPoint
getNodePortPoint
renderSelectionHandles
```

수정 목표:

- 맨홀 좌/우 포트는 하단부 기준으로 붙게 하기
- 자기 자신과 관계 금지
- 첫 클릭 parent / 두 번째 클릭 child 개념 명확화
- child가 y 고정 객체이면 parent가 child에 맞게 움직이기
- 그룹 안에 y 고정 객체가 있을 때만 그룹 x축 이동 제한
- 관계 포트는 파란색으로 표시
- 관계선은 최종적으로 숨기고, 실제 스냅 관계만 남기기

### 2단계: 편집 결과 JSON 안정화

확인할 파일:

```text
/Users/onseoktae/Documents/swmm/react-viewer/src/components/editor/editorTypes.ts
/Users/onseoktae/Documents/swmm/react-viewer/src/components/editor/layoutStorage.ts
```

목표:

- 모든 노드에 id / swmmId / type / x / y / ports / props 유지
- 모든 링크에 from / to / fromPort / toPort / relation 정보 유지
- localStorage 새로고침 복원 안정화

### 3단계: React JSON → SWMM 매핑

React 편집 결과를 기반으로 다음을 생성하거나 매핑해야 한다.

```text
SWMM JUNCTION
SWMM STORAGE
SWMM CONDUIT
SWMM PUMP
SWMM WEIR / ORIFICE
SWMM OUTFALL
```

### 4단계: PySWMM 실시간 서버 연결

React에서 조절할 값:

- 강수량
- 객체별 막힘 정도

PySWMM에서 반환할 값:

- 수위
- 유량
- 유속
- 만관비
- 역류 여부
- 펌프 작동 여부
- 월류 여부

## 15. 사용자가 중요하게 보는 원칙

이 프로젝트에서 사용자가 계속 강조한 원칙은 다음이다.

```text
1. SWMM 물리 모델이 기준이어야 한다.
2. React는 임의 애니메이션이 아니라 SWMM 상태를 렌더링해야 한다.
3. 화면 객체 ID와 SWMM ID는 최대한 일치해야 한다.
4. ㄱ자 관은 하나의 관이 아니라 두 개의 직관과 중간 커넥터로 봐야 한다.
5. 관계가 생기면 실제로 붙어야지, 관계선만 그리면 안 된다.
6. 고정 객체와 일반 객체의 스냅 규칙이 명확해야 한다.
7. 구현 후에는 반드시 브라우저에서 직접 보고 확인해야 한다.
```

## 16. 다른 세션에 전달할 짧은 시작 프롬프트

다른 세션에서 이어갈 때는 아래처럼 시작하면 된다.

```text
/Users/onseoktae/Documents/swmm 프로젝트에서 작업 중입니다.
먼저 /Users/onseoktae/Documents/swmm/docs/handoff-react-editor-2026-06-15.md 를 읽고,
React 편집기 파일 /Users/onseoktae/Documents/swmm/react-viewer/src/components/editor/EditorCanvas.tsx 를 확인해주세요.

현재 목표는 편집모드의 관계 스냅 규칙을 고치는 것입니다.
특히 맨홀 포트가 중앙이 아니라 하단부 기준으로 붙도록 하고,
첫 번째 클릭 parent / 두 번째 클릭 child 관계를 유지하며,
child가 y 고정 객체일 경우 parent가 child에 맞춰 움직이도록 수정해야 합니다.
```

