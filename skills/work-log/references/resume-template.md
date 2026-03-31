# Resume Template — 이력서용 역량 프레임워크

## 역량 프레임워크 개요

수집된 활동을 **엔지니어 역량 프레임워크**에 맞춰 분류하고,
각 관점에서 "어떤 문제를 인식하고 어떻게 해결했는지" 서사를 만들어주는 모드.

4개 영역, 13개 관점으로 구성.

---

## 1. 기술 / 코드 / 설계 (7개 관점)

### 1-1. 라이브러리 내부 구현 이해 & 문제 해결

**무엇을 보는가**: 내부 동작을 알아야 풀 수 있는 문제를 해결했는가?
- DB pool 설정이 왜 다양하게 존재하는지 이해하고 적절히 조정
- Jackson ObjectMapper에서 Exception이 터지는 근본 원인 파악
- 라이브러리 소스를 직접 분석하여 문서화되지 않은 동작 발견

**시그널**: fix + library name, internal, deep-dive, root cause, pool, config, debug
**영어명**: Library Internals & Problem Solving

### 1-2. 모범사례 비교 & 설계 방향성 제시

**무엇을 보는가**: 다른 기업의 접근과 비교하면서 더 나은 설계를 제시했는가?
- 핀터레스트, 넷플릭스 등의 컨퍼런스 발표 참고
- "우리 구현이 최선인가?" 에 대한 답을 찾기 위한 리서치
- 글로벌 진출 시 국가별 정책 대응 아키텍처 (예: 토스)
- RFC/ADR 문서로 설계 의사결정 기록

**시그널**: architecture, design, RFC, ADR, proposal, compare, benchmark, research
**영어명**: Design Comparison & Architecture Direction

### 1-3. 리소스 최적화

**무엇을 보는가**: 리소스를 최적으로 사용하면서 요구사항을 충족했는가?
- 로그 사이즈 줄이기
- 리소스 30% 절감 (예: hyperthread 활용)
- 적정 여유 자원 판단 (낭비 vs 안전 마진)
- HA, 이중화, 속도, API 호출 수 최적화

**시그널**: optimize, reduce, resource, memory, CPU, cost, log, HA, throughput
**영어명**: Resource Optimization

### 1-4. 배포 임팩트 측정

**무엇을 보는가**: 배포한 작업의 임팩트를 측정하고 명확히 보여줬는가?
- 카나리 배포하면서 지표 모니터링
- 배포 후 예상과 다른 전개에 대응
- 일을 시작한 이유와 결과가 매칭되는지 증명

**시그널**: deploy, canary, monitoring, metrics, A/B, rollout, before/after
**영어명**: Deployment Impact Measurement

### 1-5. 장애 감지 & 신속 대응 설계

**무엇을 보는가**: 장애를 빠르게 감지하고 대응할 수 있도록 설계했는가?
- Flink vs Elasticsearch 기반 감지 체계 비교/선택
- ElasticSearch Watcher + Grafana 알림 체계
- Fault injection 테스트 (예: vivasystem)
- 장애 발생 → 감지 → 대응까지의 시간 단축

**시그널**: alert, incident, detect, watcher, grafana, flink, fault-injection, SLA
**영어명**: Fault Detection & Rapid Response

### 1-6. RCA & 재발 방지

**무엇을 보는가**: 동일 장애가 재발하지 않도록 분석하고 대책을 세웠는가?
- 단순 버전업이 아닌, 근본 원인(Root Cause) 파악
- 문제를 발견할 수 있는 수단 자체를 마련 (예: eBPF 기반 관찰)
- 사람에 의존하지 않고 시스템으로 방지하는 설계
- 외부 업체 이중화, 회피 vs 해결 구분

**시그널**: RCA, postmortem, prevention, regression, ebpf, root-cause, failover
**영어명**: Root Cause Analysis & Prevention

### 1-7. 성능 최적화 / 운영 자동화

**무엇을 보는가**: 지속적으로 성능과 운영을 개선했는가?
- 아키텍처는 계속 변화한다는 인식
- 사업 확장의 최전선에서 기술 부채 관리
- 지나간 일에 파묻히지 않고 앞으로 나아가는 동력 유지

