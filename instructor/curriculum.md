```jsx
- 시작시간 : 9시 반
- Opus 5 사용 불가

```

# 세팅

- VS Code 설치 : https://code.visualstudio.com/
    - Claude Extension 설치
- Claude Code 설치 (걔네가)
- Python + Node.js
    - 3.12 or 3.13
    - Extension 으로 깔지 Native 로 깔지 테스트 해보기
- MCP, Plugin X
- Git X
- Skill 은 미리 만들어 와서 공유
- 강사 외부망

# 1교시 (09:30~10:20)  : OT 및 초기 설정

- [5분] 강사 소개 및 OT
- [10분] Mattermost 접속, 교안 소개
- [15분] AI 시대, 개발자의 역할 전환
- [10분] VS Code 와 Claude UI 소개
- **[10분 | 실습]** 신입사원 퀘스트 1 : Hello Claude!

# 2교시 (10:30~11:20)

- [5분]  모델 & 추론
- [15분] CLAUDE CODE 핵심 명령어 소개 (10개 이하)
    - `/resume` `/rewind` `/clear` `/compact`
    - `/status` `/context`
- **[20분 | 실습]** 신입사원 퀘스트 2 : 제한 시간 내에 프로젝트 완성하기  (타임어택)
    - DDD (Dopamine Driven Development)
- [5분] 결과 공유 및 하네스의 필요성

# 3교시 (11:30~12:20) : CLAUDE.md

- [10분] 에이전트 하네스 개요
    - CLAUDE.md (System Prompt)
    - Skills
        - name, description, 지침, reference
    - Tools (MCP)
        - Bash, Powershell, Python
        - MCP : API - Notion, Obisidian
            - email 서버 - get_email, send_email, delete_email
            - MCP 서버 :
    - SubAgent
        - backend-reviewer.md
        - 멀티 에이전트 오케스트레이션
    - Hooks
        - 작업 끝 → npm lint, npm test →  에러 → stdin → 이어서 작업
    - 가드레일, 샌드박스, ……….
- [10분] CLAUDE.md
    - 들어가야 하는 내용들
        - 개요, 코딩컨벤션, 작업 유의사항, Do, Don’t
- [10분 | 실습] 나만의 CLAUDE.md 커스터마이징
    - Claude Code 껍데기를 주고, 빈칸 채워넣고 테스트 해보기
    - ex) cdn, 외부 api 호출,
- [10분] CLAUDE.md 작성 유의사항 및 Design.md 소개
- **[10분 | 실습]** 신입사원 퀘스트 3 : ex) 차량 상태 조회 대시보드

# 4교시 (14:00~14:50) : Skills

- [10분] Skill 개요 및 구조
- [10분] 직접 작성 (ex : prd-creator, simple-code-creator 등… 생각해보기 )
- [10분] Skill-creator 를 이용하여 개선하기
- [10분] 유명한 스킬들 : Grill-me 등
- [10분 | 실습] 신입사원 퀘스트 4 : grill-me 이용해서 skill , PRD 만들어보기

# 5교시 (15:00~15:50)  : SubAgents

- [10분] 컨텍스트 윈도우와 멀티 에이전트의 필요성
    - ex) 레포 탐색
- [10분] 멀티에이전트 오케스트레이션 (병렬)
- [10분] 역할 부여 : review agent, secure review agent,
- [10분] 멀티에이전트 주의사항, 꿀팁, 도구사용
- [10분 | 실습 ] 신입사원 퀘스트 5 : 에이전트 오케스트레이션

# 6교시 (16:00~16:50)  : Hooks

- [10분] Hooks 개념 및 라이프사이클
- [10분] 활용 예시 : 토큰사용 모니터링, 로그 만들기
- [10분] 회귀테스트 훅 : 클로드 작업 끝→ npm lint → npm test →  클로드 입력
- [10분] 신입사원 퀘스트 6 : Hooks 만들어보기
- [10분] 내용정리 및 다음시간 프로젝트 설명

# 7교시 (17:00~17:50)  : 프로젝트

- [40분] 캡스톤 프로젝트
- [10분] 마무리