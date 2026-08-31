@echo off
chcp 65001 >nul
REM Fleet Console 개발 서버 실행 스크립트 (Windows)
REM 사용법: 파일을 더블클릭하거나 cmd 에서 start-server.bat 실행

REM 스크립트가 있는 폴더로 이동 (어디서 실행해도 동작)
cd /d "%~dp0"

echo ========================================
echo   Fleet Console - 개발 서버 시작
echo ========================================
echo.

REM 1) Node.js 설치 확인
where node >nul 2>nul
if errorlevel 1 (
    echo [오류] Node.js 가 설치되어 있지 않습니다.
    echo        https://nodejs.org 에서 LTS 버전을 설치한 뒤 다시 실행하세요.
    echo.
    pause
    exit /b 1
)

for /f "delims=" %%v in ('node -v') do set NODE_VER=%%v
echo [1/3] Node.js %NODE_VER% 확인 완료

REM 2) 의존성 설치 (node_modules 가 없을 때만)
if not exist "node_modules" (
    echo [2/3] 의존성 설치 중... ^(최초 1회, 1~2분 소요^)
    call npm install
    if errorlevel 1 (
        echo [오류] npm install 실패
        pause
        exit /b 1
    )
) else (
    echo [2/3] 의존성 이미 설치됨 - 건너뜀
)

REM 3) 개발 서버 실행
echo [3/3] 개발 서버 실행 - http://localhost:5173
echo       종료하려면 Ctrl + C
echo.
call npm run dev

REM 서버가 종료되면 창이 바로 닫히지 않도록 대기
echo.
echo 서버가 종료되었습니다.
pause
