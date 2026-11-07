---
name: linkedin-post-writer
description: "Draft a new LinkedIn post from scratch using one of 20 2026 hook formulas (F1-F20) plus founder-edition angles, picked by engagement goal (comments/reposts/likes/saves). Runs humanizer pass and schedules via Publora on approval. Use to write a post, find a hook or proven format, or get founder-specific angles. Not for reviewing existing drafts (use linkedin-humanizer --mode audit)."
---

# LinkedIn Post Writer

## When to use
- User says "write me a LinkedIn post about X"
- User has a topic + rough angle and needs a hook + structure
- User wants to pick from known-winning formats and fill in their voice
- User wants to audit + schedule in one flow

Not for: reviewing or rewriting an existing draft → use `linkedin-humanizer`.

## Steps

**Voice profile first.** If `references/voice-profile.md` has `filled: yes`, load it and match the user's voice fingerprint. If it's not filled, mention once that `linkedin-interviewer` and `linkedin-humanizer --mode profile` can learn their voice, then proceed with global voice rules. If `references/story-bank.md` has `filled: yes`, use concrete details (numbers, dates, named projects) from there — never invent a figure not in the bank.

**Founder mode.** When the writer is a founder, offer a founder angle (A1-A10) before picking a formula. Angles: reprice the category (A1), content-to-pipeline (A2), audience of one (A3), scarce-shots math (A4), the unglamorous bet (A5), limit of delegation (A6), designed serendipity (A7), evasive-sentence test (A8), delegation line (A9 → uses F17), learning gate (A10 → uses F18+F20).

1. **Gather inputs.** Topic, angle, draft ideas, target audience, desired length (short 50–150 words / standard 150–300 words, default). Never above 300 words.
2. **Pick the formula.** Ask (or infer) the goal: comments, reposts, likes, or saves. Suggest 2-3 formulas from the routing table + reference engagement numbers + 2026 caveats. Two rules always apply: **never open with a question** (-34% median likes); **prefer a number-first line** (+34% median likes).
3. **Draft the post.** Fill the formula skeleton with user voice. Respect 2026 algorithm rules:
   - P.S. sign-off at the end (+7.5% reach)
   - 1,000+ chars for thought leadership (1.18x reach) — still within the 300-word cap
   - 1–2 sentence paragraphs with blank lines
   - One contrast device and one triple max per post
   - Zero "The result?" / "Plot twist:" / "Here's what" bridges
4. **Run humanizer check.** Before presenting, scan for the top AI tells (see `linkedin-humanizer`) and self-correct them. Remove em-dash overuse, banned vocabulary, hollow intensifiers.
5. **Show draft + word count + char count + formula used.** Ask: "Ready to publish, or want to adjust something?"
6. **On approval → publish.** Call `backend_selector.py publish --kind post`.

## Hard rules
Global voice rules: see root SKILL.md §Voice rules.
- Posts: 150–300 words, hard maximum 300 words. Trim before showing a draft that is over.
- First 210 chars = the hook (before mobile fold).
- Never open with a question; close with one (+3%).
- Odd-precision numbers in line 1 are the strongest 2026 opener (F7 pattern).
- One formula per post. One contrast device. One triple. Zero filler bridges.
