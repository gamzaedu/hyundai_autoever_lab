# 🚗 Hyundai AutoEver — Claude Code 실무 교육 (1일 과정)

> 커넥티드카 · 차량관제 · EV 충전 도메인을 소재로 **에이전트 하네스(Agent Harness)** 를 직접 만들어 보는 7교시 실습 과정 교보재 저장소.

| 항목 | 내용 |
| --- | --- |
| 🎯 대상 | 현대오토에버 개발직군 |
| ⏱️ 분량 | 1일 · 7교시 (09:30~17:50) |
| 🧰 스택 | Node.js 18+ · Python 3.12/3.13 · React + Vite + TypeScript |
| 🧠 모델 | Claude Sonnet 5 기준 (Opus 5 미사용 전제) |
| 📦 저장소 성격 | **교보재** — 강사 가이드(LAB) + 교육생 과제(exercise) |

---

## 🗺️ 커리큘럼 한눈에 보기

| 교시 | 주제 | LAB (강사 시연) | exercise (교육생 실습) |
| --- | --- | --- | --- |
| 1 | OT · 초기 설정 | 개발환경 신고식 · 첫 데이터 · `/context` | 🎮 퀘스트 1 — Hello Claude! |
| 2 | 핵심 명령어 | `/rewind` · `/compact` · `/resume` | 🎮 퀘스트 2 — PRD 타임어택 |
| 3 | **CLAUDE.md** | 하네스 없는 세상 → 규칙 추출 | 🎮 퀘스트 3 — 규칙 준수 개발 |
| 4 | **Skills** | `dtc-explainer` 손코딩 · description 함정 | 🎮 퀘스트 4 — 내 스킬로 PRD 방어 |
| 5 | **SubAgents** | 레포 탐색 대결 · 역할 부여 | 🎮 퀘스트 5 — 코드리뷰 3인 위원회 |
| 6 | **Hooks** | 작업일지 · 회귀테스트 · 가드레일 | 🎮 퀘스트 6 — 나만의 훅 |
| 7 | 캡스톤 | — | 🏗️ 하네스 총동원 프로젝트 |

📄 전체 설계 근거 → [LAB_EXERCISE_PLAN.md](LAB_EXERCISE_PLAN.md) · 원본 시간표 → [curriculum.md](curriculum.md)

---

## 🧭 하네스 5요소 — 이 교육이 가르치는 것

에이전트에게 **"잘 부탁하는 법"** 이 아니라, **"부탁하지 않아도 되게 만드는 법"** 을 다룬다.

| 요소 | 개입 시점 | 이 저장소의 실물 |
| --- | --- | --- |
| 📜 **CLAUDE.md** | 세션 시작 (System Prompt) | [CLAUDE_template.md](module_3/exercise/exercise_3-1/CLAUDE_template.md) |
| 🧩 **Skills** | 모델이 필요하다고 판단할 때 | [skills/prd-creator/](module_4/exercise/exercise_4-1/skills/prd-creator/) |
| 🛠️ **Tools** | 도구 호출 시 | Bash · Read/Write (MCP 미사용) |
| 🤖 **SubAgents** | 작업 위임 시 | [agents/](module_5/LAB/agents/) — 보안 · 성능 · 컨벤션 |
| 🪝 **Hooks** | 모델 판단과 **무관하게** 무조건 | [hooks/](module_6/LAB/hooks/) — Stop · PreToolUse |

> 💡 핵심 대비 — **CLAUDE.md 는 "규칙"이고, Hook 은 "강제"다.** 앞의 4개는 모델이 따를 수도, 안 따를 수도 있다. 훅만이 결정론적으로 실행된다.

---

## 📁 저장소 구조

