from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass
class ProviderRoute:
    provider_id: str
    provider_type: str
    priority: int = 100
    enabled: bool = True
    requires_api_key: bool = True
    env_var_name: str | None = None
    supports_text: bool = True
    supports_vision: bool = False
    supports_audio: bool = False
    supports_tools: bool = False
    max_tokens_hint: int | None = None
    cost_tier: str = "medium" # low, medium, high
    fallback_order: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "provider_type": self.provider_type,
            "priority": self.priority,
            "enabled": self.enabled,
            "requires_api_key": self.requires_api_key,
            "env_var_name": self.env_var_name,
            "supports_text": self.supports_text,
            "supports_vision": self.supports_vision,
            "supports_audio": self.supports_audio,
            "supports_tools": self.supports_tools,
            "max_tokens_hint": self.max_tokens_hint,
            "cost_tier": self.cost_tier,
            "fallback_order": self.fallback_order
        }

class ProviderRouter:
    def __init__(self):
        self.routes: dict[str, ProviderRoute] = {}

    def register_route(self, route: ProviderRoute):
        self.routes[route.provider_id] = route

    def get_route(self, provider_id: str) -> ProviderRoute | None:
        return self.routes.get(provider_id)

    def select_best_route(self, require_vision: bool = False, require_tools: bool = False) -> ProviderRoute | None:
        candidates = [
            r for r in self.routes.values() 
            if r.enabled
        ]
        
        if require_vision:
            candidates = [r for r in candidates if r.supports_vision]
        if require_tools:
            candidates = [r for r in candidates if r.supports_tools]
            
        if not candidates:
            return None
            
        # Sort by priority ascending (lower is better/higher priority)
        candidates.sort(key=lambda r: r.priority)
        return candidates[0]
