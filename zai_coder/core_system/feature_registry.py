"""Core feature registry for modules, capabilities, and addons."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Feature:
    slug: str
    name: str
    category: str
    status: str = "planned"
    description: str = ""


class FeatureRegistry:
    def __init__(self):
        self._features: Dict[str, Feature] = {}

    def register(self, feature: Feature) -> None:
        if feature.slug in self._features:
            raise ValueError(f"duplicate feature slug: {feature.slug}")
        self._features[feature.slug] = feature

    def list(self, category: str | None = None) -> List[Feature]:
        values = list(self._features.values())
        if category:
            values = [f for f in values if f.category == category]
        return sorted(values, key=lambda f: (f.category, f.slug))

    def to_dict(self) -> dict:
        return {slug: feature.__dict__ for slug, feature in sorted(self._features.items())}


def default_growth_registry() -> FeatureRegistry:
    reg = FeatureRegistry()
    defaults = [
        Feature("members-system", "Members System", "team", "scaffolded", "Roles, invites, permissions, team state."),
        Feature("update-system", "Update System", "core", "scaffolded", "Safe dry-run-first update plans."),
        Feature("core-system", "Core System", "core", "scaffolded", "Feature registry, health, system status."),
        Feature("marketing-shared", "Marketing Shared", "growth", "scaffolded", "Campaigns, assets, content calendar."),
        Feature("social-media-core", "Social Media Core", "growth", "scaffolded", "Draft, schedule, validate social posts."),
    ]
    for item in defaults:
        reg.register(item)
    return reg
