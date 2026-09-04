#!/usr/bin/env python3
"""Summarize PR checks and unresolved review threads via gh.

Usage:
    python3 pr_watch.py OWNER REPO PR_NUMBER
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter


def run(args: list[str]) -> str:
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT)


def gh_json(args: list[str]) -> object:
    return json.loads(run(args))


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: pr_watch.py OWNER REPO PR_NUMBER", file=sys.stderr)
        return 2

    owner, repo, pr = sys.argv[1], sys.argv[2], int(sys.argv[3])
    print(f"PR: {owner}/{repo}#{pr}")

    try:
        checks_raw = run(
            [
                "gh",
                "pr",
                "checks",
                str(pr),
                "--repo",
                f"{owner}/{repo}",
                "--json",
                "name,state,link,description,workflow",
            ]
        )
        checks = json.loads(checks_raw) if checks_raw.strip() else []
    except subprocess.CalledProcessError as exc:
        print("\nChecks: unavailable")
        print(exc.output.strip())
        checks = []

    if checks:
        counts = Counter(check.get("state", "UNKNOWN") for check in checks)
        print("\nChecks:")
        for state, count in sorted(counts.items()):
            print(f"  {state}: {count}")
        for check in checks:
            state = check.get("state", "UNKNOWN")
            if state not in {"SUCCESS", "SKIPPED"}:
                name = check.get("name") or check.get("workflow") or "unnamed"
                link = check.get("link") or ""
                print(f"  - {state}: {name} {link}".rstrip())
    else:
        print("\nChecks: none reported")

    query = """
    query($owner:String!,$repo:String!,$pr:Int!){
      repository(owner:$owner,name:$repo){
        pullRequest(number:$pr){
          reviewDecision
          reviewThreads(first:100){
            nodes{
              id
              isResolved
              isOutdated
              path
              line
              comments(first:20){
                nodes{
                  author{login}
                  body
                  url
                  createdAt
                }
              }
            }
          }
        }
      }
    }
    """
    data = gh_json(
        [
            "gh",
            "api",
            "graphql",
            "-f",
            f"query={query}",
            "-F",
            f"owner={owner}",
            "-F",
            f"repo={repo}",
            "-F",
            f"pr={pr}",
        ]
    )
    pull = data["data"]["repository"]["pullRequest"]
    threads = pull["reviewThreads"]["nodes"]
    unresolved = [
        thread
        for thread in threads
        if not thread["isResolved"] and not thread["isOutdated"]
    ]

    print(f"\nReview decision: {pull.get('reviewDecision')}")
    print(f"Unresolved active threads: {len(unresolved)}")
    for idx, thread in enumerate(unresolved, 1):
        comments = thread["comments"]["nodes"]
        last = comments[-1]
        body = " ".join(last["body"].split())
        if len(body) > 500:
            body = body[:497] + "..."
        anchor = f"{thread.get('path')}:{thread.get('line') or ''}".rstrip(":")
        print(f"\n[{idx}] {anchor}")
        print(f"    by {last['author']['login']}: {last['url']}")
        print(f"    {body}")

    has_bad_checks = any(
        check.get("state") not in {"SUCCESS", "SKIPPED"} for check in checks
    )
    if has_bad_checks or unresolved:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
