// 📓 트랙 C : Git 없이 쓰는 작업일지  (이벤트: Stop)
// ⬜ 표시된 곳을 채우세요.

const fs = require('fs')
const path = require('path')
const { readInput } = require('./_stdin')

function stamp() {
  const d = new Date()
  const p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`
}

// ⬜ transcript(JSONL) 에서 "이번 턴에 어떤 파일이 바뀌었는지" 를 뽑아보세요.
//    힌트 : assistant 메시지 content 배열의 { type:'tool_use', name:'Edit'|'Write' } 블록에서
//           input.file_path 를 모으면 된다.
function changedFiles(transcriptPath) {
  // ⬜
  return []
}

;(async () => {
  const input = await readInput()
  const cwd = input.cwd || process.cwd()
  const file = path.join(cwd, 'worklog.md')

  if (!fs.existsSync(file)) {
    // ⬜ 헤더(표 머리글)를 먼저 쓰세요.
  }

  // ⬜ 시각 / 변경 파일 목록 을 한 행으로 append 하세요.

  console.log('[worklog] 기록 완료')
  process.exit(0)
})()
