---
name: issue-tracker
version: 0.2.0
description: |
  팀 단위 이슈 집계 보고서 생성기. Slack과 Gmail에서 실수·요청·장애를 수집하고,
  심각도·영향 범위·빈도로 분류해서 정렬된 HTML 보고서를 만든다.
  첫 호출 시 인터랙티브 셋업으로 데이터 소스, 시그널, 영향 범위, 제외 조건을
  설정하고 저장한다. 이후 호출에서는 저장된 설정을 재사용하거나 새로 설정 가능.
  어떤 팀이든 사용 가능하도록 범용 설계.
  Trigger: "/issue-tracker", "이슈 집계", "이슈 보고서", "issue report",
  "월간 이슈", "이슈 트래킹", "뭐가 문제야", "반복 이슈"
  Use this skill whenever the user wants to collect, tally, or report on team-level
  issues, bugs, requests, or recurring problems from Slack or email — even if they
  don't say "issue tracker" explicitly.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__claude_ai_Slack__slack_search_public_and_private
  - mcp__claude_ai_Slack__slack_search_public
  - mcp__claude_ai_Slack__slack_read_channel
  - mcp__claude_ai_Slack__slack_read_thread
  - mcp__claude_ai_Slack__slack_read_user_profile
  - mcp__claude_ai_Slack__slack_search_channels
  - mcp__claude_ai_Gmail__gmail_search_messages
  - mcp__claude_ai_Gmail__gmail_read_message
  - mcp__claude_ai_Gmail__gmail_read_thread
  - mcp__claude_ai_Gmail__gmail_get_profile
  - mcp__claude_ai_Notion__notion-search
  - mcp__claude_ai_Notion__notion-create-pages
  - mcp__claude_ai_Notion__notion-update-page
  - mcp__claude_ai_Notion__notion-get-teams
---

# /issue-tracker — 팀 이슈 집계 보고서

Slack과 Gmail에서 팀의 실수·요청·장애를 수집하고, 임팩트가 큰 문제부터
정렬한 HTML 보고서를 만든다.

## User-invocable

사용자가 `/issue-tracker`를 입력하면 이 스킬을 실행한다.

## Arguments

- `/issue-tracker` — 설정된 주기에 따른 기본 기간 (주간이면 이번 주, 월간이면 이번 달)
- `/issue-tracker last` — 직전 주기 (주간이면 지난 주, 월간이면 지난 달)
- `/issue-tracker 2026-01` — 특정 월
- `/issue-tracker 2026-03-10 2026-03-24` — 커스텀 기간
- `/issue-tracker Q1` — 분기
- `/issue-tracker setup` — 셋업 강제 재실행

---

## Phase 0: 설정 로드 또는 인터랙티브 셋업

### Step 0: 기존 설정 확인

```bash
CONFIG_PATH="$HOME/.issue-tracker/config.yaml"
cat "$CONFIG_PATH" 2>/dev/null || echo "CONFIG_NOT_FOUND"
```

**설정이 존재하면** → 설정 요약을 보여주고 선택지를 제공한다:

```
question: "저장된 설정이 있습니다. 어떻게 할까요?"
header: "설정"
options:
  - label: "이 설정으로 진행 (Recommended)"
    description: "{팀명} | 소스: {sources} | 시그널: {signal} | 범위: {scope_mode}"
  - label: "설정 수정"
    description: "일부 항목만 변경합니다"
  - label: "새로 설정"
    description: "처음부터 다시 설정합니다"
```

**설정이 없거나**, arguments에 `setup`이 포함되면 → 풀 셋업 실행.

### Step 1: 인터랙티브 셋업 (첫 실행 또는 "새로 설정" 선택 시)

### Setup Call 1: 기본 맥락 (AskUserQuestion, 3문항)

**Q1. 데이터 소스**
```
question: "어떤 소스에서 이슈를 수집할까요?"
header: "데이터 소스"
multiSelect: true
options:
  - label: "Slack (Recommended)"
    description: "채널/DM에서 이슈 관련 메시지를 검색합니다"
  - label: "Gmail"
    description: "이메일에서 이슈 관련 스레드를 검색합니다"
```

