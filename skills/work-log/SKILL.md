---
name: work-log
version: 0.9.0
description: |
  Work journal, performance report, and resume builder. Collects activity from
  GitHub, Slack, Jira, Google Calendar, and Notion — generates structured outputs.
  Three modes: journal (chronological activity log + insights), report (6 business-value
  categories + impact tagging + TOP 5 + Executive Summary), resume (13 competency
  perspectives + scoring + rewriting suggestions). Maintains a brag document.
  Trigger: "/work-log", "업무일지", "work log", "성과 보고", "성과 정리",
  "이력서 업데이트", "resume update", "뭐했지", "what did I do"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

**Preamble — run this FIRST before any skill logic:**

```bash
# Find moonkit root via symlink resolution
_MK_DIR=$(cd "$(dirname "$(readlink ~/.claude/skills/work-log 2>/dev/null || readlink .claude/skills/work-log 2>/dev/null || echo .)")/.." 2>/dev/null && pwd) || true
[ -n "$_MK_DIR" ] && _UPD=$("$_MK_DIR/bin/moonkit-update-check" 2>/dev/null || true) && [ -n "$_UPD" ] && echo "$_UPD"
```

If the output shows `UPGRADE_AVAILABLE <old> <new>`:
1. Tell the user: "moonkit v{new} 버전이 있습니다. (현재 v{old}) 업데이트할까요?"
2. If yes → run `$_MK_DIR/bin/moonkit-upgrade`
3. If no → continue. To snooze 24h: `echo $(( $(date +%s) + 86400 )) > ~/.moonkit/update-snooze`

If preamble produces no output, proceed normally.

# /work-log — Work Journal, Impact Report & Achievement Organizer

Three modes:
- **Journal mode**: Chronological activity log with insights
- **Report mode**: Internal performance report — 6 business-value categories + impact tagging + TOP 5 + Executive Summary
- **Resume mode**: Engineer competency framework — 13 perspectives, 1-10 scoring, rewriting suggestions

## User-invocable

When the user types `/work-log`, run this skill.

## Arguments

- `/work-log` — interactive mode & period & source selection
- `/work-log last` — previous full week journal
- `/work-log 2026-01-01 2026-03-22` — custom date range journal
- `/work-log Q1` — current year Q1 journal
- `/work-log H1` — current year first half (Jan~Jun)
- `/work-log report` — this week's performance report
- `/work-log report Q1` — Q1 performance report
- `/work-log report 2025-07-01 2025-12-31` — custom range report
- `/work-log resume` — this week's resume preparation
- `/work-log resume H1` — H1 resume summary
- `/work-log setup` — re-run first-time setup wizard

### HTML output flag

Append `--html` to any command to also generate a styled HTML version:
- `/work-log report Q1 --html`
- `/work-log resume H1 --html`
- `/work-log --html` (interactive mode — asks as usual, HTML output included)

## Mode Detection

Parse `$ARGUMENTS` to determine:
1. **Mode**: Parse in this order:
   - `report` (anywhere in args) → report mode
   - `resume` (anywhere in args) → resume mode
   - Period token only (e.g., `Q1`, `last`, dates) → journal mode
   - **Empty arguments** (interactive mode) → AskUserQuestion with 3 modes (see Phase 0 Step 2.5). Do NOT silently default.
2. **Execution**: If user typed in conversation → **interactive**. If scheduled task → **automated**.
3. **Period**: Parse date range, `last`, `Q1-Q4`, `H1`/`H2` from arguments. **If no period argument is provided**, ask interactively (see Phase 0 Step 3). Do NOT silently default to current week.
4. **HTML output**: If `--html` is present in args, set `html_output = true`. Also check `html_output` in config. The flag overrides config (flag present = true). In interactive mode, ask via Question 4 in Step 2.5.

---

## Phase 0: Config & Date Range

### Step 1: Read config

```bash
cat ~/.work-log/config.yaml 2>/dev/null || cat ~/.weekly-log/config.yaml 2>/dev/null || echo "CONFIG_NOT_FOUND"
```

