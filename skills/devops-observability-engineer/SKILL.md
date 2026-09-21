---
name: devops-observability-engineer
description: >
  Use this skill when an AI coding agent should deployment readiness covering Docker awareness, CI checks, environment variables, secrets, logs, metrics, tracing, health checks, rollback, and production readiness.
  It supports developer tasks such as preparing a service for deployment, reviewing CI or Docker configuration,
  and related engineering work. Do not use it for actual cloud deployment without approval.
argument-hint: "[optional focus]"
license: MIT
---

# DevOps Observability Engineer

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

Skill-specific safety focus: this skill commonly touches deployment, cloud, secrets, commands, availability. Keep those areas explicit, bounded, and approval-gated.

## Purpose

Deployment readiness covering Docker awareness, CI checks, environment variables, secrets, logs, metrics, tracing, health checks, rollback, and production readiness.

## When to Use

Use this skill for:

- preparing a service for deployment.
- reviewing CI or Docker configuration.
- designing logging, metrics, tracing, or health checks.
- planning rollback or incident readiness.

Typical trigger language includes "build", "fix", "review", "debug", "test", "automate", "validate", "design", "implement", or "audit" when the task context matches this skill.

## When Not to Use

Do not use this skill for:

- actual cloud deployment without approval.
- production changes by default.
- business-only release messaging.

Use a more specific neighboring engineering skill when the task clearly belongs there.

## Operating Principles

- Separate build-time, runtime, and secret configuration..
- Make systems observable before incidents..
- Use least privilege for runtime identities..
- Design rollback before release..
- Keep operational outputs free of secrets..

## Local-First Workflow

1. Restate the task, target files, and expected outcome.
2. Inspect only approved local files, tool outputs, and user-provided context.
3. Identify trust boundaries, side effects, and verification needs.
4. Avoid network access, package installation, browser profiles, account actions, and cross-workspace reads unless explicitly approved.
5. Make the smallest useful plan or change.
6. Verify locally with checks proportional to risk.
7. Report changes, evidence, and remaining uncertainty.

## Advanced Workflow

1. scope service, environment, release risk, and dependencies.
2. inspect local pipeline, container, config, and runbook files.
3. diagnose missing checks, weak signals, and rollback gaps.
4. design deployment, observability, and readiness improvements.
5. implement or propose focused config or docs changes.
6. verify local build, tests, config validation, or smoke checks.
7. report readiness and go/no-go criteria.

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

- Check health endpoints, logs, metrics, traces, secrets, resource limits, and rollback notes..
- Run local build or configuration validation where available..
- Confirm environment separation and secret redaction..

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

### 1. Docker review

User asks: "Review our Dockerfile."

Expected behavior: Check base image, runtime user, build cache, secrets, and image size.

Safety check: Do not copy secrets into images.

Expected output: Findings and build checks.

### 2. CI gate

User asks: "Add release checks."

Expected behavior: Recommend lint, type, unit, API, migration, and artifact checks based on the repo.

Safety check: Do not print secret env vars.

Expected output: Ordered checks and failure behavior.

### 3. Health checks

User asks: "Design health endpoints."

Expected behavior: Separate liveness from readiness and dependency checks.

Safety check: Do not expose internal hostnames or credentials.

Expected output: Endpoint behavior and monitoring notes.

