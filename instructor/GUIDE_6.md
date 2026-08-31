# 6교시 — Hooks

| 항목 | 내용 |
| --- | --- |
| 시각 | 16:00 ~ 16:50 (50분) |
| 주제 | 훅 라이프사이클 · 작업일지 · 회귀테스트 자가수정 루프 · 가드레일 |
| 학습목표 | ① Hook 은 **모델 판단과 무관하게 실행**된다는 것을 이해 ② `exit 2` = 차단·재투입 메커니즘 파악 ③ **규칙과 강제의 차이**로 하루를 완결 |
| 한 줄 메시지 | **"CLAUDE.md 는 규칙이고, Hook 은 강제다."** |

> **오늘의 결론이 나오는 교시.** 6교시 마지막 정리에서 하네스 5요소가 하나로 묶인다.

---

## 1. 타임라인

| 시각 | 분 | 블록 | 유형 | 사용 파일 |
| --- | --- | --- | --- | --- |
| 16:00 | 10 | B6-1 Hooks 개념 · 라이프사이클 | 강의 | `module_6/settings.example.json` |
| 16:10 | 10 | B6-2 작업일지 훅 (LAB_6-1) | 시연 | `worklog.js` (강사 자산) |
| 16:20 | 10 | B6-3 회귀테스트 훅 (LAB_6-2) + 가드레일 (LAB_6-3) | 시연 | `regression.js` · `guard.js` (강사 자산) |
| 16:30 | 10 | B6-4 퀘스트 6 | 실습 | `module_6/QUEST_6.md` · `hooks/` |
| 16:40 | 10 | B6-5 내용 정리 · 캡스톤 설명 | 강의 | `module_7/QUEST_7.md` |

---

## 2. 블록별 상세

### B6-1 · Hooks 개념 · 라이프사이클 (16:00~16:10 · 10분)

#### 1단계 — 문제 제기 (2분)

> "6교시 시작합니다. 오늘의 마지막 하네스입니다.
>
> 쉬는 시간에 던진 질문 이어가겠습니다.
>
> 여러분 오늘 CLAUDE.md 만드셨죠. 거기에 'CDN 금지' 쓰셨을 겁니다.
>
> 질문드리겠습니다. **그 규칙, 몇 % 지켜졌나요?**
>
> 100%는 아니었을 겁니다. 90%쯤? 그럼 나머지 10%는요? **여러분이 눈으로 잡아야 합니다.**
>
> 근데 못 잡으면요? **배포됩니다.**
>
> 여기가 오늘 마지막 하네스가 필요한 지점입니다."

**판서 — 하루의 결론이 되는 대비**

```
CLAUDE.md   "CDN 쓰지 마"          →  AI 가 판단해서 따름   →  가끔 어김
Skills      "이럴 땐 이렇게 해"      →  AI 가 부를지 결정     →  안 부를 수 있음
SubAgents   "너는 보안만 봐"        →  AI 가 띄울지 결정     →  안 띄울 수 있음
─────────────────────────────────────────────────────────────────────────
Hooks       조건이 맞으면            →  무조건 실행           →  못 어김
```

> "앞의 셋은 **부탁** 입니다. Hook 은 **장치** 입니다.
>
> 비유하자면, CLAUDE.md 는 **'안전벨트 매세요' 라는 안내방송** 이고, Hook 은 **안 매면 차가 안 나가는 인터록** 입니다."

#### 2단계 — 라이프사이클 (5분)

> "Hook 은 **특정 시점에 자동으로 실행되는 스크립트** 입니다. 시점이 정해져 있어요."

**판서**

```
시점                 언제                        주 용도
──────────────────────────────────────────────────────────────
UserPromptSubmit     내가 입력을 보낼 때          입력 검사 · 컨텍스트 주입
PreToolUse           도구를 쓰기 직전             ★ 차단 (가드레일)
PostToolUse          도구를 쓴 직후               포맷팅 · 로깅
Stop                 응답을 끝내려 할 때          ★ 검증 · 재작업 유도
SessionEnd           세션이 끝날 때               리포트 · 정리
```

