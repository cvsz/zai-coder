"""Social post composer and validator."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .platforms import get_platform


@dataclass
class SocialPost:
    platform: str
    text: str
    campaign: str = ""
    media_paths: List[str] = field(default_factory=list)
    status: str = "draft"

    def to_dict(self) -> dict:
        return {
            "platform": self.platform,
            "text": self.text,
            "campaign": self.campaign,
            "media_paths": list(self.media_paths),
            "status": self.status,
        }


def validate_post(post: SocialPost) -> list[str]:
    issues: list[str] = []
    platform = get_platform(post.platform)
    if not post.text.strip():
        issues.append("empty post text")
    if len(post.text) > platform.max_chars:
        issues.append(f"text exceeds {platform.display_name} limit: {len(post.text)}/{platform.max_chars}")
    if post.media_paths and not platform.supports_images:
        issues.append(f"{platform.display_name} does not support images")
    if post.status not in {"draft", "review", "approved", "scheduled", "published"}:
        issues.append(f"invalid status: {post.status}")
    return issues


def compose_variants(base_text: str, platforms: list[str]) -> list[SocialPost]:
    posts: list[SocialPost] = []
    for slug in platforms:
        profile = get_platform(slug)
        text = base_text.strip()
        if len(text) > profile.max_chars:
            text = text[: max(0, profile.max_chars - 1)].rstrip() + "…"
        posts.append(SocialPost(platform=slug, text=text))
    return posts