```
Hyundai_Autoever/
├─ CLAUDE.md                  이 저장소 작업용 프로젝트 지침
├─ curriculum.md              원본 시간표 (교시별 블록)
├─ LAB_EXERCISE_PLAN.md       전체 실습 설계안 (근거 · 채점 · 미검증 항목)
│
├─ module_1/  OT · 초기 설정
│  └─ exercise/exercise_1-1/  QUEST_1.md
│
├─ module_2/  핵심 명령어 · PRD 타임어택
│  └─ exercise/exercise_2-1/  QUEST_2.md · PRD_fleet_console.md
│     └─ data/                vehicles.json(30대) · trips.json · alarm_cases.json(정답지)
│
├─ module_3/  CLAUDE.md
│  ├─ LAB/                    LAB_3.md · CR_v1.1.md (변경요구서)
│  ├─ LAB_3_baseline/         🚗 fleet-console 기준본 (React+Vite+TS, FR-01~07)
│  └─ exercise/               3-1 CLAUDE.md 채우기 · 3-2 규칙 준수 개발
│
├─ module_4/  Skills
│  └─ exercise/exercise_4-1/  QUEST_4.md · CHARGER_BRIEF.md · skills/
│
├─ module_5/  SubAgents
│  ├─ LAB/                    LAB_5.md · ANSWER_KEY.md 🔐 · agents/
│  └─ exercise/exercise_5-1/  review-target/ (결함 8종 매설)
│
├─ module_6/  Hooks
│  ├─ LAB/                    LAB_6.md · hooks/ · settings.example.json
│  └─ exercise/exercise_6-1/  hooks/{A,B,C}_*.js (트랙별 스텁)
│
└─ module_7/  캡스톤 (자율 · 사전 제공물 없음)
```

---

## 🚀 빠른 시작

### 1️⃣ 사전 준비

| 도구 | 버전 | 확인 |
| --- | --- | --- |
| Node.js | 18 이상 | `node -v` |
| Python | 3.12 / 3.13 | `python --version` |
| VS Code | 최신 | + Claude 확장 |
| Claude Code | 최신 | `claude --version` |

### 2️⃣ 3교시 기준본 기동

```bash
cd module_3/LAB_3_baseline
npm install
npm run dev          # → http://localhost:5173
```

> 📦 `node_modules` 는 저장소에 포함되지 않는다. 교육 당일 오프라인 환경이라면 강사가 별도 배포한 의존성 압축본을 사용할 것.

### 3️⃣ 6교시 훅 적용

```bash
# 대상 프로젝트 루트에서
mkdir -p .claude/hooks
cp module_6/LAB/hooks/*.js            .claude/hooks/
cp module_6/LAB/settings.example.json .claude/settings.json
```

---

## ⚙️ 실습 공통 제약

| 제약 | 사유 |
| --- | --- |
| 🚫 **CDN 전면 금지** | 폐쇄망 가정. 모든 자산 로컬 번들 |
| 🚫 **외부 API 호출 금지** | 제공 JSON 목데이터만 사용 |
| 🚫 MCP · Plugin 미사용 | 교육 환경 단순화 |
| 🚫 Git 미사용 (실습 중) | 버전 복원은 `/rewind` 로 대체 — 2·3교시 실습 소재 |
| ✅ `npm install` · `pip install` | **허용** — 스택 자유 선택 |

> ⚠️ 위 "Git 미사용"은 **교육생 실습 환경**의 제약이다. 본 교보재 저장소 자체는 Git 으로 관리한다.

---

## 🔐 강사 전용 자료

| 파일 | 성격 |
| --- | --- |
| [module_5/LAB/ANSWER_KEY.md](module_5/LAB/ANSWER_KEY.md) | 결함 8종 정답지 — **교육생 배포 금지** |
| [module_2/.../alarm_cases.json](module_2/exercise/exercise_2-1/data/alarm_cases.json) | 알람 판정 정답 케이스 |
| `LAB_*.md` | 강사 진행 스크립트 (타임라인 · 대사 · 실패 대응) |

> 🚨 **저장소를 Public 으로 전환할 경우 위 파일들이 그대로 노출된다.** 교육 전 배포 시에는 Private 유지 또는 별도 브랜치 분리 필요.

---

## 📌 알려진 미완 항목

| 항목 | 상태 |
| --- | --- |
| `module_1/LAB/` · `module_4/LAB/` | 📁 폴더만 존재 — 가이드 문서 미작성 |
| `module_7/` | 📁 캡스톤 — 사전 제공물 없음 (설계상 의도) |
| `module_2/LAB/` | 폴더 없음 — LAB_2 가이드 미작성 |
| `skill-creator` · `grill-me` | 🔶 강사가 당일 직접 배포 (본 저장소 미포함) |
| 훅의 **세션 내 실제 발동** | ⚠️ 스크립트 단독 실행만 검증. 강사 PC 리허설 필요 |

---

## 📄 라이선스

사내 교육용 자료. 외부 배포 전 담당자 확인 필요.
