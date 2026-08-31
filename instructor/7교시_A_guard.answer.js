// 트랙 A : 위험 명령 차단 가드레일  (이벤트: PreToolUse) — 완성 예시
//
// 종료 코드 규약
//   0 : 통과
//   2 : 차단 (stderr 내용이 Claude 에게 전달된다)

const { readInput } = require('./_stdin')

// ── 1. 차단할 Bash 명령 패턴 ─────────────────────────────
const BASH_DENY = [
  { re: /\brm\s+-[a-zA-Z]*[rR][a-zA-Z]*f/,         why: '재귀 강제 삭제는 금지되어 있습니다.' },
  { re: /\bgit\s+push\b[^\n]*(--force\b|\s-f\b)/,  why: 'force push 는 원격 히스토리를 파괴합니다.' },
  { re: /\bgit\s+reset\s+--hard\b/,                why: 'hard reset 은 미커밋 작업을 소실시킵니다.' },
  { re: /\bsudo\b/,                                why: '권한 상승 명령은 허용되지 않습니다.' },
  { re: /\bcurl\b[^\n]*\|\s*(ba)?sh\b/,            why: '검증되지 않은 원격 스크립트 실행은 금지입니다.' },
  { re: /\b(DROP\s+(TABLE|DATABASE)|TRUNCATE)\b/i, why: 'DB 파괴성 DDL 은 훅에서 차단합니다.' },
  { re: /\b(npm\s+publish|docker\s+push)\b/,       why: '외부 배포는 사람이 직접 수행해야 합니다.' },
]

// ── 2. 차단할 파일 경로 패턴 (Read / Edit / Write 대상) ───
// mode : 'all'   → 읽기·쓰기 모두 차단
//        'write' → 쓰기(Edit / Write)만 차단, 읽기는 허용
const PATH_DENY = [
  { re: /(^|\/)\.env(\.[^/]*)?$/,                          mode: 'all',   why: '.env 파일에는 시크릿이 들어 있습니다.' },
  { re: /\.(pem|key|p12|pfx|keystore|jks)$/i,              mode: 'all',   why: '개인키 · 인증서 파일입니다.' },
  { re: /\/\.(ssh|aws|gcloud|kube)\//,                     mode: 'all',   why: '클라우드 · SSH 자격증명 디렉터리입니다.' },
  { re: /(credentials|secrets?|token)[^/]*\.(json|ya?ml|txt)$/i, mode: 'all', why: '자격증명 파일로 판단됩니다.' },
  { re: /\/\.claude\/settings[^/]*\.json$/,                mode: 'write', why: '훅 설정 자체를 수정하는 것은 금지입니다.' },
  { re: /\/\.git\//,                                       mode: 'write', why: 'Git 내부 파일 직접 수정은 금지입니다.' },
  { re: /(^|\/)(package-lock\.json|yarn\.lock|pnpm-lock\.yaml)$/, mode: 'write', why: '락파일은 패키지 매니저로만 갱신해야 합니다.' },
  { re: /\/(node_modules|dist|build)\//,                   mode: 'write', why: '의존성 · 빌드 산출물은 직접 수정 대상이 아닙니다.' },
]

// Bash 로 시크릿 파일을 우회 열람하는 것도 함께 막는다. (예: cat .env)
const SECRET_HINT = [
  /(^|[/\s'"])\.env(\.[^\s'"]*)?(\s|$|['"])/,
  /\.(pem|key|p12|pfx)(\s|$|['"])/i,
  /\/\.(ssh|aws)\//,
]

function deny(reason) {
  console.error(`[guard] 차단됨 — ${reason}`)
  process.exit(2)
}

// 도구별 검사 대상 경로를 뽑아낸다.
function targetPath(tool, ti) {
  if (tool === 'Read' || tool === 'Edit' || tool === 'Write' || tool === 'NotebookEdit') {
    return String(ti.file_path || ti.notebook_path || '')
  }
  return ''
}

;(async () => {
  const input = await readInput()
  const tool = input.tool_name || ''
  const ti = input.tool_input || {}

  // ① Bash 명령 검사
  if (tool === 'Bash') {
    const cmd = String(ti.command || '').replace(/\\/g, '/')
    for (const r of BASH_DENY) if (r.re.test(cmd)) deny(r.why)
    for (const re of SECRET_HINT) {
      if (re.test(cmd)) deny('명령문에 시크릿 파일 경로가 포함되어 있습니다.')
    }
  }

  // ② 파일 경로 검사 (윈도우 역슬래시를 슬래시로 정규화 후 매칭)
  const raw = targetPath(tool, ti)
  if (raw) {
    const path = raw.replace(/\\/g, '/')
    const isWrite = tool !== 'Read'
    for (const r of PATH_DENY) {
      if (r.mode === 'write' && !isWrite) continue
      if (r.re.test(path)) deny(`${r.why} (${raw})`)
    }
  }

  process.exit(0)
})()
