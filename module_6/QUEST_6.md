#
| 파일 | 내용 |
| --- | --- |
| `hooks/_stdin.js` | ✅ 완성 — stdin JSON 읽기 (손대지 않아도 됨) |
| `hooks/A_guard.js` | ⬜ 트랙 A 스텁 |
| `hooks/B_stats.js` | ⬜ 트랙 B 스텁 |
| `hooks/C_worklog.js` | ⬜ 트랙 C 스텁 |

---

## ⏱️ 시간 배분 (권장)

| 구간 | 단계 |
| --- | --- |
| 0~1분 | 트랙 선택 + 파일 배치 |
| 1~3분 | `settings.json` 에 훅 등록 |
| 3~7분 | ⬜ 채우기 |
| 7~9분 | 발동시키기 |
| 9~10분 | 산출물 확인 |

---

## 1️⃣ 배치

```
<프로젝트>/
├─ .claude/
│  ├─ settings.json
│  └─ hooks/
│     ├─ _stdin.js
│     └─ <선택한 파일>.js
```

## 2️⃣ 등록 — `settings.json`

**트랙 A**
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash|Read|Edit|Write",
        "hooks": [{ "type": "command", "command": "node .claude/hooks/A_guard.js" }] }
    ]
  }
}
```

**트랙 B**
```json
{
  "hooks": {
    "SessionEnd": [
      { "hooks": [{ "type": "command", "command": "node .claude/hooks/B_stats.js" }] }
    ]
  }
}
```

**트랙 C**
```json
{
  "hooks": {
    "Stop": [
      { "hooks": [{ "type": "command", "command": "node .claude/hooks/C_worklog.js" }] }
    ]
  }
}
```

---

## 3️⃣ 채우기 — 트랙별 체크리스트

### 🛡️ 트랙 A

| ⬜ | 할 일 |
| --- | --- |
| 1 | `BASH_DENY` 에 차단 패턴 **2개 이상** 추가 |
| 2 | `PATH_DENY` 에 파일 경로 패턴 **1개 이상** 추가 |
| 3 | `Read`/`Edit`/`Write` 도구에 `PATH_DENY` 검사 로직 작성 |

> 💡 `tool_input` 의 파일 경로 필드명은 도구마다 다르다. (`file_path` 등)

### 📊 트랙 B

| ⬜ | 할 일 |
| --- | --- |
| 1 | `rec.type` 으로 user / assistant 발화 수 집계 |
| 2 | assistant content 배열에서 `tool_use` 블록 찾아 도구별 카운트 |
| 3 | 종료 사유 · 발화 수 · 도구 표를 마크다운으로 조립 |

### 📓 트랙 C

| ⬜ | 할 일 |
| --- | --- |
| 1 | `changedFiles()` 에서 `Edit`/`Write` 의 `file_path` 수집 |
| 2 | 파일이 없으면 표 헤더 먼저 생성 |
| 3 | `시각 / 변경 파일` 을 한 행으로 append |

---

## 4️⃣ 발동시키기

| 트랙 | 발동 방법 |
| --- | --- |
| A | 금지 명령을 일부러 요청 → **차단 메시지** 확인 |
| B | 세션 종료 (`/clear` 또는 종료) → 리포트 파일 확인 |
| C | 아무 파일이나 수정 요청 → `worklog.md` 확인 |

### 🧪 등록 없이 먼저 테스트하기 (권장)

훅을 세션에 붙이기 전에, **가짜 입력**으로 스크립트만 돌려볼 수 있다.

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf ./dist"},"cwd":"."}' | node .claude/hooks/A_guard.js
echo $?
```

| 기대 | 값 |
| --- | --- |
| 차단 | exit `2` + stderr 메시지 |
| 통과 | exit `0` |

> ⚡ **이 방법이 가장 빠르다.** 세션에 붙였다 뗐다 하지 말고 여기서 먼저 맞춰라.

---

## ✅ 성공 기준

| # | 기준 | 확인 |
| --- | --- | --- |
| ① | 훅이 **실제로 발동**하는 장면을 화면에서 재현 | ⬜ |
| ② | 발동 산출물(파일 또는 차단 메시지) 제출 | ⬜ |
| ③ | 훅 스크립트 제출 | ⬜ |
| ④ | "이 훅을 CLAUDE.md 로 대체할 수 없는 이유" 를 1문장으로 설명 | ⬜ |

---

## 💀 자주 나오는 실패

| 증상 | 원인 | 처방 |
| --- | --- | --- |
| 훅이 아예 안 돈다 | `settings.example.json` 그대로 둠 | **`settings.json`** 으로 이름 변경 |
| 훅이 안 돈다 (2) | 경로 오타 | 프로젝트 루트 기준 상대경로인지 확인 |
| `Cannot find module './_stdin'` | `_stdin.js` 미복사 | 같은 폴더에 함께 두기 |
| 세션이 멈춘다 / 반복된다 | `Stop` 훅에서 `exit 2` + 루프 가드 없음 | `input.stop_hook_active` 검사 추가 |
| 한글이 깨진다 | 파일 인코딩 | UTF-8 로 저장 |

---

## 🔍 회고 (30초)

- 내 훅은 **exit 0** 인가 **exit 2** 인가? 그 선택의 의미는?
- 이 규칙을 CLAUDE.md 에 썼다면 **몇 % 지켜졌을까**?
- 이 훅을 **과하게** 걸면 무엇이 불편해질까?

---

> 🔜 **다음 시간 예고 — 7교시 캡스톤**
> 📜 CLAUDE.md + 🩺 Skill + 🎭 SubAgent + 🪝 Hook **4종 전부**를 쓴다.
> 오늘 만든 것들을 **그대로 가져가도 된다.**
