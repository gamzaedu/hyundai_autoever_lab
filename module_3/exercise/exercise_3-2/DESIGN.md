# DESIGN.md — Fleet Console

| 항목 | 값 |
| --- | --- |
| 🚗 **Product** | Fleet Console — 차량 관제 대시보드 |
| 🏢 **Brand** | 현대오토에버 (Hyundai AutoEver) |
| 🖥️ **Platform** | Web / Desktop-first (관제실 모니터) |
| 🌓 **Mode** | Dark only |
| 📐 **Spec** | Google Stitch `DESIGN.md` 5-Section 표준 |
| 📌 **기준 버전** | v1.0 (`src/index.css` 현행값 기술) |

> ⚠️ **이 문서는 현행 코드의 기술서(記述書)임.**
> §1~§5 는 이미 구현된 상태를 서술한 것이며, **소급 리팩터 대상이 아님**.
> 신규 추가 항목은 🆕 로 표시함.

---

## 1. Visual Theme & Atmosphere

- 🎛️ **관제실(Control Room) 미학** — 어두운 배경 위 데이터가 발광하는 구조
- 📊 **고밀도 정보 우선** — 여백보다 스캔 효율. 한 화면에 30대 동시 파악
- 🧊 **무채색 베이스 + 상태색 단독 발광** — 색은 "상태"일 때만 사용
- 🔇 **정상은 조용하게, 이상은 크게** — 무알람 차량은 무채색, 알람 차량만 채도 부여

| ✅ 지향 | ❌ 배제 |
| --- | --- |
| 밀도 높은 표 · 즉시 판독 | 넓은 히어로 · 마케팅 여백 |
| 상태색 = 판정 결과 | 장식 목적 색상 |
| 플랫 표면 + 1px 경계 | 그림자 · 입체 효과 · 그라디언트 |

---

## 2. Color Palette & Roles

### 🎨 CSS 변수 (`src/index.css` `:root`) — 유일한 색상 정의 지점

| 변수 | HEX | 색상명 | 역할 |
| --- | --- | --- | --- |
| `--bg` | `#0F1420` | ⬛ Console Black | 앱 최하단 배경 |
| `--panel` | `#171D2B` | 🌑 Panel Slate | 카드 · 테이블 · 패널 표면 |
| `--panel-2` | `#1E2536` | 🌘 Panel Raised | 행 호버 표면 |
| `--line` | `#2A3245` | ➖ Divider Line | 1px 경계선 |
| `--fg` | `#E6EBF5` | ⬜ Ice White | 본문 · 수치 |
| `--muted` | `#8C97AD` | 🔘 Muted Steel | 라벨 · 단위 · 메타 |
| `--accent` | `#4DA3FF` | 🩵 Accent Blue | 선택 상태 · 활성 칩 |
| `--danger` | `#FF5F6D` | 🔴 Alert Red | 위험 — 임계 초과 · CRITICAL |
| `--warn` | `#FFB547` | 🟠 Warn Amber | 주의 — 정비 · WARNING |
| `--ok` | `#35D07F` | 🟢 Normal Green | 정상 — 운행중 |
| 🆕 `--charging` | `#00AAD2` | 💠 Charging Cyan | **충전중** 상태 (Hyundai CI *Active Blue*) |

### 🆕 신규 색상 도입 규칙

- ✅ `--charging: #00AAD2` **1건만** 추가 허용 (CR-02 대응)
- 🚫 그 외 신규 HEX 도입 금지 — 필요 시 위 11개 토큰에서 선택
- 💡 `#00AAD2` 선정 근거 : 현대자동차 CI 전용색상 *Active Blue* / 정상 초록과 색상각 분리 / 대비 기준 충족

### ♿ 대비 실측 (WCAG 2.1)

| 조합 | 비율 | 판정 |
| --- | --- | --- |
| `--fg` on `--panel` | 14.09:1 | ✅ AAA |
| `--muted` on `--panel` | 5.73:1 | ✅ AA |
| `--danger` on `--panel` | 5.70:1 | ✅ AA |
| 🆕 `--charging` on 충전중 배지 배경 | 4.78:1 | ✅ AA |
| 알람 배지 CRITICAL (`#2b0308` on `--danger`) | 6.35:1 | ✅ AA |
| 활성 칩 (`#06121f` on `--accent`) | 7.18:1 | ✅ AAA |

