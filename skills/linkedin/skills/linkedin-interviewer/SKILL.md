---
name: linkedin-interviewer
description: "Interview the user about their career, projects, turning points, and opinions to build a Story Bank and Voice Profile. Run this first if you've never posted: the Story Bank feeds every writing skill with real numbers, dates, and named projects. Start here when the user has nothing concrete for a draft to use. Not for writing posts (use linkedin-post-writer) and not for auditing drafts (use linkedin-humanizer)."
---

# LinkedIn Interviewer

## When to use
- User wants to start posting on LinkedIn but doesn't know what to write about
- User's drafts keep feeling generic because there's no real story material
- User wants to capture their career highlights in a format every writing skill can use
- User wants to build or update their voice profile from scratch
- Use this as the starting point before any writing skill, if the story bank doesn't exist yet

## What it produces

**Story Bank (`references/story-bank.md`):** A structured collection of the user's real career material — receipts, turning points, positions, opinions. Every writing skill reads this to get concrete details instead of asking mid-draft.

**Voice Profile (`references/voice-profile.md`):** The user's writing fingerprint — vocabulary, rhythm, hard rules, CTA style, emoji density preference. The humanizer and post writer read this for every draft.

## Interview flow

Run as a conversation. Ask questions in groups of 3-4. Don't ask all at once. Adapt based on what surfaces.

### Group 1 — Career moments
- What's the most surprising result you've ever gotten (with a number)?
- What did you build / ship / fix that you're most proud of?
- What decision turned out worse than expected? What did you learn?
- What's the most expensive mistake you've made professionally?

### Group 2 — Opinions and positions
- What does your industry get wrong that drives you crazy?
- What advice do you give everyone in your field?
- What have you changed your mind about in the last 2 years?
- What do you believe that most people in your role would disagree with?

### Group 3 — Specifics and proof
- Give me 3 numbers that describe your career impact (revenue, users, time saved, cost reduced, etc.).
- Name a specific project — what did you do, what happened, what was the metric?
- Who have you worked with who shaped how you think?

### Group 4 — Voice and audience
- Who are you writing for on LinkedIn? (job title + 1-2 sentence description of that person)
- What's your writing style — punchy and direct, or reflective and nuanced?
- Do you use humor? Sarcasm? Vulnerability?
- How do you usually end a post?

## Steps

1. **Open with context.** "I'm going to ask you about your career, specific moments, and opinions. The goal is to build your Story Bank — a set of real material every writing skill will use instead of asking you mid-draft. This takes about 15-20 minutes."
2. **Run Groups 1-4.** Ask 3-4 questions at a time. Wait for answers. Follow up on anything specific or numbers-rich.
3. **Extract and structure.** From the answers, write out:
   - **Receipts:** Specific outcomes with numbers (revenue grown, users acquired, time saved, cost cut, etc.)
   - **Turning Points:** Career moments that changed how you think
   - **Positions:** Opinions you hold strongly that others might disagree with
   - **Voice Rules:** Writing style, what to avoid, how they end posts
4. **Write the Story Bank.** Save to `~/.config/opencode/skills/linkedin/references/story-bank.md` with `filled: yes` at the top.
5. **Write the Voice Profile.** Save to `~/.config/opencode/skills/linkedin/references/voice-profile.md` with `filled: yes` at the top.
6. **Hand off.** "Your Story Bank and Voice Profile are ready. Every writing skill will use these now. Want to write your first post?"

## Hard rules
- Never invent or embellish user-provided facts. Record only what the user says.
- Every number in the Story Bank must come from the user. If they can't recall a number, mark it as `[estimate]`.
- Never push the user to share more than they're comfortable with. Sensitive business details stay out unless offered.
- The Story Bank is private — it lives in `references/story-bank.md`, gitignored by default.
