#!/usr/bin/env bash
# Fleet Console 개발 서버 실행 스크립트 (macOS / Linux)
# 사용법:  ./start-server.sh       (최초 1회: chmod +x start-server.sh)

set -e

# 스크립트가 있는 폴더를 기준으로 실행 (어디서 실행해도 동작)
cd "$(dirname "$0")"

echo "========================================"
echo "  Fleet Console - 개발 서버 시작"
echo "========================================"
echo

# 1) Node.js 설치 확인
if ! command -v node >/dev/null 2>&1; then
  echo "[오류] Node.js 가 설치되어 있지 않습니다."
  echo "       https://nodejs.org 에서 LTS 버전을 설치한 뒤 다시 실행하세요."
  exit 1
fi

echo "[1/3] Node.js $(node -v) / npm $(npm -v) 확인 완료"

# 2) 의존성 설치 (node_modules 가 없을 때만)
if [ ! -d "node_modules" ]; then
  echo "[2/3] 의존성 설치 중... (최초 1회, 1~2분 소요)"
  npm install
else
  echo "[2/3] 의존성 이미 설치됨 - 건너뜀"
fi

# 3) 개발 서버 실행
echo "[3/3] 개발 서버 실행 → http://localhost:5173"
echo "      종료하려면 Ctrl + C"
echo
npm run dev
