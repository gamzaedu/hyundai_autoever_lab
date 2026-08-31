# Fleet Console — 기준본 (v1.0)

2교시  「커넥티드카 관제 콘솔 v1.0」 을 ** 구현한 공용 출발점**.

## 실행

```bash
npm install
npm run dev
```

→ http://localhost:5173

### 실행 스크립트 (자동)

Node.js 확인 → 의존성 설치 → 개발 서버 실행까지 한 번에 처리합니다.

| OS | 실행 방법 |
| --- | --- |
| Windows | `start-server.bat` 더블클릭 (또는 cmd 에서 `start-server.bat`) |
| macOS / Linux | `chmod +x start-server.sh` (최초 1회) 후 `./start-server.sh` |

## 구현 범위

| ID | 요구사항 | 상태 |
| --- | --- | --- |
| FR-01 | 차량 목록 | ✅ |
| FR-02 | 통합 검색 | ✅ |
| FR-03 | 상태 필터 | ✅ |
| FR-04 | KPI 카드 4종 | ✅ |
| FR-05 | 상세 패널 + 주행 이력 | ✅ |
| FR-06 | 알람 판정 (AL-01~03) | ✅ |
| FR-07 | 정렬 | ✅ |
| FR-08 | 텔레메트리 시뮬 | ❌ 미구현 |
| FR-09 | 알람 토스트/이력 | ❌ 미구현 |
| FR-10 | 반응형 | 부분 |

## 구조

```
src/
  types.ts               타입 정의
  lib/format.ts          시각·숫자 표기
  lib/alarms.ts          알람 판정
  components/
    KpiCards.tsx         KPI 4종
    FilterBar.tsx        검색 + 상태 필터
    VehicleTable.tsx     차량 목록
    DetailPanel.tsx      상세 + 주행 이력
  App.tsx                상태 관리 · 필터/정렬
public/data/             vehicles.json · trips.json
```

## 데이터

- 기준시각은 시스템 시각이 아니라 `vehicles.json` 의 `as_of` 사용
- 알람 규칙: AL-01 SOC 15% 미만(EV) / AL-02 정비필요·DTC / AL-03 무신호 30분 초과
