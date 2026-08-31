```
- 시작시간 : 9시 반
- Opus 5 사용 불가

```

# 세팅

- Claude Code CLI 설치 (걔네가)
- MCP, Plugin, Git X
- Skill 은 미리 만들어 와서 공유
- 강사는 외부망 사용(교육생들은 사내망)
- cluade 구버전 사용자를 위해 cmd에서 `claude update` 로 업데이트 시키기
    - 터미널에서 `claude update` 로 클로드 코드 버전 업데이트 가능
        - (주의) 기존 클로드가 D드라이브에 있으면 C에 추가설치되어 충돌될 수 있음
            - 업데이트 후 claude 실행 시 명령어를 못찾으면
            - `where claude` 로 확인 : C드라이브 → D드라이브 순서라면 C를 비활성화 필요
            - `ren "C:\Users\...\claude" claude.old.exe` 로 비활성화
            - 새 터미널 열어서 `where claude` 로 D만 나오는지 확인

# 1교시 (09:30~10:20)  : OT 및 초기 설정

- [10분] 강사 소개 및 OT, Mattermost 접속, 교안 소개
- [15분] 이론 교육 - AI 시대, 개발자의 역할 전환 (ppt 31 page까지)
- [10분] VS Code 와 Claude UI 소개 (ppt 37 page까지)
    - **Python(3.13), Node.js, VS Code 및 Claude Code Extension 설치**
        - 네이티브로 Python + Node.js 설치
        (이번 교육에서는 클로드 코드가 이 둘을 사용하여 작업함)
            - **Python 설치** : https://www.python.org/downloads/
            (**설치파일로 설치시 : 시작부분에 PATH 포함 2군데 체크하고 설치**)
            - **node.js 설치** : https://nodejs.org/ko/download
            - **클로드 CLI 설치** : https://code.claude.com/docs/ko/quickstart
        - **(주의)** VS코드에 클로드 아이콘이 안보이면 VSCode 하단에 `Resricted  Mode(제한 모드)` → `Trust` 클릭하여 일반 모드로 변경해야 보임
        - 클로드 코드 확장 설치 시 바탕화면에 my_claude 폴더 생성 후 해당 폴더를 경로로 잡기
        **(경로 따로 안뜨면 채팅 세션에 잡아달라고 자연어 요청)**
- **[자체 실습] 간단한 앱 만들기**
    - 모델 : sonnet 5
    
    ```markdown
    **QUEST_1.md 참조**
    ```
    
    - 안내 포인트
        - 사내 환경에서 어떤것들이 제약이 있는지 확인
            - 기술 스택, 네트워크 제한 등
            - ex) 외부 API 사용금지, cdn 사용 금지 등
    - 실습 끝난 후 안내
        - 같은 아이디어인데 왜 옆자리랑 결과물이 다른지 생각해보기
            - 이 편차를 어떻게 통제할지가 오늘 하루의 주제

# 2교시 (10:30~11:20)

- [5분]  모델 & 추론
    - 모델을 좋은거 vs 추론을 MAX 뭐가 더 좋냐?
    - 케이스 케이스, 모델을 고정하고 추론을 바꿔 추천
- [15분] CLAUDE CODE 핵심 명령어 소개 (10개 이하)
    - `/resume` `/rewind` `/clear` `/compact` `/status` `/context`
    - 1교시에서 만든 내용으로 명령어 실행 보여주면 좋을듯
        1. 먼저 **rewind**로 이전 요청 전으로 되돌리기
        (작업 결과물도 되돌려짐, 번복 불가)
        2. config에서 여러 설정들을 변경할 수 있는데 **‘/config autoCompact=true’** 로 설정만 보여주기
        3. **clear**로 대화 세션 초기화(작업결과물은 그대로 있음)
        4. **resume**은 다른 대화로 넘어가기(CLI에서만 활용도가 있을듯)
