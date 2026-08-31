# Hyundai Reference Design System

<!-- design-md:section experience -->
## 1. 경험 (Experience)

### 비주얼 테마 · 분위기

1967년 설립된 현대자동차는 현재 완성차 제조사이자 모빌리티 기업으로 스스로를 규정하며, 공식 연혁은 울산 조립공장에서 현재의 IONIQ 전기차에 이르는 전환 과정을 기록한다. 캡처된 한국어 제품 화면에서 이 광범위한 자동차 정체성은 절제된 인터페이스로 구현된다 — 흑백 텍스트, 딥 네이비 액션 컬러(`#002c5f`), 로드된 전용 폰트 패밀리(관측값). 문서화된 차량 디자인 방향성인 Sensuous Sportiness는 2018년 이후 현대의 디자인 철학이며, 감성적 매력을 구조·비례·스타일링·기술과 연결한다. 본 레퍼런스는 이 공식 차량 디자인 맥락과 웹 주장(claim)을 분리한다 — 즉, 캡처된 KR 제품 UI를 기술할 뿐, 범용 현대 디자인 시스템을 기술하지 않는다. 또한 관측된 전용 폰트는 재사용 라이선스가 확인되지 않으므로, 본 문서의 **적용 서체는 오픈 라이선스 폰트 Pretendard(SIL OFL 1.1)로 대체**한다(§3 폰트 대체 매핑).

제품 캡처는 반복 등장하는 네이비 차량 CTA에 대해 평면·직각 액션을 선호하나, radius가 0인 시스템은 아니다 — 선택된 캐러셀 컨트롤은 6px radius, 챗봇은 원형이다. 딥 네이비(`#002c5f`)는 반복 관측된 제품 액션 컬러이며, 틸(`#007fa8`)은 캡처된 캐러셀 컨트롤에, 시안(`#00aad2`)은 챗봇에 나타난다. 블랙(`#000000`), 화이트(`#ffffff`), 뮤트 그레이(`#999999`), 유틸리티 그레이(`#444444`), 다크 푸터(`#1c1b1b`) 역시 직접 관측된 값이다.

### Do · Don't

### Do

- 관측된 네이비 차량 액션은 동일한 제품 액션 패턴을 의도할 때만 사용.
- 서체는 오픈 라이선스 대체 폰트(Pretendard, SIL OFL 1.1)만 사용. 관측된 현대 전용 KR 폰트는 사용하지 않음.
- 본 레퍼런스 재사용 시 컴포넌트의 표면(surface)과 상태 경계 유지.

### Don't

- 틸·시안·원형 챗봇을 범용 액센트 또는 플로팅 액션 시스템으로 취급 ❌
- 대체 폰트를 Hyundai Sans 또는 HyundaiSans*로 표기 ❌
- 재사용 라이선스가 확인되지 않은 폰트 파일을 번들·배포 ❌
- 본 캡처로부터 hover·focus·disabled·폼 에러·반응형 변형을 임의 생성 ❌

### 브랜드 내러티브

현대자동차는 1967년 법인 설립되었으며, 공식 연혁은 1968년 울산 조립공장, 1976년 포니 출시, 그리고 현재의 모빌리티 솔루션 프로바이더로서의 위상을 기록한다. 2024년 마일스톤 기록은 이 역사를 현재의 IONIQ 전용 전기차 라인업으로 연결한다.

2018년 이후 현대는 Sensuous Sportiness를 디자인 정체성의 진화로 설명해 왔다. 공식 디자인 페이지는 구조·비례·스타일링을 명시하며, 2023년 뉴스룸 기록은 차량 인포테인먼트 작업을 별도로 구분한다 — Seon 디자인 시스템과 Hyundai Sans UI는 차량 내 ccNC 맥락이며, 위 KR 공개 웹 컴포넌트 규칙의 근거가 되지 않는다.

### 원칙

