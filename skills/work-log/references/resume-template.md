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

## 분류 프로세스

1. 수집된 각 활동(커밋, PR, 티켓, 미팅, Slack 대화 등)을 위 13개 관점의 시그널과 매칭
2. 하나의 활동이 여러 관점에 해당하면 가장 강하게 드러나는 쪽에 배치
3. 각 관점에 대해: 활동 나열 + "어떤 문제를 인식하고 → 어떻게 해결했고 → 결과/임팩트" 서사 생성
4. 활동 데이터만으로 서사가 부족하면 → interactive 모드에서 AskUserQuestion으로 보충 질문
5. automated 모드에서는 데이터 기반으로만 서사 생성, 부족한 부분은 placeholder 표시

---

## 이력서 스코어 (각 항목 1-10)

### 채점 기준

| 점수 요소 | 배점 | 설명 |
|-----------|------|------|
| 정량적 수치 포함 (before/after) | +3 | "빌드 시간 50s → 22s" 같은 구체적 수치 |
| 구체적 action verb 사용 | +2 | "Implemented", "Designed", "Led" vs "Worked on", "Helped" |
| 문제 → 해결 → 임팩트 서사 완성 | +2 | 세 단계가 모두 있는지 |
| specific vs generic (구체적일수록 높음) | +2 | "Improved performance" vs "Reduced API latency by 40% via Redis caching" |
| 임팩트 범위 (팀 < 조직 < 회사 < 업계) | +1 | 영향 범위가 넓을수록 높음 |

### 리라이팅 규칙

스코어 7 미만 항목에는 AI가 강한 버전으로 리라이팅 제안:
- 정량적 수치가 없으면 → 추정 가능한 수치 제안 ("측정 가능한 수치를 추가하면 더 강해집니다: 예) 처리 시간 X% 감소")
- action verb가 약하면 → 강한 동사로 교체 제안
- 서사가 불완전하면 → 빠진 단계(문제/해결/임팩트) 보충 제안
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

## 복사용 포맷

resume_path 확장자 감지:
- .tex: config의 `organize.resume_latex_macro` 사용 (미설정 시 자동 감지, 실패 시 `\item`)
- .md: Markdown bullet 형식
- 미설정/미지원: Markdown 기본값 + 경고
```

---

## English Template (language: en)

Same structure with English headers and perspective names:
- "Resume Achievement Summary"
- "Technical / Code / Design" (Library Internals & Problem Solving, Design Comparison & Architecture Direction, Resource Optimization, Deployment Impact Measurement, Fault Detection & Rapid Response, Root Cause Analysis & Prevention, Performance Optimization & Operational Automation)
- "Product" (Business Growth Contribution, Product Scope & Impact)
- "Communication" (Data-Driven Coordination, Documentation & Context Transfer)
- "Culture" (Team Culture Building, Precise Feedback)
- "Rewriting Suggestions (Score < 7)"
- "Copy Format"

---

## Conditional Sections

- Only include a perspective section if it has ≥1 matching activity
- If a perspective has 0 activities, omit it entirely (don't show empty sections)
- If total activities are 0, show error and suggest checking config/date range
- In automated mode, skip AskUserQuestion for narrative gaps — use placeholder instead
