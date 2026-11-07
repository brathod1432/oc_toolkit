---
name: linkedin-profile-optimizer
description: "Audit and rewrite a LinkedIn profile: headline, About section, experience bullet points, featured section strategy, banner recommendations, and skills selection. User pastes their current profile or provides their LinkedIn URL. Returns scored audit + rewritten sections. Not for drafting posts (use linkedin-post-writer) and not for building a voice profile for content (use linkedin-humanizer --mode profile)."
---

# LinkedIn Profile Optimizer

## When to use
- User wants their LinkedIn profile headline rewritten
- User wants the About section audited and rewritten
- User wants their experience bullets to be keyword-optimized and accomplishment-focused
- User wants a full profile audit with scores and prioritized fixes
- User is job searching, fundraising, or building inbound from LinkedIn

## Sections to audit

| Section | Weight | Common issues |
|---|---|---|
| Headline | High | Generic title ("Software Engineer at Company"), no value prop, no keywords |
| About | High | Wall of text, no hook in line 1, no CTA at end, first-person pronouns missing |
| Experience | Medium | Duties not accomplishments, no metrics, passive voice |
| Featured | Medium | Empty, or points to old/irrelevant content |
| Banner | Low | Generic LinkedIn blue, no text/brand element |
| Skills | Low | Irrelevant, unendorsed, not ordered by ICP keywords |

## Steps

1. **Get the profile.** Accept pasted profile text or a LinkedIn profile URL (Apify fetch if `APIFY_TOKEN` set). If pasting, ask for: current headline, About section, last 2-3 experience entries, current featured section items.
2. **Identify the goal.** Job search / fundraising / inbound clients / thought leadership / all of the above?
3. **Audit each section.** Score each 1-10. List specific issues with line-level callouts.
4. **Rewrite.** Start with the highest-impact sections (headline + About). Offer rewrites for experience bullets on request.

## Headline formulas (use one)

- `[Role] helping [ICP] achieve [outcome] via [method]`
- `[Title] | [Differentiator #1] | [Differentiator #2] | [Social proof / result]`
- `[Number] [outcomes delivered] for [ICP] | [Current role] @ [Company]`
- `[Aspiration or claim] → [How] → [Proof or CTA]`

## About section rules

- Line 1 is the hook: must work as a standalone statement before "see more". Never start with "I am" or "I'm a".
- 3-5 short paragraphs. Each paragraph = one idea. Blank lines between.
- Include: who you help, how you do it, proof (a number or named outcome), and a CTA (DM, visit site, follow for X).
- First-person throughout ("I help" not "John helps").
- End with a specific CTA — not just "feel free to connect".

## Hard rules
Global voice rules: see root SKILL.md §Voice rules.
- Rewrites must preserve the user's actual experience, companies, and accomplishments. Never invent metrics.
- If the user doesn't have metrics to share, use qualitative specifics: named projects, team sizes, named technologies.
- Headline: max 220 chars (LinkedIn display limit).
- About: 300-2,000 chars (aim for 400-700 for mobile).
