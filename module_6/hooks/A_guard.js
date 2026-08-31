// 🛡️ 트랙 A : 위험 명령 차단 가드레일  (이벤트: PreToolUse)
// ⬜ 표시된 곳을 채우세요.

const { readInput } = require('./_stdin')

// ⬜ 차단할 Bash 명령 패턴을 추가하세요.
const BASH_DENY = [
  // 예시 1개만 제공. 최소 2개 더 추가할 것.
  { re: /\brm\s+-[a-zA-Z]*[rR][a-zA-Z]*f/, why: '재귀 강제 삭제는 금지되어 있습니다.' },
  // ⬜
  // ⬜
]

// ⬜ 차단할 파일 경로 패턴을 추가하세요. (Read / Edit / Write 대상)
const PATH_DENY = [
  // ⬜
]

function deny(reason) {
  console.error(`[guard] 차단됨 — ${reason}`)
  process.exit(2) // 2 = 차단. stderr 가 Claude 에게 전달된다.
}

;(async () => {
  const input = await readInput()
  const tool = input.tool_name || ''
  const ti = input.tool_input || {}

  if (tool === 'Bash') {
    const cmd = String(ti.command || '')
    for (const r of BASH_DENY) if (r.re.test(cmd)) deny(r.why)
  }

  // ⬜ Read / Edit / Write 도구에 대해 PATH_DENY 를 검사하세요.

  process.exit(0)
})()
