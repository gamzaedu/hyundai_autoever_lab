# LAB / Exercise 구성안

> - **LAB** : 수업 중 강사 주도 시연·따라하기
> - **exercise** : 교육생 자율 실습 (커리큘럼상 `실습`, 신입사원 퀘스트)
> - 도메인 소재 : 커넥티드카 / 차량관제 / EV 충전 / 스마트팩토리 (현대오토에버 개발직군 맥락)

---

## ⚙️ 공통 제약 (확정)

| 제약 | 실습 설계 반영 |
| --- | --- |
| 🚫 Opus 5 사용 불가 | Sonnet 5 기준 작업량 산정 |
| 🚫 MCP / Plugin 미사용 | 외부 연동 없음, 로컬 JSON 목데이터만 사용 |
| 🚫 Git 미사용 | 버전 복원은 `/rewind` 로 대체 (2·3교시 실습 소재로 활용) |
| ✅ npm / pip install | **허용** — 스택 자유 선택 가능 |
| 🚫 CDN | **전면 금지** — 모든 자산 로컬 번들. 전 교시 공통 규칙 |
| 🚫 외부 API 호출 | 금지 — 제공 JSON 만 사용 |
| 📐 난이도 | 개발직군 대상. 단일 HTML 수준 배제, 실행 가능한 앱 단위 |
| 🎯 통과율 목표 | 2교시 타임어택 기준 **약 50%** (Claude 경험자 다수 고려) |

---

## 🧭 LAB 전체 지도 — 무엇으로 하네스 원리를 보여줄 것인가

| 교시 | LAB | 실습 | 도메인 소재 | 🔑 전달할 원리 |
| --- | --- | --- | --- | --- |
| 1 | LAB_1-1 | 🔍 개발환경 신고식 | node/python/claude 버전 점검 → `env-check.md` | 에이전트가 **직접 명령을 실행**한다 |
| 1 | LAB_1-2 | 🚗 첫 데이터 만들기 | "업무차량 5대 목록 JSON 만들어줘" | 대화가 **파일 생성**으로 귀결 |
| 1 | LAB_1-3 | 📊 `/context` 첫 관람 | 방금 대화의 컨텍스트 점유율 확인 | 컨텍스트는 **유한한 자원** |
| 2 | LAB_2-1 | ⏮️ 타임머신 | 차량 목록 코드를 일부러 붕괴 → `/rewind` | Git 없이도 **체크포인트 복원** |
| 2 | LAB_2-2 | 🧹 컨텍스트 다이어트 | 5,000줄 텔레메트리 로그 투입 → 잔량 급감 → `/compact` vs `/clear` | **무엇을 버릴지**가 품질을 좌우 |
| 2 | LAB_2-3 | 🔁 세션 이어받기 | `/resume` 로 직전 작업 복귀 | 세션은 **자산** |
| 3 | LAB_3-1 | 🕳️ 하네스 없는 세상 | 빈 CLAUDE.md + CR-01 투입 → 임계값 산재·CDN·영어주석 | 지시는 **휘발**, 규칙은 **잔존** |
| 3 | LAB_3-2 | 🧭 하네스 5요소 지도 | CLAUDE.md·Skill·Tool·SubAgent·Hook 각 1분 시연 | 요소마다 **개입 시점**이 다름 |
| 3 | LAB_3-3 | ✍️ 규칙 추출 | LAB_3-1 위반 목록 → 규칙 문장 변환 | 좋은 규칙 = **검증 가능한 문장** |
| 4 | LAB_4-1 | 🩺 `dtc-explainer` 손코딩 | 진단코드 P0420·C1234 를 신입 눈높이로 해설 | Skill = **name + description + 지침** |
| 4 | LAB_4-2 | 🎣 description 함정 | description 부실 → 스킬 미호출 시연 | description 은 **트리거** |
| 4 | LAB_4-3 | 🛠️ skill-creator 로 개선 | LAB_4-1 결과물 리팩터 | 스킬이 **스킬을 만든다** |
| 4 | LAB_4-4 | 🔥 grill-me 맛보기 | 2교시 PRD 를 심문 | 스킬은 **검증에도** 쓰인다 |
| 5 | LAB_5-1 | 🏁 레포 탐색 대결 | fleet-console 레포를 단일 세션 vs 병렬 3 | 서브에이전트가 **컨텍스트를 대신 태움** |
| 5 | LAB_5-2 | 🎭 역할 부여 | 보안·성능·컨벤션 리뷰어 3종 정의 | **시야 제한**이 리뷰 품질을 올림 |
| 5 | LAB_5-3 | ⚖️ 실패 사례 | 충돌하는 지시로 결과 뒤엉킴 재현 | 오케스트레이션 **주의사항** |
| 6 | LAB_6-1 | 📓 작업일지 훅 | Stop → `worklog.md` 자동 append | Hook 은 **모델 판단 없이** 실행 |
| 6 | LAB_6-2 | 🧪 회귀테스트 훅 | Stop → lint/test → 실패 시 stdin 재투입 | **자가 수정 루프** |
| 6 | LAB_6-3 | 🛡️ 가드레일 훅 | `rm -rf` · `.env` 접근 차단 (PreToolUse) | 하네스의 **안전장치** |
| 7 | — | 🏗️ 캡스톤 | LAB 없음, 전 구간 자율 | 하네스 **총동원** |

