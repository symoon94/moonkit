# Report Template — 사내 성과 보고용

## 카테고리 체계

경영진/오너 시각의 6개 비즈니스 가치 카테고리로 분류.

### Auto-categorization Rules

| 카테고리 | 판별 기준 | 키워드/시그널 |
|----------|----------|-------------|
| **매출/딜리버리** | 고객 대면 제품 출시, 파트너 시스템 구축, 딜리버리 완료, 매출 직결 기능 릴리즈 | feat + customer/partner, release, launch, delivery, demo, sales, 고객, 파트너, 납품, 출시 |
| **운영 효율화** | CI/CD 개선, 자동화 파이프라인, 모니터링, 프로세스 간소화, DX 향상 | chore, ci, automate, pipeline, monitoring, dx, devops, workflow, 자동화, 파이프라인 |
| **장애 & 보안 리스크 감소** | 보안 취약점 수정, 권한 제어, 장애 감지/대응 설계, RCA + 재발 방지 | fix, security, vulnerability, incident, RCA, postmortem, alert, hotfix, 장애, 보안, 수정 |
| **비용 절감** | 인프라 비용 절감, 리소스 최적화, 성능 최적화, 불필요 의존성 제거 | optimize, reduce, cost, perf, resource, memory, infra, deprecate, 최적화, 비용, 절감 |
| **채용 & 홍보** | 발표, 블로그, 오픈소스 기여, 기술 브랜딩, 컨퍼런스 | talk, blog, conference, open-source, meetup, article, presentation, 발표, 블로그, 컨퍼런스 |
| **팀 빌딩/리더십** | 미팅 주최, 온보딩, 멘토링, 크로스팀 협업 주도, 문화 활동 | onboarding, mentoring, team, lead, 1on1, sync, retro, culture, 온보딩, 멘토링, 팀 |

### Source-based defaults

| 데이터 | 기본 카테고리 | 예외 |
|--------|-------------|------|
| 커밋/PR (`feat`) | 매출/딜리버리 | customer/partner 맥락 없으면 → 운영 효율화 |
| 커밋/PR (`fix`, `security`) | 장애 & 보안 리스크 감소 | — |
| 커밋/PR (`chore`, `ci`) | 운영 효율화 | — |
| 커밋/PR (`perf`, `optimize`) | 비용 절감 | — |
| 커밋/PR (`test`, `refactor`) | 운영 효율화 | — |
| 코드 리뷰 | 팀 빌딩/리더십 | 기술적 깊은 리뷰 → 운영 효율화 |
| Jira 티켓 | 제목/라벨로 판단 | type=Bug → 리스크, type=Story+customer → 매출 |
| Slack 메시지 | 채널/토픽으로 판단 | 기술 채널 → 운영, 고객 채널 → 매출 |
| 미팅 (주최) | 팀 빌딩/리더십 | — |
| 미팅 (참석) | 해당 카테고리 추론 | 고객 미팅 → 매출 |
| Notion 페이지 | 제목/내용으로 판단 | 기술 문서 → 운영, 발표 자료 → 홍보 |

분류 불가 항목은 "기타"로 처리. 하나의 성과가 복수 카테고리에 해당하면 가장 임팩트가 큰 쪽에 배치.

---

## Korean Template (language: ko)

```markdown
# 사내 성과 보고서
**기간**: {START} ({START_DOW}) ~ {END} ({END_DOW})  |  **작성자**: {username}  |  **작성일**: {today}

---

## Executive Summary
{핵심 성과 3줄 요약. 정량적 수치 포함. 가장 임팩트 큰 성과를 중심으로.}

---

## 주요 성과 (TOP 5)

### 1. {가장 임팩트 큰 성과 제목}
- **카테고리**: {매출/운영효율화/리스크감소/비용절감/홍보/리더십}
- **상세**: {무엇을 왜 했고, 어떻게 해결했는지 2-3문장}
- **임팩트**: {정량적 수치. 없으면 정성적 임팩트}
- **증거**: {PR #, 커밋, 티켓, 링크}

### 2. ...
### 3. ...
### 4. ...
### 5. ...

---

## 카테고리별 활동 요약

| 카테고리 | 건수 | 주요 활동 | 임팩트 |
|----------|------|----------|--------|
| 매출/딜리버리 | {N} | {1줄 요약} | {수치 또는 정성적} |
| 운영 효율화 | {N} | {1줄 요약} | {수치} |
| 장애 & 보안 리스크 감소 | {N} | {1줄 요약} | {수치} |
| 비용 절감 | {N} | {1줄 요약} | {수치} |
| 채용 & 홍보 | {N} | {1줄 요약} | {수치} |
| 팀 빌딩/리더십 | {N} | {1줄 요약} | {수치} |

---

## 상세 활동

### 매출/딜리버리
{해당 카테고리의 모든 활동 상세 나열}

### 운영 효율화
...

### 장애 & 보안 리스크 감소
...

### 비용 절감
...

### 채용 & 홍보
...

### 팀 빌딩/리더십
...

---

## 다음 기간 계획
{진행 중인 Jira 티켓(status != Done) 목록만 나열. AI 추측 없음.
Jira 비활성화 또는 진행 중 티켓 0건이면 이 섹션 생략.}
```

---

## English Template (language: en)

Same structure with English headers:
- "Performance Report", "Executive Summary"
- "Top Achievements (TOP 5)"
- "Category Summary" (Revenue/Delivery, Operational Efficiency, Risk & Security Reduction, Cost Reduction, Hiring & Branding, Team Building/Leadership)
- "Detailed Activities"
- "Next Period Plan"

---

## Conditional Sections

- Only include a category section if it has ≥1 activity
- If a category has 0 activities, show "—" in the summary table but omit the detail section
- If all sources failed, show error and suggest checking config
- TOP N is configurable via `organize.report_top_n` in config (default: 5)
