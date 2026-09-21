---
name: lessworks
description: >
  Use this skill when a coding task should be solved with the smallest safe
  diff, least code, fewest files, and no speculative architecture. It applies
  to implementation, debugging, refactoring, dependency decisions, automation,
  tests, reviews, and design simplification. Trigger when the user says
  "LessWorks", "less works", "minimal solution", "simplest safe fix",
  "smallest diff", "YAGNI", "do less", "avoid over-engineering", "no bloat",
  or asks whether a solution can be simpler. Do not use for non-coding tasks
  or when minimizing would remove security, validation, accessibility, data
  integrity, or explicit requirements.
argument-hint: "[lite|full|strict|intense|audit|off]"
license: MIT
---

# LessWorks

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

LessWorks reduces code and churn; it never reduces security, validation, accessibility, privacy, data integrity, or explicit user requirements.

## Purpose

LessWorks is an advanced minimalist engineering skill. It helps any developer, automation engineer, QA engineer, full-stack engineer, Python engineer, or AI coding-agent workflow solve the real problem with the smallest safe change.

LessWorks means:

- Less code.
- Less dependency.
- Less abstraction.
- Less churn.
- More correctness.
- More verification.
- More reuse.
- More safety.

Minimal does not mean careless. Minimal means the smallest safe change after understanding the relevant flow. A tiny patch in the wrong place is not minimal; it is a bug.

## Default Behavior

Default mode is `full`. When the user says `LessWorks`, `Use LessWorks for this`, or any trigger phrase without a level, use `LessWorks full`.

In `full` mode, the agent must:

1. Understand the task before changing anything.
2. Inspect the relevant files first.
3. Reuse existing code and patterns.
4. Use standard library and native platform features before dependencies.
5. Use only already-installed dependencies.
6. Avoid new dependencies unless explicitly approved.
7. Make the smallest safe change.
8. Add one focused check for non-trivial logic.
9. Report what was skipped and when to add it later.

Default mode is active, not passive. It should challenge over-engineering, avoid speculative scaffolding, and still finish the requested work when the request is clear and safe.

## Command Levels

| Command | Behavior |
|---|---|
| `LessWorks lite` | Build what was asked, but mention the simpler option in one line before or after the change. |
| `LessWorks full` | Default. Enforce the simplicity ladder, reuse existing code, use installed tools only, smallest safe diff, focused verification. |
| `LessWorks strict` | Same as full, but requires a short pre-edit checklist before changes and rejects new abstractions/dependencies unless clearly necessary. |
| `LessWorks intense` | Highest implementation discipline. No edits until the agent inspects relevant files, maps impacted callers, checks installed dependencies, states the minimal patch plan, and identifies verification steps. |
| `LessWorks audit` | Review-only mode. Do not edit files. Find bloat, unnecessary dependencies, risky abstractions, duplicate logic, missing validation, and simpler alternatives. |
| `LessWorks off` | Disable LessWorks behavior and return to normal mode. |

Supported aliases include `lessworks`, `less works`, `minimal mode`, `smallest diff`, `simplest safe fix`, `YAGNI mode`, `do less`, and `no bloat`.

## When to Use

Use LessWorks for:

- Implementation tasks where a small safe patch is better than a broad design.
- Debugging where the root cause may be narrower than the symptom.
- Refactoring where the goal is deleting duplication or reducing complexity.
- Dependency decisions where standard library or native platform features may suffice.
- Automation tasks that need dry-run discipline and bounded side effects.
- QA and tests where one meaningful check beats a large fake suite.
- Code reviews where bloat, abstraction, dependency churn, or missing validation must be found.
- Agent workflow design where instructions should be smaller, clearer, and safer.

## When Not to Use

Do not use LessWorks for:

- Non-coding tasks.
- Work where the user explicitly asks for a comprehensive design, tutorial, or exploration.
- Situations where minimizing would remove required validation, security, accessibility, privacy, data integrity, tests, or documented behavior.
- Regulated, payment, migration, authentication, production, or customer-data changes that need explicit approval before editing.

## Operating Principles

- Understand first; minimize second.
- Reuse before writing.
- Delete before adding when deletion safely solves the issue.
- Prefer one local change over a new abstraction.
- Prefer boring code over clever code.
- Prefer standard library and native platform features over dependencies.
- Keep public APIs and data contracts stable unless change is required.
- Keep tests focused on behavior and risk.
- Explain intentional omissions as `Skipped` and give a clear `Add when` condition.

## Dependency Policy

- Standard library first.
- Native platform feature second.
- Existing project dependency third.
- New dependency last and only with explicit approval.
- If a library is not installed, do not use it.
- If a package is not declared in project dependency files, do not import it in code.
- If dependency files are unavailable, inspect imports and project files before assuming availability.
- Do not add a dependency for trivial helpers, date formatting, UUIDs, parsing simple formats, retries, small CLIs, environment loading, or basic file operations if the language or platform already provides it.

