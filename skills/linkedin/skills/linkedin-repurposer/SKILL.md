---
name: linkedin-repurposer
description: "Adapt content from another platform (tweet/thread, YouTube video, blog post, podcast transcript, newsletter, slide deck) into a native LinkedIn post that follows LinkedIn's 2026 algorithm rules and voice conventions. Not for writing a post from scratch (use linkedin-post-writer) and not for auditing an existing LinkedIn draft (use linkedin-humanizer)."
---

# LinkedIn Repurposer

## When to use
- User has a tweet thread, YouTube video, blog post, podcast clip, or newsletter they want to turn into a LinkedIn post
- User says "turn this into a LinkedIn post" or "adapt this for LinkedIn"
- User wants to maximize content ROI by reusing high-performing content from other channels

## Source types and extraction strategy

| Source | What to extract | Format notes |
|---|---|---|
| Tweet / X thread | The main argument or insight, any numbers, the hook tweet | LinkedIn post is longer and more narrative — don't just stitch tweets together |
| YouTube video | The single most surprising or useful claim, the story arc, any case study | Don't summarize the video — make the LinkedIn post standalone |
| Blog post | The most counterintuitive point, one concrete example with numbers | LinkedIn ≠ blog. Cut 80% of the original length. One idea only. |
| Podcast episode | One story, one insight, one turning point from the episode | Audio-first content usually has 1 quotable moment — find it and build around it |
| Newsletter | Lead section or a specific take, a data point | Same as blog: one idea, cut massively |
| Slide deck | The single most surprising slide (often slide 3-5) | Lead with the finding, not the context |

## Steps

1. **Receive the source.** Accept: pasted text, a URL to a tweet/thread (Apify can fetch if configured), or the user pasting the key excerpt.
2. **Identify the one idea.** Ask the user (or determine): "What is the single most valuable insight from this content that would make someone stop scrolling on LinkedIn?"
3. **Find the hook.** Look for: a surprising number, a counterintuitive claim, a personal turning point, a named outcome. This becomes the LinkedIn hook (line 1, number-first if possible).
4. **Pick the LinkedIn formula.** Match the content's native shape to an F-code:
   - Data-driven insight → F7 (Odd-Precision Money Ledger) or F19 (Anecdote-Meets-Evidence)
   - Counterintuitive take → F10 (Contrarian + Receipts)
   - Personal story → F11 (Emotional Cold-Open) or F4 (Confession)
   - Framework or how-to → F15 (Explain-to-Kids) or F8 (Paid-vs-Free)
5. **Write the LinkedIn post.** Target: 150–300 words (hard maximum 300 words). Native LinkedIn format — not a summary, not a pointer to the original ("link in comments" is a 2026 reach penalty). The post stands alone. Include the original source context only if it adds credibility.
6. **Run humanizer check** (internal). Remove AI tells before presenting.
7. **Show draft + word count + source mapping.** "Here's how I translated [source type] → LinkedIn [formula]."
8. **On approval → publish.** Call `backend_selector.py publish --kind post`.

## Hard rules
Global voice rules: see root SKILL.md §Voice rules.
- **Never use "link in comments" or "full article in bio"** — LinkedIn's algorithm penalizes off-platform links in the post body and CTA.
- The repurposed post must be self-contained. The reader shouldn't need to see the original.
- Never stitch tweets together — write a new narrative shaped for LinkedIn.
- All numbers and claims from the original source must be preserved accurately. Don't round or paraphrase statistics.
