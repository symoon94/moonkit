# weekly-log: 주간 업무일지 & 이력서 자동 갱신 스킬

## Goal

5개 업무 도구(GitHub, Slack, Jira, Google Calendar, Notion)에서 주간 활동을 자동 수집하여 업무일지를 생성하고, 누적 데이터로 이력서를 자동 갱신하는 gstack/Claude Code 스킬.

## 형태

- **gstack/Claude Code 스킬** (오픈소스 배포)
- 슬래시 커맨드: `/weekly-log`

## 데이터 소스 & 수집 범위

| 소스 | 수집 항목 | on/off |
|------|----------|--------|
| GitHub | 커밋, PR(생성/리뷰/머지), 코드리뷰 | 설정 가능 |
| Slack | 특정 채널에서 내가 보낸 메시지 요약 | 설정 가능 |
| Jira | 나에게 할당된 티켓 전체 상태 | 설정 가능 |
| Google Calendar | 참석한 미팅 목록 | 설정 가능 |
| Notion | 해당 주에 수정된 페이지 목록/요약 | 설정 가능 |

## 설정

- **파일**: `~/.weekly-log/config.yaml` (YAML/JSON)
- 소스별 on/off
- 언어 설정 (한국어/영어 등)
- GitHub 사용자명, Slack 채널 목록, Jira 프로젝트 키 등

## 업무일지

- **출력**: 로컬 Markdown 파일
- **언어**: 사용자 설정 가능

## 이력서

- **포맷**: Markdown (.md)
- **방식**: 기존 `resume.md` + 주간 데이터 누적분을 반영하여 매주 자동 재생성
- **기반**: 기존 이력서 파일을 읽고, 누적된 업무일지를 참조하여 갱신

## 실행

- **트리거**: 완전 자동 (매주 토요일 scheduled task)
- **수동 실행**: `/weekly-log` 커맨드로도 실행 가능

## 대상

- 오픈소스 배포 (MIT License)
