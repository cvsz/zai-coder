"""Execution retry policy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionRetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: int = 3
    max_delay_seconds: int = 60

    def should_retry(self, attempt: int, status: str) -> bool:
        if status in {"completed", "blocked", "cancelled"}:
            return False
        return attempt < self.max_attempts

    def delay_for_attempt(self, attempt: int) -> int:
        if attempt <= 0:
            raise ValueError("attempt must be positive")
        return min(self.base_delay_seconds * (2 ** (attempt - 1)), self.max_delay_seconds)

    def to_dict(self) -> dict:
        return {
            "max_attempts": self.max_attempts,
            "base_delay_seconds": self.base_delay_seconds,
            "max_delay_seconds": self.max_delay_seconds,
        }
