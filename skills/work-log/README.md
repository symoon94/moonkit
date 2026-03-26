# work-log

Work journal, impact report, and achievement organizer for Claude Code.

## What it does

Collects your activity from up to 5 sources and generates three types of output:

- **Journal mode** (`/work-log`): Chronological activity log with insights, growth metrics, and strategic direction
- **Impact mode** (`/work-log impact`): Performance report organized by capability area (tech, product, communication, culture) with measurable outcome tags (revenue, cost, time, risk, quality)
- **Organize mode** (`/work-log organize`): Flexible achievement categorization
  - **report**: Internal performance report with business-value categories (revenue, ops efficiency, risk reduction, cost, hiring/branding, leadership)
  - **resume**: Resume preparation with engineer competency framework (13 perspectives across tech/product/communication/culture) + 1-10 scoring + AI rewriting suggestions

Journal and Impact modes maintain a cumulative brag document and can auto-update your resume.

## Data Sources

| Source | What's collected | Required tool |
|--------|-----------------|---------------|
| GitHub | Commits, PRs, code reviews | `gh` CLI |
| Slack | Messages by channel | Slack MCP |
| Jira | Assigned tickets | Atlassian MCP or REST API |
| Google Calendar | Meetings attended/organized | Google Calendar MCP |
| Notion | Pages created/edited | Notion MCP |

Each source is independently toggleable.

## Usage

```
/work-log                              # This week's journal
/work-log last                         # Last week's journal
/work-log Q1                           # Q1 journal
/work-log H1                           # First half journal
/work-log 2026-01-01 2026-03-31        # Custom range journal
/work-log impact                       # This week's impact report
/work-log impact Q1                    # Q1 impact report
/work-log organize                     # Choose categorization interactively
/work-log organize report              # Internal performance report
/work-log organize resume              # Resume competency framework
/work-log organize report Q1           # Q1 internal report
/work-log organize resume H1           # H1 resume summary
/work-log setup                        # Setup wizard
```

## Installation

1. Copy the `work-log/` directory to your Claude Code skills location
2. Run `/work-log setup` to create `~/.work-log/config.yaml`
3. Ensure data source tools are available (gh CLI, MCP servers)

## Config

`~/.work-log/config.yaml` — see `config.example.yaml` for all options.

Migrating from weekly-log? The skill auto-detects `~/.weekly-log/config.yaml` as fallback.

## Output Structure

```
{output_dir}/
├── journals/              # Chronological journals (2026-03-24.md)
├── impact-reports/        # Impact reports (2026-03-24.md)
├── organize/              # Organize outputs (2026-03-24-report.md, 2026-03-24-resume.md)
├── snapshots/             # JSON snapshots for trend tracking
├── pending-resume-updates/ # Auto-generated resume candidates
└── brag-doc.md            # Cumulative accomplishments
```

## License

MIT
