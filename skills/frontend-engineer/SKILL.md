---
name: frontend-engineer
description: >
  Use this skill when an AI coding agent should accessible, secure, maintainable frontend UI covering components, forms, state, API integration, responsive design, XSS prevention, and browser-native features.
  It supports developer tasks such as building or reviewing UI components, creating forms and client-side validation,
  and related engineering work. Do not use it for backend-only API work.
argument-hint: "[optional focus]"
license: MIT
---

# Frontend Engineer

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

Skill-specific safety focus: this skill commonly touches browser, XSS, tokens, accessibility, API-data. Keep those areas explicit, bounded, and approval-gated.

## Purpose

Accessible, secure, maintainable frontend UI covering components, forms, state, API integration, responsive design, XSS prevention, and browser-native features.

## When to Use

Use this skill for:

- building or reviewing UI components.
- creating forms and client-side validation.
- integrating frontend code with APIs.
- improving accessibility or responsive behavior.

Typical trigger language includes "build", "fix", "review", "debug", "test", "automate", "validate", "design", "implement", or "audit" when the task context matches this skill.

## When Not to Use

Do not use this skill for:

- backend-only API work.
- database schema work.
- visual-only branding without application behavior.

Use a more specific neighboring engineering skill when the task clearly belongs there.

## Operating Principles

- Use semantic HTML and browser-native features first..
- Keep state close to where it is used..
- Represent loading, empty, error, disabled, and success states explicitly..
- Render untrusted content safely..
- Treat client validation as user experience, not enforcement..

## Local-First Workflow

1. Restate the task, target files, and expected outcome.
2. Inspect only approved local files, tool outputs, and user-provided context.
3. Identify trust boundaries, side effects, and verification needs.
4. Avoid network access, package installation, browser profiles, account actions, and cross-workspace reads unless explicitly approved.
5. Make the smallest useful plan or change.
6. Verify locally with checks proportional to risk.
7. Report changes, evidence, and remaining uncertainty.

## Advanced Workflow

1. scope user flow, devices, accessibility needs, and data sources.
2. inspect existing components, styling, state, and API conventions.
3. design component boundaries and state transitions.
4. implement UI, forms, validation, and API integration.
5. verify keyboard, screen reader, responsive, error, and XSS cases.
6. report behavior and remaining browser risks.

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

- Check keyboard navigation, focus, labels, and contrast..
- Test slow network, empty data, validation failure, and forbidden responses..
- Confirm no unsafe HTML injection or secret exposure..

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

### 1. Settings form

User asks: "Create a settings form for name and timezone."

Expected behavior: Build labeled fields, local dirty state, validation, save state, and API error display.

Safety check: Server validation must still enforce rules.

Expected output: Component behavior and accessibility checks.

### 2. Comment rendering

User asks: "Show user comments safely."

Expected behavior: Render text safely or use an approved sanitizer already in the project.

Safety check: Avoid raw HTML injection.

Expected output: Implementation summary and XSS test cases.

### 3. Invoice table

User asks: "Build a responsive invoice table."

Expected behavior: Add accessible sort controls, loading, empty, error, and compact layouts.

Safety check: Do not expose unauthorized fields.

Expected output: UI states and responsive verification.