**시그널**: perf, automate, pipeline, optimize, refactor, migration, scale
**영어명**: Performance Optimization & Operational Automation

---

## 2. 제품 (2개 관점)

### 2-1. 비즈니스 성장 기여

**무엇을 보는가**: 비즈니스가 지금보다 더 성장하도록 만들었는가?
- 중요한 건 만들어가는 것. 10개 중 1개 성공이라도 도전
- 새로운 기능/제품을 출시하여 비즈니스 성장에 기여

**시그널**: feature, launch, customer, revenue, growth, product, ship
**영어명**: Business Growth Contribution

### 2-2. 담당 제품 규모 & 영향력

**무엇을 보는가**: 내가 있고 없고의 차이를 팀이 느끼는가?
- 담당 제품의 규모와 복잡도
- 여력이 있으면 더 많은 제품에 도전하고 결과를 만든다

**시그널**: scope, ownership, lead, expand, module, service, domain
**영어명**: Product Scope & Impact

---

## 3. 커뮤니케이션 (2개 관점)

### 3-1. 데이터 기반 의견 조율

**무엇을 보는가**: 데이터로 설득하고 합의를 이끌어냈는가?
- 미래의 일을 가정으로만 조율하면 합의가 어려움
- 데이터가 있어도 해석이 다를 수 있지만, 없으면 시작도 못 함
- 때로는 PoC를 두 가지 다 해보는 게 더 효율적
- DB 성능, 이중화, 데이터 이동 등을 PoC로 검증

**시그널**: data, benchmark, PoC, comparison, decision, metrics, experiment
**영어명**: Data-Driven Coordination

### 3-2. 기록을 통한 문맥 전달

**무엇을 보는가**: 기록으로 문맥을 명확히 전달했는가?
- 사람 간의 피드백도 마찬가지 (최근성 효과에 의존하지 않기)
- 현재 수준을 개선하려면 기록이 가장 중요
- 기준 → 전파 → 개선 사이클

**시그널**: doc, RFC, ADR, runbook, postmortem, feedback, wiki, notion
**영어명**: Documentation & Context Transfer

---

## 4. 문화 (2개 관점)

### 4-1. 가고 싶은 팀 만들기

**무엇을 보는가**: 누군가로 인해, 기피하던 팀도 가고 싶은 팀이 되는가?
- 팀 문화를 변화시키는 노력
- 온보딩, 팀 이벤트, 크로스팀 교류

**시그널**: team-building, onboarding, culture, event, lunch, social
**영어명**: Team Culture Building

### 4-2. 정확한 피드백

**무엇을 보는가**: 아는 만큼 보이는 수준의 구체적 피드백을 줬는가?
- 듣는 사람과 스스로 모두 부족한 부분을 파악할 수 있는 좋은 경험
- 코드 리뷰에서의 교육적 피드백도 포함

**시그널**: review, feedback, mentoring, coaching, 1on1, growth
**영어명**: Precise Feedback

---

## 서사 구조 원칙 (Narrative Arc)

모든 이력서 항목은 **기능 나열이 아닌 서사**로 작성한다.
단순히 "뭘 만들었다"가 아니라, "왜 만들었고 → 어떤 고민을 했고 → 어떻게 해결했고 → 결과가 뭔지"가 드러나야 한다.

### 4단계 서사 구조

| 단계 | 설명 | 예시 |
|------|------|------|
| **1. 문제 인식** | 왜 이 일을 시작했는가? 어떤 페인포인트가 있었는가? | "동기 추론만으로는 대용량 문서를 처리할 수 없었다" |
| **2. 고민/접근** | 어떤 선택지가 있었고, 왜 이 방법을 골랐는가? | "SQS→RabbitMQ→Asynq로 3세대에 걸쳐 아키텍처를 진화시켰다" |
| **3. 해결** | 구체적으로 무엇을 구현/설계/도입했는가? | "Go 기반 Redis 큐를 도입하여 운영 복잡도를 낮추면서 처리량을 확보" |
| **4. 정량적 결과** | 측정 가능한 임팩트는? (before/after 수치 필수) | "응답 시간 30s→0.2s, 일 16만장 처리, 18x 쓰루풋 달성" |

