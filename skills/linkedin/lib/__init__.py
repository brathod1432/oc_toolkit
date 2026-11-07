"""
LinkedIn Skills for OpenCode — lib package
Thin wrappers that expose the same API as the original linkedin-skills lib.

Source lib is copied from linkedin-skills-main/lib/ — see INSTALL.md.
This __init__.py re-exports the high-level helpers every skill uses.
"""

from ._env import load as _load_env
_load_env()

from .apify_client import ApifyClient, fetch_post, fetch_post_comments, fetch_user_recent_comments, fetch_post_engagers
from .publora_client import PubloraClient, publish, repost
from .backend_selector import dispatch as publish_dispatch, check_tier
from .url_parser import parse_url

try:
    from .pixfaro_client import PixfaroClient, illustrate, refine, quote_card, card
except ImportError:
    pass  # Pixfaro is optional — no PIXFARO_TOKEN needed for core skills

__all__ = [
    "ApifyClient", "fetch_post", "fetch_post_comments",
    "fetch_user_recent_comments", "fetch_post_engagers",
    "PubloraClient", "publish", "repost",
    "publish_dispatch", "check_tier",
    "parse_url",
]
