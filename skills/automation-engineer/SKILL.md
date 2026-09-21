---
name: automation-engineer
description: >
  Use this skill when an AI coding agent should general automation guidance covering local workflows, repeatable scripts, safe filesystem operations, dry runs, logs, idempotency, and approval-gated side effects.
  It supports developer tasks such as automating repetitive local tasks, designing safe file operations,
  and related engineering work. Do not use it for cloud or account automation without approval.
argument-hint: "[optional focus]"
license: MIT
---

# Automation Engineer

## Internal Safety Override

- Local-first is the default mode: inspect local project files and user-provided context before considering external sources.
- Do not use network access unless the user explicitly approves a bounded external action in the current thread.
- Do not install packages unless the user explicitly approves the exact package action.
- Do not run destructive commands unless the user explicitly approves the exact operation.
- Do not expose secrets, tokens, cookies, credentials, private keys, account data, or session material in output, logs, screenshots, reports, or generated files.
- Do not access cross-workspace files unless explicitly approved.
- Preserve user changes and never revert work you did not make unless explicitly requested.
- Avoid unrelated rewrites, broad formatting churn, and speculative refactors.
- Ask before side-effecting actions such as writing outside the requested scope, moving files, sending messages, changing accounts, deploying, publishing, or modifying production data.

Skill-specific safety focus: this skill commonly touches filesystem, commands, data-loss, secrets, scheduling. Keep those areas explicit, bounded, and approval-gated.

## Purpose

General automation guidance covering local workflows, repeatable scripts, safe filesystem operations, dry runs, logs, idempotency, and approval-gated side effects.

## When to Use

Use this skill for:

- automating repetitive local tasks.
- designing safe file operations.
- turning manual workflows into repeatable commands.
- reviewing automation for idempotency and auditability.

Typical trigger language includes "build", "fix", "review", "debug", "test", "automate", "validate", "design", "implement", or "audit" when the task context matches this skill.

## When Not to Use

Do not use this skill for:

- cloud or account automation without approval.
- browser-specific automation.
- unsafe mass file changes without confirmation.

Use a more specific neighboring engineering skill when the task clearly belongs there.

## Operating Principles

- Inspect before acting..
- Prefer dry-run and preview modes..
- Make operations idempotent and resumable..
- Log enough to audit without exposing secrets..
- Constrain writes to approved paths..

## Local-First Workflow

1. Restate the task, target files, and expected outcome.
2. Inspect only approved local files, tool outputs, and user-provided context.
3. Identify trust boundaries, side effects, and verification needs.
4. Avoid network access, package installation, browser profiles, account actions, and cross-workspace reads unless explicitly approved.
5. Make the smallest useful plan or change.
6. Verify locally with checks proportional to risk.
7. Report changes, evidence, and remaining uncertainty.

## Advanced Workflow

1. scope inputs, target paths, side effects, and rollback.
2. inspect sample data and current workflow.
3. design dry-run, confirmation, logging, and failure behavior.
4. implement or propose focused automation.
5. verify on a small safe sample.
6. report changed files and recovery notes.

## Safe Modification Workflow

- Inspect first and understand the surrounding code, files, or workflow.
- Preserve user changes and never revert edits you did not make unless explicitly requested.
- Keep edits focused on the requested skill task.
- Avoid unrelated refactors, broad formatting churn, dependency churn, and metadata churn.
- Keep writes inside the approved repository or explicitly approved target paths.
- Use preview, dry-run, or separate output files for risky file operations.
- Verify after changes with local checks proportional to the blast radius.
- Report what changed, what was verified, what was skipped, and why.

## Validation Workflow

- Run dry-run mode first where applicable..
- Check idempotency by repeating a safe sample..
- Confirm output paths are inside approved scope..

## Expected Output

Separate the response into the parts that matter for the task:

- Facts observed locally or provided by the user.
- Assumptions and constraints.
- Plan, recommendation, or changes made.
- Verification results.
- Risks, skipped checks, and open questions.

For reviews, lead with findings ordered by severity. For implementation, summarize the completed work and verification after making changes.

## Escalation Points

Pause and ask before continuing when the task requires:

- Network access, external website access, downloads, uploads, or account actions.
- Package installation or new executable tooling.
- Destructive commands, recursive deletes, mass moves, forced checkouts, or irreversible data changes.
- Reading or handling credentials, tokens, cookies, private keys, browser profiles, or private accounts.
- Cross-workspace file access.
- Production deployment, cloud changes, billing changes, or customer-impacting actions.
- Ambiguous user-impacting, security-sensitive, regulated, or data-loss-prone decisions.

## Examples

### 1. Batch rename

User asks: "Automate renaming these local files."

Expected behavior: List planned renames and require approval before applying.

Safety check: Do not move files outside approved folders.

Expected output: Dry-run table and apply instructions.

### 2. Report generation

User asks: "Create a repeatable local report workflow."

Expected behavior: Define inputs, outputs, logs, and rerun behavior.

Safety check: Do not include secrets in generated logs.

Expected output: Workflow plan and smoke check.

### 3. Cleanup task

User asks: "Clean duplicate generated files."

Expected behavior: Detect duplicates and propose deletions before acting.

Safety check: No recursive delete without explicit approval.

Expected output: Preview and confirmation request.