- **[자체 실습] Data(trips.json, vehicles.json)와 간단한 개발 가이드를 주고 콘솔창 만들게 지시**
    - 처음부터 ‘**fleet_console.md’** 파일 넣어서 만들기
    - 교육생 실습 후 강사가 완성된 콘솔(exercies_3_baseline로 만든) 보여주고 PRD 기반으로 체계적으로 요청했다고 언급(지시나 규정을 고정해두는게 CLAUDE.md 파일이고 다음시간에 배울 내용!)
    
    ```markdown
    ### [Exercise 2] : Time Attack
    Claude Code 를 이용하여, 주어진 PRD 기반으로 미션을 수행합니다.  
    
    #### 첨부파일 설명
    | 파일 | 내용 |
    | --- | --- |
    | `PRD_fleet_console.md` | PRD + 기능요구서 + 채점표 |
    | `vehicles.json` | 차량 30대 스냅샷 (`as_of` 기준시각 포함) |
    | `trips.json` | 차량별 최근 주행 5건 |
    | `alarm_cases.json` | **자가채점 정답지** — **코드에서 참조 금지** |
    
    #### 미션 
    - 「커넥티드카 관제 콘솔 v1.0」 을 PRD 명세대로 구현
    - 스택 자유 · **CDN 금지** (`npm/pip install` 은 허용)
    - 20분 종료 시점의 **작동하는 상태**로 채점
    
    #### 전략 팁
    | 팁 | 내용 |
    | --- | --- |
    | :one: | PRD 를 **먼저 통째로 읽히기** — 요약 시키지 말 것 |
    | :two: | 필수(FR-01~04) 먼저 확보 후 중요 → 도전 순서로 |
    | :three: | 실제 데이터 30건이 화면에 뜨는지 **눈으로** 확인 |
    | :four: | 망가지면 처음부터 다시 말고 `/rewind` |
    | :five: | 컨텍스트가 부족하면 `/compact` (`/clear` 는 다 날아감) |
    | :six: | 세션을 하나 더 열면 병렬적으로도 진행 가능 |
    ```
    
- [5분] 결과 공유 및 하네스의 필요성
    - 20분 중 **재지시·수정**에 쓴 시간은 얼마인가
    - Claude 가 PRD 를 어긴 지점은 어디인가 (CDN · 하드코딩 · 시각 처리)
    - 같은 지시를 **매번 말로** 반복하지 않으려면?
        - (ex : CDN 은 쓰지마, 하드코딩 하지마)
        - 3교시 : CLAUDE.md 의 필요성

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
        - User Prompt, System Prompt 따로 있음
        - 200줄 이하로 작성 → 매 세션 대화에 반복적으로 들어감
- **[자체 실습] CLAUDE_template.md 파일의 공란을 먼저 작성하게 시킴**
    - CLAUDE_example.md 로 작성 가이드를 제공
    - exercies_3_baseline 파일 제공 후 이대로 콘솔 띄우기
- **[자체 실습] 띄워진 콘솔 내용을 FleetConsole_v1.1.md 로 작업 변경요구**
    - 변경 요구시 본인이 작성한 CLAUDE.md 파일 및 DESIGN.md 파일 참조 시키기
        - DESIGN.md 파일 설명
        
        ※ 오마이디자인에서 현대에서 만든 DESIGN.md 파일을 가져와서 폰트 변경 후 활용
        
    
    ```markdown
    ### [Exercise 3] : CLAUDE.md, DESIGN.md 기반 프로젝트 개발 
    제공한 프로젝트의 미구현 내용을 개발합니다. 
    CLAUDE.md, DESIGN.md 의 내용을 기반으로 개발할 때, 이전과 어떤 차이가 있는지 생각해보며 개발해 보세요.
    
    #### 첨부파일 설명
    | 파일 | 내용 |
    | --- | --- |
    | `PRD_fleet_console.md` | PRD + 기능요구서 + 채점표 |
    | `vehicles.json` | 차량 30대 스냅샷 (`as_of` 기준시각 포함) |
    | `trips.json` | 차량별 최근 주행 5건 |
    | `alarm_cases.json` | **자가채점 정답지** — **코드에서 참조 금지** |
    
    #### 미션 
    - 「커넥티드카 관제 콘솔 v1.0」 을 PRD 명세대로 구현
    - 스택 자유 · **CDN 금지** (`npm/pip install` 은 허용)
    - 20분 종료 시점의 **작동하는 상태**로 채점
    
    #### 전략 팁
    | 팁 | 내용 |
    | --- | --- |
    | :one: | PRD 를 **먼저 통째로 읽히기** — 요약 시키지 말 것 |
    | :two: | 필수(FR-01~04) 먼저 확보 후 중요 → 도전 순서로 |
    | :three: | 실제 데이터 30건이 화면에 뜨는지 **눈으로** 확인 |
    | :four: | 망가지면 처음부터 다시 말고 `/rewind` |
    | :five: | 컨텍스트가 부족하면 `/compact` (`/clear` 는 다 날아감) |
    | :six: | 세션을 하나 더 열면 병렬적으로도 진행 가능 |
    ```
    

# 4교시 (14:00~14:50) : Skills

※ https://artificialanalysis.ai/ : 모델 벤치마크 비교

※ https://arena.ai/ : LM Arena (모델 배틀)

- [10분] Skill 개요 및 구조
    - name | description | 지침 | reference |
