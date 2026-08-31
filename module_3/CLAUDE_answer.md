# CLAUDE.md — Fleet Console

## 프로젝트 개요

- 서비스명 : Fleet Console — 커넥티드카 관제 콘솔 (v1.x)
- 목적 : 업무차량 30대의 상태를 한 화면에서 확인하고, 조치가 필요한 차량을 즉시 식별
- 사용자 : 관제 담당자(알람 확인·조치 요청) · 정비 담당자(DTC 확인·입고 계획) · 운영 관리자(KPI 확인)

### 도메인 용어

| 용어 | 뜻 |
| --- | --- |
| SOC | State of Charge — 구동 배터리 잔량(%). `EV` · `HEV` 만 값이 있고 `ICE` 는 `null` |
| DTC | Diagnostic Trouble Code — 차량 진단 코드. 1건 이상이면 정비 필요(AL-02) 대상 |
| 텔레메트리 | 차량이 서버로 전송하는 상태 데이터 (SOC · 주행거리 · 위치 · `last_seen`) |
| `as_of` | `vehicles.json` 의 스냅샷 기준시각. 모든 경과시간 계산의 기준점 |

---

## 기술 스택

| 구분 | 내용 |
| --- | --- |
| 프레임워크 | React 18.3 (함수형 컴포넌트 + Hooks) |
| 언어 | TypeScript 5.6 (`strict`) |
| 빌드 | Vite 5.4 — `npm run dev` · `npm run build`(`tsc -b && vite build`) |
| 상태관리 | `useState` · `useMemo` 만 사용. 상태관리 라이브러리 도입 금지 |
| 금지 의존성 | CDN `<script>` · `<link>`, 차트/시각화 라이브러리, UI 프레임워크, 날짜 라이브러리 |

---

## 코딩 컨벤션

- 파일 분리 기준 : 판정·계산 로직은 `src/lib/`, 화면은 `src/components/`(1 컴포넌트 1 파일), 타입은 `src/types.ts`, 임계값·라벨 상수는 `src/config/`
- 컴포넌트 네이밍 : `PascalCase` named export, 파일명 = 컴포넌트명 (`VehicleTable.tsx` → `export function VehicleTable`)
- 주석 / UI 문구 언어 : 한국어. 기존 한국어 주석 위에 영어 주석을 추가하지 않는다
- 함수 최대 길이 : 40줄. 초과 시 `src/lib/` 로 함수를 분리한다
- 타입 정의 위치 : 공용 타입은 `src/types.ts`, 컴포넌트 전용 props 는 해당 `.tsx` 파일 상단 `interface Props`

---

## 작업 유의사항

- 데이터 출처 : `public/data/*.json` 을 `fetch` 로만 읽는다. 차량 값·집계 결과를 코드에 하드코딩하지 않는다
- 기준 시각 처리 : 경과시간은 `minutesSince(iso, asOf)` 로 계산한다. 현재 시각(`new Date()` · `Date.now()`)을 판정에 사용하지 않는다
- 알람 임계값 정의 위치 : `src/config/thresholds.ts` (없으면 생성). SOC 임계값 `SOC_LOW_PCT`, 무신호 임계값 `STALE_MINUTES` 로 export
- 판정 로직 변경 시 함께 확인할 화면 : `lib/alarms.ts` · `components/VehicleTable.tsx` · `components/DetailPanel.tsx` · `components/KpiCards.tsx` — 4곳 모두 확인 후 결과를 보고
- 작업 완료 전 실행할 검증 명령 : `npm run build` (통과 필수) + `grep -rn "soc_pct <\|minutesSince(" src --include=*.tsx` (컴포넌트에 판정식이 남아 있지 않은지 확인)

---

## ✅ Do

| # | 규칙 |
| --- | --- |
| 1 | 판정 임계값은 `src/config/thresholds.ts` 에만 정의하고, 다른 파일은 해당 상수를 `import` 해서 사용한다 |
| 2 | 알람 여부·심각도는 `lib/alarms.ts` 의 `evaluateAlarms()` 반환값으로만 판단한다 (화면에서 SOC·경과분을 직접 비교하지 않는다) |
| 3 | 상태 코드 → 한글 라벨 매핑은 `src/config/labels.ts` 한 곳에만 정의하고, 목록·필터칩·상세 패널이 모두 이 매핑을 사용한다 |
| 4 | 상태값을 추가하면 같은 커밋에서 `types.ts` 의 union · 라벨 매핑 · `index.css` 의 `.status--*` 규칙을 함께 추가한다 |
| 5 | 변경 후 `npm run build` 를 실행하고, 통과 여부와 수정한 파일 목록을 보고한다 |

## ❌ Don't

| # | 규칙 |
| --- | --- |
| 1 | `index.html` · CSS · 소스에 외부 URL(CDN)을 추가하지 않는다 |
| 2 | `package.json` 에 의존성을 추가하지 않는다 (필요하면 추가 전에 먼저 묻는다) |
| 3 | 요청 범위 밖의 파일을 수정하지 않는다 — 파일 이동·이름 변경·구조 리팩터·기존 컬럼 삭제 금지 |
| 4 | 판정 기준 숫자(`15` · `20` · `30`)를 컴포넌트나 `lib` 에 직접 쓰지 않는다 |
| 5 | 요구되지 않은 기능·컬럼·KPI 카드를 추가하지 않는다 |

---

## 자가 점검

| 질문 | ☑️ |
| --- | --- |
| 모든 규칙이 **참/거짓 판정 가능**한가 | ☑️ (파일 경로 · 명령 · 숫자로 표현) |
| 판정 불가한 모호어가 0개인가 | ☑️ 0개 |
| 도메인 용어를 모르는 사람도 이해되는가 | ☑️ SOC · DTC · 텔레메트리 · `as_of` 정의 |
| 규칙이 10개 내외인가 | ☑️ Do 5 + Don't 5 = 10개 |
| LAB 에서 본 위반이 **전부 규칙으로 막히는가** | ☑️ 임계값 산재(Do1) · 일부 파일만 수정(유의사항·Do5) · 영어 주석(컨벤션) · 임의 리팩터(Don't3) · 검증 생략(Do5) |