**Q2. 팀 소개**
```
question: "어떤 팀인지, 주로 어떤 일을 하는지 한 줄로 알려주세요. (예: '솔라박스팀, 온프렘 에너지 솔루션 개발/운영')"
header: "팀 소개"
options:
  - label: "직접 입력"
    description: "팀명과 역할을 직접 작성합니다"
  - label: "건너뛰기"
    description: "팀 맥락 없이 범용으로 수집합니다"
```
> 이 답변은 제외 필터와 영향 범위 auto 추출의 맥락으로 사용된다.
> 예: "온프렘 팀"이라고 하면 SaaS 관련 이슈는 자동 제외 후보가 된다.

**Q3. 영향 범위 설정**
```
question: "이슈의 영향 범위(어떤 팀/조직이 영향받는지)를 어떻게 설정할까요?"
header: "영향 범위"
options:
  - label: "자동 추출 (Recommended)"
    description: "수집된 메시지에서 팀명·조직명을 자동으로 감지합니다. 빠르지만 정밀도가 낮을 수 있습니다."
  - label: "직접 입력"
    description: "영향 범위 목록을 직접 작성합니다. (예: 우리팀, EBS팀, 사업개발팀, 파트너사, 고객사)"
  - label: "자동 + 확인"
    description: "자동 추출 후 결과를 보여주고 수정할 기회를 줍니다"
```

### Setup Call 2: 시그널과 필터 (AskUserQuestion, 2~3문항)

**Q4. Slack 이슈 시그널** (Slack 선택 시에만)
```
question: "Slack에서 이슈를 식별하는 특별한 시그널이 있나요?"
header: "Slack 시그널"
options:
  - label: "특정 이모지"
    description: "예: :solarbox-issue: 같은 커스텀 이모지가 달린 메시지만 수집"
  - label: "키워드 패턴"
    description: "이슈성 키워드('장애', '오류', '요청' 등)가 포함된 메시지를 수집"
  - label: "이모지 + 키워드 둘 다"
    description: "이모지가 달린 것 + 키워드 매칭 메시지 모두 수집 (더 넓은 범위)"
  - label: "전체 스캔"
    description: "필터 없이 관련 채널 전체를 읽고 이슈성 메시지를 판별"
```
> "특정 이모지" 선택 시 → "Other"로 이모지 이름 입력받음 (예: `:solarbox-issue:`)
> "키워드 패턴" 선택 시 → 기본 패턴 사용 (아래 Phase 1 참조), 사용자가 추가 가능

**Q5. Gmail 필터** (Gmail 선택 시에만)
```
question: "Gmail에서 어떤 이메일을 이슈로 볼까요?"
header: "Gmail 필터"
options:
  - label: "특정 발신자/도메인"
    description: "예: 파트너사 도메인, 고객사 메일 등 — 발신자를 지정합니다"
  - label: "특정 라벨"
    description: "예: 'issues', '장애보고' 등 Gmail 라벨로 필터링"
  - label: "키워드 검색"
    description: "제목이나 본문에 이슈성 키워드가 포함된 메일을 검색"
```
> 선택에 따라 "Other"로 구체적인 발신자/라벨/키워드 입력받음

**Q6. 제외 조건**
```
question: "수집에서 제외할 것이 있나요? (예: 'SaaS 관련 이슈는 우리팀과 무관', '특정 채널은 제외')"
header: "제외 조건"
options:
  - label: "있음 — 직접 입력"
    description: "제외할 키워드, 채널, 주제를 작성합니다"
  - label: "없음"
    description: "필터 없이 전부 수집합니다"
```

### Setup Call 3: 주기 및 출력 설정 (AskUserQuestion, 2~3문항)

**Q7. 수집 주기**
```
question: "이슈를 얼마나 자주 집계할까요? 이 주기가 기본 기간으로 사용됩니다."
header: "수집 주기"
options:
  - label: "주간 (Recommended)"
    description: "매주 월~일 단위로 집계. 이슈를 빠르게 잡고 싶을 때."
  - label: "격주"
    description: "2주 단위로 집계. 스프린트와 맞출 때 좋음."
  - label: "월간"
    description: "매월 1일~말일 단위로 집계. 정기 리포트용."
  - label: "분기"
    description: "Q1~Q4 단위로 집계. 전략적 이슈 파악용."
```

