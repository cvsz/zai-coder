"""In-memory gateway rate-limit policy."""

from __future__ import annotations

from dataclasses import dataclass
from time import time


@dataclass(frozen=True)
class RateLimitPolicy:
    key: str
    limit: int
    window_seconds: int

    def validate(self) -> list[str]:
        issues = []
        if self.limit <= 0:
            issues.append("limit must be positive")
        if self.window_seconds <= 0:
            issues.append("window_seconds must be positive")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


DEFAULT_POLICIES = {
    "standard": RateLimitPolicy("standard", 120, 60),
    "strict": RateLimitPolicy("strict", 30, 60),
    "admin": RateLimitPolicy("admin", 300, 60),
}


class InMemoryRateLimiter:
    def __init__(self):
        self._buckets: dict[tuple[str, str], list[float]] = {}

    def check(self, identity: str, policy_key: str = "standard") -> dict:
        policy = DEFAULT_POLICIES.get(policy_key, DEFAULT_POLICIES["standard"])
        now = time()
        bucket_key = (identity, policy.key)
        bucket = [ts for ts in self._buckets.get(bucket_key, []) if now - ts < policy.window_seconds]
        allowed = len(bucket) < policy.limit
        if allowed:
            bucket.append(now)
        self._buckets[bucket_key] = bucket
        return {
            "allowed": allowed,
            "identity": identity,
            "policy": policy.to_dict(),
            "remaining": max(policy.limit - len(bucket), 0),
            "reset_seconds": policy.window_seconds,
        }


def rate_limit_policy_manifest() -> list[dict]:
    return [policy.to_dict() for policy in DEFAULT_POLICIES.values()]