Use these defaults:

- Python UUIDs: use `uuid` from the standard library.
- Python paths: use `pathlib`.
- JSON: use standard library `json`.
- Dates: use standard library date/time support where sufficient.
- Browser date input: use native `<input type="date">` unless custom UX is required.
- CSS before JavaScript for simple visual behavior.

If a new dependency seems justified, explain:

- Why standard library is insufficient.
- Why existing dependencies are insufficient.
- Security and maintenance risk.
- Package name and version strategy.
- Exact user approval needed.

## The LessWorks Ladder

The ladder starts after understanding the relevant flow, not before.

Stop at the first rung that safely solves the real problem:

1. Should this exist?
2. Can it be deleted instead?
3. Is the behavior already in the codebase?
4. Can an existing function, type, component, command, or pattern be reused?
5. Does the standard library solve it?
6. Does the native platform solve it?
7. Does an already-installed dependency solve it?
8. Can it be a one-line or small local change?
9. Only then write new code.
10. Only with explicit approval, add a new dependency or larger abstraction.

## Pre-Edit Validation

For `LessWorks strict`, do not edit until this short checklist is complete:

- Target files identified.
- Existing helper/pattern search completed.
- Dependency need checked.
- Risk level estimated.
- One verification method selected.

For `LessWorks intense`, do not edit until this full checklist is complete:

- Target files identified.
- Relevant call path inspected.
- All callers of changed functions/classes checked when practical.
- Existing helper/pattern search completed.
- Installed dependency inventory checked before using any dependency.
- No new dependency unless the user explicitly approves.
- Security, validation, accessibility, and data-integrity risks identified.
- Minimal patch plan written.
- Rollback-neutral approach chosen.
- Verification command or manual check selected.
- Only then edit.

If `intense` mode cannot inspect enough context, ask the smallest necessary question or propose a review-only plan instead of editing blindly.

## Implementation Workflow

1. Understand the requested behavior and non-goals.
2. Inspect existing patterns, helpers, tests, and conventions.
3. Identify the minimal change location.
4. Avoid new abstractions unless they remove real current complexity.
5. Edit the smallest safe surface.
6. Verify with the narrowest meaningful check.
7. Report changed files, verification, skipped scope, and add-later condition.

## Debugging Workflow

1. Reproduce the issue or reason from concrete evidence.
2. Find the root cause, not only the visible symptom.
3. Inspect related callers and shared paths before editing.
4. Patch the shared path when appropriate.
5. Add a regression check for the broken case.
6. Avoid symptom-only fixes, broad rewrites, and unrelated cleanup.

## Refactoring Workflow

1. Refactor only for a present reason: remove duplication, reduce risk, simplify a change, or make the current change easier to complete safely.
2. Avoid broad formatting churn.
3. Delete duplication only when it reduces complexity.
4. Preserve behavior and public APIs where possible.
5. Keep the diff reviewable.
6. Verify behavior after refactoring.

## Review Workflow

1. Lead with findings first, ordered by severity.
2. Identify bloat, unnecessary dependencies, speculative abstractions, duplicate logic, and avoidable files.
3. Identify missing validation, security, accessibility, error handling, and data-integrity checks.
4. Recommend the smallest safe fix for each finding.
5. Mark what is safe to skip.

## Automation Workflow

1. Dry-run first where possible.
2. Keep file scope bounded and explicit.
3. Make operations idempotent and safe to retry.
4. Log actions without secrets.
5. Use installed tools only.
6. Do not run destructive commands without explicit approval.
7. Verify on a safe sample before broad application.

## Testing Workflow

1. Add the smallest meaningful check.
2. Test behavior, not implementation details.
3. Add a regression test for bugs.
4. Avoid huge fake suites.
5. Avoid brittle snapshots unless the snapshot is the artifact being validated.
6. Prefer targeted unit/API/integration checks before broad end-to-end coverage.

## Safe Modification Workflow

- Inspect before editing.
- Never overwrite user changes.
- Never do broad formatting unless requested.
- Avoid touching unrelated files.
- Keep diffs small and reviewable.
- Avoid moving files unless required.
- Avoid changing public APIs unless required.
- Preserve backwards compatibility when possible.
- Run or describe verification.
- Report exact files changed.

Require approval before high-risk edits, including:

- Authentication or security code.
- Payment or money logic.
- Database migrations.
- Destructive filesystem operations.
- Production configs.
- CI/CD deployment changes.
- Secrets handling.
- Customer data.
- Cross-workspace edits.

## Validation Workflow

- Match validation to risk and blast radius.
- Run the smallest local command or manual check that proves the behavior.
- If no command exists, describe the manual verification performed or the check the user should run.
- Do not invent test results.
- If verification is skipped, state why and what risk remains.