1. **Progress for Humanity.** 현대 공식 자료는 이를 모빌리티·지속가능성 비전으로 규정. *UI 함의:* 기록된 제품 화면 범위를 넘어선 추론 없음.
2. **Sensuous Sportiness.** 감성적 매력을 구조·비례·스타일링·기술과 결합한 공식 차량 디자인 철학. *UI 함의:* 해당 차량 철학을 근거 없는 웹 토큰으로 전환하지 말 것.
3. **모빌리티 UX의 가독성.** 현대 공식 Hyundai Sans UI 설명은 주행 환경에서의 가독성과 위계를 강조. *UI 함의:* 이는 서체의 브랜드 맥락일 뿐 웹 라이선스 근거가 아님. 다만 **가독성·위계**는 대체 폰트 선정 기준으로 채택하며, 그 기준에 따라 Pretendard를 적용 서체로 지정.

### 페르소나

본 재검증 패킷에는 페르소나를 정의할 만큼 상세한 1차 출처 기반 오디언스 세분화가 수집되지 않음. 합성 페르소나를 현대 제품 의사결정의 근거로 사용하지 말 것.

<!-- design-md:section foundations -->
## 2. 파운데이션 (Foundations)

<!-- design-md:claim foundations kind=rules-or-constraints lang=ko -->
### 컬러 팔레트 · 역할

### 제품 화면 컬러

- **Primary navy** (`#002c5f`) : 카탈로그 및 IONIQ 6 제품 화면 양쪽에서 관측된 채움형 차량 액션.
- **Teal** (`#007fa8`) : 홈 화면 캐러셀 컨트롤에서 관측. 그 이상의 시맨틱 역할 추론 없음.
- **Cyan** (`#00aad2`) : 홈 화면 챗봇 버튼 배경으로 관측.
- **Ink** (`#000000`) · **White** (`#ffffff`) : 3개 제품 화면 전반에서 반복 관측된 텍스트·보더 값.
- **Muted gray** (`#999999`) · **Utility gray** (`#444444`) : 각각 푸터/리스트, 인라인 외부 링크 크롬에서 관측.
- **Footer dark** (`#1c1b1b`) : KR 제품 푸터의 Family Site 컨트롤에서 관측.
<!-- design-md:claim-end -->

### 깊이 · 엘리베이션

§4의 반복 캡처 컴포넌트는 모두 `box-shadow: none`이며, 예외는 홈 화면 챗봇 트리거 단일 건(`rgba(0,0,0,0.15) 0px 0px 20px 0px`). 그 이상의 엘리베이션 스케일은 주장하지 않음.

### 모션 · 이징

duration·easing·animation·reduced-motion 동작은 캡처되지 않음. 모션 토큰 및 규칙 미해결(unresolved).

<!-- design-md:section typography-assets -->
## 3. 타이포그래피 · 에셋

### 타이포그래피 규칙

### 근거 등급 (Evidence classes)

- **실사용 computed 값, FontFaceSet 확인:** `HyundaiSansTextKR`(관측 287건), `HyundaiSansHeadKR`(84건)은 제공된 KR 제품 캡처에서 FontFaceSet 항목과 일치하는 가시 computed 패밀리. `HyundaiSansHeadKRR`(43건), `HyundaiSansTextKRR`(35건) 역시 로드·가시 사용된 변형.
- **공식 브랜드/서체 맥락:** 현대 2023년 공식 뉴스룸은 Hyundai Sans UI를 Hyundai Sans의 조형적 특성을 계승한 차세대 모빌리티 UX 서체로 설명. 이는 ccNC 인포테인먼트 맥락에 한정되며, Hyundai Sans UI를 웹 제품 화면의 패밀리로 확립하지 않음.
- **시스템 / 선언만 존재:** Arial은 유틸리티 크롬에서 관측된 시스템 패밀리. `element-icons`는 캡처에 선언되었으나 가시 사용 없음. 두 항목 모두 UI 패밀리 토큰으로 승격하지 않음.
- **라이선스 · 배포 경계 🔴 사용 금지:** 제공된 캡처에 폰트 소스 URL 기록 없음. 본 검토에서 KR 폰트 파일에 대한 1차 출처 웹폰트 라이선스 확인 불가. 로드된 패밀리는 **관측 기록(명칭·메트릭)으로만** 기술하며, 구현·배포에 사용하지 않음. 실제 적용 서체는 아래 대체 매핑을 따른다.

