# LessWorks

LessWorks is an advanced minimalist engineering skill for AI coding agents. It drives work toward the smallest safe diff, least code, fewest files, no speculative architecture, and stronger verification.

## Summary

Use LessWorks when a developer task risks over-engineering, unnecessary dependencies, broad rewrites, or symptom-only fixes. It applies to implementation, debugging, refactoring, reviews, automation, tests, dependency decisions, Python work, full-stack work, QA, and agent workflow design.

Default mode is `LessWorks full`.

## Command Levels

| Command | Behavior |
|---|---|
| `LessWorks lite` | Build what was asked, but mention the simpler option in one line. |
| `LessWorks full` | Default. Enforce reuse, installed tools only, smallest safe diff, and focused verification. |
| `LessWorks strict` | Requires a short pre-edit checklist and rejects new abstractions or dependencies unless necessary. |
| `LessWorks intense` | Requires inspection, caller mapping, dependency inventory, minimal patch plan, and verification plan before edits. |
| `LessWorks audit` | Review-only mode for finding bloat, risky abstractions, missing validation, and simpler alternatives. |
| `LessWorks off` | Disable LessWorks behavior. |

Aliases include `lessworks`, `less works`, `minimal mode`, `smallest diff`, `simplest safe fix`, `YAGNI mode`, `do less`, and `no bloat`.

## Dependency Policy

LessWorks uses standard library first, native platform features second, existing project dependencies third, and new dependencies last with explicit approval. If a package is not installed or declared, do not import it.

## What This Skill Helps With

- Minimal implementation and smallest safe diffs.
- Dependency avoidance and installed-dependency checks.
- Root-cause debugging with caller inspection.
- Refactoring without broad churn.
- Review/audit of bloat, abstraction, and validation gaps.
- Automation dry-runs and bounded side effects.
- Focused tests and verification.

## Safety Model

LessWorks is local-first. Network access, package installation, destructive commands, cross-workspace access, secret handling, production-impacting changes, and side-effecting account actions require explicit user approval.

## Files Included

- `SKILL.md` is the canonical agent instruction.
- `SKILL_METADATA.json` contains local metadata.
- `examples.md` shows practical usage examples.
- `validation.md` contains a LessWorks validation checklist.
- `references/README.md` explains optional local references.

## How to Use

Use `LessWorks` for default `full` mode, or specify a level such as `LessWorks strict`, `LessWorks intense`, or `LessWorks audit`.

## Validation

Validate by checking metadata, command levels, dependency policy, pre-edit gates, local-first safety, examples, and output mode behavior.
