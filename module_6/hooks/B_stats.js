// 📊 트랙 B : 작업 통계 리포트  (이벤트: SessionEnd)
// ⬜ 표시된 곳을 채우세요.

const fs = require('fs')
const path = require('path')
const { readInput } = require('./_stdin')

// transcript(JSONL) 한 줄 = 대화 레코드 1건.
// rec.type 은 'user' | 'assistant' 등이며, 도구 사용은 assistant 메시지의
// content 배열 안에 { type: 'tool_use', name: '<도구명>' } 형태로 들어있다.
function analyze(transcriptPath) {
  const stat = { user: 0, assistant: 0, tools: {} }
  if (!transcriptPath || !fs.existsSync(transcriptPath)) return stat

  const lines = fs.readFileSync(transcriptPath, 'utf8').trim().split('\n')
  for (const line of lines) {
    let rec
    try {
      rec = JSON.parse(line)
    } catch {
      continue
    }

    // ⬜ rec.type 에 따라 stat.user / stat.assistant 를 세세요.

    // ⬜ assistant 메시지의 content 배열에서 tool_use 블록을 찾아
    //    stat.tools[블록.name] 카운트를 올리세요.
  }
  return stat
}

;(async () => {
  const input = await readInput()
  const cwd = input.cwd || process.cwd()
  const stat = analyze(input.transcript_path)

  // ⬜ 아래 리포트를 session_report.md 로 저장하세요.
  //    포함할 내용 : 종료 사유(input.reason) · 발화 수 · 도구별 호출 횟수 표
  const report = '⬜ 여기에 리포트 문자열을 만드세요'

  fs.writeFileSync(path.join(cwd, 'session_report.md'), report, 'utf8')
  console.log('[stats] session_report.md 생성 완료')
  process.exit(0)
})()
