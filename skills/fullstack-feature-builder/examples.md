# Examples: Fullstack Feature Builder

## Example: Saved filters

User asks:
> Add saved dashboard filters for each user.

Skill behavior:
- Design the UI state, API contract, ownership model, persistence, and tests.

Safety check:
- Enforce server-side ownership for every saved filter.

Expected output:
- Plan, changed files, verification, and residual risk.

## Example: Invitation flow

User asks:
> Build team invitations with roles.

Skill behavior:
- Plan token lifecycle, role permissions, email boundary, acceptance, and expiration.

Safety check:
- Use single-use expiring tokens and server-side authorization.

Expected output:
- Feature flow, tests, and safety notes.

## Example: Profile settings

User asks:
> Add profile display name and locale settings.

Skill behavior:
- Reuse existing form patterns, add server validation, and preserve failed input.

Safety check:
- Do not trust client validation alone.

Expected output:
- Implementation summary and checks.

## Example: Admin export

User asks:
> Add an admin CSV export.

Skill behavior:
- Define fields, pagination or streaming, audit logging, and access control.

Safety check:
- Exclude secrets and minimize personal data.

Expected output:
- Contract and verification checklist.

## Example: Upload feature

User asks:
> Let users upload profile images.

Skill behavior:
- Plan file input, endpoint validation, storage naming, preview, and fallback.

Safety check:
- Validate type and size server-side and prevent path traversal.

Expected output:
- Flow, tests, and manual checks.
