---
name: work-log
version: 0.3.0
description: |
  Work journal, impact report, and achievement organizer. Collects activity from
  GitHub, Slack, Jira, Google Calendar, and Notion — generates structured journals,
  performance impact reports, and organized achievement summaries for internal
  reporting or resume preparation. Maintains a brag document and updates your resume.
  Three modes: journal (chronological activity log), impact (capability-based
  performance report), and organize (flexible categorization for reports/resume).
  Trigger: "/work-log", "업무일지", "work log", "성과 보고", "impact report",
  "이력서 업데이트", "resume update", "성과 정리", "뭐했지", "what did I do"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# /work-log — Work Journal, Impact Report & Achievement Organizer

Three modes in one skill:
- **Journal mode** (default): Chronological activity log with insights
- **Impact mode**: Performance report — categorize work by capability area, tag measurable outcomes
- **Organize mode**: Flexible achievement categorization — internal reports (business-value categories) or resume preparation (engineer competency framework with scoring)

## User-invocable

When the user types `/work-log`, run this skill.

## Arguments

- `/work-log` — this week's journal (Monday to today)
- `/work-log last` — previous full week journal
- `/work-log 2026-01-01 2026-03-22` — custom date range journal
- `/work-log Q1` — current year Q1 journal
- `/work-log H1` — current year first half (Jan~Jun)
- `/work-log impact` — this week's impact report
- `/work-log impact Q1` — Q1 impact report
- `/work-log impact 2025-10-01 2026-03-31` — custom range impact report
- `/work-log organize` — this week, choose categorization method interactively
- `/work-log organize report` — internal performance report (business-value categories)
- `/work-log organize resume` — resume preparation (engineer competency framework)
- `/work-log organize report Q1` — Q1 internal report
- `/work-log organize resume H1` — H1 resume summary
- `/work-log setup` — re-run first-time setup wizard

## Mode Detection

Parse `$ARGUMENTS` to determine:
1. **Mode**: If arguments contain `organize` → organize mode. If `impact` → impact mode. Otherwise → journal mode.
2. **Organize submode** (organize mode only): First token after `organize` that matches `report` or `resume` → that submode. If first token is a period format (Q1, last, YYYY-MM-DD) → no submode specified, period detected. If no recognized token → AskUserQuestion in interactive mode, default to `report` in automated mode.
3. **Execution**: If user typed in conversation → **interactive**. If scheduled task → **automated**.
4. **Period**: Parse date range, `last`, `Q1-Q4`, `H1`/`H2`, or default to current week. Reuse existing Phase 0 parsing logic.

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

### Step 3: Calculate date range

```bash
DOW=$(date +%u)
WEEK_START=$(date -v-$((DOW-1))d +%Y-%m-%d)  # macOS
WEEK_END=$(date +%Y-%m-%d)
```

Handle special arguments:
- Two dates (YYYY-MM-DD YYYY-MM-DD) → use directly
- `last` → previous Monday to Sunday
- `Q1`~`Q4` → quarter boundaries of current year
- `H1` → Jan 1 ~ Jun 30, `H2` → Jul 1 ~ Dec 31

### Step 4: Ensure output directories

```bash
OUTPUT_DIR=$(grep 'output_dir:' <config_path> | awk '{print $2}' | sed "s|~|$HOME|")
mkdir -p "$OUTPUT_DIR/journals" "$OUTPUT_DIR/snapshots" "$OUTPUT_DIR/impact-reports" "$OUTPUT_DIR/pending-resume-updates"
```

---

## Phase 1: Data Collection

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

For commit discovery, prefer `gh search commits` (works with private repos):
```bash
gh search commits --author={username} --author-date=">={WEEK_START}" \
  --json repository,sha,commit --limit 50
```

For PRs:
```bash
gh search prs --author={username} --created=">={WEEK_START}" \
  --json repository,title,number,state,url,createdAt --limit 20
```

