---
name: linkedin-content-planner
description: "Plan a week (or multi-week) of LinkedIn content using a pillar framework. Produces a day-by-day schedule with topic, formula, goal, and hook draft for each post. Offers a general plan or a founders-edition plan (Conviction / Building in Public / The Math / Proof pillars). Not for writing individual posts (use linkedin-post-writer) and not for auditing drafts (use linkedin-humanizer)."
---

# LinkedIn Content Planner

## When to use
- User wants a weekly LinkedIn content calendar
- User wants to plan content across multiple pillars (themes)
- User wants a structured posting schedule with varied formats

## Modes

**General plan:** Content pillars for operators, marketers, practitioners. Mix of formats (thought leadership, how-to, personal story, data-driven).

**Founders plan:** Pillars — Conviction (why you believe what others dismiss), Building in Public (progress, setbacks, unglamorous bets), The Math (unit economics, scarce-shots math, cost breakdowns), Proof (receipts, case studies, outcomes). Optimized for a narrow high-value audience: investors, hires, design partners.

## Steps

1. **Clarify.** Ask: "General content plan or founders edition?" + "Which days do you post?" + "Your primary goal this week: comments, audience growth, or sales?"
2. **Load context.** Read `references/voice-profile.md` and `references/story-bank.md` if filled. Use the user's actual stories, numbers, and positions — never generic filler topics.
3. **Select pillars.** For general: suggest 3-4 pillars based on the user's role and audience (e.g., Leadership / Technical Deep-Dive / Personal Growth / Industry Trend). For founders: use the four fixed founder pillars.
4. **Build the plan.** For each posting day:
   - **Pillar** (which theme)
   - **Topic** (specific, not vague — "The 3 hidden costs of scaling a support team to 12" not "Scaling tips")
   - **Formula** (F1-F20 — pick based on pillar + goal)
   - **Goal** (comments / reposts / likes / saves)
   - **Hook draft** (first 210 chars, ready to use)
   - **Estimated length** (short / medium / long)
5. **Present the plan.** Show as a table + one-paragraph summary of the week's strategic arc.
6. **Optional: draft mode.** Ask "Want me to draft any of these now?" and hand off to `linkedin-post-writer` for each the user selects.

## Pillar Framework (general edition — adapt to user)

| Pillar | Purpose | Formula family |
|---|---|---|
| Thought Leadership | Your contrarian take on industry trends | F10, F2, F18 |
| How-To / Framework | Practical, save-worthy reference content | F15, F7, F8 |
| Personal Story | Vulnerability, lessons, turning points | F4, F11, F19 |
| Social Proof / Receipts | Outcomes, case studies, client wins | F5, F7, F3 |

## Hard rules
Global voice rules: see root SKILL.md §Voice rules.
- Plans must use the user's actual expertise and real story material. No made-up topics.
- Each day's hook draft must be ready-to-use (applies voice rules, no AI tells).
- Never schedule more than 2 posts per week in the same formula family.
- Never put a question opener on any day's hook draft.