---

## 1교시 : OT 및 초기 설정 (09:30~10:20)

### 🧑‍🏫 LAB (강사 시연)

| ID | 실습 | 핵심 장면 |
| --- | --- | --- |
| LAB_1-1 | 🔍 개발환경 신고식 | "이 PC 환경 점검해서 `env-check.md` 로 정리해줘" → Bash 실행 목격 |
| LAB_1-2 | 🚗 첫 데이터 만들기 | "업무차량 5대 목록 JSON" → 파일이 실제로 생성됨 |
| LAB_1-3 | 📊 `/context` 첫 관람 | `/status` · `/context` 화면 해석 |

### 🎮 exercise_1-1 「신입사원 퀘스트 1 : Hello Claude!」 (10분)

- 📄 산출물 : [QUEST_1.md](module_1/exercise/exercise_1-1/QUEST_1.md)
- 🧰 **스택 자유** (React / FastAPI / Express / Streamlit …) — 규격 미지정, 아이디어만 제시
- 💡 아이디어 6종 : 사원증 카드 · 모여모여 커뮤니티 · 명함첩 · 온보딩 체크리스트 · TIL 로그 · 점심 투표
- ✅ 성공 기준 : ① 로컬 기동 ② README 재현 ③ 저장→조회 1건
- 🚫 CDN 금지 / 외부 API 금지 (`npm`·`pip install` 은 허용)
- 🔍 관찰 포인트 : "같은 요구, 다른 결과" → 하루 전체의 문제의식

---

## 2교시 : 핵심 명령어 + PRD 타임어택 (10:30~11:20)

### 🧑‍🏫 LAB (강사 시연 + 따라하기)

| ID | 실습 | 핵심 장면 |
| --- | --- | --- |
| LAB_2-1 | ⏮️ 타임머신 | 잘못된 지시로 코드 붕괴 → `/rewind` 복구 |
| LAB_2-2 | 🧹 컨텍스트 다이어트 | 텔레메트리 로그 5,000줄 투입 → 잔량 급감 → `/compact` vs `/clear` 비교 |
| LAB_2-3 | 🔁 세션 이어받기 | `/resume` 로 직전 세션 복귀 |

### 🎮 exercise_2-1 「신입사원 퀘스트 2 : PRD 타임어택」 (20분, DDD)

- 📄 산출물 : [QUEST_2.md](module_2/exercise/exercise_2-1/QUEST_2.md) · [PRD](module_2/exercise/exercise_2-1/PRD_fleet_console.md)
- 🚗 데이터 : `vehicles.json` (30대) · `trips.json` · `alarm_cases.json` (정답지)

| 구분 | FR | 요구사항 | 배점 |
| --- | --- | --- | --- |
| 🟢 필수 | 01~04 | 목록 · 검색 · 상태필터 · KPI 4종 | 30 |
| 🟡 중요 | 05~07 | 상세패널 · **알람 판정** · 정렬 | 27 |
| 🔴 도전 | 08~10 | 텔레메트리 시뮬 · 알람 토스트/이력 · 반응형 | 23 |