**Q8. 출력 포맷**
```
question: "보고서를 어떤 형식으로 받을까요? (복수 선택 가능)"
header: "출력 포맷"
multiSelect: true
options:
  - label: "HTML (Recommended)"
    description: "인터랙티브 보고서 — 정렬, 필터, 검색, 이슈 삭제 가능"
  - label: "Markdown"
    description: "텍스트 기반 보고서 — Git으로 이력 관리하기 좋음"
  - label: "Notion"
    description: "Notion 페이지에 직접 작성 — 팀원과 바로 공유 가능"
```
> DOCX가 필요하면 "Other"로 입력 가능

**Q9. Notion 페이지** (Notion 선택 시에만)
```
question: "보고서를 작성할 Notion 페이지 URL을 붙여넣어 주세요."
header: "Notion 페이지"
options:
  - label: "URL 입력"
    description: "기존 페이지에 작성합니다 (예: https://notion.so/...)"
  - label: "새 페이지 생성"
    description: "지정한 스페이스에 새 페이지를 만듭니다"
```
> "URL 입력" 선택 시 → "Other"로 Notion URL을 붙여넣음
> "새 페이지 생성" 선택 시 → `notion-search`로 스페이스 목록을 보여주고 선택

### Step 3: 설정 저장

셋업 답변을 YAML로 정리하고 `~/.issue-tracker/config.yaml`에 저장한다.
다음 호출 때 이 파일을 읽어서 재사용한다.

```bash
mkdir -p "$HOME/.issue-tracker"
```

```yaml
# ~/.issue-tracker/config.yaml
team: "솔라박스팀, 온프렘 에너지 솔루션"
sources:
  - slack
  - gmail
scope_mode: auto           # auto | manual | auto_confirm
scope_list:                # manual / auto_confirm일 때
  - 우리팀
  - EBS팀
  - 파트너사
  - 고객사
slack:
  signal: emoji             # emoji | keyword | both | full_scan
  emoji: ":solarbox-issue:"
  channels: []              # full_scan일 때 사용
gmail:
  filter_type: sender       # sender | label | keyword
  filter_value: "@partner.com"
exclusions:
  - SaaS
  - console 장애
frequency: weekly           # weekly | biweekly | monthly | quarterly
output:
  formats:                   # 복수 선택 가능
    - html
    - markdown
    - notion
  notion_page: "https://notion.so/..."  # notion 선택 시
  dir: output
```

> "설정 수정" 선택 시에는 기존 config.yaml을 읽은 뒤,
> 수정하고 싶은 항목만 AskUserQuestion으로 물어본다.

### 내부 참조용 설정 객체

이후 Phase에서는 config.yaml의 내용을 아래 구조로 참조한다:

```
SETUP = {
  sources: ["slack", "gmail"],
  team: "솔라박스팀, 온프렘 에너지 솔루션",
  scope_mode: "auto" | "manual" | "auto_confirm",
  scope_list: [...],
  slack_signal: "emoji" | "keyword" | "both" | "full_scan",
  slack_emoji: ":solarbox-issue:",
  slack_channels: [],
  gmail_filter: { type: "sender"|"label"|"keyword", value: "..." },
  exclusions: ["SaaS", "console 장애"],
  frequency: "weekly" | "biweekly" | "monthly" | "quarterly",
  output_formats: ["html", "markdown", "notion"],
  notion_page: "https://notion.so/...",
}
```

---

## Phase 1: 기간 계산

**명시적 기간 지정 시** (arguments에 날짜/월/분기가 있으면):
- `2026-01` → 해당 월 1일 ~ 말일
- `2026-03-10 2026-03-24` → 커스텀 기간 그대로 사용
- `Q1`~`Q4` → 분기 경계

**`last` 또는 인자 없이 호출 시** → `SETUP.frequency`에 따라 기간을 계산:

| frequency | `/issue-tracker` (현재 기간) | `/issue-tracker last` (직전 기간) |
|-----------|------------------------------|-----------------------------------|
| **weekly** | 이번 주 월요일 ~ 오늘 | 지난 주 월~일 |
| **biweekly** | 이번 격주 시작일 ~ 오늘 | 직전 2주 |
| **monthly** | 이번 달 1일 ~ 오늘 | 지난 달 1일 ~ 말일 |
| **quarterly** | 이번 분기 시작일 ~ 오늘 | 직전 분기 |

