# Examples: Automation Engineer

## Example: Batch rename

User asks:
> Automate renaming these local files.

Skill behavior:
- List planned renames and require approval before applying.

Safety check:
- Do not move files outside approved folders.

Expected output:
- Dry-run table and apply instructions.

## Example: Report generation

User asks:
> Create a repeatable local report workflow.

Skill behavior:
- Define inputs, outputs, logs, and rerun behavior.

Safety check:
- Do not include secrets in generated logs.

Expected output:
- Workflow plan and smoke check.

## Example: Cleanup task

User asks:
> Clean duplicate generated files.

Skill behavior:
- Detect duplicates and propose deletions before acting.

Safety check:
- No recursive delete without explicit approval.

Expected output:
- Preview and confirmation request.

## Example: Scheduled job

User asks:
> Design a local daily automation.

Skill behavior:
- Plan idempotency, lock files, logs, and failure alerts.

Safety check:
- Do not store credentials in the script.

Expected output:
- Runbook and validation.

## Example: Automation review

User asks:
> Review this script before I run it.

Skill behavior:
- Inspect file writes, shell calls, error handling, and recovery.

Safety check:
- Flag destructive commands.

Expected output:
- Findings by severity.
