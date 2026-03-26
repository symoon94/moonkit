---
name: weekly-log
version: 0.1.0
description: |
  Weekly work journal and resume auto-updater. Collects activity from GitHub,
  Slack, Jira, Google Calendar, and Notion — each source toggleable on/off.
  Generates a markdown journal, maintains a brag document, and updates your resume.
  Trigger: "/weekly-log", "주간 업무일지", "weekly journal", "work log", "이력서 업데이트"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# /weekly-log — Weekly Work Journal & Resume Updater

Collect your weekly activity from up to 5 sources, generate a structured work journal,
maintain a cumulative brag document, and auto-update your resume.

## User-invocable

When the user types `/weekly-log`, run this skill.

## Arguments

- `/weekly-log` — current week (Monday to today)
- `/weekly-log last` — previous full week (Monday to Sunday)
- `/weekly-log 2026-01-01 2026-03-22` — custom date range (start end)
- `/weekly-log Q1` — current year Q1 (Jan 1 ~ Mar 31)
- `/weekly-log setup` — re-run first-time setup wizard

## Execution Mode Detection

Determine if this is an **interactive** or **automated** run:
- If the user typed `/weekly-log` in a conversation → **interactive mode** (use AskUserQuestion)
- If running as a scheduled task (no active user conversation) → **automated mode** (skip all AskUserQuestion, never modify resume directly)

---

## Phase 0: Config Load

### Step 1: Read config

```bash
cat ~/.weekly-log/config.yaml 2>/dev/null || echo "CONFIG_NOT_FOUND"
```

If `CONFIG_NOT_FOUND` or `$ARGUMENTS` contains `setup`, run the **First-Run Wizard** below.
Otherwise, parse the YAML config.

### Step 2: First-Run Wizard (interactive only)

Use a single AskUserQuestion call with up to 3 questions:

1. **Language**: "업무일지 언어를 선택하세요" — options: "한국어 (ko)", "English (en)"
2. **Sources**: "어떤 소스를 활성화할까요?" (multiSelect) — options: "GitHub", "Slack", "Jira", "Google Calendar", "Notion"
3. **Output directory**: "업무일지 저장 경로" — options: "~/weekly-log (Recommended)", "~/Documents/weekly-log", "Custom path"

Then generate `~/.weekly-log/config.yaml` using the Write tool with the user's choices.
Use the template from the skill's `config.example.yaml` as the base structure.
All source-specific fields (username, user_id, repos, etc.) are left empty for auto-discovery.

After writing the config, ask if the user wants to set up a **Saturday scheduled task**:
- If yes: use the `create_scheduled_task` MCP tool:
  - taskId: "weekly-log"
  - cronExpression: "0 10 * * 6" (Saturday 10 AM)
  - description: "주간 업무일지 자동 생성 및 이력서 갱신"
  - prompt: Read this SKILL.md file and execute it in automated mode. Config is at ~/.weekly-log/config.yaml.

### Step 3: Calculate date range

```bash
# Get current day of week (1=Monday, 7=Sunday)
DOW=$(date +%u)

# This week's Monday at 00:00 (default)
if [ "$(uname)" = "Darwin" ]; then
  WEEK_START=$(date -v-$((DOW-1))d +%Y-%m-%d)
else
  WEEK_START=$(date -d "last Monday" +%Y-%m-%d)
fi
WEEK_END=$(date +%Y-%m-%d)

echo "RANGE: $WEEK_START to $WEEK_END"
```

If `$ARGUMENTS` contains two dates (YYYY-MM-DD YYYY-MM-DD format):
```bash
WEEK_START={first date}
WEEK_END={second date}
```

If `$ARGUMENTS` contains `Q1`, `Q2`, `Q3`, or `Q4`:
```bash
YEAR=$(date +%Y)
# Q1: Jan 1 ~ Mar 31, Q2: Apr 1 ~ Jun 30, Q3: Jul 1 ~ Sep 30, Q4: Oct 1 ~ Dec 31
```

If `$ARGUMENTS` contains `last`:
```bash
# Previous week: Monday to Sunday
if [ "$(uname)" = "Darwin" ]; then
  WEEK_START=$(date -v-$((DOW+6))d +%Y-%m-%d)
  WEEK_END=$(date -v-${DOW}d +%Y-%m-%d)
else
  WEEK_START=$(date -d "last Monday -7 days" +%Y-%m-%d)
  WEEK_END=$(date -d "last Sunday" +%Y-%m-%d)
fi
```