```bash
# 예: monthly (기본값)
YEAR=$(date +%Y)
MONTH=$(date +%m)
PERIOD_START="${YEAR}-${MONTH}-01"
PERIOD_END=$(date +%Y-%m-%d)
PERIOD_LABEL="${YEAR}년 ${MONTH}월"

# 예: weekly
DOW=$(date +%u)  # 1=월 ~ 7=일
PERIOD_START=$(date -v-$((DOW-1))d +%Y-%m-%d)  # 이번 주 월요일
PERIOD_END=$(date +%Y-%m-%d)
PERIOD_LABEL="$(date -v-$((DOW-1))d +%m/%d) ~ $(date +%m/%d)"
```

frequency가 설정되지 않았으면 **monthly**를 기본값으로 사용한다.

---

## Phase 2: 데이터 수집

SETUP 설정에 따라 소스별로 수집한다. 각 소스는 독립적 — 하나가 실패해도 나머지 진행.

> **DM/비공개 채널 주의**: `slack_search_public_and_private`는 DM과 비공개 채널도
> 검색한다. 셋업 시 사용자에게 이 사실을 안내한다:
> "Slack 검색은 공개 채널뿐 아니라 비공개 채널과 DM도 포함됩니다.
> 민감한 대화 내용이 보고서에 포함될 수 있으니 유의하세요."

> **수집 상한**: 소스별 최대 200건까지 수집한다. 200건을 초과하면 수집을 중단하고
> 사용자에게 알린다: "200건 이상 수집됨 — 최근 200건만 분석합니다."
> 스레드 읽기도 상위 100개 메시지까지만 수행한다.

### 2a. Slack 수집

시그널 모드에 따라 검색 쿼리를 구성한다:

**이모지 모드** (`slack_signal: "emoji"`):
```
slack_search_public_and_private:
  query: "has:{SETUP.slack_emoji} after:{PERIOD_START} before:{PERIOD_END}"
  limit: 100, sort: "timestamp"
```
결과 0건이면 텍스트 매칭으로 폴백:
```
  query: "{SETUP.slack_emoji} after:{PERIOD_START} before:{PERIOD_END}"
```

**키워드 모드** (`slack_signal: "keyword"`):
기본 키워드 패턴으로 검색한다. 한 번에 모든 키워드를 넣지 말고, 카테고리별로 나눠서 검색:

```
# 장애/오류 계열
query: "(장애 OR 오류 OR 에러 OR 실패 OR 버그) after:{PERIOD_START}"

# 요청/필요 계열
query: "(요청 OR 필요 OR 해주세요 OR 부탁) after:{PERIOD_START}"

# 반복/불만 계열
query: "(또 OR 매번 OR 반복 OR 왜 항상) after:{PERIOD_START}"
```

**전체 스캔** (`slack_signal: "full_scan"`):
`slack_channels`에 지정된 채널을 `slack_read_channel`로 읽는다.
채널이 지정되지 않았으면 사용자에게 채널 목록을 요청한다.

**모든 모드 공통 — 스레드 확인**:
각 메시지의 스레드를 `slack_read_thread`로 읽어서:
- 재발 여부 ("또 발생", "이번에도", "다시")
- 영향 받은 팀/조직 언급
- 해결 여부 ("해결됨", "완료", "fixed", "closed")
- **permalink 수집** — 각 메시지의 Slack 링크를 저장 (보고서에 첨부용)

**제외 필터 적용**:
`SETUP.exclusions`에 포함된 키워드가 메시지에 있으면 해당 메시지를 제외한다.
팀 맥락도 활용 — 예: 팀 소개에 "온프렘"이 있고 제외에 "SaaS"가 있으면,
"SaaS Console 장애" 같은 메시지는 자동 제외.

### 2b. Gmail 수집

SETUP.gmail_filter에 따라 검색:

**발신자/도메인 모드**:
```
gmail_search_messages:
  query: "from:{value} after:{PERIOD_START} before:{PERIOD_END}"
  max_results: 50
```

**라벨 모드**:
```
gmail_search_messages:
  query: "label:{value} after:{PERIOD_START} before:{PERIOD_END}"
  max_results: 50
```

**키워드 모드**:
```
gmail_search_messages:
  query: "(장애 OR 오류 OR 요청 OR 이슈) after:{PERIOD_START} before:{PERIOD_END}"
  max_results: 50
```

각 메일에 대해 `gmail_read_message`로 본문을 읽고, 스레드가 있으면
`gmail_read_thread`로 전체 맥락을 파악한다.

### 2c. 수집 결과 0건 처리