### 안티패턴 (피해야 할 것)

- ❌ "Built X with Y and Z" — 기술 스택 나열만 하고 WHY가 없음
- ❌ "Implemented A, B, C, D, E" — 피처 나열, 서사 없음
- ❌ "Improved performance" — 구체적 수치 없는 generic 서술
- ❌ 출처에 없는 수치/사실을 추론하여 작성 — 허위 기재 위험
- ✅ "X 문제가 있었다. Y 접근으로 해결했다. 결과 Z를 달성했다."

### 출처 기반 작성 원칙 (Source-of-Truth)

이력서의 모든 내용은 **검증 가능한 출처에서 확인된 사실만** 작성한다.

| 허용 | 금지 |
|------|------|
| GitHub PR/커밋에서 확인된 수치 | 출처 없이 추론한 수치 ("약 50개" 등) |
| Slack 메시지에서 확인된 의사결정 | 인과관계 추론 ("A를 했더니 B에 선발됨") |
| 사용자가 직접 제공한 성과 기록의 수치 | 수치를 과장하거나 반올림 |
| Notion 문서에서 확인된 프로젝트 사실 | 확인 안 된 사용률/피드백 지표 |

**확인 안 된 내용이 필요한 경우**: placeholder로 표시하고 사용자에게 확인 요청.
예) "처리량 [확인 필요]건/일 달성"

### 개발자 이력서 작성 가이드

개발자 포지션 지원 시, 아래 관점이 이력서에 드러나도록 작성한다:

1. **기술 스택보다 문제와 설계 의도 우선**: 어떤 문제를 풀었는지, 왜 그 구조를 선택했는지를 먼저 설명
2. **실험→프로덕션 신뢰성**: sanity test, 알람 체계, 모니터링 등 실행 신뢰성과 확장성을 어떻게 확보했는지 구체적으로
3. **장애/성능/비용 대응**: 장애, 성능 저하, 비용 문제를 어떻게 탐지하고 해결했는지
4. **내부 니즈→플랫폼 기능**: 내부 팀의 니즈를 발굴하고 플랫폼 기능으로 연결한 과정과 결과(사용률, 피드백 등)
5. **오픈소스 기여**: 오픈소스 기여 경험이 있다면 포함

### 서사 변환 예시

**Before (나열형):**
> Built a production Slack agent with Solar/Claude dual-LLM routing, Jira daily briefings, eval test suite, persona system, knowledge system.

**After (서사형):**
> Manual briefings and Q&A routing across 4+ teams created significant coordination overhead. Built a Slack agent with Solar/Claude dual-LLM routing—Solar classifies intent, then routes to Claude or Solar for execution—with eval test suite for quality assurance and knowledge system with selective context loading. Eliminated manual coordination and enabled self-service partner operations.

---

## 분류 프로세스

1. 수집된 각 활동(커밋, PR, 티켓, 미팅, Slack 대화 등)을 위 13개 관점의 시그널과 매칭
2. 하나의 활동이 여러 관점에 해당하면 가장 강하게 드러나는 쪽에 배치
3. 각 관점에 대해: **4단계 서사 구조**(문제 인식 → 고민/접근 → 해결 → 정량적 결과)로 서사 생성. 기능 나열 금지.
4. 활동 데이터만으로 서사가 부족하면 → interactive 모드에서 AskUserQuestion으로 "왜 이 일을 시작했는지", "어떤 대안이 있었는지" 보충 질문
5. automated 모드에서는 데이터 기반으로만 서사 생성, 부족한 부분은 placeholder 표시

---

## 이력서 스코어 (각 항목 1-10)

### 채점 기준