For reviews:
```bash
gh search prs --reviewed-by={username} --updated=">={WEEK_START}" \
  --json repository,title,number,state,url --limit 20
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

Use `notion-search` MCP with date filter. Extract: title, URL, edit time.
Note: query must be non-empty (use a space or keyword if needed).

---

## Phase 2: Output Generation

**Branch based on mode:**
- Journal mode → Phase 2A (Journal)
- Impact mode → Phase 2B (Impact Report)
- Organize mode → Phase 2C (Organize)

Journal and Impact modes still run Phase 3 (Brag Doc), Phase 4 (Resume), Phase 5 (Snapshot).
Organize mode **skips** Phase 3 (Brag Doc) and Phase 4 (Resume), runs Phase 5 (Snapshot) and Phase 6 (Completion).

---

## Phase 2A: Journal Generation

Generate chronological activity journal. Read `references/journal-template.md` for the
full template structure including the Insights section (Growth Metrics, Skill Radar,
What to Improve, Strategic Direction, Owner's Scorecard).

Save to: `{OUTPUT_DIR}/journals/{WEEK_END}.md`

---

## Phase 2B: Impact Report Generation

This is the core of the impact mode. Read `references/impact-template.md` for the full
template and categorization rules.

### Step 1: Categorize all collected work

Take every task (commit, PR, ticket, meeting, Slack thread, Notion page) and assign it
to one of 4 capability areas:

| 역량 영역 | 판별 기준 |
|-----------|----------|
| **기술/코드/설계** | 커밋, PR, 코드리뷰, 기술 관련 Slack 토픽, 기술 문서 |
| **제품** | 고객/파트너 관련 PR, 제품 미팅, 제품 관련 Jira 티켓 |
| **커뮤니케이션** | Slack 스레드 주도, 크로스팀 미팅, 데이터 공유 |
| **문화** | 팀 미팅 주최, 북클럽, 온보딩, 멘토링, 사내 발표 |

### Step 2: Tag impact metrics

For each categorized task, attempt to find a measurable outcome from one of 5 impact types:

| 임팩트 태그 | 키워드/시그널 |
|------------|-------------|
| 💰 **매출** | customer, partner, delivery, release, launch, 고객, 파트너, 납품 |
| 💰 **비용** | optimize, reduce, automate, remove dependency, 최적화, 비용, 절감 |
| ⏱ **시간** | speed up, reduce time, pipeline, CI/CD, 시간 단축, 자동화 |
| 🛡 **리스크** | fix, security, bug, crash, validation, 장애, 보안, 수정 |
| ✅ **품질** | test, refactor, clean, lint, 테스트, 리팩토링, 품질 |

**Auto-tagging rules:**
- PR/commit messages containing `fix`, `security`, `vulnerability` → 🛡 리스크
- PR/commit messages containing `perf`, `optimize`, `reduce` → 💰 비용 or ⏱ 시간
- PR/commit messages containing `feat` + customer/partner context → 💰 매출
- `chore`, `ci`, `automation` → ⏱ 시간
- `test`, `refactor` → ✅ 품질
- Meeting where user was organizer → 문화 (no impact tag needed)
- If impact is quantified in the commit message or PR (e.g., "reduced from 50s to 22s") → use that number directly

### Step 3: Interactive impact filling (interactive mode only)

For tasks where no impact metric was found automatically, present them to the user
grouped by capability area using AskUserQuestion. For each untagged task:

1. Show the task description
2. Ask which impact tag applies (or "없음/측정 불가")
3. Ask for a specific metric if available ("얼마나 변했나요?")

Batch tasks into groups of 3-4 per AskUserQuestion call to avoid overwhelming the user.
If the user selects "없음/측정 불가", accept and move on — not everything needs a number.

### Step 4: Generate measurement suggestions

For tasks tagged "없음/측정 불가" or where the user couldn't provide metrics, generate
a concrete suggestion for how to measure impact in the future.

Examples:
- "이 자동화 파이프라인의 임팩트를 측정하려면: 도입 전/후 수동 작업 시간을 비교해보세요. `time` 커맨드로 파이프라인 실행 시간을 기록하면 됩니다."
- "코드 리뷰 임팩트 측정: 리뷰 코멘트 중 실제 버그를 잡은 건수를 추적해보세요."
- "미팅 효과 측정: 미팅 후 생성된 액션 아이템 수와 완료율을 노션에 기록해보세요."

### Step 5: Save impact report

Save to: `{OUTPUT_DIR}/impact-reports/{WEEK_END}.md`

In automated mode, skip Step 3 (interactive filling) and mark untagged items as
"⬜ 미측정" with measurement suggestions inline.

---

## Phase 2C: Organize Generation

Flexible achievement categorization. Two submodes: **report** (internal performance report)
and **resume** (engineer competency framework).

### Step 1: Submode selection

If submode was not specified in arguments:
- **Interactive mode**: Use AskUserQuestion:
  - "성과를 어떤 방식으로 정리할까요?"
  - A) 사내 성과 보고용 — 경영진 시각의 카테고리 (매출, 운영효율화, 리스크 등)
  - B) 이력서용 — 엔지니어 역량 프레임워크 기반 (기술/제품/커뮤니케이션/문화)
- **Automated mode**: Use config `organize.schedule.submode` (default: `report`)

### Step 2: Ensure output directory

```bash
mkdir -p "$OUTPUT_DIR/organize"
```

### Step 3A: Report generation (`report` submode)

Read `references/report-template.md` for the full template structure, categorization rules,
and auto-categorization signals.

Take all collected data from Phase 1 and categorize each activity into one of 6 business-value
categories: 매출/딜리버리, 운영 효율화, 장애 & 보안 리스크 감소, 비용 절감, 채용 & 홍보,
팀 빌딩/리더십.

Use the keyword signals and source-based defaults from the template to auto-categorize.
For ambiguous items, pick the category with the strongest signal match.

Generate the report using the Korean or English template based on the config `language` setting.

Save to: `{OUTPUT_DIR}/organize/{WEEK_END}-report.md`

### Step 3B: Resume generation (`resume` submode)

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

Save to: `{OUTPUT_DIR}/organize/{WEEK_END}-resume.md`

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
- Brag doc: {N}개 항목 추가 (organize 모드에서는 생략)
- 이력서: {업데이트됨 / pending / 변경 없음} (organize 모드에서는 생략)
```

For organize mode, the completion report additionally shows:
- **서브모드**: report / resume
- **카테고리 수**: {N}개 카테고리에 활동 분류됨
- **이력서 스코어** (resume submode only): 평균 {N}/10, 리라이팅 제안 {N}건

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
