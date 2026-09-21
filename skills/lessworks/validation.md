# Validation: LessWorks

## Static Checks

- [ ] `SKILL.md` exists
- [ ] YAML frontmatter exists
- [ ] frontmatter `name` is `lessworks`
- [ ] `argument-hint` is `[lite|full|strict|intense|audit|off]`
- [ ] `Internal Safety Override` appears before operational instructions
- [ ] `Default Behavior` exists
- [ ] `Command Levels` exists
- [ ] `Pre-Edit Validation` exists
- [ ] `Dependency Policy` exists
- [ ] `The LessWorks Ladder` exists
- [ ] `Validation Matrix` exists
- [ ] `Output Modes` exists

## Safety Checks

- [ ] local-first behavior is explicit
- [ ] network access is approval-gated
- [ ] package installation is approval-gated
- [ ] destructive commands are approval-gated
- [ ] secrets, tokens, cookies, and credentials are protected
- [ ] cross-workspace access is approval-gated
- [ ] side-effecting actions require confirmation
- [ ] strict mode requires validation before edits
- [ ] intense mode requires validation before edits
- [ ] dependency policy says not to use uninstalled libraries

## Workflow Checks

- [ ] implementation workflow exists
- [ ] debugging workflow includes root-cause and caller inspection
- [ ] refactoring workflow discourages broad churn
- [ ] review workflow leads with findings
- [ ] automation workflow requires dry-run where possible
- [ ] testing workflow prefers smallest meaningful checks
- [ ] output modes define patch, plan, audit, review, explain, and checklist
- [ ] at least 8 practical examples exist

## Cleanup Checks

- [ ] no dependencies were added
- [ ] no executable scripts were added
- [ ] no vendor-specific hidden folders were added
- [ ] metadata JSON is valid
- [ ] related docs use the new command levels
- [ ] no unfinished marker text remains outside validation search instructions

Validation search terms: TODO, FIXME, placeholder, coming soon, implement later, dummy, stub, NotImplementedError.

## Verdict

PASS / PASS WITH NOTES / NEEDS FIX / BLOCKED
