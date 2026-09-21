---
name: backend-api-engineer
description: >
  Use this skill when an AI coding agent should backend API design and implementation covering schemas, validation, auth boundaries, pagination, idempotency, errors, logging, and safe CORS.
  It supports developer tasks such as creating or changing HTTP APIs, defining request and response schemas,
  and related engineering work. Do not use it for frontend-only UI work.
argument-hint: "[optional focus]"
license: MIT
---

# Backend API Engineer

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

Skill-specific safety focus: this skill commonly touches auth, CORS, secrets, user-data, logging. Keep those areas explicit, bounded, and approval-gated.

## Purpose

Backend API design and implementation covering schemas, validation, auth boundaries, pagination, idempotency, errors, logging, and safe CORS.

## When to Use

Use this skill for:

- creating or changing HTTP APIs.
- defining request and response schemas.
- adding pagination, rate limits, or idempotency.
- reviewing auth boundaries and error handling.

Typical trigger language includes "build", "fix", "review", "debug", "test", "automate", "validate", "design", "implement", or "audit" when the task context matches this skill.

## When Not to Use

Do not use this skill for:

- frontend-only UI work.
- database-only migration planning.
- tasks where no service boundary is involved.

Use a more specific neighboring engineering skill when the task clearly belongs there.

## Operating Principles

- Define contracts before implementation..
- Validate path, query, header, and body inputs..
- Authorize before side effects..
- Return consistent safe errors..
- Keep controllers thin and service logic focused..

## Local-First Workflow

1. Restate the task, target files, and expected outcome.
2. Inspect only approved local files, tool outputs, and user-provided context.
3. Identify trust boundaries, side effects, and verification needs.
4. Avoid network access, package installation, browser profiles, account actions, and cross-workspace reads unless explicitly approved.
5. Make the smallest useful plan or change.
6. Verify locally with checks proportional to risk.
7. Report changes, evidence, and remaining uncertainty.

## Advanced Workflow

1. scope resource, method, users, and permissions.
2. inspect existing routes, middleware, validators, services, and tests.
3. design schemas, status codes, errors, pagination, and idempotency.
4. implement controller and service changes.
5. add API tests for success, validation, auth, conflicts, and limits.
6. verify logs, CORS, and sensitive error behavior.

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

- Run API tests or local request checks..
- Confirm unauthorized and forbidden cases are distinct where the project expects that..
- Check logs do not print secrets or sensitive payloads..

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

### 1. Create endpoint

User asks: "Add an endpoint to create projects."

Expected behavior: Define route, schemas, validation, auth, service call, and response.

Safety check: Create only within the authenticated tenant or account.

Expected output: API contract, files changed, and tests.

### 2. Activity feed

User asks: "Return paginated account activity."

Expected behavior: Use bounded page size and stable ordering.

Safety check: Filter by authorized scope before pagination.

Expected output: Contract and edge cases.

### 3. Retryable import

User asks: "Make CSV import safe to retry."

Expected behavior: Add idempotency and conflict behavior.

Safety check: Do not log full uploaded rows.

Expected output: Idempotency design and tests.