| 점수 요소 | 배점 | 설명 |
|-----------|------|------|
| 4단계 서사 완성 (문제→고민→해결→결과) | +3 | 4단계가 모두 있는지. 나열형은 최대 5점. |
| 정량적 수치 포함 (before/after) | +3 | "응답 시간 30s → 0.2s" 같은 구체적 수치 |
| 구체적 action verb 사용 | +1 | "Traced", "Designed", "Led" vs "Worked on", "Helped" |
| specific vs generic (구체적일수록 높음) | +2 | "Improved performance" vs "Reduced API latency by 40% via Redis caching" |
| 임팩트 범위 (팀 < 조직 < 회사 < 업계) | +1 | 영향 범위가 넓을수록 높음 |

### 리라이팅 규칙

스코어 7 미만 항목에는 AI가 강한 버전으로 리라이팅 제안:
- **서사가 없으면 (나열형)** → 4단계 서사 구조로 전환. "Built X with Y" → "Z 문제가 있었다. X를 Y로 해결했다. 결과 W."
- 정량적 수치가 없으면 → 추정 가능한 수치 제안 ("측정 가능한 수치를 추가하면 더 강해집니다: 예) 처리 시간 X% 감소")
- action verb가 약하면 → 강한 동사로 교체 제안
- 서사에서 "고민/접근" 단계가 빠져있으면 → "왜 이 방법을 선택했는지" 보충 제안
- generic하면 → 구체화 제안

---

## Korean Template (language: ko)

```markdown
# 이력서용 성과 정리
**기간**: {START} ({START_DOW}) ~ {END} ({END_DOW})  |  **작성일**: {today}

---

## 기술 / 코드 / 설계

### 라이브러리 내부 구현 이해 & 문제 해결
- **{스코어}/10** {Action verb} {what}: {문제 인식} → {해결 과정} → {결과/임팩트}
  - 원본: {PR #, 커밋, 티켓}

### 모범사례 비교 & 설계 방향성 제시
- **{스코어}/10** {설명}
  - 원본: {출처}

### 리소스 최적화
...

### 배포 임팩트 측정
...

### 장애 감지 & 신속 대응 설계
...

### RCA & 재발 방지
...

### 성능 최적화 / 운영 자동화
...

---

## 제품

### 비즈니스 성장 기여
...

### 담당 제품 규모 & 영향력
...

---

## 커뮤니케이션

### 데이터 기반 의견 조율
...

### 기록을 통한 문맥 전달
...

---

## 문화

### 가고 싶은 팀 만들기
...

### 정확한 피드백
...

---

## 리라이팅 제안 (스코어 7 미만 항목)

| 원본 | 스코어 | 리라이팅 제안 | 개선 이유 |
|------|--------|-------------|----------|
| {원본 텍스트} | {4/10} | {강화된 버전} | {무엇이 부족했고 어떻게 개선되었는지} |

---

## 복사용 포맷 (2개 언어 버전)

resume_path 확장자 감지:
- .tex: **Jake's Resume 포맷** (`\resumeItem{Title}{Description}`) 사용. 서사 구조(문제→접근→해결→결과)를 Description에 인라인으로 작성.
- .md: Markdown bullet 형식
- 미설정/미지원: Markdown 기본값 + 경고

**항상 영문 버전과 한글 버전을 모두 생성한다.**

### LaTeX 포맷 규칙 (Jake's Resume)

```latex
% 프로젝트 헤더 (불릿 없음, 볼드 + 날짜)
\resumeProjectSubheading{프로젝트명}{기간}

% 개별 항목 (○ 불릿, 서사형)
\resumeItem{제목}{문제 상황 서술. 접근 방법 및 해결 과정. 정량적 결과.}
```

**서사 작성 규칙**: Description 안에 4단계 서사를 자연스러운 문장으로 이어 쓴다.
- 1문장: 문제/배경 (왜 시작했나)
- 1-2문장: 접근/해결 (뭘 어떻게 했나, 왜 이 방법인지)
- 1문장: 정량적 결과 (before/after 수치)

**예시:**
```latex
\resumeItem{Service Stability}
  {A 10-month intermittent panic had defied debugging across the team.
   Traced the root cause to thread-unsafe \textbf{go-fitz} PDF library
   internals through systematic reproduction; applied application-level
   \textbf{Locking} as a targeted fix. Eliminated 10,000+ daily
   Segmentation Faults and reduced 500-error false alarms from 65/week
   to zero.}