### Step 4: Ensure output directories

```bash
OUTPUT_DIR=$(grep 'output_dir:' ~/.weekly-log/config.yaml | awk '{print $2}' | sed "s|~|$HOME|")
mkdir -p "$OUTPUT_DIR/journals" "$OUTPUT_DIR/snapshots" "$OUTPUT_DIR/pending-resume-updates"
echo "OUTPUT_DIR: $OUTPUT_DIR"
```

---

## Phase 1: Data Collection

Collect data from each enabled source independently. If a source fails, log the error and continue with the remaining sources. Track which sources succeeded and which failed.

Initialize tracking variables mentally:
- `collected_sources`: list of successfully collected sources
- `failed_sources`: list of sources that failed with reasons
- `github_data`, `slack_data`, `jira_data`, `calendar_data`, `notion_data`: collected results

### 1a. GitHub (if enabled)

Use Bash with the `gh` CLI. Auto-detect everything.

**Step 1: Detect username**
```bash
gh api user --jq '.login' 2>/dev/null || echo "GH_AUTH_FAILED"
```
If `GH_AUTH_FAILED`: add GitHub to failed_sources with reason "gh CLI not authenticated", skip to next source.

**Step 2: Discover active repos**
```bash
# Get repos I recently pushed to or interacted with
gh api users/{username}/events --paginate --jq '
  [.[] | select(.created_at >= "{WEEK_START}T00:00:00Z") | .repo.name] | unique | .[]
' 2>/dev/null
```

Apply filters from config:
- If `repos_include` is set and non-empty: only keep repos in that list
- If `repos_exclude` is set: remove repos in that list

**Step 3: For each repo, collect data (run these in parallel per repo)**

Commits:
```bash
gh api repos/{owner}/{repo}/commits \
  -f since="{WEEK_START}T00:00:00Z" -f author="{username}" \
  --jq '.[] | {sha: .sha[0:7], message: (.commit.message | split("\n")[0]), date: .commit.author.date}' \
  2>/dev/null
```

PRs authored:
```bash
gh pr list -R {owner}/{repo} --author {username} --state all \
  --json number,title,state,createdAt,mergedAt,url \
  --jq '[.[] | select(.createdAt >= "{WEEK_START}T00:00:00Z")]' \
  2>/dev/null
```

PRs reviewed:
```bash
gh api search/issues \
  -f q="type:pr reviewed-by:{username} repo:{owner}/{repo} updated:>={WEEK_START}" \
  --jq '.items | [.[] | {number: .number, title: .title, url: .html_url}]' \
  2>/dev/null
```

### 1b. Slack (if enabled)

Use the `slack_read_user_profile` MCP tool (no user_id parameter) to get the current user's Slack user ID automatically.

Then use the `slack_search_public` MCP tool:
```
query: "from:<@{user_id}> after:{WEEK_START} before:{WEEK_END}"
limit: 20
sort: "timestamp"
include_context: false
```

If `channels_include` is configured, run additional filtered searches:
```
query: "from:<@{user_id}> in:#{channel} after:{WEEK_START} before:{WEEK_END}"
```

If `channels_exclude` is configured, filter out messages from those channels from results.

Summarize the collected messages: group by channel, extract key topics and threads.

If Slack MCP tools are not available: add to failed_sources, skip.

### 1c. Jira (if enabled)

**Strategy: try MCP first, fall back to REST.**

Try to use the Jira/Atlassian MCP tool to search issues:
- JQL: `assignee = currentUser() AND updated >= "{WEEK_START}"`
- If `projects_include` is set: add `AND project IN ({projects})`
- If `projects_exclude` is set: add `AND project NOT IN ({projects})`

If MCP tool is not available, check for REST config:
- If `base_url` is set in config:
```bash
# Requires JIRA_API_TOKEN and JIRA_EMAIL env vars
JIRA_AUTH=$(echo -n "${JIRA_EMAIL}:${JIRA_API_TOKEN}" | base64)
curl -s -H "Authorization: Basic $JIRA_AUTH" -H "Content-Type: application/json" \
  "{base_url}/rest/api/3/search?jql=assignee=currentUser()+AND+updated>='{WEEK_START}'&fields=key,summary,status,priority,updated" \
  2>/dev/null
```

