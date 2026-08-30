// 🧪 LAB_6-2 : 회귀테스트 훅  (이벤트: Stop)
// 응답이 끝나면 타입체크를 돌린다. 실패하면 exit 2 로 에러를 Claude 에게 되돌린다.
// → Claude 가 "끝냈다" 고 판단한 시점에 강제로 검증이 끼어든다 = 자가 수정 루프

const { execSync } = require('child_process')
const { readInput } = require('./_stdin')

const CHECK_CMD = 'npx tsc -b'

;(async () => {
  const input = await readInput()

  // ⚠️ 무한 루프 방지 : 이 훅 때문에 재개된 세션이면 다시 검사하지 않는다.
  if (input.stop_hook_active) {
    console.log('[regression] skip (stop_hook_active)')
    process.exit(0)
  }

  try {
    execSync(CHECK_CMD, { cwd: input.cwd || process.cwd(), stdio: 'pipe', encoding: 'utf8' })
    console.log('[regression] PASS')
    process.exit(0)
  } catch (e) {
    const raw = `${e.stdout || ''}${e.stderr || ''}`.trim()
    const out = (raw || e.message || '알 수 없는 오류').split('\n').slice(0, 30).join('\n')
    // stderr 로 내보내고 exit 2 → Claude 에게 전달되어 이어서 작업하게 된다.
    console.error(`[regression] FAIL — 타입체크가 실패했습니다. 아래 오류를 수정하세요.\n\n${out}`)
    process.exit(2)
  }
})()
