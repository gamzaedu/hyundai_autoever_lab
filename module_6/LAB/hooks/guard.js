// 🛡️ LAB_6-3 : 가드레일 훅  (이벤트: PreToolUse)
// 도구가 실행되기 "전에" 끼어들어 위험한 호출을 차단한다.
// exit 2 = 차단. stderr 내용이 Claude 에게 전달된다.

const { readInput } = require('./_stdin')

const BASH_DENY = [
  { re: /\brm\s+(-[a-zA-Z]*\s+)*-[a-zA-Z]*[rR][a-zA-Z]*f|\brm\s+-fr\b/, why: '재귀 강제 삭제(rm -rf) 는 금지되어 있습니다.' },
  { re: /\b(git\s+push\s+.*--force|git\s+reset\s+--hard)\b/, why: '되돌릴 수 없는 git 명령은 금지되어 있습니다.' },
  { re: /(^|\s)(>|>>)\s*\.env\b/, why: '.env 파일 쓰기는 금지되어 있습니다.' },
  { re: /\b(curl|wget|Invoke-WebRequest)\b/, why: '외부 네트워크 호출은 금지되어 있습니다. (CDN·외부 API 금지 규칙)' },
]

const PATH_DENY = [
  { re: /(^|[\/])\.env(\.|$)/, why: '.env 파일 접근은 금지되어 있습니다.' },
  { re: /(^|[\/])(id_rsa|id_ed25519|\.npmrc|credentials)$/, why: '인증정보 파일 접근은 금지되어 있습니다.' },
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

  if (['Read', 'Edit', 'Write', 'NotebookEdit'].includes(tool)) {
    const p = String(ti.file_path || ti.notebook_path || '')
    for (const r of PATH_DENY) if (r.re.test(p)) deny(r.why)
  }

  process.exit(0) // 통과
})()
