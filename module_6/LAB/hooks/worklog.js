// 📓 LAB_6-1 : 작업일지 훅  (이벤트: Stop)
// 응답이 끝날 때마다 worklog.md 에 한 줄씩 append 한다.
// 모델이 "기록할지 말지" 판단하지 않는다. 무조건 실행된다.

const fs = require('fs')
const path = require('path')
const { readInput } = require('./_stdin')

function stamp() {
  const d = new Date()
  const p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`
}

// transcript(JSONL) 에서 마지막 사용자 발화를 뽑아 요약 대신 사용한다.
function lastUserText(transcriptPath) {
  try {
    if (!transcriptPath || !fs.existsSync(transcriptPath)) return '(transcript 없음)'
    const lines = fs.readFileSync(transcriptPath, 'utf8').trim().split('\n')
    for (let i = lines.length - 1; i >= 0; i--) {
      const rec = JSON.parse(lines[i])
      if (rec.type !== 'user') continue
      const c = rec.message && rec.message.content
      const text = typeof c === 'string' ? c : Array.isArray(c) ? (c.find((b) => b.type === 'text') || {}).text : ''
      if (text) return text.replace(/\s+/g, ' ').slice(0, 80)
    }
    return '(사용자 발화 없음)'
  } catch {
    return '(파싱 실패)'
  }
}

;(async () => {
  const input = await readInput()
  const cwd = input.cwd || process.cwd()
  const file = path.join(cwd, 'worklog.md')

  if (!fs.existsSync(file)) {
    fs.writeFileSync(file, '# 작업일지\n\n| 시각 | 세션 | 요청 |\n| --- | --- | --- |\n', 'utf8')
  }

  const sid = String(input.session_id || 'unknown').slice(0, 8)
  const req = lastUserText(input.transcript_path)
  fs.appendFileSync(file, `| ${stamp()} | \`${sid}\` | ${req} |\n`, 'utf8')

  console.log(`[worklog] appended -> ${file}`)
  process.exit(0) // 0 = 정상 종료. 세션 흐름에 개입하지 않는다.
})()