If both fail: add to failed_sources with reason, skip.

### 1d. Google Calendar (if enabled)

Use the `gcal_list_events` MCP tool:
- timeMin: "{WEEK_START}T00:00:00"
- timeMax: "{WEEK_END}T23:59:59"
- calendarId: from config `calendar_ids` (default: "primary")

From the results, filter to events where:
- `myResponseStatus` is "accepted", "tentative", or the user is the organizer
- Skip declined events unless `include_declined: true` in config

Extract: summary (title), start/end time, duration, number of attendees.

If Calendar MCP tools are not available: add to failed_sources, skip.

### 1e. Notion (if enabled)

Use the `notion-search` MCP tool:
- query: "" (search everything)
- filters: `{ created_date_range: { start_date: "{WEEK_START}" } }`

If `workspace_filter` is set in config, use `page_url` parameter to scope the search.

From results, extract: page title, URL, last edited time.

If Notion MCP tools are not available: add to failed_sources, skip.

---

## Phase 2: Journal Generation

Based on the config `language` field, generate the journal in the appropriate language.
Use the collected data to fill in each section. Only include sections for sources that
were successfully collected.

### Korean Template (language: ko)

**Important**: Derive day-of-week labels from the actual dates using `date` command, NOT hardcoded.
WEEK_START is always Monday (월). For WEEK_END, compute the actual day of week:
```bash
# Get Korean day-of-week label for WEEK_END
WEEK_END_DOW=$(LC_ALL=ko_KR.UTF-8 date -j -f "%Y-%m-%d" "{WEEK_END}" "+%a" 2>/dev/null || date -d "{WEEK_END}" "+%a")
```

```markdown
# 주간 업무일지
**기간**: {WEEK_START} (월) ~ {WEEK_END} ({WEEK_END_DOW})  |  **작성일**: {today}

---

## 요약
{LLM이 전체 활동을 1-3문장으로 자연스럽게 요약. 핵심 성과와 주요 활동을 포함.}

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

| 지표 | 이번 주 | 전주 | 변화 |
|------|---------|------|------|
| 커밋 수 | {N} | {N or "—"} | {↑/↓/→} |
| PR 머지 | {N} | {N or "—"} | {↑/↓/→} |
| 미팅 시간 | {N}h | {N or "—"} | {↑/↓/→} |
| Deep Work 비율 | {추정}% | {N or "—"} | {↑/↓/→} |
{전주 데이터는 이전 스냅샷(snapshots/)에서 로드. 없으면 "—"으로 표시.
Deep Work 비율 = (주 40h - 미팅시간) / 40h × 100. 미팅 과다 시 경고.}

### 스킬 맵 (Skill Radar)
{이번 주 활동에서 감지된 기술 스택과 역할 영역을 정리.
- **활발히 사용한 기술**: PR 제목, 커밋 메시지, Slack 대화에서 추출 (e.g., AWS CDK, GitHub Actions, Redis, Go 등)
- **새로 등장한 기술/도구**: 이전 스냅샷에 없던 기술이 이번 주에 등장하면 "🆕" 표시
- **역할 분포**: 이번 주 활동 비중을 분류 — Engineering / Leadership / Communication / Documentation
  예: "Engineering 60% | Leadership 20% | Communication 15% | Documentation 5%"}

### 개선 제안 (What to Improve)
{데이터 기반으로 구체적이고 실행 가능한 개선 제안 2-3개.
분석 기준:
- 미팅/코딩 비율이 비정상적이면 → "미팅 최적화" 제안
- 한 레포에 커밋이 편중되면 → "기술 부채 또는 병목" 가능성 언급
- PR이 많은데 리뷰가 적으면 → "코드 리뷰 프로세스" 제안
- Slack 메시지가 과다하면 → "비동기 커뮤니케이션 전환" 제안
제안은 "~하면 좋겠다" 형태가 아니라, "이번 주 X 데이터 기준으로, Y를 Z로 바꾸면 A 효과가 예상됨" 형태로 구체적으로.}

### 방향성 (Strategic Direction)
{현재 맡고 있는 프로젝트/제품의 맥락에서, 이번 주 활동이 시사하는 전략적 방향.
분석 기준:
- 이번 주 가장 많은 시간을 쓴 영역이 장기적으로 어떤 의미인지
- PR/커밋 패턴에서 보이는 제품 진화 방향 (e.g., "버그픽스 위주 → 안정화 단계", "신규 프로젝트 시작 → 확장기")
- Slack 대화에서 감지되는 팀/시장 트렌드 (e.g., 특정 기술/고객 이슈가 반복 언급)
- 다음 주에 집중해야 할 영역 제안
이 섹션은 "코치가 1:1에서 해줄 법한 피드백" 톤으로 작성.}

### 오너 관점 성과 분류 (Owner's Scorecard)
{**기간이 2주 이상인 경우에만 이 섹션을 생성.**
수집된 활동을 경영진/오너가 중시하는 카테고리로 재분류.
각 카테고리에 해당하는 구체적 성과를 나열하고, 성과가 없는 카테고리도 빈칸으로 표시하여 커버리지를 시각화.

| 카테고리 | 성과 |
|----------|------|
| **매출/딜리버리** | 고객 대면 제품 출시, 파트너 시스템 구축, 딜리버리 완료, 매출에 직결되는 기능 릴리즈 |
| **보안 리스크 감소** | 보안 취약점 수정, 권한 제어 강화, 암호화 도입, 접근 통제 개선 |
| **비용 감소** | 인프라 비용 절감, 성능 최적화, 자동화로 인한 인건비 절감, 리소스 효율화 |
| **운영 효율화** | CI/CD 개선, 자동화 파이프라인, 모니터링, 프로세스 간소화, dev 경험 향상 |
| **채용/홍보** | 발표, 블로그, 오픈소스 기여, 기술 브랜딩, 채용에 도움되는 활동 |
| **팀 빌딩/리더십** | 미팅 주최, 온보딩, 멘토링, 팀 문화 활동, 크로스팀 협업 주도 |

분류 기준:
- PR/커밋 메시지의 키워드로 판단 (fix/security → 보안, perf/optimize → 비용, feat → 매출, chore/ci → 운영)
- Slack 대화 토픽에서 고객/파트너 관련 → 매출, 내부 프로세스 → 운영
- 미팅 제목에서 "onboarding", "lunch", "team" → 팀 빌딩
- 발표/컨퍼런스 → 채용/홍보
하나의 성과가 복수 카테고리에 해당하면 가장 임팩트가 큰 쪽에 배치.}
```

