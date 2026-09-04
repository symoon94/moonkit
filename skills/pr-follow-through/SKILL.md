---
name: pr-follow-through
description: Use after creating or pushing a GitHub PR to wait for CI, verify every bot or human review comment against the code, fix and resolve valid findings, explain and resolve invalid findings, and repeat until the PR is ready to land.
metadata:
  short-description: Verify PR feedback and loop fixes through CI
---

# PR Follow Through

Use this skill after opening a PR, pushing updates to a PR branch, or when the user asks Claude to wait for CI or review comments. The goal is a PR in a reasonable landing state, not merely a created PR.

## Workflow

1. Resolve the PR from the supplied URL or number. Otherwise run:
   ```bash
   gh pr view --json number,url,headRefName,baseRefName
   ```
2. Run the complete audit:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/pr-follow-through/scripts/pr_watch.py" OWNER REPO PR_NUMBER
   ```
   This audit is mandatory because top-level PR comment APIs miss inline review threads.
3. Inspect every unresolved thread and verify its claim against the current code, tests, and PR scope. Reviewer confidence, severity labels, and bot output are not proof. Record one evidence-backed verdict:
   - **Valid:** fix the underlying issue, run relevant checks, commit and push, then resolve the thread. Never resolve before the fix exists on the remote PR branch.
   - **Invalid:** do not change the code. Post a concise reply explaining why the scenario cannot occur, is already handled, is stale, or would be made worse by the suggestion. Cite concrete evidence such as `file:line`, runtime behavior, or test output, then resolve the thread.
   - **Unclear:** post the specific question or missing assumption and leave the thread unresolved.
   - **Valid but out of scope:** explain why it should not expand this PR, propose a concrete follow-up, and leave it unresolved unless the reviewer accepts that disposition.
   Apply the same rules to stale and outdated threads. Verify that the underlying concern is gone, reply with the evidence, and only then resolve it.
4. When fixes are needed:
   - Patch only the relevant code.
   - Run relevant tests and checks.
   - Stage specific files and inspect `git diff --cached --name-only`.
   - Commit and push to the PR branch.
   - Wait for checks to complete, then run the audit again. Review bots often comment only after CI finishes.
5. Repeat until checks pass and all threads are resolved, except threads explicitly identified as requiring more work, an accepted out-of-scope decision, or a human decision.

## Review Judgment

Treat review comments as hypotheses. A finding is valid only when the current code and a realistic execution path support it. A finding is invalid when the claimed path cannot occur, existing behavior already handles it, the comment is stale, or the proposed change would make behavior worse. A low-risk patch is still unjustified without evidence.

## Exit Checklist

- Run the audit after the latest push and after CI or review bots have settled.
- Confirm checks pass, are expectedly skipped, or are blocked by named infrastructure.
- Confirm every reviewed thread has an evidence-backed verdict.
- Confirm every valid thread was resolved only after its fix was pushed.
- Confirm every invalid or obsolete thread received an explanatory reply before resolution.
- List every intentionally open thread with its ID and exact reason.
- Report totals for valid-and-fixed, invalid-and-explained, and intentionally open findings, plus test and CI evidence.

## Authorization and Safety

- Invoking this skill to handle PR feedback authorizes the evidence-backed thread replies and resolutions required by this workflow. Do not post unrelated PR conversation comments.
- Do not expand scope to fix a valid but out-of-scope finding without the user's approval.
- Do not stage unrelated generated workspace or data files.
- If CI is queued on unavailable self-hosted runners, report an infrastructure wait rather than a code failure.
