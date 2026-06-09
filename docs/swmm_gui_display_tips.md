# SWMM GUI 화면을 더 보기 좋게 보는 법

EPA SWMM GUI 화면은 기본값으로 열면 회색 선과 작은 점만 보입니다.

다음 순서로 보면 훨씬 이해하기 쉽습니다.

## 1. 먼저 실행하기

```text
Project > Run Simulation
```

실행이 끝나야 수위, 유량, 침수 같은 결과를 색상/그래프로 확인할 수 있습니다.

## 2. Map Browser에서 결과 테마 선택

실행 후 Map Browser에서 다음을 바꿔봅니다.

```text
Nodes: Depth 또는 Flooding
Links: Flow 또는 Velocity
```

이렇게 하면 노드와 관이 결과값에 따라 색으로 보입니다.

## 3. 시간 애니메이션 보기

Map Browser의 Animator 패널에서 앞으로 재생 버튼을 누르면 시간에 따라 결과가 바뀌는 것을 볼 수 있습니다.

즉 SWMM GUI에서도 시간 재생은 가능합니다.

다만 디자인이 예쁘지는 않기 때문에, 발표용 설명은 `Open_Network_Viewer.bat` 화면이 더 적합합니다.

## 4. 추천 사용 방식

```text
정확한 계산 검증
→ EPA SWMM GUI

발표/설명용 시각화
→ Open_Network_Viewer.bat

센서값 표 확인
→ sample-results/*.csv
```