- 🏁 **통과선 65점** — 필수+중요 완주 시 도달, 도전 과제는 상위권 변별용
- 💀 함정 4종 : `as_of` 기준시각 / 경계값 미포함 / ICE `soc_pct=null` / 차량 중복제거
- 🎯 난이도 목표 : **통과율 약 50%**

---

## 3교시 : CLAUDE.md (11:30~12:20)

> 🧩 **설계 원칙 : 2교시와 같은 코드, 같은 도메인, 작은 변경요구(CR) 3건.**
> 새 과제를 주지 않는 이유 — **동일 조건 대조군**이 있어야 CLAUDE.md 의 효과가 눈에 보임.

### 📦 출발점 통일 (제작 완료)

| 제공물 | 경로 | 내용 |
| --- | --- | --- |
| 📁 기준본 | `module_3/fleet-console-base/` | **React + Vite + TS**, FR-01~07 구현 (65점 수준). `node_modules` 포함 배포 → 즉시 `npm run dev` |
| 📄 변경요구서 | `module_3/CR_v1.1.md` | CR-01 · CR-02 · CR-03 |
| 🧑‍🏫 강사 가이드 | `module_3/LAB/LAB_3.md` | LAB_3-1~3-3 진행 스크립트 |
| 📝 템플릿 | `module_3/exercise/exercise_3-1/CLAUDE_template.md` | 빈칸 CLAUDE.md |
| 🚗 v1.1 데이터 | `fleet-console-base/public/data/vehicles_v11.json` | `CHARGING` 4대 포함 |

**⚙️ 기준본에 의도적으로 심은 구조 결함**

| 결함 | 위치 | 어느 CR 에서 터지나 |
| --- | --- | --- |
| SOC 임계값 `15` **3곳 산재** | `lib/alarms.ts` · `VehicleTable.tsx` · `DetailPanel.tsx` | CR-01 |
| 무신호 `30` **2곳 산재** | `lib/alarms.ts` · `VehicleTable.tsx` | CR-01 |
| 상태 라벨 **영어 직출력 3곳** | `VehicleTable` · `FilterBar` · `DetailPanel` | CR-02 |
| `DRIVING` 하드코딩 카운트 | `KpiCards.tsx` | CR-02 |

### 📝 변경요구서 v1.1 — 작지만 규칙이 없으면 무너지는 3건

| ID | 변경 내용 | 🕳️ 규칙 없을 때 터지는 지점 |
| --- | --- | --- |
| **CR-01** | 알람 임계값 정책 변경 (SOC 15%→20%, 무신호 30분→15분) | 임계값이 코드 3~4곳에 산재 → **일부만 수정, 화면마다 값 불일치** |
| **CR-02** | 상태 라벨 한글화 + 신규 상태 `CHARGING(충전중)` 추가 | 영어 라벨 잔존 · 신규 상태가 KPI '운행중'에 오집계 |
| **CR-03** | 목록에 '최근 통신 경과(분)' 컬럼 추가 + 임계 초과 강조 | 차트 넣는다며 **CDN 삽입** · 임의 전체 리팩터로 기존 기능 파손 |

### 🧑‍🏫 LAB (강사 시연)

| ID | 실습 | 핵심 장면 |
| --- | --- | --- |
| LAB_3-1 | 🕳️ 하네스 없는 세상 | **빈 CLAUDE.md** 상태로 CR-01 투입 → 위반 실황 중계 |
| LAB_3-2 | 🧭 하네스 5요소 지도 | CLAUDE.md · Skill · Tool · SubAgent · Hook 개입 시점 비교 |
| LAB_3-3 | ✍️ 규칙 추출 | LAB_3-1 에서 나온 위반 → 검증 가능한 규칙 문장으로 변환 |

### 🎮 exercise_3-1 「나만의 CLAUDE.md 채우기 + 동일 CR 재실행」 (10분)

- 📄 산출물 : [QUEST_3-1.md](module_3/exercise/exercise_3-1/QUEST_3-1.md) · [CLAUDE_template.md](module_3/exercise/exercise_3-1/CLAUDE_template.md)