Supports both `~/.work-log/` and legacy `~/.weekly-log/` paths.
If `CONFIG_NOT_FOUND` or arguments contain `setup`, run the **First-Run Wizard**.

### Step 2: First-Run Wizard (interactive only)

Use AskUserQuestion calls:

**First call (up to 3 questions):**
1. **Language**: "언어를 선택하세요" — options: "한국어 (ko)", "English (en)"
2. **Sources**: "어떤 소스를 활성화할까요?" (multiSelect) — "GitHub", "Slack", "Jira", "Google Calendar", "Notion"
3. **Output directory**: "저장 경로" — "~/work-log (Recommended)", "~/Documents/work-log", "Custom path"

**Second call (scheduling):**
4. **Organize schedule**: "organize 모드를 자동으로 실행할까요?" — options: "매주 자동 실행 (토요일 10시) (Recommended)", "수동으로만 실행", "커스텀 스케줄"
   - If "매주 자동 실행": set `organize.schedule.enabled: true`, `cron: "0 10 * * 6"`
   - If "커스텀 스케줄": ask follow-up for cron expression and submode (report/resume)
   - If "수동으로만 실행": set `organize.schedule.enabled: false`

Generate `~/.work-log/config.yaml` using the skill's `config.example.yaml` as template.

### Step 2.5: Interactive mode & period selection (when arguments are empty)

**Only runs when `$ARGUMENTS` is empty AND interactive mode.**

Use a single AskUserQuestion call with up to 4 questions to collect mode, period, sources, and organize submode at once:

**Question 1 — Mode:**
- Question: "어떤 용도로 생성할까요?"
- Options:
  - "업무일지 (Journal)" — 시간순 활동 기록 + 인사이트 (Recommended)
  - "성과 보고 (Report)" — 경영진 시각의 6개 카테고리 + 임팩트 태깅 + TOP 5 + Executive Summary
  - "이력서 정리 (Resume)" — 엔지니어 역량 프레임워크 13개 관점 + 1-10 스코어링 + 리라이팅 제안

**Question 2 — Period:**
- Question: "기간을 선택하세요"
- Options (show up to 4, prioritize by relevance):
  - "이번 주 (월요일 ~ 오늘)"
  - "지난주 (월 ~ 일)"
  - "이번 달" / "지난달"
  - "Q1 (1~3월)" / "Q2 (4~6월)" / etc. — show only the current and previous quarter
  - "H1 (1~6월)" / "H2 (7~12월)" — show only the current and previous half
- AskUserQuestion allows max 4 options, so pick the most relevant 4 based on the current date. Always include "이번 주" and at least one long-range option (Q or H). The user can always select "Other" for custom dates (YYYY-MM-DD ~ YYYY-MM-DD).
- If user selects "Other": ask a follow-up for custom dates, including the target year if it differs from the current year (e.g., "2025-07-01 ~ 2025-12-31").

**Question 3 — Sources:**
- Question: "어떤 소스를 사용할까요?"
- multiSelect: true
- Options: Show only the sources that are `enabled: true` in config, pre-labeled with checkmarks. For example if all 5 are enabled:
  - "GitHub" — 커밋, PR, 코드 리뷰
  - "Slack" — 채널별 대화 토픽
  - "Jira" — 티켓 상태, 에픽
  - "Google Calendar" — 미팅, 주최 여부
  - "Notion" — 페이지 생성/편집 이력
- If user deselects a source, skip that source in Phase 1 data collection. This lets users exclude noisy or irrelevant sources per run without changing config.

**Question 4 — HTML output:**
- Question: "HTML 파일도 함께 생성할까요?"
- Options:
  - "Markdown만 (Recommended)" — .md 파일만 생성
  - "Markdown + HTML" — .md와 styled .html 파일 모두 생성
- If `html_output: true` in config, default to "Markdown + HTML".
- If `--html` flag was passed in arguments, skip this question and set html_output = true.

**In automated mode** (scheduled task), skip this step — default to journal mode + current week + all enabled sources + config's `html_output` setting.