모든 소스에서 0건이면:
> "{PERIOD_LABEL} 기간에 이슈를 찾지 못했습니다.
> Slack에서 이슈에 {SETUP.slack_emoji} 이모지를 달거나,
> 이슈 관련 키워드가 포함된 메시지를 확인해주세요."

빈 보고서는 생성하지 않는다.

---

## Phase 3: 이슈 분류

수집된 메시지를 3개 축으로 분류한다.

### 3a. 심각도 (severity)

| 등급 | 정의 | 판별 시그널 |
|------|------|------------|
| **상** | 없으면 업무가 막히는 것 | "장애", "블로커", "긴급", "서비스 중단", "데이터 유실", "배포 실패", "고객 이탈", "P0", "hotfix" |
| **중** | 해결하면 확실히 나아지는 것 | "반복", "수작업", "비효율", "누락", "불일치", "지연", "매번", "개선 필요" |
| **하** | 있으면 좋은 것 | "개선", "제안", "있으면 좋겠", "UI", "편의", "나중에", "nice to have" |

**보정 규칙** (시그널만으로 판단이 애매할 때):
- 동일 이슈 3회 이상 반복 → 한 단계 올림 (하→중, 중→상)
- 외부 영향 (고객사/파트너사) → 한 단계 올림
- 이미 해결된 이슈도 발생 사실 자체를 기록한다 (심각도를 내리지 않음)

### 3b. 영향 범위 (scope)

**scope_mode에 따라 다르게 동작한다:**

**manual 모드**: `SETUP.scope_list`에 있는 범위만 사용.
메시지 내용에서 해당 범위와 관련된 언급이 있으면 태깅한다.

