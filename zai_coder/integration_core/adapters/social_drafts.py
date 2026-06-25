"""Social media draft adapters."""

from __future__ import annotations

from dataclasses import dataclass

from zai_coder.integration_core.models import IntegrationPlan


PLATFORM_LIMITS = {
    "x": 280,
    "linkedin": 3000,
    "facebook": 63206,
    "instagram": 2200,
    "tiktok": 2200,
    "youtube": 5000,
}


@dataclass(frozen=True)
class SocialDraft:
    platform: str
    title: str
    body: str
    tags: tuple[str, ...] = ()

    def validate(self) -> list[str]:
        issues: list[str] = []
        if self.platform not in PLATFORM_LIMITS:
            issues.append(f"unsupported platform: {self.platform}")
        limit = PLATFORM_LIMITS.get(self.platform, 0)
        if limit and len(self.body) > limit:
            issues.append(f"body exceeds {self.platform} limit: {len(self.body)}/{limit}")
        return issues

    def to_dict(self) -> dict:
        return {"platform": self.platform, "title": self.title, "body": self.body, "tags": list(self.tags)}


def create_social_drafts(title: str, body: str, tags: tuple[str, ...] = ("zai", "ai")) -> IntegrationPlan:
    drafts = [
        SocialDraft(platform="x", title=title, body=body[:280], tags=tags),
        SocialDraft(platform="linkedin", title=title, body=body, tags=tags),
        SocialDraft(platform="facebook", title=title, body=body, tags=tags),
        SocialDraft(platform="instagram", title=title, body=body[:2200], tags=tags),
        SocialDraft(platform="tiktok", title=title, body=body[:2200], tags=tags),
        SocialDraft(platform="youtube", title=title, body=body, tags=tags),
    ]
    warnings = []
    for draft in drafts:
        warnings.extend(draft.validate())
    return IntegrationPlan(
        provider="social",
        action="drafts",
        payload={"drafts": [d.to_dict() for d in drafts]},
        warnings=warnings + ["Drafts only. No automatic posting."],
    )
