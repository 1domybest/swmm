# SWMM 물리 감사 수정 준비 요약

- 입력: `/Users/onseoktae/Downloads/drainage-layout (1).json`
- 최종 감사: `sample-results/physics-audit-20260619-012748`
- 조건: 강수 100%, 600초 baseline, SWMM link 65개를 하나씩 100% 막힘
- 최종 결과: pass 33, inconclusive 18, suspect 14

## 확인된 핵심 원인

1. 커넥터/T자/ㄱ자 connector의 SWMM node 위치가 시각 중심으로 잡혀 수평관이 오르막이 되던 문제가 있었다.
   - 예: 수정 전 `우수 본관 01`, `우수 본관 02`, `오수 본관 01`, `합류식 본관 01`, `우수 간선관거 01`이 baseline에서 음수 유량이었다.
   - 조치: `scripts/editor_layout_to_swmm_inp.py`에서 connector/elbowConnector/teeConnector도 relation attach point 중 가장 깊은 관 접속부를 hydraulic node 위치로 사용하도록 수정했다.
   - 결과: 위 본관들은 최종 감사에서 모두 정방향 유량으로 바뀌었다.

2. 변환 warning 6개는 여전히 남아 있다.
   - `오수 연결관 수평 02`, `우수 연결관 수평 02`, `우수 연결관 수평 04`, 이름이 `파이프`인 3개 객체에서 relation 클릭 순서와 rotation 기반 기대 방향이 충돌한다.
   - 다음 조치: warning을 단순 통과가 아니라 물리 audit fail로 승격하고, editor UI에서 문제 객체를 바로 찾을 수 있게 sourceEditorId를 함께 노출한다.

3. 최종 baseline에서 여전히 음수 유량인 link 10개가 남았다.
   - relation: `REL_029_CONDUIT`, `REL_030_CONDUIT`, `REL_057_CONDUIT`, `REL_058_CONDUIT`, `REL_066_CONDUIT`
   - pipeSegment: `pipe_free_1781771598332`, `pipe_free_1781771856872`, `pipe_free_1781771871446`, `pipe_free_1781771885636`, `pipe_free_1781772019999`
   - 다음 조치: relation 클릭 방향 오류인지, 주변 시설/맨홀 head 때문에 실제 역류가 생기는지 분리해야 한다. 특히 자유 파이프는 화면 이름이 모두 `파이프`라 sourceEditorId로 위치 표시가 필요하다.

4. suspect 14개는 target flow는 거의 0으로 막히지만 upstream depth/head 상승이 2cm 미만이다.
   - 주요 후보: `PIPE_SEWER_MAIN_02`, `PIPE_OVERFLOW_INTERCEPTOR_DROP_01`, `PIPE_SEWER_MAIN_DROP_01`, 위 음수 relation/자유 파이프 일부.
   - 다음 조치: 막힘이 물리적으로 압력/수위 상승을 만들지 않는 이유를 확인해야 한다. 후보는 upstream node가 실제 유입 경계가 아니거나, 인접 relation conduit가 역방향이라 막힘 경계가 UI 의도와 다르게 잡힌 경우다.

## 다음 코드 수정 준비

1. 변환기 topology audit 강화
   - relation 방향과 pipe rotation 충돌을 report warning이 아니라 test/audit fail로 분류한다.
   - report에 sourceEditorId, sourceEditorName, relation id, from/to endpoint를 함께 남긴다.

2. connector 계열 hydraulic point 보정 유지
   - 이번 수정은 주요 본관 역방향을 해결했으므로 유지한다.
   - 추가로 시설/맨홀/connector가 여러 깊이의 관을 동시에 받는 경우 link offset을 도입할지 검토한다.

3. 수평관 기본 경사 반영
   - connector 접속점 y를 맞추면 수평관 기울기가 거의 0이 된다.
   - SWMM node elevation만으로 경사를 표현하기 어려운 구간은 conduit inlet/outlet offset 또는 station 기반 invert profile을 써야 한다.

4. 실험 UI 상세 패널 보강
   - 표시용 `editorObjects.maxFullness`와 raw SWMM `node.depth/head`, `link.flow/fullness`를 구분해 보여준다.
   - 역류 표시는 raw flow 부호와 설계 방향을 함께 보여서 UI 애니메이션 문제와 모델링 문제를 구분한다.

5. 재검증 명령

```bash
python3 scripts/run_swmm_physics_audit.py \
  --input "/Users/onseoktae/Downloads/drainage-layout (1).json" \
  --steps 600 \
  --rainfall-ratio 1.0 \
  --max-rainfall-mm-per-hour 100
```