- **[자체 실습] PRD 파일(prd-creater의 SKILL.md 파일) 공란 직접 작성**
- PRD 파일 강사와 함께 같이 작성
    
    ```
    내용은 기 작성된 내용 참조
    ```
    
- Skill-creator 를 이용하여 개선하기
    - **CLAUDE.md, skills, agents, hooks** 는 ‘**.claude 폴더’**에 들어가 있어야 동작함
    
    ```markdown
    /skill-creator 를 활용하여 /prd-creator 개선점을 검토해줘. 
    - ex) 현재 스킬에는 예시가 없어서 Few shot 추가
    
    -> 추가된 내용으로 스킬 개선해줘
    ```
    
- grill-me 이용해서 skill 다양하게 만들어보기, 현재 핫한 스킬들(Caveman)
    - grill-me, caveman, ELI5 등 스킬 파일을 제공 후 grill-me 활용
    
    ```markdown
    /grill-me
    직장에서 간단히 사용할 만한 재밌는 프로그램 (ex : 커피 메뉴 취합, 점심메뉴 룰렛 등) 만들어보려고 하는데, 어디서부터 시작해야 할지 모르겠어. 
    ```
    
    ```markdown
    # 심화 : 팀에 필요한 스킬 만들어봐라
    ```
    

# 5교시 (15:00~15:50)  : SubAgents

- [20분] 컨텍스트 윈도우와 멀티 에이전트의 필요성, 멀티에이전트 오케스트레이션 (병렬)
- **[자체 실습] 에이전트 하나 짜보기 : simple-code-reviewer**
    - 실습 agent 파일들은 아직 넣어 놓지 않기(agents 폴더의 3개)
    
    ```markdown
    /grill-me 
    사내에서 활용할 리서치 에이전트를 md 파일로 정의해두고 싶어. 어디에서부터 시작하면 좋을까?
    - 활용 툴 : Claude Code 서브에이전트
    
    -> 위 내용들을 묶어서, 현재작업 폴더에 `simple-code-reviewer` 에이전트 파일로 만들어줘.
    ```
    
- [10분] 멀티에이전트 주의사항, 꿀팁, 도구사용
    - tdd → 예를들어, TDD 에서 테스트 코드 작성 에이전트가 리뷰까지 같이 하게되거나, 통과 코드까지 같이 작성하게 되면 치팅이 발생하는 경우가 많다.
    - 리뷰같은 경우는 역할과 책임을 분리해 주는 것이 좋다.
    - 사람도 업무의 복잡도에 따라~
- [자체실습] 신입사원 퀘스트 5 : 에이전트 오케스트레이션
    
    ```markdown
    # 작업 디렉토리
    module_5\review-target
    
    # 과제
    서브에이전트 3개를 모두 활용하여, 컨벤션 / 성능 / 보안 리뷰를 진행하려고 해. 
    서브에이전트 활용 계획을 세워줘.
    ```
    
    ```markdown
    위 계획대로 진행하며, 리뷰 결과는 html 파일로 만들어서 전달해줘
    ```
    
    주의사항
    
    컨텍스트 윈도우를 효율적으로 사용하려고 나온건데, 서브에이전트가 프로젝트 디렉토리를 다 읽음
    
    → 오히려 비용이 더 발생하는 문제가 생길 수 있음
    
    → 아직도 계속 발전중인 분야
    

# 6교시 (16:00~16:50)  : Hooks

- [10분] Hooks 개념 및 라이프사이클
    - CLAUDE.md : 자연어로 지침을 정리(확률적)
    - Hooks : 코드로 결정론적인 실행을 정리(결정적)
        - CLAUDE 가 결정 X
        - 클로드 질의응답 사이클 : https://code.claude.com/docs/en/hooks
- [10분] 활용 예시 : 토큰사용 모니터링, 로그 만들기
    - 훅 만들기
        - A_guard(공란 파일) 로 아래 프롬프트 실행
        
        ```markdown
        해당 훅에서, 차단할 명령어와 차단할 파일 경로 추천해줘
        
        위 내용으로, 예시 완성 훅 작성해줘
        ```
        
    - settings.json 에 등록하기
        
        ```
        settings.json 에 훅을 등록해줘
        ```
        
    - .env 읽어오는지 테스트
        - .env 예시 (.env 파일은 module_6 바로 하위에 넣기)
        
        ```markdown
        CLAUDE_SECRET="클로드야 보면안돼"
        MY_SECRET="되는지 안되는지 테스트"
        ```
        
        ```markdown
        .env 에 있는 MY_SECRET 내용 읽어줘.
        ```
        
- [프로젝트 설명]

# 7교시 (17:00~17:50)  : 프로젝트

- [10분]
- [10분]
- [10분]
- [10분]
- [10분]