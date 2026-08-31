# 지금 뜨는 스킬들 — 둘러보기용 목록

> 전부 **실존 GitHub 레포**입니다. ★(스타) 수는 **2026-08-31 기준 실측**이며 계속 변합니다.
> 사내망에서 github.com 접속이 막혀 있을 수 있습니다. **이 문서만 읽어도 되도록** 내용을 요약해 두었습니다.

---

## 0. 이 폴더에 이미 들어있는 스킬

| 스킬 | 위치 | 하는 일 | 뜯어볼 포인트 |
| --- | --- | --- | --- |
| `prd-creator` | `skills/prd-creator/` | 브리프 → PRD 문서 | ⬜ 빈칸 스텁 — **무엇을 채워야** 스킬이 되나 |
| `grill-me` | `skills/grill-me/` | 계획·아이디어를 집요하게 심문 | 절차(라운드)를 어떻게 지시했나 |
| `skill-creator` | `skills/skill-creator/` | 스킬을 만들고 개선·평가 | 스킬이 스킬을 만든다 |
| `caveman` | `skills/caveman/` | 원시인 말투로 답변 강제 → 출력 토큰 절감 | **SKILL.md 한 장**으로 10만 스타 |
| `eli5` | `skills/eli5/` | 다섯 살에게 설명하듯 쉬운 말로 | 톤·형식만 바꾸는 초경량 스킬 |

> `caveman` 의 토큰 절감률(65%)은 **제작자 자체 측정치**입니다. 제3자 재현 검증은 없습니다.
> 레포 전체는 Go·TS 모노레포(26MB)지만, **실제 동작에 필요한 건 `SKILL.md` 한 장**입니다.

---

## 1. 스킬 생태계의 원점 — 여기서부터 찾으면 된다

| 레포 | ★ | 내용 |
| --- | --- | --- |
| `anthropics/skills` | 172.7k | Anthropic 공식 Agent Skills. `skill-creator`, `docx`·`pptx`·`xlsx`·`pdf`, `mcp-builder`, `artifacts-builder` |
| `obra/superpowers` | 279.8k | `grill-me` 의 원본. 에이전트 스킬 프레임워크 + 개발 방법론 |
| `ComposioHQ/awesome-claude-skills` | 74.1k | 스킬 큐레이션 인덱스 |
| `VoltAgent/awesome-agent-skills` | 33.4k | 1000+ 스킬. Codex · Cursor · Gemini CLI 호환 |
| `hesreallyhim/awesome-claude-code` | 53.3k | Claude Code 전반 리소스 모음 |

**연결점** — 이 폴더의 `skill-creator` 는 1행, `grill-me` 는 2행에서 왔습니다.

---

## 2. 화제성 — "스킬 한 장이 이렇게까지 된다"

| 스킬 | ★ | 핵심 | 참고 |
| --- | --- | --- | --- |
| `affaan-m/ECC` | 244.9k | 하네스 성능 최적화 종합 (스킬 · 메모리 · 보안 · 리서치) | 규모가 커서 통째로 쓰기보단 구경용 |
| `multica-ai/andrej-karpathy-skills` | 209.0k | Karpathy 의 LLM 코딩 함정 관찰 → CLAUDE.md 규칙화 | **3교시 CLAUDE.md 와 직결** |
| `JuliusBrussee/caveman` | 101.9k | 원시인 말투 강제 → 출력 토큰 절감 | 절감률은 자체 벤치마크 |
| `teamchong/pxpipe` | 7.3k | 텍스트 컨텍스트를 PNG 로 렌더 → 입력 토큰 절감 | 엄밀히는 로컬 프록시, 스킬 아님 |

---

## 3. SW 개발 실무

| 스킬 | ★ | 하는 일 | 오늘 교육과의 연결 |
| --- | --- | --- | --- |
| `Graphify-Labs/graphify` | 112.8k | 코드베이스·SQL 스키마·설정·PDF → 질의 가능한 지식그래프 | 5교시 레포 탐색 |
| `vercel-labs/agent-browser` | 41.6k | 에이전트용 브라우저 자동화 CLI | 6교시 Hooks · 회귀 테스트 |
| `zhaoxuya520/reverse-skill` | 32.4k | 리버스엔지니어링 · 인가된 모의침투 라우터 팩 | 보안 리뷰 에이전트 |
| `mukul975/Anthropic-Cybersecurity-Skills` | 31.8k | 817개 보안 스킬. MITRE ATT&CK · NIST CSF 2.0 매핑 | 5교시 보안 리뷰 |
| `Nutlope/hallmark` | 27.6k | Anti-AI-slop 디자인 스킬. UI 결과물 품질 교정 | 3교시 DESIGN.md |
| `OthmanAdi/planning-with-files` | 26.5k | 파일 기반 영속 플래닝. `/clear`·compaction 이후 세션 복구 | 2교시 `/compact` |

**추천 조합** — `graphify` + `planning-with-files` : 컨텍스트 윈도우 한계를 스킬로 우회하는 사례.

---

## 4. 모빌리티 · 임베디드 — 우리 도메인

| 스킬 | ★ | 하는 일 |
| --- | --- | --- |
| `jherrodthomas/automotive-skills-suite` | 2.4k | 100+ 설치형 스킬. **ISO 26262 기능안전**, **ISO/SAE 21434 사이버보안** 등 |
| `zhinkgit/embeddedskills` | 608 | 임베디드 개발·디버깅 스킬. Claude Code · Copilot · TRAE 호환 |
| `agodianel/esp32-claude-workbench` | 78 | ESP32 펌웨어 개발용 결정적 워크플로 |

**여기서 볼 것** — 범용 스킬은 **10만 스타 단위**, 모빌리티 도메인은 **1천 스타 단위**입니다.
도메인 지식이 아직 스킬로 정리되지 않았다는 뜻이고, 사내 규격·설계 리뷰 기준을 스킬로 만들면 그대로 자산이 됩니다.

---

## 5. 스킬을 고를 때 확인할 것

| 확인 | 왜 |
| --- | --- |
| `SKILL.md` 를 **직접 열어봤는가** | 스타 수와 품질은 별개다 |
| `description` 에 **트리거 단어**가 있는가 | 없으면 자동 호출되지 않는다 |
| 성능 수치의 **출처**가 있는가 | 자체 측정치인 경우가 많다 |
| **라이선스** | 사내 배포 가능한 범위인지 (예 `caveman` 은 `skills/` 만 MIT) |
| 외부 네트워크·API 를 쓰는가 | 폐쇄망에서는 동작하지 않는다 |