- 🚫 신규 조합은 **4.5:1 이상**일 것

### 🏢 브랜드 앵커 — v1.x 미적용

| 색상 | HEX | 비고 |
| --- | --- | --- |
| Hyundai Blue | `#002C5F` | 🔒 v2.0 헤더·GNB 도입 예정 — **현 버전 사용 금지** |
| Autoever Blue | `#1472CF` | 🔒 v2.0 Primary 버튼 도입 예정 — **현 버전 사용 금지** |

---

## 3. Typography Rules

| 항목 | 규정 |
| --- | --- |
| 🔤 **Font** | `"Pretendard", "Malgun Gothic", system-ui, sans-serif` (`:root` 선언, 변경 금지) |
| 🔢 **수치** | `font-variant-numeric: tabular-nums` **필수** → `.mono` / `.num` 클래스 재사용 |
| 🌐 **언어** | UI 문구 · 주석 모두 **한국어**. 도메인 약어(SOC · DTC · VIN · AL-01)는 원문 유지 |

| 레벨 | 크기 / 굵기 | 적용처 |
| --- | --- | --- |
| 📰 H1 | 22px / 700 | 화면 타이틀 |
| 📌 H2 | 18px / 700 | 상세 패널 헤더 |
| 🔢 KPI Value | 26px / 700 | 지표 수치 |
| 📄 Table | 13px / 400 | 목록 셀 |
| 🏷️ Label | 11~12px / 400 | 라벨 · 단위 · 캡션 |
| 🚨 Badge | 11px / 700 | 알람 배지 |

- ❌ 이탤릭 금지 (수치 오독)
- ✅ 단위(`%`, `분`, `km`)는 `--muted` 로 수치와 분리

---

## 4. Component Stylings

> 📌 아래는 **현행 구현 상태**. 신규 요소는 이 패턴을 **복제**할 것.

### 🗂️ Card / Panel

| 속성 | 값 |
| --- | --- |
| 배경 / 보더 | `var(--panel)` / `1px solid var(--line)` |
| radius | **10px** |
| padding | `14px 16px` (KPI) · `16px` (상세) |
| 그림자 | 🚫 **없음** — 깊이는 표면 3단계로만 표현 |
| 위험 강조 | 보더만 `var(--danger)` 로 교체 (배경 유지) |

### 📋 Data Table

| 요소 | 값 |
| --- | --- |
| 본문 | 13px |
| `th` | padding `11px 12px` · `var(--muted)` · 600 · `nowrap` |
| `td` | padding `10px 12px` · 하단 `1px solid rgba(42,50,69,.55)` |
| Hover | 배경 `var(--panel-2)` |
| Selected | 배경 `rgba(77,163,255,.12)` |
| 수치 열 | `.num` — 우측 정렬 + tabular-nums |
| 정렬 헤더 | `.sortable` + ` ▲` / ` ▼` 접미 |

### 🏷️ Status Badge (`.status`)

| 속성 | 값 |
| --- | --- |
| 형태 | 11px · padding `3px 8px` · radius **5px** |
| 공식 | **배경 `rgba(색상, .16)` + 텍스트 `색상`** |

| 상태 | 클래스 | 색상 |
| --- | --- | --- |
| 🟢 운행중 | `.status--driving` | `var(--ok)` |
| ⚪ 정차 | `.status--idle` | `var(--muted)` |
| 🟠 정비필요 | `.status--maintenance` | `var(--warn)` |
| 🔴 오프라인 | `.status--offline` | `var(--danger)` |
| 🆕 💠 **충전중** | `.status--charging` | `var(--charging)` → 배경 `rgba(0,170,210,.16)` |

- ⚠️ 상태 5종은 **모두 스타일 정의 필수**. 미지정 상태 = 결함

### 🚨 Alarm Badge (`.badge`)