```

### 영문 복사용 포맷

영문 이력서에 바로 붙여넣을 수 있는 원본 코드. 서사 구조 필수.

### 한글 복사용 포맷

동일 내용을 한국어로 작성한 버전. 한국어 이력서/성과 보고서에 붙여넣기용.
- action verb → 한국어 서술형 ("구현", "설계", "주도", "자동화" 등)
- 서사 구조는 동일하게 유지 (문제→접근→해결→결과)
- .tex 포맷이면 LaTeX 매크로 동일 사용, 내용만 한국어

---

## 프리뷰 (2개 언어 버전)

복사용 포맷을 사람이 읽기 쉬운 Markdown으로 렌더링한 것.
**영문 프리뷰와 한글 프리뷰를 모두 생성한다.**

### 프리뷰 변환 규칙

LaTeX/Markdown 원본을 아래 규칙에 따라 변환:
- `\resumeItem{Title}{Description}` → `- **Title**: Description`
- `\resumeProjectSubheading{Name}{Date}` → `### Name (Date)` + horizontal rule
- `\textbf{...}` → `**...**`
- `\texttt{...}` → `` `...` ``
- 각 프로젝트 섹션 사이에 `---` 구분선 삽입
- 서사 구조(문제→해결→결과)가 Description 안에 자연스럽게 포함되어야 함

**레거시 매크로 지원** (기존 이력서 호환):
- `\SmallBulletItem` / `\BulletItem` / `\item` → Markdown bullet (`-`)
- `\Impact{...}` → blockquote + italic (`> *...*`)

### 출력 구조

Markdown 파일과 대화 출력에서:
```
## 복사용 포맷 (English)
{영문 LaTeX/Markdown 코드블록}

## 복사용 포맷 (한국어)
{한글 LaTeX/Markdown 코드블록}

## 프리뷰 (English)
{영문 프리뷰 — ### 카테고리 (스코어) + bullet + blockquote}

## 프리뷰 (한국어)
{한글 프리뷰 — ### 카테고리 (스코어) + bullet + blockquote}
```

### 예시

**영문 프리뷰:**
```markdown
### Resource Optimization (9/10)

- **Dev Server Performance Optimization**: Identified 70x redundant `git log` subprocess calls...
  > *Reduced dev server startup from 50s to 22s (**56% reduction**)...*
```

**한글 프리뷰:**
```markdown
### 리소스 최적화 (9/10)

- **Dev 서버 성능 최적화**: MDX 파일당 `git log` subprocess 70회 중복 호출 및 미사용 **aws-amplify** 54MB 의존성 발견. **Turbopack** 적용 및 불필요 의존성 제거.
  > *Dev 서버 기동 시간 50s → 22s로 단축 (**56% 감소**), 1,331줄 삭제 / 6줄 추가.*
```

**HTML 출력 시에도 영문/한글 복사용 포맷과 프리뷰 4개 섹션을 모두 포함한다.**
상세 스타일링은 `html-template.md`의 "Resume Mode: Copy Format & Preview in HTML" 참조.

---

## English Template (language: en)

Same structure with English headers and perspective names:
- "Resume Achievement Summary"
- "Technical / Code / Design" (Library Internals & Problem Solving, Design Comparison & Architecture Direction, Resource Optimization, Deployment Impact Measurement, Fault Detection & Rapid Response, Root Cause Analysis & Prevention, Performance Optimization & Operational Automation)
- "Product" (Business Growth Contribution, Product Scope & Impact)
- "Communication" (Data-Driven Coordination, Documentation & Context Transfer)
- "Culture" (Team Culture Building, Precise Feedback)
- "Rewriting Suggestions (Score < 7)"
- "Copy Format (English)" + "Copy Format (한국어)"
- "Preview (English)" + "Preview (한국어)"

---

## Conditional Sections

- Only include a perspective section if it has ≥1 matching activity
- If a perspective has 0 activities, omit it entirely (don't show empty sections)
- If total activities are 0, show error and suggest checking config/date range
- In automated mode, skip AskUserQuestion for narrative gaps — use placeholder instead