> "오늘은 별표 두 개만 씁니다. **PreToolUse 와 Stop.**
>
> `PreToolUse` 는 **하기 전에** 막는 겁니다. `rm -rf` 실행하려는 걸 미리 차단.
>
> `Stop` 은 **끝내려 할 때** 붙잡는 겁니다. '잠깐, 테스트 돌리고 가.'"

#### 3단계 — 어떻게 만드나 (3분)

> "만드는 건 두 단계입니다. **스크립트 하나, 등록 하나.**
>
> 스크립트는 Node.js 로 씁니다. 왜 Node 냐면요. **여러분 PC에 이미 깔려 있고**, 윈도우든 맥이든 똑같이 돌고, JSON 파싱이 제일 쉽습니다."

**판서 — 동작 방식**

```
Claude  ──(이벤트 JSON)──▶  stdin  ──▶  내 스크립트
                                          │
                          exit 0  ◀───────┤  통과
                          exit 2  ◀───────┘  차단 + stderr 를 Claude 에게 전달
```

> "핵심은 **종료 코드** 입니다.
>
> `exit 0` 이면 그냥 통과합니다.
>
> **`exit 2` 면 차단됩니다.** 그리고 여러분이 `stderr` 에 쓴 메시지가 **Claude한테 전달됩니다.**
>
> 이게 왜 강력하냐면요. 단순히 막는 게 아니라 **'왜 막혔는지'를 알려주고 다시 시키는 것** 이기 때문입니다.
>
> 등록은 `settings.json` 에 합니다."

**화면 — `module_6/settings.example.json`**

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash|Read|Edit|Write",
        "hooks": [{ "type": "command", "command": "node .claude/hooks/guard.js" }] }
    ],
    "Stop": [
      { "hooks": [
          { "type": "command", "command": "node .claude/hooks/worklog.js" },
          { "type": "command", "command": "node .claude/hooks/regression.js" }
        ] }
    ]
  }
}
```

> "`matcher` 는 어떤 도구에 걸지입니다. `Stop` 은 도구가 없으니 matcher 가 없고요.
>
> 자, 만들어 보겠습니다."

---

### B6-2 · 작업일지 훅 (16:10~16:20 · 10분)

#### LAB_6-1 · `worklog.js` (Stop)

> "첫 번째는 가벼운 걸로 시작하겠습니다. **작업일지** 입니다.
>
> 오늘 우리 Git 안 썼죠. 그럼 뭘 언제 고쳤는지 어떻게 남기냐. 이걸로 남깁니다.
>
> Claude가 **응답을 끝낼 때마다**, 뭘 고쳤는지 자동으로 기록하는 겁니다."

**시연 코드 — `.claude/hooks/worklog.js`**

```javascript
// Stop 훅 — 응답이 끝날 때마다 변경 파일을 worklog.md 에 append
const fs = require('fs')
const path = require('path')
const { readInput } = require('./_stdin')

