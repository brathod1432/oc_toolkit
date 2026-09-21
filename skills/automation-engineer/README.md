# Automation Engineer

## Summary

General automation guidance covering local workflows, repeatable scripts, safe filesystem operations, dry runs, logs, idempotency, and approval-gated side effects.

## What This Skill Helps With

- workflow automation.
- safe filesystem operations.
- dry-run design.
- idempotent scripting.
- automation review.

## Typical Use Cases

- automating repetitive local tasks.
- designing safe file operations.
- turning manual workflows into repeatable commands.
- reviewing automation for idempotency and auditability.

## Safety Model

This skill is local-first. Network access, package installation, destructive commands, cross-workspace file access, credential handling, browser profile access, account actions, and production-impacting changes require explicit user approval.

## Files Included

- `SKILL.md` is the canonical agent instruction.
- `SKILL_METADATA.json` contains local metadata.
- `examples.md` shows practical usage examples.
- `validation.md` contains a skill-specific validation checklist.
- `references/README.md` explains optional local references.

## How to Use

Open `SKILL.md` and provide it to any AI coding agent when the task matches the trigger description. Use `examples.md` for calibration and `validation.md` for readiness checks.

## Validation

Validate by checking structure, metadata consistency, local-first safety gates, workflow depth, practical examples, and final output quality.