**auto 모드**: 메시지에서 팀명·조직명·회사명을 추출한다.
추출 전략:
1. 명시적 팀명 언급 ("EBS팀에서", "제품팀이", "파트너사가")
2. 채널 이름에서 추론 (#ebs-연동 → EBS팀)
3. 메일 발신자 도메인에서 추론 (partner.com → 파트너사)
4. 맥락 기반 추론 ("고객이 불만", "API 연동 오류" 등)

추출된 범위는 자연스러운 단위로 그룹핑:
- 내부 팀들: 각 팀명 그대로
- 외부: "파트너사", "고객사", "협업사" 등으로 통합
- 자기 팀은 항상 포함 (이슈 제보의 기본 주체)

**auto_confirm 모드**: auto로 추출한 뒤, 결과를 AskUserQuestion으로 보여주고
사용자가 수정/확인할 수 있게 한다:
```
question: "자동 추출된 영향 범위입니다. 수정이 필요한가요?"
options:
  - "이대로 진행 (Recommended)"
  - "수정 필요"
```

### 3c. 빈도 카운트 (frequency)

1. 각 메시지에서 핵심 이슈를 한 줄로 요약
2. 유사한 이슈를 그룹핑 (예: "토큰 만료" + "인증 실패" → 같은 그룹)
3. 그룹당 발생 건수를 카운트
4. 같은 날 같은 사람의 중복 언급도 별도 건수로 카운트
5. 각 그룹에 원본 Slack permalink / Gmail 링크를 모아둔다
6. **대표 메시지 1개를 선정한다** — 그룹 내에서 이슈를 가장 잘 설명하는 메시지의
   원문 내용(snippet)을 저장. 보고서에서 이 이슈가 구체적으로 어떤 맥락인지
   바로 파악할 수 있게 하기 위함.

**누락 방지 규칙**: 수집된 메시지 중 어떤 그룹에도 속하지 않는 것은
"기타"로 묶지 말고 **1건짜리 별개 이슈**로 등록한다.
모든 수집된 이슈는 하나도 빠지지 않고 최종 테이블에 포함되어야 한다.
그룹핑 후 전체 건수의 합이 수집된 원본 건수와 일치하는지 검증한다.

### 3d. 소스 태깅

각 이슈에 출처를 태깅한다: `slack` / `gmail` / `both`
동일 이슈가 Slack과 Gmail 양쪽에서 발견되면 `both`로 태깅하고 빈도 합산.

---

## Phase 4: 임팩트 점수

```
임팩트 점수 = 심각도 가중치 × 영향 범위 수 × 빈도
```

| 심각도 | 가중치 |
|--------|--------|
| 상 | 3 |
| 중 | 2 |
| 하 | 1 |

이 점수는 "이 이슈를 해결하면 팀 전체에 얼마나 임팩트가 큰지"를 나타낸다.
완벽한 정량 지표는 아니지만, 어떤 문제부터 손대야 하는지 우선순위를 잡는 데 유용하다.

---

## Phase 5: 보고서 생성

`SETUP.output_formats`에 선택된 포맷별로 보고서를 생성한다. 복수 선택 시 모두 생성.

### 공통 데이터 구조

모든 포맷이 동일한 데이터를 사용한다:

```javascript
const DATA = [
  {
    issue: "이슈 제목 (한 줄 요약)",
    severity: "상|중|하",
    scopes: ["우리팀", "EBS팀", ...],
    freq: 숫자,
    source: "slack|gmail|both",
    firstSeen: "2026-03-05",
    lastSeen: "2026-03-25",
    resolved: false,
    snippet: "파트너 A 토큰이 또 만료돼서 데이터 싱크가 3시간 중단됨...",  // 대표 메시지 원문 (1개)
    snippetLink: "https://team.slack.com/archives/...",                    // 대표 메시지 permalink
    links: [
      { type: "slack", url: "https://team.slack.com/archives/...", text: "3/5 — 원본 메시지" },
      { type: "gmail", url: "https://mail.google.com/...", text: "3/8 — 관련 메일" }
    ]
  },
  ...
];
```

### 공통 보고서 구조

포맷에 상관없이 아래 구조를 따른다:

**1. 헤더**: 팀명, 집계 기간, 생성 일시

**2. Executive Summary (카드 4장)**

| 카드 | 내용 |
|------|------|
| 총 이슈 | 고유 이슈 수 + 전월 대비 증감 |
| 심각도 상 | 상 등급 건수 |
| 최다 빈도 | 가장 많이 발생한 이슈명 |
| 최다 영향 | 가장 많은 이슈에 등장한 범위 |

**3. 메인 테이블** (기본 정렬: 심각도→영향 범위 수→빈도)

| 컬럼 | 설명 |
|------|------|
| # | 순위 |
| 심각도 | 상/중/하 |
| 이슈 | 한 줄 요약 + 링크 |
| 영향 범위 | 범위별 태그 |
| 빈도 | 발생 건수 |
| 점수 | 임팩트 점수 |

**4. 신규 이슈**: 이번 기간 처음 등장한 이슈. 전월 보고서 없으면 "첫 집계"로 표시.

**5. 권장 액션 — TOP 3**: 임팩트 상위 3개 이슈별로:
- 왜 임팩트가 큰지 (1~2문장)
- 제안하는 다음 스텝 (1~2개)
- Slack/Gmail 링크 예시 (2~3개)

---

### 5a. HTML 출력

`references/report-template.html`을 읽어서 DATA를 주입한다.

**인터랙티브 기능:**
- 컬럼 헤더 클릭 재정렬
- 텍스트 검색, 심각도/영향 범위 필터
- 빈도 막대 그래프

**이슈 삭제 기능 (HTML 전용):**

각 행에 `×` 버튼을 표시한다. 클릭하면:
1. 해당 행이 취소선 + 페이드 애니메이션으로 사라짐
2. 상단에 "삭제됨: N건" 카운터와 "되돌리기" 버튼 표시
3. 삭제된 이슈는 테이블 아래 "제외된 이슈" 접힌 섹션에 모임
4. Executive Summary와 임팩트 점수가 실시간 재계산됨

이 기능이 필요한 이유: 자동 수집은 오탐이 있을 수 있고, 보고서를 공유하기 전에
우리 팀과 무관한 이슈를 걸러내고 싶을 때 유용하다.

```javascript
// 삭제 버튼 클릭 핸들러 (개념)
function dismissIssue(index) {
  dismissed.push(DATA[index]);
  DATA.splice(index, 1);
  render();                    // 테이블 + 카드 모두 재렌더
  updateDismissedPanel();      // "제외된 이슈" 패널 업데이트
}

function undoLastDismiss() {
  const restored = dismissed.pop();
  DATA.push(restored);
  DATA.sort(defaultSort);
  render();
}
```

**"정리된 보고서 내보내기" 버튼:**
삭제 후 최종 상태를 새 HTML 파일로 다운로드할 수 있다.
공유용으로 깔끔하게 정리된 버전을 만들 때 사용.

저장: `{OUTPUT_DIR}/issue-tracker-{YEAR}-{MONTH}.html`

---

### 5b. Markdown 출력

같은 데이터를 Markdown 테이블 + 링크 형식으로 생성한다.
Git 이력 관리나 PR에 첨부하기 좋은 포맷.

```markdown
# 이슈 집계 보고서 — {SETUP.team}
**기간**: {PERIOD_LABEL} | **총 이슈**: {N}건

## Executive Summary
- 심각도 상: {N}건 | 중: {N}건 | 하: {N}건
- 최다 빈도: {이슈명} ({N}회)
- 최다 영향: {범위명} ({N}건)

## 이슈 목록
| # | 심각도 | 이슈 | 영향 범위 | 빈도 | 점수 |
|---|--------|------|----------|------|------|
| 1 | 상 | [이슈명](slack-link) | 우리팀, EBS팀 | 12 | 72 |
...

## 권장 액션
### 1. {이슈명} (점수: {N})
**임팩트**: ...
**다음 스텝**: ...
**참고**: [3/5 메시지](link), [3/12 메시지](link)
```

저장: `{OUTPUT_DIR}/issue-tracker-{YEAR}-{MONTH}.md`

---

### 5c. Notion 출력

`notion-update-page` 또는 `notion-create-pages` MCP로 Notion에 직접 작성한다.

**기존 페이지에 작성** (`SETUP.notion_page` URL 제공 시):
1. URL에서 page_id를 추출
2. `notion-update-page`로 페이지 내용을 업데이트

**새 페이지 생성** (URL 미제공 시):
1. `notion-search`로 워크스페이스 내 대상 페이지/DB를 찾음
2. `notion-create-pages`로 하위 페이지 생성

**Notion 페이지 구조:**
- 제목: `이슈 집계 — {SETUP.team} {PERIOD_LABEL}`
- Executive Summary를 callout 블록으로
- 이슈 목록을 테이블 블록으로 (심각도·영향 범위·빈도·점수)
- 각 이슈에 Slack permalink를 인라인 링크로 첨부
- 권장 액션을 toggle heading으로

> Notion은 팀원과 바로 공유할 수 있어서 리뷰용으로 편리하다.
> 다만 정렬/필터/삭제 같은 인터랙티브 기능은 HTML에만 있으므로,
> 정리 작업이 필요하면 HTML을 먼저 만들고 Notion은 최종본으로 사용하는 것을 권장.

---

### 저장 경로 요약

| 포맷 | 파일/위치 |
|------|----------|
| HTML | `{OUTPUT_DIR}/issue-tracker-{PERIOD_START}--{PERIOD_END}.html` |
| Markdown | `{OUTPUT_DIR}/issue-tracker-{PERIOD_START}--{PERIOD_END}.md` |
| Notion | 지정된 Notion 페이지 (URL 출력) |

---

## Phase 6: 완료 보고

```markdown
## 이슈 집계 완료

**팀**: {SETUP.team}
**기간**: {PERIOD_LABEL}

| 항목 | 수치 |
|------|------|
| Slack 메시지 수집 | {N}건 |
| Gmail 메일 수집 | {N}건 |
| 고유 이슈 (그룹핑 후) | {N}건 |
| 심각도 상 / 중 / 하 | {N} / {N} / {N} |
| 영향 범위 | {N}개 팀·조직 감지 |

**TOP 3 임팩트 이슈:**
1. {이슈명} — 점수 {N} (심각도 상, {N}개 팀, {N}회)
2. ...
3. ...

**저장된 파일:** `{path}`
```

---

## Error Handling

| 상황 | 대응 |
|------|------|
| Slack MCP 미연결 | "Slack MCP가 연결되지 않았습니다" 안내, Gmail만으로 진행 가능 |
| Gmail MCP 미연결 | Gmail 없이 Slack만으로 진행 |
| 모든 소스 실패 | 에러 안내 후 종료 |
| 수집 0건 | 안내 메시지 출력, 빈 보고서 생성하지 않음 |
| 이모지 검색 0건 | 텍스트 매칭으로 폴백, 그래도 0건이면 사용자에게 안내 |
| 분류 애매 | 보수적 판단 — 심각도는 높은 쪽, 영향 범위는 넓은 쪽 |
| 영향 범위 auto 추출이 너무 적음 | "팀", "협업사", "고객사" 3개로 최소 분류 |
