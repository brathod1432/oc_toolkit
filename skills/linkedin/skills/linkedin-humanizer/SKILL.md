---
name: linkedin-humanizer
description: "Rewrite or audit a LinkedIn draft to remove AI tells, or build/update a voice profile. Modes: rewrite (default), audit (score only, no rewrite), profile (learn voice from the user's existing posts), emoji (check emoji density). Use before publishing any AI-drafted post. Not for writing a new post from scratch (use linkedin-post-writer) and not for commenting (use linkedin-comment-drafter)."
---

# LinkedIn Humanizer

## When to use
- User has a draft that sounds AI-written and wants it fixed
- User wants to audit a draft before publishing (score AI tells, keep what's good)
- User wants to build or update a voice profile from their existing posts
- User wants to check emoji density on a draft
- Use `--mode audit` before any post is published as the final quality gate

## Modes

**`--mode rewrite` (default):** Rewrite the draft to remove AI tells, match voice profile if available, keep the user's facts and numbers.

**`--mode audit`:** Score only. Return the AI-tell score (0-100, lower is better), list each tell found, explain why each is a tell, recommend fixes. No rewrite.

**`--mode profile`:** Build or update the voice profile. Ask the user to paste 3-5 of their best recent LinkedIn posts. Analyze vocabulary, sentence rhythm, em-dash usage, opening patterns, CTA style, emoji density. Write the profile to `references/voice-profile.md`.

**`--mode emoji`:** Check emoji density on a draft. Return: total emoji count, positions (hook / body / close), assessment (none / light / heavy / overdone), recommendation.

## Steps (rewrite mode)

1. **Load voice profile** if `references/voice-profile.md` has `filled: yes`. Extract: vocabulary fingerprint, hard rules, CTA style, sentence rhythm.
2. **Run AI-tell scan.** Check for (in order of impact):
   - Banned vocabulary: `leverage`, `streamline`, `harness`, `delve`, `unlock`, `foster`, `fundamentally`, `innovative`, `synergy`, `game-changer`, `robust`, `cutting-edge`, `landscape`, `paradigm`, `revolutionize`.
   - Hollow openers: "In today's fast-paced world", "I'm excited to share", "I've been reflecting on".
   - Em-dash overuse (>1 per 100 words).
   - Triple-colon lists ("Here are 3 things:", "Key takeaways:", followed by bullets).
   - Question opener (first line ends in `?`).
   - Filler bridges: "The result?", "Plot twist:", "Here's what happened:", "Here's the thing:".
   - Vague adjectives replacing numbers ("significant", "massive", "huge") where a number would fit.
3. **Rewrite.** Preserve: all user-specific facts, numbers, dates, named people/products, the core argument. Replace AI tells with user's natural voice or generic neutral alternatives. Do not add new claims.
4. **Show before/after + change log.** List each change and why.
5. **Char count check.** Confirm the rewrite stays in target range (posts: 150–300 words, hard maximum 300 words).

## Hard rules
Global voice rules: see root SKILL.md §Voice rules.
- **Never change a user's number, fact, or named reference.** Only the phrasing changes.
- **Never add** a claim, metaphor, or example not in the original.
- **The rewrite serves the user's voice, not a generic LinkedIn voice.**
- In audit mode: report, don't fix. Give the user the score + actionable list.
- In profile mode: ask before overwriting an existing profile. Never delete story bank entries.
