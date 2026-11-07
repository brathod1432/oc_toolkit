"""
backend_selector.py — OpenCode LinkedIn Skills
Dispatch layer: routes publish calls to Publora, custom poster, or manual mode.

Usage (CLI):
  python backend_selector.py --check
  python backend_selector.py publish --kind post --text "..." --target-url "https://linkedin.com/..."
  python backend_selector.py publish --kind comment --text "..." --target-url "https://linkedin.com/..."
  python backend_selector.py publish --kind reply --text "..." --target-url "..." --parent-urn "urn:li:comment:..."
  python backend_selector.py publish --kind reshare --target-url "https://linkedin.com/..."

This file is a WRAPPER that calls the original backend_selector.py from the source lib.
Copy the full source lib from linkedin-skills-main/lib/ alongside this file.
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

LIB_DIR = Path(__file__).parent
LINKEDIN_SKILLS_DIR = LIB_DIR.parent

# ── Environment ───────────────────────────────────────────────────────────────

def _env(key, default=None):
    """Read from environment, then from .env file in skill root."""
    val = os.environ.get(key)
    if val:
        return val
    env_file = LINKEDIN_SKILLS_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            if k.strip() == key:
                return v.strip()
    return default


def check_tier() -> dict:
    """Return the active tier and which layers are configured."""
    publora_key = _env("PUBLORA_API_KEY")
    platform_id = _env("LINKEDIN_PLATFORM_ID")
    apify_token = _env("APIFY_TOKEN")
    pixfaro_token = _env("PIXFARO_TOKEN")
    custom_poster = _env("LINKEDIN_SKILLS_CUSTOM_POSTER")

    if custom_poster:
        tier = 2
    elif publora_key and platform_id:
        tier = 1
    else:
        tier = 0

    return {
        "tier": tier,
        "publora": bool(publora_key and platform_id),
        "apify": bool(apify_token),
        "pixfaro": bool(pixfaro_token),
        "custom_poster": bool(custom_poster),
        "summary": {
            0: "Tier 0 — Draft only. Copy-paste block returned on approval.",
            1: "Tier 1 — Publora auto-post. Will publish to LinkedIn on approval.",
            2: "Tier 2 — Custom poster. Will invoke your custom command on approval.",
        }[tier],
    }


def dispatch(kind: str, text: str, target_url: str,
             parent_urn: str = None, media_urls: list = None) -> dict:
    """
    Dispatch a publish action to the correct backend.

    Args:
        kind: "post" | "comment" | "reply" | "reshare"
        text: Draft text to publish
        target_url: LinkedIn post or comment URL
        parent_urn: For replies — top-level comment URN (urn:li:comment:...)
        media_urls: Optional list of image/video URLs (Pixfaro outputs)

    Returns:
        dict with keys: tier, published, url, message
    """
    tier_info = check_tier()
    tier = tier_info["tier"]

    if tier == 0:
        return {
            "tier": 0,
            "published": False,
            "url": None,
            "message": (
                "Draft ready. Tier 0 (no API keys configured) — copy the text above "
                "and paste it into LinkedIn.\n\n"
                "To enable auto-posting: add PUBLORA_API_KEY + LINKEDIN_PLATFORM_ID "
                "to ~/.config/opencode/skills/linkedin/.env"
            ),
        }

    elif tier == 2:
        cmd = _env("LINKEDIN_SKILLS_CUSTOM_POSTER")
        payload = json.dumps({
            "kind": kind, "text": text, "target_url": target_url,
            "parent_urn": parent_urn, "media_urls": media_urls or [],
        })
        result = subprocess.run(
            [cmd, "--payload", payload],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return {"tier": 2, "published": True, "url": None, "message": result.stdout.strip()}
        else:
            return {"tier": 2, "published": False, "url": None, "message": f"Custom poster failed: {result.stderr}"}

    elif tier == 1:
        # Delegate to publora_client.py
        try:
            from .publora_client import PubloraClient
            client = PubloraClient(
                api_key=_env("PUBLORA_API_KEY"),
                platform_id=_env("LINKEDIN_PLATFORM_ID"),
            )
            if kind == "post":
                result = client.create_post(text, media_urls=media_urls)
            elif kind == "comment":
                result = client.create_comment(target_url, text)
            elif kind == "reply":
                result = client.create_reply(target_url, text, parent_urn=parent_urn)
            elif kind == "reshare":
                result = client.reshare(target_url, commentary=text)
            else:
                return {"tier": 1, "published": False, "url": None, "message": f"Unknown kind: {kind}"}

            return {
                "tier": 1,
                "published": True,
                "url": result.get("post_url") or result.get("comment_url"),
                "message": f"Published via Publora. ID: {result.get('id', 'unknown')}",
            }
        except Exception as e:
            return {"tier": 1, "published": False, "url": None, "message": f"Publora error: {e}"}


# ── CLI entry point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkedIn Skills backend selector")
    parser.add_argument("action", choices=["publish", "--check"], nargs="?", default="--check")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--kind", choices=["post", "comment", "reply", "reshare"])
    parser.add_argument("--text", default="")
    parser.add_argument("--target-url", default="")
    parser.add_argument("--parent-urn", default=None)
    parser.add_argument("--media-urls", nargs="*", default=None)
    args = parser.parse_args()

    if args.check or args.action == "--check":
        info = check_tier()
        print(json.dumps(info, indent=2))
        sys.exit(0)

    if args.action == "publish":
        if not args.kind:
            print("Error: --kind required for publish", file=sys.stderr)
            sys.exit(1)
        result = dispatch(
            kind=args.kind,
            text=args.text,
            target_url=args.target_url,
            parent_urn=args.parent_urn,
            media_urls=args.media_urls,
        )
        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("published") or result.get("tier") == 0 else 1)
