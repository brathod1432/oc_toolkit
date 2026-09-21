# LessWorks — Always-Active Engineering Discipline

**This rule is PERMANENTLY ACTIVE. It applies to every coding task in every session without the user having to ask.**

LessWorks `full` mode is the default for all code work here. Do not wait for a trigger phrase.

---

## The Core Rule

**Smallest safe change. Every time.**

Before writing a single line of code:
1. Understand what's actually needed
2. Check if it already exists in the codebase
3. Walk the LessWorks Ladder (stop at the first rung that safely solves it):
   - Should this exist at all?
   - Can it be deleted instead?
   - Is this already in the codebase?
   - Can an existing function, pattern, or component be reused?
   - Does the standard library solve it?
   - Does the native platform solve it?
   - Does an already-installed dependency solve it?
   - Can it be a one-line or small local change?
   - Only then write new code
   - Only with explicit approval: add a new dependency or larger abstraction

---

## Always-On Constraints

- **No new files** unless the task genuinely requires them
- **No new dependencies** without explicit user approval for that specific package
- **No broad rewrites** — change only what the task requires
- **No speculative code** — do not add abstractions for hypothetical future use
- **No formatting churn** — do not reformat lines not being changed
- **No touching unrelated files** — even if they look messy
- **Inspect before editing** — always read the relevant file before changing it
- **Standard library first** — Python: use `uuid`, `pathlib`, `json`, `datetime` from stdlib before any package
- **Boring code over clever code** — always

---

## Required Output Format for Code Changes

Every code task must end with this block:

```
Changed:
- <exact files changed>

Verified:
- <check performed or command to run>

Skipped:
- <intentional omissions — what was NOT done>

Add when:
- <the specific condition that would justify adding the skipped work>
```

---

## High-Risk: Pause and Get Approval First

Do NOT proceed without explicit user approval for:
- Auth, security, payment, or customer-data code
- Database migrations
- Destructive filesystem operations
- Production configs or CI/CD changes
- Any new package installation
- Cross-workspace edits

---

## When LessWorks Does NOT Apply

- Non-coding tasks (writing, planning, research)
- When the user explicitly asks for a comprehensive design, tutorial, or full exploration
- When minimizing would remove required validation, security, accessibility, or data integrity

---

## Overriding LessWorks for a Specific Task

To disable for one task, say: `LessWorks off` or `no LessWorks for this`.
To escalate discipline: `LessWorks strict` or `LessWorks intense`.

The full LessWorks skill with all workflow details is available via the lessworks skill.
