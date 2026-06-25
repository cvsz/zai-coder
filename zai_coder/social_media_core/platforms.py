"""Social media platform profiles and constraints."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlatformProfile:
    slug: str
    display_name: str
    max_chars: int
    supports_images: bool = True
    supports_video: bool = True
    supports_threads: bool = False


PLATFORMS = {
    "x": PlatformProfile("x", "X / Twitter", 280, True, True, True),
    "linkedin": PlatformProfile("linkedin", "LinkedIn", 3000, True, True, False),
    "facebook": PlatformProfile("facebook", "Facebook", 63206, True, True, False),
    "instagram": PlatformProfile("instagram", "Instagram", 2200, True, True, False),
    "tiktok": PlatformProfile("tiktok", "TikTok", 2200, True, True, False),
    "youtube": PlatformProfile("youtube", "YouTube", 5000, True, True, False),
}


def get_platform(slug: str) -> PlatformProfile:
    key = slug.strip().lower()
    if key not in PLATFORMS:
        raise ValueError(f"unsupported platform: {slug}")
    return PLATFORMS[key]