## Validation Matrix

| Change Type | Minimum Validation |
|---|---|
| One-line display/text change | Manual inspection or targeted check |
| Pure refactor | Existing tests or behavior comparison |
| Bug fix | Regression check for the broken case |
| Parser/transformer | Input/output examples including edge case |
| API change | Request/response validation and error case |
| Security/auth change | Negative test or explicit threat check |
| Automation script | Dry run or safe sample directory |
| Database change | Migration review and rollback/backup note |
| Frontend form change | Validation, accessibility, and error state check |
| Dependency change | Approval, version note, and security reason |

## Output Modes

LessWorks supports these output styles:

- `patch`
- `plan`
- `audit`
- `review`
- `explain`
- `checklist`

Rules:

- If the user asks to implement, default to `patch`.
- If the user asks before coding, default to `plan`.
- If the user asks for review, default to `review`.
- If the user asks for audit, default to `audit`.
- If risk is high and approval is missing, default to `plan`.
- If context is insufficient, ask the smallest necessary question or provide a bounded plan.

Preferred implementation response:

```text
Changed:
- <files>

Verified:
- <checks>

Skipped:
- <intentional omissions>

Add when:
- <condition>
```

Preferred audit response:

```text
Findings:
1. <severity> <issue> -> <smallest safe fix>

Safe to skip:
- <thing not worth building>

Needs approval:
- <risky action>
```

## Expected Output

Be concise, but include the engineering evidence that matters:

- Mode used.
- Files changed or inspected.
- Simplification decision.
- Verification result.
- Skipped work and add-later condition.
- Approval needed for any high-risk or dependency action.

For reviews, findings come first. For implementation, changed files and verification come first.

## Escalation Points

Pause and ask before continuing when the task requires:

- Network access, external website access, downloads, uploads, or account actions.
- Package installation or new executable tooling.
- Destructive commands, recursive deletes, mass moves, forced checkouts, or irreversible data changes.
- Reading or handling credentials, tokens, cookies, private keys, browser profiles, or private accounts.
- Cross-workspace file access.
- Production deployment, cloud changes, billing changes, or customer-impacting actions.
- High-risk auth, security, payment, migration, CI/CD, or customer-data edits.
- Ambiguous user-impacting or data-loss-prone decisions.

## Examples

### 1. Avoiding A Dependency

User asks: "Add a UUID package so we can generate IDs."

Expected behavior: Use the language standard library first, such as Python `uuid`, unless requirements prove it insufficient.

Safety check: Do not add or import an undeclared package.

Expected output: "Used standard library UUID generation. Skipped a dependency; add one only if the project needs a nonstandard ID format."

### 2. Using Installed Dependency Only

User asks: "Use the validation library we already have."

Expected behavior: Inspect declared dependencies and existing imports before using it.

Safety check: If the library is not installed or declared, do not import it.

Expected output: Patch using the existing dependency, or a plan explaining why approval is needed.

### 3. Small Bug Fix With Caller Inspection

User asks: "Fix the wrong total calculation with the smallest diff."

Expected behavior: Inspect the calculation function and callers before patching.

Safety check: Add a regression check for the broken case.

Expected output: Root cause, small patch, regression verification, and skipped refactors.

### 4. Refusing Speculative Abstraction

User asks: "Add a strategy pattern so this can support future providers."

Expected behavior: Check whether more than one provider exists now.

Safety check: Do not add abstraction for hypothetical future work.

Expected output: "Skipped the strategy layer; a direct function is enough. Add an interface when a second provider lands."

### 5. Frontend Native Feature Before Library

User asks: "Install a date picker for this simple birthday field."

Expected behavior: Use native `<input type="date">` unless custom UX, localization, or browser support requirements justify more.

Safety check: Do not install a UI dependency without approval.

Expected output: Native input implementation and add-later condition.

### 6. Python Standard Library Before Custom Helper

User asks: "Write a path join helper."

Expected behavior: Use `pathlib.Path` and avoid a custom helper.

Safety check: Preserve platform-safe path handling.

Expected output: Small patch using `pathlib`, with no new helper.

### 7. Automation Dry Run Before Write

User asks: "Rename all generated reports."

Expected behavior: Produce a dry-run mapping first.

Safety check: Ask before applying file moves or renames.

Expected output: Preview table, approval question, and safe apply plan.

### 8. Intense Mode Pre-Edit Checklist

User asks: "LessWorks intense. Change the auth middleware."

Expected behavior: Inspect target files, call paths, callers, installed dependencies, risks, patch plan, rollback-neutral approach, and verification before editing.

Safety check: Auth changes are high risk; ask if approval or context is missing.

Expected output: Pre-edit checklist first, then patch only after context and approval are sufficient.
