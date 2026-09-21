---
name: fullstack-feature-builder
description: >
  Use this skill when an AI coding agent should end-to-end feature planning and implementation across frontend, backend, database, validation, tests, and deployment readiness.
  It supports developer tasks such as a feature crosses UI, API, and data boundaries, the API contract and frontend behavior need alignment,
  and related engineering work. Do not use it for single-file cosmetic changes.
argument-hint: "[optional focus]"
license: MIT
---

# Fullstack Feature Builder

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

Skill-specific safety focus: this skill commonly touches filesystem, commands, secrets, user-data, database. Keep those areas explicit, bounded, and approval-gated.

## Purpose

End-to-end feature planning and implementation across frontend, backend, database, validation, tests, and deployment readiness.

## When to Use

Use this skill for:

- a feature crosses UI, API, and data boundaries.
- the API contract and frontend behavior need alignment.
- validation and error states must be designed.
- tests and release checks are part of the feature.

Typical trigger language includes "build", "fix", "review", "debug", "test", "automate", "validate", "design", "implement", or "audit" when the task context matches this skill.

## When Not to Use

Do not use this skill for:

- single-file cosmetic changes.
- pure infrastructure work.
- business strategy without code or system impact.

Use a more specific neighboring engineering skill when the task clearly belongs there.

## Operating Principles

- Clarify the outcome, actors, permissions, inputs, and non-goals..
- Define the API and data flow before editing both ends..
- Validate at client, server, and persistence boundaries..
- Include loading, empty, success, and failure states..
- Keep implementation focused and verifiable..

## Local-First Workflow

1. Restate the task, target files, and expected outcome.
2. Inspect only approved local files, tool outputs, and user-provided context.
3. Identify trust boundaries, side effects, and verification needs.
4. Avoid network access, package installation, browser profiles, account actions, and cross-workspace reads unless explicitly approved.
5. Make the smallest useful plan or change.
6. Verify locally with checks proportional to risk.
7. Report changes, evidence, and remaining uncertainty.

## Advanced Workflow

1. scope requirements and trust boundaries.
2. inspect current components, routes, services, models, and tests.
3. design frontend/backend/database flow and API contract.
4. implement focused slices from data model to UI.
5. add tests around behavior, validation, auth, and regressions.
6. verify local checks and deployment readiness notes.

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

- Exercise success, invalid input, auth failure, and persistence behavior..
- Run relevant unit, API, and UI checks where available..
- Confirm no secrets or internal errors leak..

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

### 1. Saved filters

User asks: "Add saved dashboard filters for each user."

Expected behavior: Design the UI state, API contract, ownership model, persistence, and tests.

Safety check: Enforce server-side ownership for every saved filter.

Expected output: Plan, changed files, verification, and residual risk.

### 2. Invitation flow

User asks: "Build team invitations with roles."

Expected behavior: Plan token lifecycle, role permissions, email boundary, acceptance, and expiration.

Safety check: Use single-use expiring tokens and server-side authorization.

Expected output: Feature flow, tests, and safety notes.

### 3. Profile settings

User asks: "Add profile display name and locale settings."

Expected behavior: Reuse existing form patterns, add server validation, and preserve failed input.

Safety check: Do not trust client validation alone.

Expected output: Implementation summary and checks.

