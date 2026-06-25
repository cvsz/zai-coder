"""Simple local token bucket rate limiter."""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic


@dataclass
class TokenBucket:
    capacity: int
    refill_per_second: float
    tokens: float = 0.0
    updated_at: float = 0.0

    def __post_init__(self):
        if self.tokens <= 0:
            self.tokens = float(self.capacity)
        if self.updated_at <= 0:
            self.updated_at = monotonic()

    def allow(self, cost: int = 1) -> bool:
        if cost <= 0:
            raise ValueError("cost must be positive")
        now = monotonic()
        elapsed = now - self.updated_at
        self.updated_at = now
        self.tokens = min(float(self.capacity), self.tokens + elapsed * self.refill_per_second)
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False
