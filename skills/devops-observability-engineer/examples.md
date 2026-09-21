# Examples: DevOps Observability Engineer

## Example: Docker review

User asks:
> Review our Dockerfile.

Skill behavior:
- Check base image, runtime user, build cache, secrets, and image size.

Safety check:
- Do not copy secrets into images.

Expected output:
- Findings and build checks.

## Example: CI gate

User asks:
> Add release checks.

Skill behavior:
- Recommend lint, type, unit, API, migration, and artifact checks based on the repo.

Safety check:
- Do not print secret env vars.

Expected output:
- Ordered checks and failure behavior.

## Example: Health checks

User asks:
> Design health endpoints.

Skill behavior:
- Separate liveness from readiness and dependency checks.

Safety check:
- Do not expose internal hostnames or credentials.

Expected output:
- Endpoint behavior and monitoring notes.

## Example: Logging

User asks:
> Improve failed payment logs.

Skill behavior:
- Add sanitized structured fields and correlation IDs.

Safety check:
- Never log provider secrets or full payloads.

Expected output:
- Field list and redaction rules.

## Example: Rollback

User asks:
> Prepare rollback for a migration release.

Skill behavior:
- Identify compatibility, backups, forward fix, smoke checks, and stop conditions.

Safety check:
- Restrict backup access and avoid credential exposure.

Expected output:
- Deployment and rollback checklist.