### Step 2.7: Partial answer recovery (when AskUserQuestion is rejected)

If AskUserQuestion is rejected but partial answers are visible in the rejection message:
1. **Accept all clearly answered questions** — do not re-ask them.
2. **Only re-ask unanswered questions** — either via a single follow-up AskUserQuestion or by inferring from context (e.g., if all other answers are clear, ask only the missing one).
3. **Never ask "어떤 부분을 clarify 하고 싶으신가요?"** — the user didn't ask to clarify; the system reported a rejection. Proceed with what you have.
4. If the user's text response after rejection provides the missing answer (e.g., "html 만들어줘"), accept it and proceed immediately.

### Step 3: Calculate date range

**If a period argument was provided**, parse it directly:
- Two dates (YYYY-MM-DD YYYY-MM-DD) → use directly
- `last` → previous Monday to Sunday
- `Q1`~`Q4` → quarter boundaries of current year
- `H1` → Jan 1 ~ Jun 30, `H2` → Jul 1 ~ Dec 31

**If NO period argument was provided** (interactive mode only), use AskUserQuestion to ask:
- Question: "기간을 선택하세요"
- Options:
  - "이번 주 (월요일 ~ 오늘)" — calculate dynamically
  - "지난주 (월 ~ 일)"
  - "이번 달"
  - "지난달"
  - "Q1 (1~3월)" / "Q2 (4~6월)" / etc. — show only the current and previous quarter
  - "H1 (1~6월)" / "H2 (7~12월)" — show only the current half
  - "직접 입력 (YYYY-MM-DD ~ YYYY-MM-DD)"
- If user selects "직접 입력": ask a follow-up AskUserQuestion for start and end dates.
- If user selects "이번 달": start = first day of current month, end = today.
- If user selects "지난달": start = first day of previous month, end = last day of previous month.

**In automated mode** (scheduled task), default to current week without asking:
```bash
DOW=$(date +%u)
WEEK_START=$(date -v-$((DOW-1))d +%Y-%m-%d)  # macOS
WEEK_END=$(date +%Y-%m-%d)
```

### Step 4: Ensure output directories

```bash
OUTPUT_DIR=$(grep 'output_dir:' <config_path> | awk '{print $2}' | sed "s|~|$HOME|")
mkdir -p "$OUTPUT_DIR/journals" "$OUTPUT_DIR/snapshots" "$OUTPUT_DIR/impact-reports" "$OUTPUT_DIR/pending-resume-updates"
```

---

## Phase 1: Data Collection

**IMPORTANT: Use parallel sub-agents for data collection.** Launch one Agent per enabled source (up to 5 agents: GitHub, Slack, Jira, Calendar, Notion) running in the background simultaneously. Each agent collects its source data and returns a structured summary. Wait for all agents to complete, then merge results for Phase 2.

This dramatically reduces total collection time — especially for long periods where each source may take 30-60 seconds.

Collect from each enabled source independently. If a source fails, log and continue.

**For long periods (>2 weeks)**: First check for existing snapshots and journals in the output directory. Use them as primary data to avoid redundant API calls. Only collect fresh data for uncovered date ranges.

```bash
ls "$OUTPUT_DIR/snapshots/"*.json 2>/dev/null | sort
ls "$OUTPUT_DIR/journals/"*.md 2>/dev/null | sort
```

If existing data covers the requested period, read those files instead of re-collecting.
If gaps exist, collect only for the missing date ranges.

### 1a. GitHub (if enabled)

Use `gh` CLI. Auto-detect username via `gh api user --jq '.login'`.

**For short periods (≤4 weeks)**: query the full range at once.

**For long periods (>4 weeks)**: split into monthly sub-ranges to avoid GitHub Search API limits (100 commits, 50 PRs per query). For example, a 6-month range becomes 6 monthly queries. Aggregate and deduplicate results across all sub-ranges.

