# Examples: LessWorks

Default mode is `LessWorks full`. Use `LessWorks strict` when a short pre-edit checklist is required, `LessWorks intense` for maximum pre-edit discipline, and `LessWorks audit` for review-only bloat detection.

## Example: Avoiding A Dependency

User asks:
> Add a UUID package so we can generate IDs.

Skill behavior:
- Use the language standard library first, such as Python `uuid`, unless requirements prove it insufficient.

Safety check:
- Do not add or import an undeclared package.

Expected output:
- Used standard library UUID generation. Skipped a dependency; add one only if a nonstandard ID format is required.

## Example: Using Installed Dependency Only

User asks:
> Use the validation library we already have.

Skill behavior:
- Inspect dependency files and existing imports before using the library.

Safety check:
- If the library is not installed or declared, do not import it.

Expected output:
- A patch using the existing dependency, or a plan explaining the approval needed.

## Example: Small Bug Fix With Caller Inspection

User asks:
> Fix the wrong total calculation with the smallest diff.

Skill behavior:
- Inspect the calculation function and callers before patching.

Safety check:
- Add a regression check for the broken case.

Expected output:
- Root cause, small patch, regression verification, and skipped refactors.

## Example: Refusing Speculative Abstraction

User asks:
> Add a strategy pattern so this can support future providers.

Skill behavior:
- Check whether more than one provider exists now and avoid abstraction for hypothetical future work.

Safety check:
- Do not add files or interfaces that do not solve the current requirement.

Expected output:
- Skipped strategy layer; add it when a second provider lands.

## Example: Frontend Native Feature Before Library

User asks:
> Install a date picker for this simple birthday field.

Skill behavior:
- Use native `<input type="date">` unless custom UX, localization, or browser requirements justify more.

Safety check:
- Do not install a UI dependency without explicit approval.

Expected output:
- Native input implementation and add-later condition.

## Example: Python Standard Library Before Custom Helper

User asks:
> Write a path join helper.

Skill behavior:
- Use `pathlib.Path` and avoid a custom helper.

Safety check:
- Preserve platform-safe path handling.

Expected output:
- Small patch using `pathlib`, with no new helper.

## Example: Automation Dry Run Before Write

User asks:
> Rename all generated reports.

Skill behavior:
- Produce a dry-run mapping first.

Safety check:
- Ask before applying file moves or renames.

Expected output:
- Preview table, approval question, and safe apply plan.

## Example: Intense Mode Pre-Edit Checklist

User asks:
> LessWorks intense. Change the auth middleware.

Skill behavior:
- Inspect target files, call paths, callers, installed dependencies, risks, patch plan, rollback-neutral approach, and verification before editing.

Safety check:
- Auth changes are high risk; ask if approval or context is missing.

Expected output:
- Pre-edit checklist first, then patch only after context and approval are sufficient.

## Example: Strict Mode Before Editing

User asks:
> LessWorks strict. Simplify this API handler.

Skill behavior:
- Identify target files, search existing helpers, check dependency need, estimate risk, and select verification before editing.

Safety check:
- Reject a new abstraction unless the existing code proves it is necessary.

Expected output:
- Short pre-edit checklist, minimal patch, and verification result.

## Example: Audit Mode Review

User asks:
> LessWorks audit this pull request for bloat.

Skill behavior:
- Review only; identify unnecessary dependencies, speculative abstractions, duplicate logic, and missing validation.

Safety check:
- Do not edit files in audit mode.

Expected output:
- Findings ordered by severity, safe-to-skip items, and actions needing approval.