### English Template (language: en)

Use equivalent English headers: "Weekly Work Journal", "Summary", "Code & Engineering",
"Commits", "Pull Requests", "Code Reviews", "Communication (Slack)",
"Project Management (Jira)", "Meetings", "Documentation (Notion)",
"Insights" (with sub-sections: "Growth Metrics", "Skill Radar", "What to Improve", "Strategic Direction").

### Conditional Sections

- Only include a section if the corresponding source was enabled AND collected successfully
- If a source was enabled but failed, add a note at the bottom: "Note: {source} data could not be collected ({reason})"
- If only 1 source has data, still generate the journal (even a meetings-only journal is useful)

### Save the journal

```bash
# Save to output directory
JOURNAL_PATH="{OUTPUT_DIR}/journals/{WEEK_END}.md"
```

Use the Write tool to save the journal markdown to this path.

---

## Phase 3: Brag Document Update

The brag document is a cumulative record of notable accomplishments, structured for easy
resume extraction.

### Step 1: Read existing brag doc

```bash
cat "{OUTPUT_DIR}/brag-doc.md" 2>/dev/null || echo "BRAG_NOT_FOUND"
```

If `BRAG_NOT_FOUND`, create a new one with this header:
```markdown
# Brag Document
<!-- Auto-maintained by weekly-log. Manual edits are preserved. -->
```

### Step 2: Extract accomplishments from this week's journal

Apply these rules to identify brag-worthy items:
- **PRs merged**: Any merged PR, especially features or significant changes
- **Jira tickets completed**: Tickets moved to Done/Closed status
- **Meetings led**: Events where user was the organizer
- **Documents created**: New Notion pages (not just edits)
- **Notable Slack threads**: If the user initiated a significant discussion

Transform each item into an accomplishment statement:
- Use action verb + what + result/impact format
- Examples:
  - "Implemented OAuth2 flow for partner API integration (PR #45, moonkit)"
  - "Completed PROJ-234: Automated deployment pipeline"
  - "Led architecture review meeting for Q2 platform migration"

### Step 3: Append to brag doc

