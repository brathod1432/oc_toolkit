# Examples: Test QA Engineer

## Example: Signup tests

User asks:
> Add tests for signup.

Skill behavior:
- Cover success, duplicate email, invalid input, weak password, and session behavior.

Safety check:
- Password must never be returned.

Expected output:
- Test list and commands.

## Example: Bug regression

User asks:
> Users can save blank names.

Skill behavior:
- Add a regression test at the enforcing layer.

Safety check:
- Server validation must reject bypassed clients.

Expected output:
- Failing case and fix verification.

## Example: Protected API

User asks:
> Test the project update endpoint.

Skill behavior:
- Cover success, unauthenticated, unauthorized, missing resource, invalid payload, and conflict.

Safety check:
- Prevent IDOR.

Expected output:
- API test matrix.

## Example: Checkout E2E

User asks:
> Create an E2E checkout test.

Skill behavior:
- Keep one critical path with fake payment data.

Safety check:
- No real card or account data.

Expected output:
- Journey and assertions.

## Example: Flaky test

User asks:
> Fix this flaky dashboard test.

Skill behavior:
- Identify timing, data coupling, or selector instability.

Safety check:
- Do not hide failures with arbitrary sleeps.

Expected output:
- Cause and reliable fix.
