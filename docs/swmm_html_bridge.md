# SWMM-HTML 실시간 브릿지 설계

## 원칙

- SWMM이 수리 계산의 원본입니다.
- HTML은 강수량과 객체별 막힘정도만 입력합니다.
- HTML은 유량, 유속, 만관, 역류, 펌프 배출량을 계산하지 않습니다.
- Python 브릿지는 PySWMM으로 1초씩 진행하고 현재 상태를 HTML payload로 돌려줍니다.

## 파일

- 계약 생성: `scripts/build_swmm_html_contract.py`
- 계약 JSON: `sample-results/swmm_html_contract.json`
- 브라우저 계약: `viewer/swmm_html_contract.js`
- 브릿지: `scripts/swmm_html_bridge.py`
- HTTP 엔진 서버: `server/swmm_engine_server.py`
- 기준 모델: `models/seoul_rebuild_v2.inp`

## 데이터 흐름

```text
HTML 컨트롤
→ rainfallRatio, 객체별 blockage 전송
→ Python 엔진 서버
→ Python 브릿지
→ PySWMM Simulation 1초 진행
→ SWMM 노드/링크 상태 읽기
→ HTML applySwmmStatePayload(payload)
→ 화면 렌더링
```

## HTML에서 보낼 값

```json
{
  "sourceOfTruth": "SWMM",
  "physicsMode": "swmm-step",
  "rainfallRatio": 0.75,
  "exceptions": [
    {
      "id": "sep_storm_main_2",
      "objectType": "pipe",
      "blockage": 0.4,
      "swmmNodes": ["sep_storm_manhole", "sep_storm_main_2_catch_basin_2_connector", "sep_storm_main_2_outlet_connector"],
      "swmmLinks": ["sep_storm_main_2_upstream_segment", "sep_storm_main_2_downstream_segment"]
    }
  ]
}
```

## 브릿지 적용 방식

- 강수량: `Node.generated_inflow()`로 빗물 유입 노드에 주입합니다.
- 모델 내 기존 `TS_STORM_RAIN` 유입은 런타임 임시 모델에서 0으로 낮춥니다.
- 오수 기본 유입 `TS_SEWER_DWF`는 그대로 둡니다.
- 오리피스, 위어, 펌프 막힘: `target_setting = 1 - blockage`
- 일반 관 막힘: 가능하면 PySWMM의 link flow limit을 사용해 유효 통수능을 낮춥니다.
- 결과 payload는 HTML의 `applySwmmStatePayload()` 형식에 맞춥니다.

## 실행

처음 한 번만 가상환경을 만들고 PySWMM을 설치합니다.

```bash
cd /Users/onseoktae/Documents/swmm
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/python -m pip install -r requirements.txt
```

macOS에서 `Code Signature Invalid`로 Python이 종료되면 PySWMM 바이너리를 재서명합니다.

```bash
./scripts/repair_pyswmm_macos_codesign.sh
```

브릿지 단독 실행:

```bash
.venv/bin/python scripts/swmm_html_bridge.py --steps 60
```

샘플 HTML 제어 payload 확인:

```bash
.venv/bin/python scripts/swmm_html_bridge.py --sample-control
```

HTML과 HTTP로 연결:

```bash
./Start_SWMM_Engine_Server.command
```

기본 엔드포인트:

```text
GET  http://127.0.0.1:8765/health
GET  http://127.0.0.1:8765/contract
POST http://127.0.0.1:8765/session/reset
POST http://127.0.0.1:8765/session/step
```

HTML 기본 연결 주소는 `http://127.0.0.1:8765`입니다.
다른 주소를 쓰려면 HTML을 다음처럼 열면 됩니다.

```text
overall_drainage_diagram.html?engineUrl=http://127.0.0.1:8765
```

정적 플레이백만 보고 싶으면 다음처럼 엔진 호출을 끕니다.

```text
overall_drainage_diagram.html?engine=0
```

## 현재 확인 상태

- 계약 생성 결과: HTML 대표 객체 42개, SWMM 노드 67개, SWMM 링크 65개, 누락 매핑 0개
- 로컬 현재 상태: PySWMM 미설치로 실제 SWMM step 실행은 보류
