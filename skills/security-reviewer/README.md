# Security Reviewer

## Summary

Secure coding and web security review covering auth, authorization, OWASP-style risks, XSS, CSRF, SSRF, SQL injection, secrets, dependency risk, and safe recommendations.

## What This Skill Helps With

- secure code review.
- auth review.
- OWASP risk analysis.
- secret handling.
- dependency risk review.

## Typical Use Cases

- reviewing code for security risks.
- changing authentication or authorization.
- checking secret handling.
- assessing web attack surfaces.

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
