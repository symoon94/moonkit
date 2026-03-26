# Impact Report Template & Categorization Rules

## Korean Template (language: ko)

```markdown
# 성과 보고서
**기간**: {START} ~ {END}  |  **작성일**: {today}

---

## 요약
{전체 활동을 2-3문장으로 요약. 핵심 성과와 임팩트를 중심으로.}

---

## 기술 / 코드 / 설계

{이 영역에 해당하는 모든 작업을 나열. 각 항목에 임팩트 태그를 붙인다.}

| 작업 | 상세 | 임팩트 |
|------|------|--------|
| {커밋/PR/티켓 제목} | {1줄 설명} | {💰/⏱/🛡/✅ 태그 + 수치} |
| ... | ... | ... |

**세부 항목:**

- **라이브러리/기술 스택**: {이번 기간 사용한 기술 나열}
- **설계 & 아키텍처**: {새로운 설계 또는 아키텍처 결정}
- **장애 대응**: {장애 감지, 대응, 재발 방지 대책}
- **성능 최적화**: {측정 가능한 성능 개선}
- **운영 자동화**: {자동화한 프로세스}

---

## 제품

| 작업 | 상세 | 임팩트 |
|------|------|--------|
| {제품 관련 작업} | {설명} | {태그 + 수치} |

**세부 항목:**

- **비즈니스 기여**: {매출, 전환율, 고객 가치에 어떻게 기여했는지}
- **제품 내 비중**: {이 기간 내가 담당한 제품 영역과 역할}

---

## 커뮤니케이션

| 작업 | 상세 | 임팩트 |
|------|------|--------|
| {커뮤니케이션 관련 작업} | {설명} | {태그 + 수치} |

**세부 항목:**

- **데이터 기반 커뮤니케이션**: {데이터로 설득하거나 의사결정한 사례}

---

## 문화

| 작업 | 상세 | 임팩트 |
|------|------|--------|
| {문화 관련 작업} | {설명} | {태그 또는 비고} |

**세부 항목:**

- **오고 싶은 팀 만들기**: {팀 문화 활동, 온보딩, 사내 이벤트}
- **피드백**: {구체적 피드백을 준 사례}

---

## 임팩트 미측정 항목

{자동으로 임팩트 태그를 찾지 못한 항목들. 유저가 직접 채우지 않은 항목.}

| 작업 | 역량 영역 | 측정 제안 |
|------|-----------|----------|
| {작업명} | {기술/제품/커뮤니케이션/문화} | {임팩트를 측정하기 위해 할 수 있는 구체적 행동 제안} |

---

## 임팩트 요약 대시보드

| 임팩트 유형 | 건수 | 대표 성과 |
|------------|------|----------|
| 💰 매출 | {N} | {가장 큰 매출 기여 항목} |
| 💰 비용 | {N} | {가장 큰 비용 절감 항목} |
| ⏱ 시간 | {N} | {가장 큰 시간 절약 항목} |
| 🛡 리스크 | {N} | {가장 큰 리스크 감소 항목} |
| ✅ 품질 | {N} | {가장 큰 품질 개선 항목} |
| ⬜ 미측정 | {N} | — |

---

## 다음 기간 측정 계획

{미측정 항목을 다음 기간에 측정하기 위한 구체적 액션 플랜}

1. {측정 계획 1}
2. {측정 계획 2}
3. ...
```

## English Template (language: en)

Same structure with English headers:
- "Impact Report", "Summary"
- "Technical / Code / Design", "Product", "Communication", "Culture"
- "Untagged Items", "Impact Dashboard", "Next Period Measurement Plan"

## Categorization Rules

### Auto-categorization by source

| 데이터 | 기본 역량 영역 | 예외 |
|--------|--------------|------|
| 커밋/PR | 기술 | 제목에 customer/partner/delivery → 제품 |
| 코드 리뷰 | 기술 | — |
| Jira 티켓 | 기술 | type=Bug → 기술+리스크, type=Story+customer → 제품 |
| Slack 메시지 | 커뮤니케이션 | 기술 채널 → 기술, #general/#random → 문화 |
| 미팅 (참석) | 커뮤니케이션 | — |
| 미팅 (주최) | 문화 | 기술 리뷰 미팅 → 기술 |
| Notion 페이지 | 기술 | 팀 문화 관련 → 문화 |

### Impact auto-tagging signals

**💰 매출 (Revenue)**
- Keywords: customer, partner, delivery, release, launch, demo, sales, 고객, 파트너, 납품, 출시
- Context: PR merged to production + customer-facing feature

**💰 비용 (Cost)**
- Keywords: optimize, reduce, cost, remove, deprecate, migrate, 최적화, 비용, 절감, 제거
- Context: dependency removal, infrastructure change, vendor switch

**⏱ 시간 (Time)**
- Keywords: speed, fast, pipeline, CI/CD, automate, batch, 시간, 자동화, 단축, 파이프라인
- Context: automation scripts, build time improvements, process changes
- If specific numbers in commit message (e.g., "50s → 22s"), use them directly

**🛡 리스크 (Risk)**
- Keywords: fix, bug, crash, security, vulnerability, validation, error, 장애, 보안, 수정, 버그
- Context: hotfix PRs, security patches, error handling improvements

**✅ 품질 (Quality)**
- Keywords: test, refactor, clean, lint, coverage, type, 테스트, 리팩토링, 품질, 정리
- Context: test additions, code cleanup, type safety improvements

### Measurement suggestion templates

When a task has no measurable impact, suggest one of these patterns:

**기술/설계 작업:**
- "이 변경의 효과를 측정하려면: 변경 전/후 {빌드 시간|응답 시간|에러율}을 비교해보세요."
- "모니터링 대시보드에서 {메트릭}을 추적하면 임팩트를 수치화할 수 있습니다."

**제품 작업:**
- "이 기능의 비즈니스 임팩트: {사용량|전환율|고객 피드백}을 트래킹해보세요."
- "파트너/고객에게 이 기능을 소개한 후 반응을 기록해두세요."

**커뮤니케이션:**
- "이 커뮤니케이션의 효과: 논의 후 생성된 액션 아이템 수와 완료율을 추적해보세요."
- "의사결정까지 걸린 시간(thread 시작~결론)을 측정하면 비동기 소통 효율을 알 수 있습니다."

**문화:**
- "팀 활동의 임팩트는 직접 수치화하기 어렵습니다. 참석자 수, 반복 참여율, 또는 팀 서베이 점수 변화를 참고할 수 있습니다."
- "온보딩 효과: 신규 멤버의 첫 PR까지 걸린 시간을 before/after로 비교해보세요."