### 🆕 폰트 대체 매핑

관측된 전용 폰트는 재사용 라이선스 미확인(🔴). 구현에는 아래 오픈 라이선스 폰트를 사용한다.

| 관측 패밀리 (근거) | 적용 패밀리 | 적용 weight | 비고 |
|---|---|---|---|
| HyundaiSansHeadKR | Pretendard | 600 | 헤드라인 |
| HyundaiSansHeadKRR | Pretendard | 500 | 내비·링크 |
| HyundaiSansTextKR | Pretendard | 400 / 500 | 관측 weight 1:1 유지 |
| HyundaiSansTextKRR | Pretendard | 400 | 본문 변형 |
| Arial (푸터 유틸리티) | 시스템 스택 유지 | — | 시스템 폰트, 라이선스 무관 |

- **적용 폰트 스택:** `Pretendard, "Pretendard Variable", -apple-system, system-ui, "Malgun Gothic", sans-serif`
- **라이선스:** SIL Open Font License 1.1 — 재배포 시 OFL 원문·저작권 고지 동봉 필요.
- **자간(letter-spacing):** 관측된 `-0.4px`는 원 서체 메트릭에 종속된 값으로, 폰트 교체 시 근거 소멸. 적용값은 `normal`로 리셋한다. 크기·행간은 레이아웃 근거이므로 관측값 그대로 유지.
- **weight 매핑:** Head 계열은 원 서체의 시각 두께를 맞추기 위해 관측 weight(400)보다 상향(500/600) 적용. Text 계열은 관측값 1:1 유지.

### 🆕 폰트 설치 · 로드 (CDN 금지)

Pretendard 는 **CDN(`fonts.googleapis.com`, `cdn.jsdelivr.net` 등)으로 불러오지 않는다.** npm 패키지로 설치해 번들에 포함한다.

```bash
npm install pretendard
```

프로젝트 진입 CSS(예: `src/index.css`) 최상단 또는 엔트리 모듈에서 로드한다.

```css
/* src/index.css 최상단 */
@import "pretendard/dist/web/variable/pretendardvariable.css";

:root {
  font-family: "Pretendard Variable", Pretendard, -apple-system, system-ui, "Malgun Gothic", sans-serif;
}
```

- 가변 폰트 대신 정적 weight 만 필요하면 `pretendard/dist/web/static/pretendard.css` 를 사용한다.
- 실제 경로는 설치 후 `node_modules/pretendard/dist/web/` 아래에서 확인할 것.
- 배포 시 SIL OFL 1.1 원문·저작권 고지를 동봉한다(§3 라이선스 항목).

#### ❌ 금지

```html
<!-- CDN 링크 삽입 금지 -->
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/..." rel="stylesheet" />
```

### 관측된 위계

| 역할 | 관측 패밀리 | 적용 패밀리 / weight | 크기 | 행간 | 자간 (관측 → 적용) | 화면 |
|------|------|------|------|------|------|------|
| H2 | HyundaiSansHeadKR (400) | Pretendard 600 | 44px | 58px | -0.4px → normal | home |
| 본문/리스트 | HyundaiSansTextKR (400) | Pretendard 400 | 16px | 18.4px | normal → normal | 3개 제품 화면 전체 |
| 차량 액션 | HyundaiSansTextKR (500) | Pretendard 500 | 16px | 18.4px | -0.4px → normal | 카탈로그 · IONIQ 6 |
| 주 내비 트리거 | HyundaiSansHeadKRR (400) | Pretendard 500 | 16px | 30px | -0.4px → normal | 3개 제품 화면 전체 |
| 인라인 외부 링크 | HyundaiSansHeadKR (500) | Pretendard 600 | 14px | 14px | -0.4px → normal | 3개 제품 화면 전체 |

