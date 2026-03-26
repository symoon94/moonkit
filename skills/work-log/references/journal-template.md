# Journal Template

## Korean Template (language: ko)

**Important**: Derive day-of-week labels from actual dates using `date` command, NOT hardcoded.

```markdown
# 업무일지
**기간**: {START} ({START_DOW}) ~ {END} ({END_DOW})  |  **작성일**: {today}

---

## 요약
{전체 활동을 1-3문장으로 자연스럽게 요약. 핵심 성과와 주요 활동을 포함.}

## 코드 & 엔지니어링

### 커밋
| 레포 | 커밋 수 | 주요 변경 |
|------|---------|----------|
{각 레포별 커밋 수와 주요 변경 사항 1줄 요약}

### Pull Requests
| 레포 | PR | 제목 | 상태 |
|------|-----|------|------|
{PR 목록: 번호, 제목, Merged/Open/Closed}

### 코드 리뷰
{리뷰한 PR 목록}

## 커뮤니케이션 (Slack)
{채널별 주요 대화 토픽 요약}

## 프로젝트 관리 (Jira)
| 티켓 | 제목 | 상태 | 우선순위 |
|------|------|------|---------|
{티켓 목록}

## 미팅
| 날짜 | 제목 | 시간 |
|------|------|------|
{미팅 목록}

## 문서 (Notion)
{수정한 페이지 목록과 간단 설명}

---

## Insights

### 성장 지표 (Growth Metrics)

| 지표 | 이번 기간 | 이전 기간 | 변화 |
|------|----------|----------|------|
| 커밋 수 | {N} | {N or "—"} | {↑/↓/→} |
| PR 머지 | {N} | {N or "—"} | {↑/↓/→} |
| 미팅 시간 | {N}h | {N or "—"} | {↑/↓/→} |
| Deep Work 비율 | {추정}% | {N or "—"} | {↑/↓/→} |

이전 기간 데이터는 snapshots/ 에서 로드. 없으면 "—".
Deep Work 비율 = (주 40h - 미팅시간) / 40h × 100. 미팅 과다 시 경고.

### 스킬 맵 (Skill Radar)
- **활발히 사용한 기술**: PR 제목, 커밋 메시지, Slack 대화에서 추출
- **새로 등장한 기술/도구**: 이전 스냅샷에 없던 기술이면 "🆕" 표시
- **역할 분포**: Engineering / Leadership / Communication / Documentation 비중

### 개선 제안 (What to Improve)
데이터 기반 2-3개. "이번 기간 X 데이터 기준으로, Y를 Z로 바꾸면 A 효과가 예상됨" 형태.

### 방향성 (Strategic Direction)
코치가 1:1에서 해줄 법한 피드백 톤으로 작성.

### 오너 관점 성과 분류 (Owner's Scorecard)
**기간이 2주 이상인 경우에만 생성.**

| 카테고리 | 성과 |
|----------|------|
| **매출/딜리버리** | 고객 대면 제품 출시, 파트너 시스템 구축, 매출 직결 기능 |
| **보안 리스크 감소** | 보안 취약점 수정, 권한 제어, 접근 통제 |
| **비용 감소** | 인프라 비용 절감, 성능 최적화, 자동화 |
| **운영 효율화** | CI/CD 개선, 모니터링, 프로세스 간소화 |
| **채용/홍보** | 발표, 블로그, 오픈소스 기여 |
| **팀 빌딩/리더십** | 미팅 주최, 온보딩, 멘토링, 크로스팀 협업 |

분류 기준: fix/security → 보안, perf/optimize → 비용, feat → 매출, chore/ci → 운영
```

## English Template (language: en)

Same structure with English headers: "Work Journal", "Summary", "Code & Engineering",
"Commits", "Pull Requests", "Code Reviews", "Communication (Slack)",
"Project Management (Jira)", "Meetings", "Documentation (Notion)",
"Insights" (Growth Metrics, Skill Radar, What to Improve, Strategic Direction, Owner's Scorecard).

## Conditional Sections

- Only include a section if the corresponding source was enabled AND collected successfully
- If a source was enabled but failed: note at bottom "Note: {source} data unavailable ({reason})"
- If only 1 source has data, still generate (even a meetings-only journal is useful)