| 단계 | 할 일 |
| --- | --- |
| 1️⃣ | `CLAUDE_template.md` 빈칸 채우기 (개요 · 스택 · 컨벤션 · 유의사항 · Do/Don't) |
| 2️⃣ | `/rewind` 로 CR-01 이전 상태 복원 |
| 3️⃣ | **완전히 동일한 프롬프트**로 CR-01 재실행 |
| 4️⃣ | Before / After 나란히 비교 |

**⚠️ 규칙 품질 기준 — 모호어 금지**

| ❌ 나쁜 규칙 | ✅ 좋은 규칙 |
| --- | --- |
| "깔끔하게 작성" | "함수 40줄 초과 금지" |
| "적절히 상수화" | "알람 임계값은 `config/thresholds` 한 곳에만 정의" |
| "최신 라이브러리 사용" | "CDN 링크 금지, 의존성은 `package.json` 에만 추가" |

### 🎮 exercise_3-2 「신입사원 퀘스트 3 : 규칙 준수 개발」 (10분)

- 📄 산출물 : [QUEST_3-2.md](module_3/exercise/exercise_3-2/QUEST_3-2.md) · [CR_v1.1.md](module_3/CR_v1.1.md)

- 🎯 미션 : **처음 보는 변경요구** CR-02 · CR-03 을 내 CLAUDE.md 상태로 수행 (통과선 70점)
- 🔑 검증 포인트 : 내 규칙이 **겪어보지 않은 작업에도 작동하는가**

| 채점 항목 | 배점 | 판정 |
| --- | --- | --- |
| CR-02 · CR-03 동작 | 40 | 기능 확인 |
| 내 CLAUDE.md 규칙 위반 0건 | 40 | 위반 1건당 −10 |
| CLAUDE.md 품질 | 20 | 모호어 1개당 −5 |

- 💡 **체감 포인트** : "매번 말로 지시" vs "한 번 규칙으로 고정" 의 누적 비용 차이

---


## 4교시 : Skills (14:00~14:50)

> 🧩 **설계 원칙 : 스킬은 "문서"가 아니라 "트리거"다.**
> description 한 줄이 호출 여부를 가른다는 것을 실패 장면으로 먼저 보여준 뒤 개선.

### 🧑‍🏫 LAB (강사 시연)

| ID | 실습 | ⏱️ | 소재 | 🔑 전달 원리 |
| --- | --- | --- | --- | --- |
| LAB_4-1 | 🩺 `dtc-explainer` 손코딩 | 10분 | 진단코드 P0420 · C1234 → 신입 눈높이 해설 | Skill = `name` + `description` + 지침 + `reference/` |
| LAB_4-2 | 🎣 description 함정 | (4-1 내 5분) | description "코드 설명" → **미호출** → 문구 교체 → 호출 | description 은 설명문이 아니라 **트리거** |
| LAB_4-3 | 🛠️ `skill-creator` 리팩터 | 10분 | LAB_4-1 결과물 투입 → 구조·트리거 개선 | 스킬이 **스킬을 만든다** |
| LAB_4-4 | 🔥 `grill-me` 맛보기 | 10분 | **2교시 PRD** 를 심문 → 허점 실황 | 스킬은 생성뿐 아니라 **검증**에도 쓰임 |

### 📦 제공물

| 경로 | 용도 | 상태 |
| --- | --- | --- |
| [LAB_4.md](module_4/LAB/LAB_4.md) | 강사 진행 가이드 | ✅ |
| `module_4/LAB/skills/dtc-explainer/` | 완성본 — `SKILL.md` + `reference/dtc_codes.md` | ✅ |
| `module_4/LAB/skills/dtc-explainer-bad/` | ❌ description 부실 버전 (LAB_4-2 전용) | ✅ |
| [QUEST_4.md](module_4/exercise/exercise_4-1/QUEST_4.md) | 퀘스트 문서 | ✅ |
| [CHARGER_BRIEF.md](module_4/exercise/exercise_4-1/CHARGER_BRIEF.md) | EV 충전기 예약 요구 브리프 | ✅ |
| `module_4/exercise/exercise_4-1/skills/prd-creator/` | ⬜ **스텁** — `description` · 지침 빈칸 | ✅ |
| `module_4/exercise/exercise_4-1/skills/grill-me/` | 🔶 **강사 배포** (Matt grill-me 한국어 번역본) | 자리만 |
| `skill-creator` | 🔶 **강사 배포** (Anthropic 배포본) | 자리 없음 |

### 🎮 exercise_4-1 「신입사원 퀘스트 4 : 내 스킬로 PRD 만들고 방어하기」 (10분)

- 🔋 **소재 : 사내 EV 충전기 예약 서비스** (신규 도메인 — 오후 환기용)

| 단계 | 할 일 | ⏱️ |
| --- | --- | --- |
| 1️⃣ | `prd-creator` **스텁 채우기** — `description` + 지침 (PRD 목차·필수 섹션·금지어) | 3분 |
| 2️⃣ | 내 스킬 호출 → `PRD_charger_v1.md` 생성 | 2분 |
| 3️⃣ | `grill-me` 로 심문 → 허점 리스트 확보 | 2분 |
| 4️⃣ | 지적 **3건 이상** 반영 → `PRD_charger_v2.md` | 3분 |

**🎯 성공 기준**

| # | 기준 |
| --- | --- |
| ① | 내 스킬이 **자동 호출**됨 (description 이 트리거로 작동) |
| ② | grill-me 지적 **3건 이상** v2 에 반영 |
| ③ | 반영 **거부 1건 + 사유** 기재 (맹종 방지) |

- ⏱️ **시간 방어 장치** : 스킬 폴더·frontmatter 골격은 제공. 교육생이 쓰는 것은 `description` 과 지침 본문뿐
- 💡 흥미 포인트 : "내 PRD 가 몇 대 맞았나" 라이브 집계

---

## 5교시 : SubAgents (15:00~15:50)

### 🧑‍🏫 LAB (강사 시연)

| ID | 실습 | ⏱️ | 소재 | 🔑 전달 원리 |
| --- | --- | --- | --- | --- |
| LAB_5-1 | 🏁 레포 탐색 대결 | 10분 | `fleet-console-base` 를 ⓐ단일 세션 ⓑ병렬 3 으로 파악 | 서브에이전트가 **내 컨텍스트를 대신 태움** |
| LAB_5-2 | 🎭 역할 부여 | 10분 | `.claude/agents/` 에 보안·성능·컨벤션 3종 정의 | **시야 제한**이 리뷰 품질을 올림 |
| LAB_5-3 | ⚖️ 실패 사례 | (5-2 내 3분) | 3 에이전트에 **같은 파일 수정** 지시 → 결과 뒤엉킴 | 병렬은 **읽기에 강하고 쓰기에 약함** |

- 📊 LAB_5-1 비교 지표 : `/context` 잔량 · 소요 시간 · 요약 정확도

### 📦 제공물

| 경로 | 용도 | 상태 |
| --- | --- | --- |
| [LAB_5.md](module_5/LAB/LAB_5.md) | 강사 진행 가이드 | ✅ |
| [ANSWER_KEY.md](module_5/LAB/ANSWER_KEY.md) | 🔐 정답지 (강사 전용, 배포 금지) | ✅ |
| `module_5/LAB/agents/*.md` | 보안 · 성능 · 컨벤션 리뷰어 정의 3종 | ✅ |
| [QUEST_5.md](module_5/exercise/exercise_5-1/QUEST_5.md) | 퀘스트 문서 | ✅ |
| `module_5/exercise/exercise_5-1/agents/` | 교육생 배포용 정의 3종 (사본) | ✅ |
| `module_5/exercise/exercise_5-1/review-target/telemetry_api.py` | 🐍 결함 1~5 + 보너스 2종 | ✅ |
| `module_5/exercise/exercise_5-1/review-target/web/` | ⚛️ 결함 6~8 (fleet-console 스냅샷) | ✅ |

### 🎮 exercise_5-1 「신입사원 퀘스트 5 : 코드리뷰 3인 위원회」 (10분)

| 항목 | 내용 |
| --- | --- |
| 🎯 미션 | 보안 · 성능 · 컨벤션 3 에이전트 **병렬** 실행 → 통합 리포트 1장 |
| 📦 리뷰 대상 | ⓐ `telemetry_api.py` (신규, 백엔드) + ⓑ `fleet-console-base/src/` (3교시 레포) |
| 🐛 심어둔 결함 | **8종** (아래 배치표) |
| 📝 산출물 | `REVIEW.md` — 결함 / 심각도 / 파일:라인 / 수정안 |
| 🏆 채점 | 탐지 8점 + 통합 품질 2점 − 오탐 감점 |

**🐛 결함 배치 (교육생 비공개)**

| # | 결함 | 위치 | 담당 에이전트 |
| --- | --- | --- | --- |
| 1 | SQL 인젝션 | `telemetry_api.py` | 🔒 보안 |
| 2 | 하드코딩 시크릿 | `telemetry_api.py` | 🔒 보안 |
| 3 | 미검증 입력 | `telemetry_api.py` | 🔒 보안 |
| 4 | N+1 조회 | `telemetry_api.py` | ⚡ 성능 |
| 5 | 예외 삼킴 (`except: pass`) | `telemetry_api.py` | 🔒 보안 / ⚡ 성능 |
| 6 | 불필요 전체 재계산 | `fleet-console-base/src/` | ⚡ 성능 |
| 7 | 네이밍·매직넘버 위반 | `fleet-console-base/src/` | 📏 컨벤션 |
| 8 | 데드코드 | `fleet-console-base/src/` | 📏 컨벤션 |

- 🎉 흥미 포인트 : 실시간 스코어보드 **"8개 중 몇 개?"**
- ⚠️ 오탐 감점 존재 → "많이 찍기" 전략 차단

---

## 6교시 : Hooks (16:00~16:50)

> ⚙️ **훅 스크립트 언어 : Node.js 확정** (`.claude/hooks/*.js`)
> 사유 — Node 사전 설치 확정 · OS 셸 차이 무영향 · stdin JSON 파싱 최단.

### 🧑‍🏫 LAB (강사 시연)

| ID | 실습 | ⏱️ | 시점 | 🔑 전달 원리 |
| --- | --- | --- | --- | --- |
| LAB_6-1 | 📓 작업일지 훅 | 10분 | `Stop` | Hook 은 **모델 판단 없이 무조건** 실행 |
| LAB_6-2 | 🧪 회귀테스트 훅 | 10분 | `Stop` | 실패 결과 재투입 = **자가 수정 루프** |
| LAB_6-3 | 🛡️ 가드레일 훅 | (6-2 내 5분) | `PreToolUse` | 하네스의 **안전장치** (차단 = `exit 2`) |

- 🎬 LAB_6-2 결정타 : 일부러 타입 오류를 심음 → 훅이 잡음 → Claude 가 **스스로** 고침
- 🧱 대상 레포 : `fleet-console-base` (`npx tsc -b` 를 lint/test 로 사용)

### 📦 제공물

| 경로 | 용도 | 상태 |
| --- | --- | --- |
| [LAB_6.md](module_6/LAB/LAB_6.md) | 강사 진행 가이드 | ✅ |
| `module_6/LAB/hooks/worklog.js` | 📓 Stop — 작업일지 append | ✅ 실행 검증 |
| `module_6/LAB/hooks/regression.js` | 🧪 Stop — `npx tsc -b` → 실패 시 `exit 2` | ✅ 실행 검증 |
| `module_6/LAB/hooks/guard.js` | 🛡️ PreToolUse — 위험 명령·경로 차단 | ✅ 실행 검증 |
| `module_6/LAB/settings.example.json` | 훅 등록 예시 | ✅ |
| [QUEST_6.md](module_6/exercise/exercise_6-1/QUEST_6.md) | 퀘스트 문서 | ✅ |
| `module_6/exercise/exercise_6-1/hooks/{A,B,C}_*.js` | ⬜ 트랙별 스텁 3종 | ✅ |

### 🎮 exercise_6-1 「신입사원 퀘스트 6 : 나만의 훅」 (10분, 택1)

| 트랙 | 훅 | 시점 | 난이도 | 판정 방법 |
| --- | --- | --- | --- | --- |
| A | 🛡️ 위험 명령 차단 (`rm -rf` · `.env` 읽기) | `PreToolUse` | ⭐⭐ | 금지 명령 요청 → 차단 로그 |
| B | 📊 작업 통계 리포트 | `SessionEnd` | ⭐⭐ | 세션 종료 → 리포트 파일 생성 |
| C | 📓 Git 없이 쓰는 작업일지 | `Stop` | ⭐ | 응답 종료 → `worklog.md` append |

- ✅ 성공 기준 : ① 훅 **발동 장면** 화면 재현 ② 발동 산출물 파일 제출 ③ 훅 스크립트 제출

---

## 7교시 : 캡스톤 프로젝트 (17:00~17:50)

> 🧩 **설계 원칙 : 난이도가 아니라 하네스 활용도로 평가한다.**
> 배점 = 하네스 **65** : 기능 **25** : 발표 **10**

### 🧑‍🏫 강사 운영

- 📄 [GUIDE_7.md](module_7/LAB/GUIDE_7.md) — LAB 없음. 트랙 배정 · 순회 코칭 · 채점 · 총정리
- 🚨 **30분 시점 강제 전환** : "손 멈추세요" → 리뷰·훅 확인 단계

### 🎮 exercise_7-1 「캡스톤 : 하네스 총동원」 (40분 + 발표 3분)

- 📄 [QUEST_7.md](module_7/exercise/exercise_7-1/QUEST_7.md)
- 🧰 스택 **자유** · `fleet-console-base` 복사 출발 허용 · 오전·오후 산출물 **반입 허용**

**🗂️ 트랙 7종**

| 난이도 | 트랙 | 프로젝트 | 데이터 | 🔥 핵심 |
| --- | --- | --- | --- | --- |
| 🟢 하 | H1 | 🩺 [DTC 진단코드 사전](module_7/exercise/exercise_7-1/tracks/H1_dtc_dictionary/BRIEF.md) | 코드 60건 | 제조사 정의 코드 `null` 처리 |
| 🟢 하 | H2 | 📖 [신입 온보딩 용어집](module_7/exercise/exercise_7-1/tracks/H2_glossary/BRIEF.md) | 용어 36건 | 통합검색 · 연관 이동 |
| 🟢 하 | H3 | 🔌 [EV 충전소 현황판](module_7/exercise/exercise_7-1/tracks/H3_charger_board/BRIEF.md) | 충전기 8 · 세션 20 | 진행 세션 `null` 처리 |
| 🟢 하 | H4 | 📦 [차량 부품 재고](module_7/exercise/exercise_7-1/tracks/H4_parts_inventory/BRIEF.md) | 부품 80 · 차종 12 | 재고 부족 경계값 |
| 🟡 중 | M1 | 🔋 [EV 충전기 예약](module_7/exercise/exercise_7-1/tracks/M1_charger_reservation/BRIEF.md) | 충전기 8 · 예약 24 | **중복 예약 차단** |
| 🟡 중 | M2 | 🔧 [차량 정비 이력](module_7/exercise/exercise_7-1/tracks/M2_maintenance_history/BRIEF.md) | 이력 90 · 차량 30 | **지연 판정(거리+기간)** |
| 🟡 중 | M3 | 🏭 [스마트팩토리 모니터링](module_7/exercise/exercise_7-1/tracks/M3_factory_monitor/BRIEF.md) | 설비 12 · 실적 168 | **가동률 정의 통일** |

**🏆 채점표 (100점)**

| 영역 | 항목 | 배점 |
| --- | --- | --- |
| 🧰 하네스 65 | 📜 CLAUDE.md | 20 |
| | 🩺 Skill | 15 |
| | 🎭 SubAgent | 15 |
| | 🪝 Hook | 15 |
| ⚙️ 기능 25 | 필수 FR / 데이터 정확성 / 실행 가능성 | 15 / 5 / 5 |
| 🎤 발표 10 | 하네스 선택 이유 3분 | 10 |

- 📊 등급 : 85+ 🏆S / 70~84 ✅통과 / 50~69 🟡아쉬움 / ~49 🔁재도전

**📐 문서 분리 원칙**

| 문서 | 성격 | 담는 것 |
| --- | --- | --- |
| `BRIEF.md` | 실무 요구사항서 | 배경 · 사용자 · FR · 판정규칙 · 데이터명세 · NFR · 범위밖 |
| `QUEST_7.md` | 교육 문서 | 하네스 필수조건 · 시간배분 · 채점표 · 발표 · 체크리스트 |

**💀 트랙별 기대값 (채점 참고)**

| 트랙 | 기대값 |
| --- | --- |
| H3 | 이용 불가 **2대** (CH-04 고장 · CH-08 점검) |
| H4 | 부족 **17** · 소진 **3** · 단종 **12** |
| M2 | 지연 이력 **22건** · 지연 차량 **17대** |
| M3 | 이상 설비 **2기** (EQ-05 · EQ-06, 도장) |

---

## 🔗 교시 간 자산 재사용

| 교시 | 재사용 대상 | 방식 |
| --- | --- | --- |
| 4 | 2교시 `PRD_fleet_console.md` | LAB_4-4 grill-me 심문 대상 |
| 5 | `module_3/fleet-console-base/` | 병렬 탐색 + 리뷰 대상 |
| 6 | `module_3/fleet-console-base/` | 회귀테스트 훅 대상 |
| 7 | 하네스 4종 전부 | 캡스톤 필수 조건 (오전·오후 산출물 반입 허용) |
| 7 | 2교시 `vehicles`·`trips` | M2 트랙 데이터로 동봉 |
| 7 | `fleet-console-base` | 캡스톤 출발점으로 복사 허용 |

---

## ⚠️ 미검증 / 불확실 항목

| 항목 | 현재 상태 | 신뢰도 | 비고 |
| --- | --- | --- | --- |
| `grill-me` | 🔶 **강사 직접 배포** (Matt grill-me 한국어 번역본) | — | 제작 대상 아님 |
| `skill-creator` | 🔶 **강사 직접 배포** (Anthropic 배포본) | — | 마켓플레이스 접근 불가 → 폴더 복사 |
| 훅 스크립트 동작 | ✅ **로컬 실행 검증 완료** (stdin JSON · exit 0/2 · 루프 가드) | 🟢 높음 | Node 단독 실행 기준 |
| 훅의 **세션 내 실제 발동** | ⚠️ 미검증 | 🟡 중간 | `.claude/settings.json` 등록 후 강사 PC 에서 리허설 필요 |
| 서브에이전트 정의 파일 스키마 | ⚠️ `name`·`description`·`tools` frontmatter 기준으로 작성 | 🟡 중간 | 강사 PC 버전에서 호출 확인 필요 |

---

## ✅ 확정 사항

| # | 항목 | 결정 |
| --- | --- | --- |
| 1 | 3교시 기준본 | **React + Vite + TS** 로 제작 완료 (빌드·기동 검증 완료) |
| 2 | 캡스톤 | `capstone_*` 분리 없이 `module_7/exercise` 로 운영 |
| 3 | data / docs | 모듈 레벨 `data`·`docs` 폴더 **삭제**. 각 실습 폴더 안에 동봉 |
| 4 | 망 정책 | `npm`·`pip install` 허용 / **CDN 전면 금지** |
| 5 | 2교시 난이도 | 통과선 65점, 통과율 목표 약 50% |
| 6 | 4교시 소재 | **사내 EV 충전기 예약 서비스** (신규 도메인) |
| 7 | 4교시 범위 | 교육생 **자기 스킬 1개 제작 포함** — 단, 폴더·frontmatter 골격은 제공 |
| 8 | 5교시 리뷰 대상 | `telemetry_api.py` (신규) **+** `fleet-console-base` 레포 동시 제공 |
| 9 | 6교시 훅 언어 | **Node.js** (`.claude/hooks/*.js`) |
| 10 | 캡스톤 트랙 | 난이도 하 4종(H1~H4) + 중 3종(M1~M3) = **7트랙** |
| 11 | 캡스톤 스택 | **자유** + `fleet-console-base` 복사 허용 |
| 12 | BRIEF 상세도 | **2교시 PRD 수준** (FR 상세 + 데이터 명세) |
| 13 | 캡스톤 데이터 함정 | **현실적 결측만** (`null` · 빈 배열). 경계값 함정 없음 |
| 14 | 캡스톤 배점 | 하네스 **65** : 기능 **25** : 발표 **10** |
