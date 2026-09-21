# Examples: Frontend Engineer

## Example: Settings form

User asks:
> Create a settings form for name and timezone.

Skill behavior:
- Build labeled fields, local dirty state, validation, save state, and API error display.

Safety check:
- Server validation must still enforce rules.

Expected output:
- Component behavior and accessibility checks.

## Example: Comment rendering

User asks:
> Show user comments safely.

Skill behavior:
- Render text safely or use an approved sanitizer already in the project.

Safety check:
- Avoid raw HTML injection.

Expected output:
- Implementation summary and XSS test cases.

## Example: Invoice table

User asks:
> Build a responsive invoice table.

Skill behavior:
- Add accessible sort controls, loading, empty, error, and compact layouts.

Safety check:
- Do not expose unauthorized fields.

Expected output:
- UI states and responsive verification.

## Example: Magic link page

User asks:
> Build the page opened from an email link.

Skill behavior:
- Handle pending, success, expired, and invalid token states.

Safety check:
- Do not store or log the token unnecessarily.

Expected output:
- Flow summary and manual checks.

## Example: Upload control

User asks:
> Add drag-and-drop PDF upload.

Skill behavior:
- Use native file input semantics, progress state, and keyboard support.

Safety check:
- Browser file checks are advisory only.

Expected output:
- Component states and server validation reminder.
