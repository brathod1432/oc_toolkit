# Examples: Backend API Engineer

## Example: Create endpoint

User asks:
> Add an endpoint to create projects.

Skill behavior:
- Define route, schemas, validation, auth, service call, and response.

Safety check:
- Create only within the authenticated tenant or account.

Expected output:
- API contract, files changed, and tests.

## Example: Activity feed

User asks:
> Return paginated account activity.

Skill behavior:
- Use bounded page size and stable ordering.

Safety check:
- Filter by authorized scope before pagination.

Expected output:
- Contract and edge cases.

## Example: Retryable import

User asks:
> Make CSV import safe to retry.

Skill behavior:
- Add idempotency and conflict behavior.

Safety check:
- Do not log full uploaded rows.

Expected output:
- Idempotency design and tests.

## Example: Public search

User asks:
> Expose public search.

Skill behavior:
- Constrain query fields, limits, and rate behavior.

Safety check:
- Do not return private records.

Expected output:
- Risk summary and endpoint contract.

## Example: Billing address

User asks:
> Update billing address through the API.

Skill behavior:
- Separate request validation from service update logic.

Safety check:
- Verify ownership and protect provider secrets.

Expected output:
- Authorization verification.
