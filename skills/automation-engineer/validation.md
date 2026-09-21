# Validation: Automation Engineer

## Static Checks

- [ ] `SKILL.md` exists
- [ ] frontmatter has `name`, `description`, `argument-hint`, and `license`
- [ ] `Internal Safety Override` exists before operational instructions
- [ ] metadata name matches directory and frontmatter
- [ ] `references/README.md` exists
- [ ] markdown and JSON files are non-empty

## Safety Checks

- [ ] network access is approval-gated
- [ ] package installation is approval-gated
- [ ] destructive operations are approval-gated
- [ ] secrets, tokens, cookies, and credentials are protected
- [ ] cross-workspace access is approval-gated
- [ ] side-effecting actions require confirmation

## Workflow Checks

- [ ] trigger rules are specific
- [ ] non-trigger guidance exists
- [ ] advanced workflow exists
- [ ] safe modification workflow exists
- [ ] validation workflow exists
- [ ] examples are practical for developer or automation work

## Cleanup Checks

- [ ] no broken links
- [ ] no dependencies or executable scripts are required
- [ ] no vendor-specific hidden folders are created
- [ ] no forbidden marker text remains outside validation search instructions

## Verdict

PASS / PASS WITH NOTES / NEEDS FIX / BLOCKED
