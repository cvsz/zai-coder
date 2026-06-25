"""Plugin marketplace model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Plugin:
    slug: str
    name: str
    category: str
    description: str
    enabled: bool = False
    permissions: tuple[str, ...] = field(default_factory=tuple)

    def validate(self) -> list[str]:
        issues = []
        if not self.slug:
            issues.append("missing slug")
        if not self.name:
            issues.append("missing name")
        if not self.category:
            issues.append("missing category")
        return issues

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "enabled": self.enabled,
            "permissions": list(self.permissions),
        }


DEFAULT_PLUGINS: Dict[str, Plugin] = {
    "github": Plugin("github", "GitHub Publisher", "integration", "Create safe GitHub publish/release plans.", permissions=("integrations:plan",)),
    "cloudflare": Plugin("cloudflare", "Cloudflare Deploy Planner", "deployment", "Generate tunnel/DNS/deploy plans.", permissions=("deploy:plan",)),
    "creative": Plugin("creative", "Creative Studio", "creative", "Game, document, movie, marketing, and social production tools.", permissions=("creative:*",)),
    "billing": Plugin("billing", "Billing and Quota", "saas", "Plan catalog, quota checks, usage, and reconciliation.", permissions=("billing:read",)),
    "huggingface": Plugin("huggingface", "Hugging Face Publisher", "ml", "Generate model, dataset, and Space publish plans.", permissions=("integrations:plan",)),
}


def list_plugins() -> list[dict]:
    return [plugin.to_dict() for plugin in DEFAULT_PLUGINS.values()]


def get_plugin(slug: str) -> Plugin:
    key = slug.strip().lower()
    if key not in DEFAULT_PLUGINS:
        raise ValueError(f"unknown plugin: {slug}")
    return DEFAULT_PLUGINS[key]