<!-- design-md:section components-states -->
## 4. 컴포넌트 · 상태

### 컴포넌트 스타일

아래 변형만 유지 — 제공된 수집기 근거에 셀렉터·화면·computed 값이 기록된 항목에 한함. 캡처의 `interactionCount: 0`이며, hover·focus·pressed·disabled·menu-open·validation 상태는 주장하지 않음.

### 차량 액션

**네이비 채움형 액션**
- 배경 : `#002c5f`
- 텍스트 : `#ffffff`
- Radius : 0px
- 폰트 : 16px / 500 / Pretendard (관측 : HyundaiSansTextKR 500)
- 사용 : `surface-2::[captured element]`, class `btn nuxt-link-active` / `surface-2`(차량 카탈로그) · `surface-3`(IONIQ 6 소개)에서 관측, 2회, 상태 캡처 없음.

### 주 내비게이션

**최상위 트리거**
- 배경 : transparent
- 텍스트 : `#000000`
- Radius : 0px
- 폰트 : 16px / 500 / Pretendard (관측 : HyundaiSansHeadKRR 400)
- 사용 : `home::[captured element]`, class `lnb_depth0_btn` / 홈 · 차량 카탈로그 · IONIQ 6 소개에서 관측, 15회, 상태 캡처 없음.

### 인라인 외부 링크

**스몰 외부 링크**
- 배경 : transparent
- 텍스트 : `#444444`
- Radius : 0px
- Padding : 10px 0px
- 폰트 : 14px / 600 / Pretendard (관측 : HyundaiSansHeadKR 500)
- 사용 : `home::[captured element]`, class `btn btn-external-sm in-phrase` / 3개 제품 화면 전체에서 관측, 9회, 상태 캡처 없음.

### 캐러셀 페이지네이션

**틸 페이저 컨트롤**
- 배경 : `#007fa8`
- Radius : 6px
- 사용 : `home::[captured element]`, class `el-carousel__button` / 홈에서만 관측, 2회, 상태 캡처 없음.

**선택 인디케이터 셸**
- 배경 : transparent
- 텍스트 : `#000000`
- Radius : 0px
- Padding : 0px 4px
- 폰트 : 16px / 400 / Pretendard (관측 : HyundaiSansTextKR 400)
- 사용 : `home::li`, class `el-carousel__indicator el-carousel__indicator--horizontal is-active` / 홈에서만 관측, 13회, 캡처된 유일한 상태는 `selected`. 하위 시각 컨트롤은 별도 측정되지 않음.

### 푸터 유틸리티 컨트롤

**Family Site 컨트롤**
- 배경 : `#1c1b1b`
- 텍스트 : `#999999`
- 보더 : 1px solid `#676767`
- Radius : 0px
- Padding : 0px 13px
- 사용 : `home::[captured element]` / 3개 제품 화면 전체에서 관측, 3회. 시스템 Arial 사용 — 시스템 폰트이므로 라이선스 무관, 대체 대상 아님. UI 패밀리 토큰이 아닌 푸터 유틸리티 크롬으로 유지.

### 챗봇 트리거

**원형 챗봇 버튼**
- 배경 : `#00aad2`
- Radius : 100%
- Shadow : rgba(0,0,0,0.15) 0px 0px 20px 0px
- 폰트 : 16px / 500 / Pretendard (관측 : HyundaiSansTextKR 500)
- 사용 : `home::[captured element]`, class `btn ibtn chatbot` / 홈 제품 화면에서 1회 관측, 상태 캡처 없음. 단일 화면·저신뢰 컴포넌트 근거이며, 범용 플로팅 액션 패턴을 확립하지 않음.

