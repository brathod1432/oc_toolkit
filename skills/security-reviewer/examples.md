# Examples: Security Reviewer

## Example: Invoice leak

User asks:
> A user can see another user's invoice.

Skill behavior:
- Trace route parameters to data access and fix ownership enforcement.

Safety check:
- Do not rely on UI-only checks.

Expected output:
- Severity, root cause, fix, tests.

## Example: Session review

User asks:
> Review session cookie settings.

Skill behavior:
- Check expiration, rotation, revocation, and cookie flags.

Safety check:
- Do not weaken cookie protections.

Expected output:
- Findings and verification.

## Example: SSRF risk

User asks:
> We fetch user-provided webhook URLs.

Skill behavior:
- Review scheme, DNS, private IP blocking, redirects, and timeouts.

Safety check:
- Block internal networks and metadata services.

Expected output:
- Attack path and mitigations.

## Example: Secret logs

User asks:
> Check whether tokens are logged.

Skill behavior:
- Inspect logging paths and redaction behavior.

Safety check:
- Never print token values.

Expected output:
- Affected flows and fix plan.

## Example: Dependency add

User asks:
> Can we add this auth package?

Skill behavior:
- Assess necessity and risk from local metadata or ask before network lookup.

Safety check:
- Do not install without approval.

Expected output:
- Recommendation and alternatives.
