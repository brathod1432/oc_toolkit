---
name: python-engineer
description: >
  Use this skill when an AI coding agent should python coding guidance covering clean Python, standard library first, typing, packaging awareness, CLI utilities, file processing, error handling, tests, and safe automation scripts.
  It supports developer tasks such as writing or reviewing Python modules, building CLI utilities or local tools,
  and related engineering work. Do not use it for non-Python implementation tasks.
argument-hint: "[optional focus]"
license: MIT
---

# Python Engineer

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

Skill-specific safety focus: this skill commonly touches filesystem, commands, dependencies, secrets, data-loss. Keep those areas explicit, bounded, and approval-gated.

## Purpose

Python coding guidance covering clean Python, standard library first, typing, packaging awareness, CLI utilities, file processing, error handling, tests, and safe automation scripts.

## When to Use

Use this skill for:

- writing or reviewing Python modules.
- building CLI utilities or local tools.
- processing files safely.
- adding tests or typing to Python code.

Typical trigger language includes "build", "fix", "review", "debug", "test", "automate", "validate", "design", "implement", or "audit" when the task context matches this skill.

## When Not to Use

Do not use this skill for:

- non-Python implementation tasks.
- unsafe automation that mutates files without approval.
- package installation without explicit approval.

Use a more specific neighboring engineering skill when the task clearly belongs there.

## Operating Principles

- Prefer the standard library before adding dependencies..
- Use clear functions, types, and errors..
- Stream large files where practical..
- Keep CLIs dry-run friendly for side effects..
- Test non-trivial parsing, branching, and filesystem behavior..

## Local-First Workflow

1. Restate the task, target files, and expected outcome.
2. Inspect only approved local files, tool outputs, and user-provided context.
3. Identify trust boundaries, side effects, and verification needs.
4. Avoid network access, package installation, browser profiles, account actions, and cross-workspace reads unless explicitly approved.
5. Make the smallest useful plan or change.
6. Verify locally with checks proportional to risk.
7. Report changes, evidence, and remaining uncertainty.

## Advanced Workflow

1. scope inputs, outputs, environment, and side effects.
2. inspect existing Python style, dependency files, and tests.
3. design small functions and typed boundaries.
4. implement parsing, error handling, and CLI behavior.
5. add focused tests or self-checks.
6. verify lint, type, or test commands if available.

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

- Run relevant Python tests or a local smoke command..
- Check path handling, encoding, large input, and failure cases..
- Confirm no secrets are logged or embedded..

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

### 1. CLI utility

User asks: "Write a Python CLI to rename report files."

Expected behavior: Design dry-run output, literal path handling, and clear errors.

Safety check: Ask before actual rename operations.

Expected output: CLI behavior and verification.

### 2. CSV parser

User asks: "Parse messy CSV exports."

Expected behavior: Use standard library or existing dependencies and validate headers.

Safety check: Do not print sensitive rows.

Expected output: Parsed output and edge-case tests.

### 3. Type cleanup

User asks: "Add typing to this module."

Expected behavior: Introduce useful annotations without broad rewrites.

Safety check: Do not change runtime behavior unexpectedly.

Expected output: Focused patch and tests.