Tier 2 데이터는 확보되지 않았으므로 어떤 토큰·컴포넌트 값의 근거로도 사용되지 않음.

### 상태

컴포넌트 인터랙션 상태 캡처 없음. 수집기 보고 `interactionCount: 0`이며, 캐러셀 인디케이터 셸만 관측된 `selected` 상태 보유. empty·loading·error·success·skeleton·disabled·hover·focus·pressed 처리 미해결.

<!-- design-md:section layout-platforms -->
## 5. 레이아웃 · 플랫폼

### 레이아웃 원칙

제공된 근거는 3개 데스크톱 제품 라우트를 확립하나, 반응형 브레이크포인트나 그리드 측정값을 포함하지 않음. 카탈로그와 IONIQ 6 라우트는 네이비 채움형 차량 액션을 공유하며, 캡처로부터 범용 카드·간격 스케일·레이아웃 그리드를 승격하지 않음.

### 반응형 동작

반응형 뷰포트 비교 자료 미제공. 브레이크포인트·터치 타겟 규칙·접힘(collapse) 동작 미해결.

<!-- design-md:section content-locales -->
## 6. 콘텐츠 · 로케일

### 보이스 · 톤

공식 기업 언어는 현대를 “Progress for Humanity”로 규정하며, 공식 디자인 자료는 Sensuous Sportiness를 감성적 매력과 구조·비례·스타일링·기술의 결합으로 설명. 제공된 캡처는 신뢰 가능한 제품 카피 텍스트를 보존하지 않으므로, 축자 보이스 샘플이나 규범적 카피 규칙은 주장하지 않음.

<!-- design-md:section governance -->
## 7. 거버넌스

### 에이전트 프롬프트 가이드

출처에 근거한 값만 적용 — 네이비 차량 액션(`#002c5f`, 흰색 텍스트, 0px radius, 16px/500 Pretendard)은 2개 차량 제품 화면에서만 뒷받침됨. 본 레퍼런스로부터 카드·인풋·에러 상태·모션 사양을 도출하지 말 것.

서체는 **Pretendard(SIL OFL 1.1)만 사용**. `HyundaiSans*` 계열 전용 폰트는 관측 기록일 뿐이므로 코드·에셋에 포함하지 말 것.

### 🆕 폰트 라이선스 준수

- 적용 서체 Pretendard는 SIL Open Font License 1.1. 임베드·번들·재배포 모두 허용되나, **OFL 원문과 저작권 고지 동봉이 의무**.
- 폰트 파일명에 예약 폰트 이름(Reserved Font Name) 규정 위반 소지가 없는지 확인 후 배포.
- 관측된 `HyundaiSans*` 계열은 1차 출처 라이선스 미확인 🔴 — 저장소·빌드 산출물에 포함 금지.

<!-- design-md:claim authority kind=evidence-backed-reconstruction lang=ko -->
### 권위 범위 (Authority)

본 문서는 근거 기반 재구성(evidence-backed reconstruction)이며, 무관한 대상 프로젝트에 대한 권위 문서가 아님.
<!-- design-md:claim-end -->

<!-- design-md:claim application-priority order=prompt-fact,repository-fact,system-contract,reference-inspiration lang=ko -->
### 적용 우선순위

1. 요청 범위에 대한 사용자 직접 지시
2. 리포지토리 사실
3. 본 시스템 계약(system contract)
4. 레퍼런스 영감(reference inspiration)
<!-- design-md:claim-end -->

<!-- design-md:claim unknowns policy=absent-at-smallest-unresolved-boundary lang=ko -->
### 미해결 항목 (Unknowns)

미해결 값 또는 그룹은 최소 단위로만 생략. 그럴듯한 기본값으로 대체하지 말 것.
<!-- design-md:claim-end -->

<!-- design-md:claim changes policy=review-record-validate-before-adoption lang=ko -->
### 변경 관리

변경 사항은 채택 전 기록·검토·검증 수행.
<!-- design-md:claim-end -->
