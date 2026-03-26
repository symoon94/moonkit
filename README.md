# moonkit

Claude Code skills for work automation.

## Installation

```bash
# 1. Clone
git clone https://github.com/symoon94/moonkit.git

# 2. Install skills to your project
cd your-project
/path/to/moonkit/install.sh

# Or install globally (all projects)
/path/to/moonkit/install.sh --global
```

The installer creates symlinks from your `.claude/skills/` to the moonkit `skills/` directory. This means:
- Skills stay up to date when you `git pull` moonkit
- No file duplication
- Works with any Claude Code project

### Manual install

If you prefer not to use symlinks, copy the skill directories directly:

```bash
cp -r /path/to/moonkit/skills/issue-tracker .claude/skills/
cp -r /path/to/moonkit/skills/work-log .claude/skills/
```

### Required MCP servers

Skills use these MCP integrations (enable as needed in Claude Code settings):

| MCP | Used by | Purpose |
|-----|---------|---------|
| Slack | issue-tracker, work-log | Channel/DM message search and thread reading |
| Gmail | issue-tracker | Email search and thread reading |
| Notion | issue-tracker, work-log | Report output to Notion pages |
| Jira | work-log | Issue tracking data |
| Google Calendar | work-log | Meeting/schedule data |

## Skills

### issue-tracker

Slack과 Gmail에서 팀의 실수/요청/장애를 수집하고, 심각도/영향 범위/빈도로 분류해서 임팩트가 큰 문제부터 정렬한 보고서를 만드는 스킬.

```
/issue-tracker              # 기본 기간으로 집계
/issue-tracker last         # 직전 기간
/issue-tracker 2026-03      # 특정 월
/issue-tracker setup        # 셋업 재실행
```

- 인터랙티브 셋업 — 데이터 소스, 시그널, 제외 조건 등 설정 후 재사용
- HTML/Markdown/Notion 출력 지원
- 임팩트 점수 = 심각도 x 영향 범위 x 빈도

자세한 내용은 [skills/issue-tracker/](skills/issue-tracker/) 참고.

### work-log

GitHub, Slack, Jira, Google Calendar, Notion에서 활동을 수집해서 업무일지/성과보고서/이력서 소재를 만들어주는 스킬.

```
/work-log                   # 이번 주 업무일지
/work-log impact            # 역량 기반 성과 보고서
/work-log organize          # 보고용/이력서용 성과 정리
```

- 3가지 모드: journal / impact / organize
- brag document 자동 유지
- 설정은 `~/.work-log/config.yaml`에 저장

자세한 내용은 [skills/work-log/](skills/work-log/) 참고.

## Project structure

```
moonkit/
  install.sh                # Skill installer (symlinks to .claude/skills/)
  skills/
    issue-tracker/
      SKILL.md              # Skill definition
      README.md             # Documentation
      references/           # Templates
    work-log/
      SKILL.md              # Skill definition
      README.md             # Documentation
      references/           # Templates
```

## License

MIT
