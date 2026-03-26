# weekly-log

Auto-generate weekly work journals from your tools, maintain a brag document, and keep your resume updated.

## What it does

1. **Collects** weekly activity from up to 5 sources (each toggleable on/off):
   - **GitHub** — commits, PRs, code reviews (via `gh` CLI)
   - **Slack** — messages you sent in channels (via MCP)
   - **Jira** — your assigned tickets (via MCP or REST API)
   - **Google Calendar** — meetings you attended (via MCP)
   - **Notion** — pages you modified (via MCP)

2. **Generates** a structured Markdown work journal

3. **Maintains** a cumulative brag document extracting key accomplishments

4. **Updates** your resume with new accomplishments (with your approval)

## Zero-Config Auto-Discovery

You don't need to list every repo, channel, or project. The skill auto-detects:
- Your GitHub username and active repos via `gh api`
- Your Slack user ID via `slack_read_user_profile`
- Your Jira tickets via `currentUser()` JQL
- Your calendar via the `primary` calendar

Optional filters (`repos_include`, `channels_exclude`, etc.) are available if you want to narrow the scope.

## Installation

### 1. Copy the skill

```bash
# Option A: Symlink (recommended — stays up to date with git pulls)
ln -s /path/to/moonkit/skills/weekly-log ~/.claude/skills/weekly-log

# Option B: Copy
cp -r /path/to/moonkit/skills/weekly-log ~/.claude/skills/weekly-log
```

### 2. First run

```
/weekly-log
```

The skill will walk you through setup: language, sources, output path.
Config is saved to `~/.weekly-log/config.yaml`.

### 3. (Optional) Set up automatic Saturday runs

During first run, the skill offers to create a scheduled task that runs every Saturday at 10 AM.

## Usage

```
/weekly-log          # Current week (Monday to today)
/weekly-log last     # Previous full week (Monday to Sunday)
/weekly-log setup    # Re-run setup wizard
```

## Requirements

### Required
- [Claude Code](https://claude.ai/claude-code) with skill support

### Per-source requirements

| Source | Requirement |
|--------|------------|
| GitHub | `gh` CLI installed and authenticated (`gh auth login`) |
| Slack | Slack MCP plugin connected |
| Jira | Atlassian MCP plugin connected, OR `JIRA_EMAIL` + `JIRA_API_TOKEN` env vars for REST |
| Google Calendar | Google Calendar MCP plugin connected |
| Notion | Notion MCP plugin connected |

Only install/connect what you need — disabled sources are skipped entirely.

## Config

`~/.weekly-log/config.yaml` — see [config.example.yaml](config.example.yaml) for all options.

Minimal config:
```yaml
language: ko
output_dir: ~/weekly-log
resume_path: ~/resume.md

github:
  enabled: true
slack:
  enabled: true
jira:
  enabled: false
google_calendar:
  enabled: true
notion:
  enabled: true
```

## Output

```
~/weekly-log/
├── journals/
│   ├── 2026-03-22.md        # Weekly journals
│   └── 2026-03-15.md
├── snapshots/
│   ├── 2026-03-22.json      # Stats snapshots for trends
│   └── 2026-03-15.json
├── pending-resume-updates/   # Auto-mode resume suggestions
│   └── 2026-03-22.md
└── brag-doc.md               # Cumulative accomplishments
```

## License

MIT