For commit discovery, prefer `gh search commits` (works with private repos):
```bash
# Short period:
gh search commits --author={username} --author-date=">={START}" \
  --json repository,sha,commit --limit 100
# Long period (repeat per month):
gh search commits --author={username} --author-date="{MONTH_START}..{MONTH_END}" \
  --json repository,sha,commit --limit 100
```

For PRs:
```bash
gh search prs --author={username} --created=">={START}" \
  --json repository,title,number,state,url,createdAt --limit 50
# Long period: use --created="{MONTH_START}..{MONTH_END}" per month
```

For reviews:
```bash
gh search prs --reviewed-by={username} --updated=">={START}" \
  --json repository,title,number,state,url --limit 50
# Long period: use --updated="{MONTH_START}..{MONTH_END}" per month
```

Apply `repos_include` / `repos_exclude` filters from config.

### 1b. Slack (if enabled)

Use `slack_read_user_profile` MCP (no params) → get user_id.
Then `slack_search_public_and_private`:
```
query: "from:<@{user_id}> after:{WEEK_START} before:{WEEK_END}"
limit: 20, sort: "timestamp", include_context: false
```

Apply `channels_include`/`channels_exclude` filters. Group by channel, extract topics.

### 1c. Jira (if enabled)

Try Atlassian MCP first (`getAccessibleAtlassianResources` → `searchJiraIssuesUsingJql`).
JQL: `assignee = currentUser() AND updated >= "{WEEK_START}"`
Fall back to REST API if MCP unavailable.

### 1d. Google Calendar (if enabled)

Use `gcal_list_events` MCP. Filter: accepted, tentative, or organizer. Skip declined.
Extract: title, time, duration, attendee count.

### 1e. Notion (if enabled)

Use `notion-search` MCP. Extract: title, URL, edit time.

**API limitations to work around:**
- `query` must be non-empty (use a space if no keyword).
- Returns max 25 results per query, ranked by semantic relevance — NOT by date.
- `created_date_range` filter applies to *creation date*, but the returned `timestamp` is *last edited time*. These can diverge significantly.
- For comprehensive coverage, run multiple searches with different keywords relevant to the user's work (e.g., project names, "review", "design", "onboarding", product names). Deduplicate by page ID.
- Post-filter results to keep only pages whose `last_edited_time` falls within the requested date range.

---

## Phase 2: Output Generation

**Branch based on mode:**
- Journal mode → Phase 2A (Journal)
- Report mode → Phase 2B (Report)
- Resume mode → Phase 2C (Resume)

Journal mode runs Phase 2H (HTML, if enabled), Phase 3 (Brag Doc), Phase 4 (Resume Update), Phase 5 (Snapshot).
Report and Resume modes **skip** Phase 3 and Phase 4, run Phase 2H (HTML, if enabled), Phase 5 (Snapshot) and Phase 6 (Completion).

---

## Phase 2A: Journal Generation

