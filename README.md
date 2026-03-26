# moonkit

Claude Code plugin for work automation.

## Installation

Claude Code에서 아래 명령어를 실행하세요:

```
/plugin marketplace add symoon94/moonkit
/plugin install moonkit@moonkit
```

설치 후 `/issue-tracker`, `/work-log` 명령어를 사용할 수 있습니다.

### Required MCP servers

스킬에서 사용하는 MCP 연동입니다. 필요한 것만 Claude Code 설정에서 활성화하세요.

| MCP | Used by | Purpose |
|-----|---------|---------|
| Slack | issue-tracker, work-log | 채널/DM 메시지 검색, 스레드 읽기 |
| Gmail | issue-tracker | 이메일 검색, 스레드 읽기 |
| Notion | issue-tracker, work-log | Notion 페이지에 보고서 작성 |
| Jira | work-log | 이슈 트래킹 데이터 |
| Google Calendar | work-log | 미팅/일정 데이터 |

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
  .claude-plugin/
    plugin.json               # Plugin manifest
    marketplace.json          # Marketplace registry
  skills/
    issue-tracker/
      SKILL.md                # Skill definition
      README.md               # Documentation
      references/             # Templates
    work-log/
      SKILL.md                # Skill definition
      README.md               # Documentation
      references/             # Templates
```

## License

MIT
