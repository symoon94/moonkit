# /issue-tracker

팀 단위 이슈 집계 보고서 생성기.

Slack과 Gmail에서 실수, 요청, 장애를 수집하고 심각도/영향 범위/빈도로 분류해서
임팩트가 큰 문제부터 정렬한 보고서를 만든다.

## 사용법

```
/issue-tracker              # 기본 기간으로 집계 (설정에 따라 이번 주/이번 달 등)
/issue-tracker last         # 직전 기간
/issue-tracker 2026-01      # 특정 월
/issue-tracker 2026-03-10 2026-03-24   # 커스텀 기간
/issue-tracker Q1           # 분기
/issue-tracker setup        # 셋업 재실행
```

## 첫 실행

처음 실행하면 인터랙티브 셋업이 시작된다:

1. **데이터 소스** - Slack, Gmail 중 선택
2. **팀 소개** - 팀명과 역할 (제외 필터/영향 범위 추출에 활용)
3. **영향 범위** - 자동 추출 / 직접 입력 / 자동+확인
4. **Slack 시그널** - 이모지 / 키워드 / 전체 스캔
5. **제외 조건** - 수집에서 빼고 싶은 키워드/주제
6. **기본 집계 기간** - 주간 / 격주 / 월간 / 분기
7. **출력 포맷** - HTML / Markdown / Notion (복수 선택 가능)

설정은 `~/.issue-tracker/config.yaml`에 저장되고 다음 호출 시 재사용된다.

## 워크플로우

```
Slack/Gmail 수집 → 이슈 분류(심각도/영향/빈도) → 임팩트 점수 계산 → 보고서 생성
```

### 임팩트 점수

```
점수 = 심각도 가중치(상3/중2/하1) x 영향 범위 수 x 빈도
```

### 출력

| 포맷 | 특징 |
|------|------|
| **HTML** | 인터랙티브 - 정렬, 필터, 검색, 이슈 삭제, 내보내기 |
| **Markdown** | Git 이력 관리용 |
| **Notion** | 팀 공유용 - 지정 페이지에 직접 작성 |

보고서에는 Executive Summary, 메인 이슈 테이블, 신규 이슈, TOP 3 권장 액션이 포함된다.

## 파일 구조

```
skills/issue-tracker/
  SKILL.md                          # 스킬 정의
  README.md                         # 이 파일
  references/
    report-template.html            # HTML 보고서 템플릿
```

## 필요한 MCP

- **Slack** - `slack_search_public_and_private`, `slack_read_channel`, `slack_read_thread`
- **Gmail** (선택) - `gmail_search_messages`, `gmail_read_message`, `gmail_read_thread`
- **Notion** (선택) - `notion-update-page`, `notion-create-pages`
