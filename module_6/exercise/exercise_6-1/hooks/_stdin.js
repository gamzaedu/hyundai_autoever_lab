// 훅 공통 유틸 : stdin 으로 들어오는 JSON 을 읽는다.
// Claude Code 는 훅 프로세스의 stdin 으로 이벤트 JSON 을 흘려보낸다.

function readInput() {
  return new Promise((resolve) => {
    let buf = ''
    process.stdin.setEncoding('utf8')
    process.stdin.on('data', (c) => (buf += c))
    process.stdin.on('end', () => {
      try {
        resolve(JSON.parse(buf))
      } catch {
        resolve({}) // 파싱 실패해도 훅이 세션을 죽이지 않게 한다
      }
    })
    // stdin 이 아예 안 붙는 환경 대비
    setTimeout(() => resolve(buf ? safeParse(buf) : {}), 3000).unref?.()
  })
}

function safeParse(s) {
  try {
    return JSON.parse(s)
  } catch {
    return {}
  }
}

module.exports = { readInput }