function stamp() {
  const d = new Date()
  const p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`
}

// transcript(JSONL) 에서 Edit/Write 로 건드린 파일 경로를 모은다
function changedFiles(transcriptPath) {
  if (!transcriptPath || !fs.existsSync(transcriptPath)) return []
  const files = new Set()
  for (const line of fs.readFileSync(transcriptPath, 'utf8').trim().split('\n')) {
    let rec
    try { rec = JSON.parse(line) } catch { continue }
    if (rec.type !== 'assistant') continue
    const content = rec.message?.content
    if (!Array.isArray(content)) continue
    for (const b of content) {
      if (b.type === 'tool_use' && (b.name === 'Edit' || b.name === 'Write')) {
        if (b.input?.file_path) files.add(path.basename(b.input.file_path))
      }
    }
  }
  return [...files]
}

;(async () => {
  const input = await readInput()
  const cwd = input.cwd || process.cwd()
  const file = path.join(cwd, 'worklog.md')

  if (!fs.existsSync(file)) {
    fs.writeFileSync(file, '# 작업일지\n\n| 시각 | 변경 파일 |\n| --- | --- |\n', 'utf8')
  }

  const files = changedFiles(input.transcript_path)
  fs.appendFileSync(file, `| ${stamp()} | ${files.join(', ') || '—'} |\n`, 'utf8')

  console.log('[worklog] 기록 완료')
  process.exit(0)
})()
```

> "등록하고 아무 작업이나 시켜보겠습니다."

**입력**

```
src/lib/format.ts 에 주석을 한 줄 추가해줘.
```

> "(완료 후 `worklog.md` 열기)
>
> 보세요. **제가 아무것도 안 했는데 파일이 생겼고, 기록이 들어갔습니다.**
>
> 여기서 중요한 건 이겁니다. 제가 Claude한테 **'작업일지 써줘' 라고 안 했습니다.**
>
> Claude가 '아 일지를 써야겠다' 고 판단한 것도 아닙니다.
>
> **그냥 응답이 끝났으니까 실행된 겁니다.** 이게 Hook 입니다.
>
> 한 번 더 시켜보겠습니다. (다른 작업) 또 쌓이죠. **매번 쌓입니다. 빠짐없이.**
>
> 활용 예시를 몇 개 말씀드리면요."

**판서**

```
Stop / PostToolUse 활용 예시
├─ 작업일지 자동 기록          ← 방금 본 것
├─ 토큰 사용량 모니터링         세션별 비용 추적
├─ 변경 파일 자동 포맷팅        prettier · black
└─ 세션 종료 리포트            SessionEnd
```

---

### B6-3 · 회귀테스트 훅 + 가드레일 (16:20~16:30 · 10분)

#### LAB_6-2 · `regression.js` (Stop) — 자가 수정 루프 (6분)

> "이제 **오늘의 결정타** 입니다.
>
> 아까 `exit 2` 얘기했죠. 차단하고, 이유를 Claude한테 전달한다고요.
>
> 이걸로 뭘 할 수 있냐면요. **작업이 끝날 때마다 타입체크를 돌리고, 실패하면 못 끝내게 하는 겁니다.**"

**시연 코드 — `.claude/hooks/regression.js`**

```javascript
// Stop 훅 — 응답 종료 시 타입체크. 실패하면 exit 2 로 Claude 에게 재작업 지시
const { execSync } = require('child_process')
const { readInput } = require('./_stdin')

;(async () => {
  const input = await readInput()

  // 무한 루프 방지 — 훅 때문에 재개된 턴에서는 다시 검사하지 않는다
  if (input.stop_hook_active) process.exit(0)

  try {
    execSync('npx tsc -b --pretty false', {
      cwd: input.cwd || process.cwd(),
      stdio: 'pipe',
      timeout: 120000,
    })
    console.log('[regression] 타입체크 통과')
    process.exit(0)
  } catch (e) {
    const out = `${e.stdout || ''}${e.stderr || ''}`.trim()
    console.error(`[regression] 타입체크 실패. 아래 오류를 수정한 뒤 다시 마무리할 것.\n\n${out.slice(0, 3000)}`)
    process.exit(2)
  }
})()
```

> "핵심이 두 군데입니다.
>
> 하나는 맨 위 **`stop_hook_active`** 검사입니다. 이게 없으면 어떻게 될까요? 훅이 막고, Claude가 고치고, 또 훅이 돌고. **무한 루프** 입니다. 반드시 넣으세요.
>
> 또 하나는 아래 **`exit 2` 와 `console.error`** 입니다. 종료를 막고, **오류 메시지를 그대로 Claude한테 던집니다.**
>
> 자, 이제 제가 **일부러 타입 오류를 심겠습니다.**"

**시연 — 의도적 오류 주입**

```
src/lib/format.ts 의 함수 반환 타입을 number 로 바꿔줘.
(실제로는 string 을 반환하는 함수 — 타입 오류 발생)
```

> "(응답이 끝나려는 순간 훅 발동)
>
> **보세요. 끝나려다가 붙잡혔습니다.**
>
> 아래 메시지 보이시죠. 타입 오류가 그대로 나왔습니다.
>
> 그리고 지금... **Claude가 스스로 고치고 있습니다.**
>
> 제가 아무 말도 안 했습니다. '고쳐줘' 라고 안 했어요. **훅이 오류를 던졌고, Claude가 받아서 고치는 겁니다.**
>
> (수정 완료 · 훅 재실행 · 통과)
>
> **통과했습니다. 이제 끝납니다.**
>
> 이걸 뭐라고 부르냐면요."

**판서**

```
자가 수정 루프 (Self-correcting loop)

  작업 종료 시도  →  Hook: 검증  →  실패  →  exit 2 + 오류 전달
                                              │
                        ┌─────────────────────┘
                        ▼
                    Claude 가 수정  →  다시 종료 시도  →  통과  →  끝
```

> "실무에서 이걸 붙이면 뭐가 달라지냐면요.
>
> **'AI가 짠 코드가 빌드가 안 되는' 상황이 사라집니다.** 빌드 안 되면 애초에 끝나질 않으니까요.
>
> lint, test, 뭐든 붙일 수 있습니다. **여러분 팀의 CI를 로컬로 당겨오는 겁니다.**"

#### LAB_6-3 · `guard.js` (PreToolUse) — 가드레일 (4분)

> "마지막으로 **안전장치** 입니다. 이건 반대 방향이에요. **하기 전에** 막습니다."

**시연 코드 — `.claude/hooks/guard.js`**

```javascript
// PreToolUse 훅 — 위험 명령·민감 경로 차단
const { readInput } = require('./_stdin')

const BASH_DENY = [
  { re: /\brm\s+-[a-zA-Z]*[rR][a-zA-Z]*f/, why: '재귀 강제 삭제는 금지되어 있습니다.' },
  { re: /\bgit\s+push\s+.*--force/,        why: '강제 푸시는 금지되어 있습니다.' },
  { re: /\bcurl\b|\bwget\b/,               why: '외부 네트워크 접근은 폐쇄망 정책상 금지입니다.' },
]

const PATH_DENY = [
  { re: /(^|[\\/])\.env(\.|$)/, why: '.env 파일 접근은 금지되어 있습니다.' },
  { re: /(^|[\\/])\.git[\\/]/,  why: '.git 내부 직접 조작은 금지되어 있습니다.' },
]

function deny(reason) {
  console.error(`[guard] 차단됨 — ${reason}`)
  process.exit(2)
}

;(async () => {
  const input = await readInput()
  const tool = input.tool_name || ''
  const ti = input.tool_input || {}

  if (tool === 'Bash') {
    const cmd = String(ti.command || '')
    for (const r of BASH_DENY) if (r.re.test(cmd)) deny(r.why)
  }

  if (tool === 'Read' || tool === 'Edit' || tool === 'Write') {
    const p = String(ti.file_path || '')
    for (const r of PATH_DENY) if (r.re.test(p)) deny(r.why)
  }

  process.exit(0)
})()
```

> "등록하고, **일부러 금지된 걸 시켜보겠습니다.**"

**입력**

```
dist 폴더를 rm -rf 로 지워줘.
```

> "(차단 메시지 확인)
>
> **막혔습니다.** 그리고 Claude가 '금지되어 있어서 다른 방법을 쓰겠다' 고 하죠.
>
> 하나 더 해보겠습니다."

**입력**

```
.env 파일 내용 좀 보여줘.
```

> "(차단)
>
> 여기서 중요한 관점 하나 드리겠습니다.
>
> 이걸 CLAUDE.md 에 **'`.env` 파일 읽지 마라'** 라고 쓸 수도 있습니다. 그리고 아마 **대부분 지켜집니다.**
>
> 그런데 **'대부분'** 이면 되나요? 시크릿이 새는 문제인데요.
>
> **CLAUDE.md 는 규칙이고, Hook 은 강제입니다.** 이 차이가 여기서 갈립니다.
>
> 판단 기준은 간단합니다."

**판서**

```
어겨도 되는 것 (품질 · 스타일)      →  CLAUDE.md
어기면 안 되는 것 (안전 · 검증)      →  Hook
```

---

### B6-4 · 퀘스트 6 (16:30~16:40 · 10분)

**배포** — `module_6/QUEST_6.md` · `module_6/hooks/` · `module_6/settings.example.json`

> "10분입니다. 트랙 세 개 중 **하나만** 고르세요."

**판서**

```
A  위험 명령 차단      PreToolUse    ⭐⭐    방금 본 guard 와 유사
B  세션 통계 리포트    SessionEnd    ⭐⭐    transcript 분석 필요
C  작업일지           Stop          ⭐      가장 쉬움
```

> "스텁을 드렸습니다. `⬜` 표시된 데만 채우시면 됩니다. `_stdin.js` 는 완성돼 있으니 손대지 마세요.
>
> **꿀팁 하나 드리겠습니다. 이게 제일 중요합니다.**
>
> 훅을 세션에 붙였다 뗐다 하면서 테스트하지 마세요. **시간 다 갑니다.**
>
> **가짜 입력을 넣어서 스크립트만 먼저 돌려보세요.**"

**화면 — 반드시 시연**

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf ./dist"},"cwd":"."}' | node .claude/hooks/A_guard.js
echo $?
```

> "이러면 **1초 만에** 됩니다. 차단되면 `2`, 통과면 `0` 이 찍힙니다.
>
> 여기서 먼저 맞춘 다음에 세션에 붙이세요.
>
> 성공 기준은 세 개입니다. **① 훅이 실제로 발동하는 장면 ② 발동 산출물 ③ 스크립트.**
>
> 그리고 마지막에 한 문장 적어주세요. **'이 훅을 CLAUDE.md 로 대체할 수 없는 이유.'**
>
> 시작하세요."

---

### B6-5 · 내용 정리 · 캡스톤 설명 (16:40~16:50 · 10분)

#### 1단계 — 하루 정리 (5분)

> "손 멈추세요. 오늘 하루를 정리하겠습니다.
>
> 아침에 제가 이렇게 말씀드렸죠. **오늘 배울 건 잘 부탁하는 법이 아니라, 부탁하지 않아도 되게 만드는 법이다.**
>
> 이제 그게 무슨 뜻인지 아실 겁니다."

**판서 — 하루 전체 (오늘 처음으로 5요소가 다 채워진 상태로 제시)**

```
요소            개입 시점              성격          강제력      우리가 만든 것
────────────────────────────────────────────────────────────────────────────
① CLAUDE.md     세션 시작 · 항상        규칙          약함        내 규칙 10개
② Skills        AI 가 판단할 때         조건부 지식    약함        prd-creator
③ Tools         도구 호출 시            실행 수단      —          Bash · Read/Write
④ SubAgents     작업 위임 시            분업          약함        리뷰어 3종
⑤ Hooks         무조건                  강제          강함        내 훅 1종
```

> "여기서 오늘의 결론이 나옵니다.
>
> **위로 갈수록 유연하고, 아래로 갈수록 확실합니다.**
>
> 그래서 실무에서는 이렇게 씁니다.
>
> **품질과 스타일은 CLAUDE.md 로.** 어겨도 큰일 안 납니다.
>
> **안전과 검증은 Hook 으로.** 어기면 사고입니다.
>
> 그리고 오늘 하루를 한 문장으로 남기면 이겁니다."

**판서 — 마지막 문장**

```
좋은 AI 사용자는 프롬프트를 잘 쓰는 사람이 아니라,
AI 가 실수할 수 없는 환경을 만드는 사람이다.
```

#### 2단계 — 캡스톤 설명 (5분)

> "마지막 7교시는 여러분이 직접 하네스를 설계하는 시간입니다.
>
> `QUEST_7.md` 열어주세요. 트랙이 **7개** 있습니다."

**판서**

```
🟢 하  H1 DTC 진단코드 사전    H2 온보딩 용어집
       H3 EV 충전소 현황판     H4 차량 부품 재고

🟡 중  M1 EV 충전기 예약  (중복 예약 차단)
       M2 차량 정비 이력  (지연 판정)
       M3 스마트팩토리    (가동률 정의 통일)
```

> "하나 고르시면 됩니다. **데이터는 제가 다 드립니다.**
>
> 그런데 **채점표를 먼저 보셔야 합니다.** 이게 오늘 교육의 핵심이거든요."

**판서 — 채점표**

```
하네스   65점    CLAUDE.md 20 · Skill 15 · SubAgent 15 · Hook 15
기능     25점    필수 FR 15 · 데이터 정확성 5 · 실행 가능성 5
발표     10점    하네스 선택 이유 3분
                ─────
                100점
```

> "보세요. **기능은 25점밖에 안 됩니다.**
>
> 화려하게 만드는 게 목표가 아닙니다. **하네스를 제대로 붙였는지가 65점** 입니다.
>
> 그래서 전략은 명확합니다. **하네스부터 붙이고 시작하세요.**
>
> 그리고 좋은 소식. **오늘 만든 거 전부 가져다 쓰셔도 됩니다.**
>
> 3교시 CLAUDE.md, 4교시 스킬, 5교시 리뷰어, 6교시 훅. 그대로 복사해서 쓰세요. **그러라고 만든 겁니다.**
>
> 난이도 하 트랙 네 개는 **하네스 조립에 집중** 하시라고 만든 거고요. 중 트랙 세 개는 판정 로직이 좀 있습니다.
>
> **처음 하시는 분은 무조건 '하' 트랙 고르세요.** 기능은 25점입니다.
>
> 10분 쉬고 시작하겠습니다."

---

## 3. 실습 운영

| 항목 | 내용 |
| --- | --- |
| 배포물 | `QUEST_6.md` · `hooks/{_stdin,A_guard,B_stats,C_worklog}.js` · `settings.example.json` |
| 시간 | 10분 |
| 방식 | 트랙 A/B/C 중 **택 1** |

### 트랙별 요구

| 트랙 | 이벤트 | 난이도 | 채워야 할 것 | 판정 |
| --- | --- | --- | --- | --- |
| A | `PreToolUse` | ⭐⭐ | `BASH_DENY` 2건+ · `PATH_DENY` 1건+ · 경로 검사 로직 | 금지 명령 요청 → 차단 로그 |
| B | `SessionEnd` | ⭐⭐ | 발화 수 집계 · `tool_use` 카운트 · 리포트 조립 | 세션 종료 → 리포트 파일 |
| C | `Stop` | ⭐ | `changedFiles()` · 헤더 생성 · append | 파일 수정 → `worklog.md` |

### 순회 코칭 포인트

| 관찰 상황 | 개입 |
| --- | --- |
| 훅을 붙였다 뗐다 반복 | **"가짜 입력으로 먼저 테스트하세요"** — `echo ... \| node ...` 시연 |
| 훅이 아예 안 돎 | "`settings.example.json` 을 **`settings.json`** 으로 이름 바꾸셨나요?" |
| `Cannot find module './_stdin'` | "`_stdin.js` 를 같은 폴더에 복사하세요" |
| 세션이 멈추거나 반복됨 | "`Stop` 훅에 **`stop_hook_active` 검사** 넣으세요" |
| 한글 깨짐 | "파일을 UTF-8 로 저장하세요" |
| B 트랙에서 transcript 구조를 못 찾음 | "assistant 메시지의 `content` 배열 안에 `tool_use` 블록이 있습니다" |
| 벌써 끝냄 | "훅을 **과하게** 걸면 뭐가 불편해질지 생각해보세요. 그것도 회고 항목입니다" |

---

## 4. 예상 질문

| 질문 | 답변 |
| --- | --- |
| "`exit 1` 은 뭔가요?" | "일반 오류입니다. 차단은 **`exit 2`** 만 됩니다. 이건 꼭 구분하세요" |
| "훅이 느리면 어떻게 되나요?" | "매 응답마다 기다리게 됩니다. **무거운 검사는 Stop 보다 SessionEnd** 로 빼세요" |
| "훅에서 오류가 나면 세션이 죽나요?" | "죽지는 않지만 불안정해집니다. `_stdin.js` 가 파싱 실패 시 빈 객체를 반환하는 이유가 그겁니다" |
| "Python 으로 써도 되나요?" | "됩니다. 오늘 Node 로 통일한 건 **전원 설치 확정** 이라서입니다" |
| "훅을 팀에 공유하려면요?" | "`.claude/settings.json` 과 `hooks/` 를 저장소에 커밋합니다. **팀 전체에 강제됩니다**" |
| "CLAUDE.md 랑 훅에 같은 규칙을 둘 다 쓰나요?" | "네, 권장합니다. **CLAUDE.md 로 알려주고, Hook 으로 막습니다.** 알려주면 애초에 시도를 덜 합니다" |
| "훅이 너무 많으면요?" | "느려지고, 개발이 답답해집니다. **어기면 사고나는 것만** 훅으로 만드세요" |

---

## 5. 실패 대응

| 증상 | 원인 | 처방 |
| --- | --- | --- |
| **훅이 세션에서 발동하지 않음** | 등록 경로 · 버전 차 | **최우선 리허설 항목.** 안 되면 스크립트 단독 실행(`echo \| node`)으로 시연을 전환하고, 발동 장면은 원리 설명으로 대체 |
| `npx tsc -b` 가 매우 느림 | 첫 빌드 | 사전에 1회 실행해 캐시 생성 |
| LAB_6-2 에서 Claude 가 안 고치고 그냥 끝냄 | 오류 전달 실패 | `console.error` 로 썼는지 확인. `console.log` 는 전달 안 됨 |
| LAB_6-2 가 무한 루프 | `stop_hook_active` 누락 | 즉시 훅 해제. **이 사고를 오히려 교보재로 활용** — "루프 가드가 왜 필요한지 방금 보셨습니다" |
| 다수가 훅 등록에서 막힘 | `settings.example.json` 파일명 | **전체 중단 후 1분 공통 안내** |
| 6교시가 지연 | — | **B6-3 의 가드레일(LAB_6-3) 절삭.** 단, **B6-5 정리는 절대 자르지 않는다** — 하루의 결론이다 |

---

## 6. 다음 교시 브릿지

> "10분 쉬고 마지막 7교시입니다.
>
> 트랙 미리 골라두세요. 쉬는 시간에 `QUEST_7.md` 랑 각 트랙의 `BRIEF.md` 훑어보시면 좋습니다.
>
> 그리고 다시 말씀드립니다. **오늘 만든 하네스를 그대로 가져다 쓰세요.**
>
> 마지막 40분은 새로 배우는 시간이 아닙니다. **오늘 배운 걸 전부 붙여보는 시간** 입니다."

---

## 7. 사전 준비 체크

| ☐ | 항목 |
| --- | --- |
| ☐ | **훅의 세션 내 실제 발동 리허설** — 🔴 최우선. 미검증 항목 |
| ☐ | `worklog.js` · `regression.js` · `guard.js` **3종 사전 작성 · 동작 확인** (저장소 미포함 — 본 가이드 코드는 **미검증**) |
| ☐ | `settings.example.json` 이 참조하는 파일명과 실제 파일명 일치 확인 |
| ☐ | LAB_6-2 용 **타입 오류 유발 프롬프트** 사전 확정 (확실히 오류가 나는 것으로) |
| ☐ | `npx tsc -b` 1회 사전 실행 (캐시 생성 · 소요시간 측정) |
| ☐ | 가짜 입력 테스트 명령 클립보드 등록 |
| ☐ | 하네스 5요소 종합표 판서 준비 (하루의 결론) |
| ☐ | `QUEST_7.md` · 트랙 7종 배포 준비 |

> **저장소 결손** — `module_6/hooks/` 에는 교육생용 스텁 3종(`A_guard.js` · `B_stats.js` · `C_worklog.js`)과 `_stdin.js` 만 있다. `settings.example.json` 이 참조하는 **`guard.js` · `worklog.js` · `regression.js` 완성본은 저장소에 없다.** 본 가이드에 실은 코드는 `_stdin.js` 인터페이스에 맞춰 작성한 것이며 **실행 검증되지 않았다.** 교육 전 강사 PC에서 반드시 동작을 확인하고 필요 시 수정할 것.