- 형태 : Pill radius `999px` · padding `2px 9px` · 11px / 700
- 배경 = 심각도 색, 텍스트 = **어두운 색** (`#2b0308` / `#2b1a03`)
- 표기 = 코드 나열이 아닌 **건수**
- 🚫 깜빡임 애니메이션 금지

### 🏷️ Filter Chip (`.chip`)

| 상태 | 값 |
| --- | --- |
| 기본 | 배경 `var(--panel)` · 보더 `var(--line)` · 텍스트 `var(--muted)` · radius `999px` · padding `6px 14px` · 12px |
| 활성 `.chip--on` | 배경·보더 `var(--accent)` · 텍스트 `#06121f` · 700 |

- ⚠️ 칩 라벨은 **상태 표시 라벨과 동일 문자열** 사용 (별도 매핑 금지)

### ⌨️ Input (`.search-input`)

- 배경 `var(--panel)` · 보더 `1px solid var(--line)` · radius **8px** · padding `9px 12px` · 14px

### 🔥 임계 초과 강조 (기존 패턴 재사용)

| 클래스 | 용도 | 스타일 |
| --- | --- | --- |
| `.soc--low` | SOC 임계 미만 | `color: var(--danger)` + 700 |
| `.stale` | 무신호 임계 초과 | `color: var(--danger)` |

- ✅ 🆕 `통신 경과(분)` 컬럼 강조는 **`.stale` 재사용** — 신규 클래스·신규 색 생성 금지
- 🚫 배경색 변경 · 보더 추가 금지 (텍스트 색상만)

---

## 5. Layout Principles

| 항목 | 값 |
| --- | --- |
| 📏 Max Width | `1440px` 중앙 정렬 |
| 🧭 Page Padding | `20px 24px 48px` |
| 📊 KPI Row | 4열 균등 grid · gap `12px` |
| 🧩 Main Split | `minmax(0, 1fr) 380px` · gap `16px` (목록 / 상세 고정폭) |
| 🧱 Spacing | 고정 스케일 없음 — **기존 컴포넌트 값을 복제**할 것 (신규 임의값 금지) |

### 📱 Breakpoint

| 구간 | 레이아웃 |
| --- | --- |
| 🖥️ ≥ 1000px | KPI 4열 + 목록/상세 2단 |
| 💻 < 1000px | KPI 2열 + 1단 세로 배치 |

- 🎯 **정보 밀도 우선** — 여백을 늘려 스크롤을 만들지 않음
- ⛔ 모바일 최적화 대상 아님 (관제실 전용)
- 🚫 컬럼 추가 시 `overflow-x: auto` 유지 (`.table-wrap` 기존 설정)

---

## 6. Agent 적용 규칙

| # | 규칙 |
| --- | --- |
| 1️⃣ | 색상은 §2 토큰만 사용. **신규 HEX 는 `--charging` 1건만 허용** |
| 2️⃣ | 색상은 `:root` 변수로 선언 후 `var()` 참조. 컴포넌트에 HEX 직접 기입 금지 |
| 3️⃣ | 신규 컴포넌트는 §4 기존 패턴을 **복제**. 새 스타일 창작 금지 |
| 4️⃣ | 색상은 **판정 결과(상태·알람·임계 초과)** 표현에만 사용 |
| 5️⃣ | 신규 색상 조합은 대비 **4.5:1 이상** |
| 6️⃣ | 외부 UI 라이브러리 · CDN · 아이콘 폰트 추가 금지 |
| 7️⃣ | 🔒 **기존 코드 소급 적용 금지** — 본 문서는 현행 상태 기술서. 요구 범위 밖 스타일은 그대로 둘 것 |

---

## 📚 Reference

| 출처 | 내용 |
| --- | --- |
| 💻 `src/index.css` | §2~§5 전체 — 현행 구현값 |
| 🎨 [현대자동차 CI 전용색상](https://www.hyundai.com/kr/ko/info/ci/ci-color) | Active Blue `#00AAD2`, Hyundai Blue `#002C5F` |
| 🌐 [hyundai-autoever.com](https://www.hyundai-autoever.com) | Autoever Blue `#1472CF`, Pretendard |
| 📐 [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | DESIGN.md 5-Section 표준 |