Generate chronological activity journal. Read `references/journal-template.md` for the
full template structure including the Insights section (Growth Metrics, Skill Radar,
What to Improve, Strategic Direction, Owner's Scorecard).

Save to: `{OUTPUT_DIR}/journals/{END}.md`

---

## Phase 2B: Report Generation

Read `references/report-template.md` for the full template structure, categorization rules,
and auto-categorization signals.

Take all collected data from Phase 1 and categorize each activity into one of 6 business-value
categories: 매출/딜리버리, 운영 효율화, 장애 & 보안 리스크 감소, 비용 절감, 채용 & 홍보,
팀 빌딩/리더십.

Also tag each activity with impact metrics where possible:

| 임팩트 태그 | 키워드/시그널 |
|------------|-------------|
| 💰 **매출** | customer, partner, delivery, release, launch, 고객, 파트너, 납품 |
| 💰 **비용** | optimize, reduce, automate, remove dependency, 최적화, 비용, 절감 |
| ⏱ **시간** | speed up, reduce time, pipeline, CI/CD, 시간 단축, 자동화 |
| 🛡 **리스크** | fix, security, bug, crash, validation, 장애, 보안, 수정 |
| ✅ **품질** | test, refactor, clean, lint, 테스트, 리팩토링, 품질 |

Use the keyword signals and source-based defaults from the template to auto-categorize.
For ambiguous items, pick the category with the strongest signal match.
If impact is quantified in the commit message or PR (e.g., "reduced from 50s to 22s") → use that number directly.

Generate the report using the Korean or English template based on the config `language` setting.

Save to: `{OUTPUT_DIR}/reports/{END}-report.md`

---

## Phase 2C: Resume Generation

Read `references/resume-template.md` for the full competency framework, 13 evaluation
perspectives, scoring rubric, and rewriting rules.

Take all collected data from Phase 1 and classify each activity into the most relevant
perspective among the 13 perspectives across 4 areas:
- 기술/코드/설계 (7 perspectives)
- 제품 (2 perspectives)
- 커뮤니케이션 (2 perspectives)
- 문화 (2 perspectives)

For each perspective with matching activities:
1. List activities with source links
2. Generate a narrative: problem recognized → how it was solved → result/impact
3. Score each item 1-10 using the scoring rubric
4. For items scoring < 7: generate a stronger rewriting suggestion

**Interactive mode**: If activity data alone is insufficient for a complete narrative,
use AskUserQuestion to ask the user for context (batch 3-4 items per question).

**Automated mode**: Generate narratives from data only. Mark insufficient items with
"[추가 컨텍스트 필요]" placeholder.

Generate the output using the Korean or English template based on the config `language` setting.

Save to: `{OUTPUT_DIR}/resume/{END}-resume.md`

---

## Phase 2H: HTML Generation (optional)

**Skip this phase if `html_output` is false.**

After generating the markdown output (Phase 2A, 2B, or 2C), convert it to a styled HTML file.
Read `references/html-template.md` for the design system and structural mapping rules.

### Process

1. Read the generated markdown file.
2. Generate a self-contained HTML file (inline CSS, no external dependencies except Google Fonts).
3. Save to the same directory as the markdown file, with `.html` extension:
   - Journal: `{OUTPUT_DIR}/journals/{WEEK_END}.html`
   - Report: `{OUTPUT_DIR}/reports/{WEEK_END}-report.html`
   - Resume: `{OUTPUT_DIR}/resume/{WEEK_END}-resume.html`
4. Open the HTML file in the browser: `open {html_path}`

### Design principles

- **Self-contained**: All CSS inline. Only external dependency is Google Fonts (Noto Sans KR + Inter).
- **Mode-aware styling**: Each mode has a distinct color accent — Journal (blue), Report (gradient blue-purple), Resume (green).
- **Responsive**: Works on mobile and desktop. Print-optimized with `@media print`.
- **Structural mapping**: Map markdown structure to semantic HTML components:
  - `# H1` → header block with gradient background
  - `## H2` → section header with numbered badge
  - `### H3` → card with left border accent
  - `**Bold label**: value` → styled key-value pair
  - Bullet lists → styled list with colored dot indicators
  - Tables → responsive styled tables
  - `**임팩트**` / `**Impact**` blocks → highlighted impact box
  - `**증거**` / `**Evidence**` → subtle reference line
- **Stats bar**: Extract key numbers (PRs, commits, meetings, etc.) from the content and render as a top-level stats card row.

---

## Phase 3: Brag Document Update

**Note: Phase 3 is skipped in organize mode.**

Read existing `{OUTPUT_DIR}/brag-doc.md`. Extract accomplishments from the generated
journal or impact report:

- PRs merged (especially features and significant changes)
- Jira tickets completed
- Meetings led (user was organizer)
- New Notion pages created
- Notable Slack threads initiated

Transform into: action verb + what + result/impact format.
Append under `### {WEEK_END}` heading. Do NOT duplicate existing items.

---

## Phase 4: Resume Update

**Note: Phase 4 is skipped in organize mode.** The organize `resume` submode generates
its own resume-ready output but does NOT modify the resume file directly.

Read resume at `resume_path` from config. Detect format (`.tex` or `.md`).

**Interactive mode**: Use AskUserQuestion to let user select which brag items to add.
Format-aware insertion (LaTeX: `\SmallBulletItem` + `\Impact{}`, Markdown: bullet points).

**Automated mode**: Write candidates to `{OUTPUT_DIR}/pending-resume-updates/{WEEK_END}.md`.

---

## Phase 5: Snapshot

Save JSON to `{OUTPUT_DIR}/snapshots/{WEEK_END}.json`:
```json
{
  "date": "{WEEK_END}",
  "range": { "start": "{WEEK_START}", "end": "{WEEK_END}" },
  "mode": "journal|impact|organize",
  "organize_submode": "report|resume|null",
  "sources": {
    "github": { "collected": true, "commits": 0, "prs": 0, "reviews": 0 },
    "slack": { "collected": true, "messages": 0 },
    "jira": { "collected": true, "tickets": 0 },
    "calendar": { "collected": true, "meetings": 0 },
    "notion": { "collected": true, "pages": 0 }
  },
  "failed_sources": [],
  "output_path": "{path to journal, impact report, or organize output}",
  "html_path": "{path to .html file, or null if html_output is false}",
  "brag_items_added": 0
}
```

---

## Phase 6: Completion Report

```
## work-log 완료

**기간**: {START} ~ {END}  |  **모드**: {journal / impact / organize-report / organize-resume}

| 소스 | 상태 | 수치 |
|------|------|------|
| GitHub | ✅ | 커밋 {N}, PR {N}, 리뷰 {N} |
| Slack | ✅ | 메시지 {N} |
| Jira | ⬚ 비활성 | — |
| Calendar | ✅ | 미팅 {N} |
| Notion | ❌ 실패 | {reason} |

**저장된 파일:**
- {journal / impact report / organize output}: `{path}`
- HTML: `{html_path}` (html_output이 true일 때만 표시)
- Brag doc: {N}개 항목 추가 (organize 모드에서는 생략)
- 이력서: {업데이트됨 / pending / 변경 없음} (organize 모드에서는 생략)
```

For organize mode, the completion report additionally shows:
- **서브모드**: report / resume
- **카테고리 수**: {N}개 카테고리에 활동 분류됨
- **이력서 스코어** (resume submode only): 평균 {N}/10, 리라이팅 제안 {N}건

### Resume mode: 영문/한글 복사용 포맷 + 프리뷰 (4개 섹션)

Resume 모드의 완료 보고 시, 위 테이블 아래에 아래 4개 섹션을 **모두** 대화에 출력한다:

1. `## 복사용 포맷 (English)` — 영문 원본 코드블록 (LaTeX 또는 Markdown)
2. `## 복사용 포맷 (한국어)` — 한글 원본 코드블록 (동일 매크로, 내용만 한국어)
3. `## 프리뷰 (English)` — 영문 원본을 읽기 쉬운 Markdown으로 렌더링
4. `## 프리뷰 (한국어)` — 한글 원본을 읽기 쉬운 Markdown으로 렌더링

Markdown 파일(.md)과 HTML 파일(.html)에도 동일하게 4개 섹션을 모두 포함한다.
**4개 중 하나라도 빠지면 안 된다.** 상세 규칙은 resume-template.md, html-template.md 참조.

---

## Error Handling

- ALL sources fail → suggest checking config/auth
- Config syntax error → suggest `/work-log setup`
- Resume not found → skip Phase 4, mention in report
- Output dir not writable → alert immediately
- Never crash silently

### Organize-specific errors

- 기간 내 수집 데이터 0건 → "해당 기간에 수집된 활동이 없습니다" + 소스별 실패 사유 표시
- 인식 불가 서브모드 토큰 → period로 파싱 시도, 실패 시 에러 메시지 "'{token}'은 유효한 서브모드나 기간이 아닙니다"
- resume 스코어 생성 실패 → 기본값 5/10 사용 + 로그
- automated 모드에서 서브모드 미지정 → 기본값 `report` 사용
