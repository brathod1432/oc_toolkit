# LinkedIn Skills for OpenCode — Installation Guide

## Overview

The LinkedIn Skills bundle gives OpenCode 12 LinkedIn operations:
post writing, comment drafting, reply handling, humanizing, hook extraction,
content planning, thread monitoring, engager analytics, profile optimization,
employee advocacy, content repurposing, and interviewer.

All skills work **immediately without any API keys** (Tier 0 — draft + copy-paste).
API keys unlock auto-posting and read operations.

---

## Step 1 — Copy this folder

The `skills/linkedin/` folder you're reading this from is already in the right
place if you followed the standard setup. Verify:

```
C:\Users\kbrat\.config\opencode\
  skills/
    linkedin/
      SKILL.md                  ← master skill (auto-loaded by opencode.jsonc glob)
      .env.example              ← copy to .env and fill in keys
      requirements.txt
      INSTALL.md                ← this file
      lib/                      ← Python helper library
      skills/                   ← 12 sub-skills
      references/               ← Story Bank + Voice Profile (created by interviewer)
```

---

## Step 2 — Copy the Python lib from linkedin-skills-main

The `lib/` folder here contains only the dispatch wrapper and `__init__.py`.
The full client library lives in `linkedin-skills-main/lib/`.

**Copy these files** from `F:\Windows_Software\oc_toolkit\linkedin-skills-main\lib\`
into `C:\Users\kbrat\.config\opencode\skills\linkedin\lib\`:

```
apify_client.py
publora_client.py
pixfaro_client.py   (optional — only needed for image generation)
url_parser.py
_env.py
```

After copying, your `lib/` folder should contain:

```
lib/
  __init__.py          ← already here
  backend_selector.py  ← already here
  _env.py              ← copy from source
  url_parser.py        ← copy from source
  apify_client.py      ← copy from source
  publora_client.py    ← copy from source
  pixfaro_client.py    ← copy from source (optional)
```

---

## Step 3 — Install Python dependencies

Open a terminal and run:

```bash
pip install -r "C:\Users\kbrat\.config\opencode\skills\linkedin\requirements.txt"
```

Or with Python explicitly:

```bash
python -m pip install requests python-dotenv cachetools
```

---

## Step 4 — Configure API keys (optional)

Copy `.env.example` to `.env` in the same folder:

```bash
copy "C:\Users\kbrat\.config\opencode\skills\linkedin\.env.example" ^
     "C:\Users\kbrat\.config\opencode\skills\linkedin\.env"
```

Then edit `.env` and fill in whichever keys you have:

| Variable | Required for | Where to get it |
|---|---|---|
| `PUBLORA_API_KEY` | Tier 1 auto-post | app.publora.com/signup |
| `LINKEDIN_PLATFORM_ID` | Tier 1 auto-post | Publora → Channels |
| `APIFY_TOKEN` | Fetching post/comment data | console.apify.com |
| `PIXFARO_TOKEN` | AI image generation | api.pixfaro.com |

**None of these are required.** Without them, all 12 skills still work — they
produce draft text you copy-paste into LinkedIn manually.

---

## Step 5 — Verify the tier

From a terminal:

```bash
python "C:\Users\kbrat\.config\opencode\skills\linkedin\lib\backend_selector.py" --check
```

Expected output (Tier 0, no keys configured):

```json
{
  "tier": 0,
  "publora": false,
  "apify": false,
  "pixfaro": false,
  "custom_poster": false,
  "summary": "Tier 0 — Draft only. Copy-paste block returned on approval."
}
```

---

## Step 6 — Run the interviewer first (recommended)

Before using the post writer, run the interviewer once to build your Story Bank
and Voice Profile. In OpenCode:

```
write linkedin post about [topic]
```

Or explicitly call the interviewer:

```
run linkedin interviewer
```

The interviewer saves to:
- `skills/linkedin/references/story-bank.md`
- `skills/linkedin/references/voice-profile.md`

Every writing skill reads these files automatically.

---

## Tiers at a Glance

| Tier | What's configured | What happens on publish |
|---|---|---|
| 0 | Nothing (default) | Draft shown — copy-paste to LinkedIn |
| 1 | PUBLORA_API_KEY + LINKEDIN_PLATFORM_ID | Auto-posts after your approval |
| 2 | LINKEDIN_SKILLS_CUSTOM_POSTER | Calls your custom poster script |

---

## Skill Routing Quick Reference

| Say… | Skill invoked |
|---|---|
| "write a LinkedIn post about X" | `linkedin-post-writer` |
| "draft a comment on [URL]" | `linkedin-comment-drafter` |
| "handle replies on [URL]" | `linkedin-reply-handler` |
| "humanize this post" | `linkedin-humanizer` |
| "extract hooks from [URL]" | `linkedin-hook-extractor` |
| "plan LinkedIn content for next month" | `linkedin-content-planner` |
| "monitor my post [URL]" | `linkedin-thread-monitor` |
| "who engaged with [URL]" | `linkedin-engager-analytics` |
| "optimize my LinkedIn profile" | `linkedin-profile-optimizer` |
| "build employee advocacy program" | `linkedin-employee-advocacy` |
| "repurpose this for LinkedIn" | `linkedin-repurposer` |
| "interview me for LinkedIn content" | `linkedin-interviewer` |