Use the Edit tool to append the new section at the end of the brag doc (before any trailing content):

```markdown
### {WEEK_END}
- {accomplishment 1}
- {accomplishment 2}
- ...
```

Do NOT duplicate items already in the brag doc. Check before appending.

---

## Phase 4: Resume Update

### Step 1: Read existing resume

Read the file at the path specified in `resume_path` config.
If the file does not exist, skip this phase entirely and note it in the report.

**Detect format from file extension:**
- `.tex` → LaTeX format (Overleaf-compatible)
- `.md` → Markdown format

### Step 2: Read the full brag doc

Read `{OUTPUT_DIR}/brag-doc.md` to get all cumulative accomplishments.

### Step 3: Generate update candidates

From recent brag doc entries (last 4 weeks), identify items that should be reflected
in the resume. Focus on:
- New features or systems built
- Quantifiable improvements (performance, automation)
- Leadership activities (meetings led, reviews)
- New technologies or skills used

Generate candidate bullet points for the current role section.

### Step 4: Apply updates

**Interactive mode:**
Use AskUserQuestion to show the candidate updates and let the user choose which to apply:
- Show each candidate as an option with multiSelect: true
- Include a "Skip all" option description

**Format-aware insertion:**

For **LaTeX (.tex)** resumes:
- Find the current role's most recent project section (the first `\hspace{1em}\textbf{...}` block under the current employer)
- Insert new bullet items using the existing LaTeX macros:
  ```latex
  \SmallBulletItem
  \textbf{Title}: Description of accomplishment.
  \Impact{Quantified result or impact.}
  ```
- Use `\textbf{}` for technologies, `\Impact{}` for impact statements
- Insert AFTER the last `\SmallBulletItem` in the most recent project block
- NEVER delete or modify existing content. Only append new bullet points.

For **Markdown (.md)** resumes:
- Find the current role section
- Append new bullet points in standard markdown format
- NEVER delete or modify existing content.

**Automated mode:**
Write candidates to `{OUTPUT_DIR}/pending-resume-updates/{WEEK_END}.md`:
```markdown
# Pending Resume Updates — {WEEK_END}
The following items were identified for your resume. Review and apply with `/weekly-log`.

- [ ] {candidate 1}
- [ ] {candidate 2}

## LaTeX format (copy-paste ready):
\SmallBulletItem
\textbf{Title}: Description.
\Impact{Impact statement.}
```
Do NOT modify the resume file in automated mode.

---

## Phase 5: Snapshot

Save a JSON snapshot for trend tracking:

Use the Write tool to create `{OUTPUT_DIR}/snapshots/{WEEK_END}.json`:
```json
{
  "date": "{WEEK_END}",
  "range": { "start": "{WEEK_START}", "end": "{WEEK_END}" },
  "sources": {
    "github": { "collected": true/false, "commits": N, "prs": N, "reviews": N },
    "slack": { "collected": true/false, "messages": N },
    "jira": { "collected": true/false, "tickets": N },
    "calendar": { "collected": true/false, "meetings": N },
    "notion": { "collected": true/false, "pages": N }
  },
  "failed_sources": ["source: reason", ...],
  "journal_path": "{path to journal file}",
  "brag_items_added": N
}
```

---

## Phase 6: Completion Report

Display a concise summary to the user.

**Format (Korean):**
```
## weekly-log 완료

**기간**: {WEEK_START} ~ {WEEK_END}

| 소스 | 상태 | 수치 |
|------|------|------|
| GitHub | ✅ | 커밋 {N}, PR {N}, 리뷰 {N} |
| Slack | ✅ | 메시지 {N} |
| Jira | ⬚ 비활성 | — |
| Calendar | ✅ | 미팅 {N} |
| Notion | ❌ 실패 | {reason} |

**저장된 파일:**
- 업무일지: `{journal_path}`
- Brag doc: {N}개 항목 추가
- 이력서: {상태 — 업데이트됨 / pending / 변경 없음}
```

Use ✅ for success, ⬚ for disabled, ❌ for failed.

**Format (English):** Same structure with English labels.

---

## Error Handling

- If ALL sources fail: display error message and suggest checking config/auth
- If config file has syntax errors: display the error and suggest running `/weekly-log setup`
- If resume file not found: skip Phase 4 gracefully, mention in report
- If output directory is not writable: alert user immediately
- Never crash silently — always report what happened
