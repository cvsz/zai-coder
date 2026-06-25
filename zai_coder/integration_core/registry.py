"""Integration registry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class IntegrationProvider:
    slug: str
    name: str
    category: str
    mutation_supported: bool = False
    dry_run_required: bool = True

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "name": self.name,
            "category": self.category,
            "mutation_supported": self.mutation_supported,
            "dry_run_required": self.dry_run_required,
        }


DEFAULT_PROVIDERS: Dict[str, IntegrationProvider] = {
    "github": IntegrationProvider("github", "GitHub", "source-control"),
    "cloudflare": IntegrationProvider("cloudflare", "Cloudflare", "edge"),
    "docker": IntegrationProvider("docker", "Docker", "runtime"),
    "huggingface": IntegrationProvider("huggingface", "Hugging Face", "ml-hub"),
    "social": IntegrationProvider("social", "Social Drafts", "growth"),
    "storage": IntegrationProvider("storage", "Storage Backends", "storage"),
    "notifications": IntegrationProvider("notifications", "Notifications", "communications"),
    "openapi": IntegrationProvider("openapi", "OpenAPI", "api"),
}


def list_integrations() -> list[dict]:
    return [provider.to_dict() for provider in DEFAULT_PROVIDERS.values()]


def get_integration(slug: str) -> IntegrationProvider:
    key = slug.strip().lower()
    if key not in DEFAULT_PROVIDERS:
        raise ValueError(f"unknown integration provider: {slug}")
    return DEFAULT_PROVIDERS[key]
