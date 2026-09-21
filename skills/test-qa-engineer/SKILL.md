---
name: test-qa-engineer
description: >
  Use this skill when an AI coding agent should testing and QA guidance covering unit, integration, API, E2E, regression, edge cases, failure cases, test data, minimal useful coverage, and quality gates.
  It supports developer tasks such as planning test strategy, adding tests for a feature or bug,
  and related engineering work. Do not use it for writing huge suites disconnected from risk.
argument-hint: "[optional focus]"
license: MIT
---

# Test QA Engineer

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

Skill-specific safety focus: this skill commonly touches commands, test-data, browser, secrets, flakiness. Keep those areas explicit, bounded, and approval-gated.

## Purpose

Testing and QA guidance covering unit, integration, API, E2E, regression, edge cases, failure cases, test data, minimal useful coverage, and quality gates.

## When to Use

Use this skill for:

- planning test strategy.
- adding tests for a feature or bug.
- reviewing QA gaps.
- debugging flaky tests or quality gates.

Typical trigger language includes "build", "fix", "review", "debug", "test", "automate", "validate", "design", "implement", or "audit" when the task context matches this skill.

## When Not to Use

Do not use this skill for:

- writing huge suites disconnected from risk.
- snapshot-heavy tests for volatile UI.
- testing implementation details unnecessarily.

Use a more specific neighboring engineering skill when the task clearly belongs there.

## Operating Principles

- Test behavior users and systems rely on..
- Cover risk, not every line mechanically..
- Use realistic minimal data..
- Add regression checks for fixed bugs..
- Keep tests deterministic and maintainable..

## Local-First Workflow

1. Restate the task, target files, and expected outcome.
2. Inspect only approved local files, tool outputs, and user-provided context.
3. Identify trust boundaries, side effects, and verification needs.
4. Avoid network access, package installation, browser profiles, account actions, and cross-workspace reads unless explicitly approved.
5. Make the smallest useful plan or change.
6. Verify locally with checks proportional to risk.
7. Report changes, evidence, and remaining uncertainty.

## Advanced Workflow

1. scope behavior, risks, and existing test layers.
2. inspect test framework, fixtures, commands, and coverage gaps.
3. design minimal unit, integration, API, E2E, regression, and security checks.
4. implement focused tests or QA plan.
5. run relevant local checks.
6. report coverage, failures, and remaining gaps.

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

- Run changed tests and nearest related suites..
- Include success, failure, edge, and authorization cases..
- Document skipped checks and residual risk..

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

### 1. Signup tests

User asks: "Add tests for signup."

Expected behavior: Cover success, duplicate email, invalid input, weak password, and session behavior.

Safety check: Password must never be returned.

Expected output: Test list and commands.

### 2. Bug regression

User asks: "Users can save blank names."

Expected behavior: Add a regression test at the enforcing layer.

Safety check: Server validation must reject bypassed clients.

Expected output: Failing case and fix verification.

### 3. Protected API

User asks: "Test the project update endpoint."

Expected behavior: Cover success, unauthenticated, unauthorized, missing resource, invalid payload, and conflict.

Safety check: Prevent IDOR.

Expected output: API test matrix.

