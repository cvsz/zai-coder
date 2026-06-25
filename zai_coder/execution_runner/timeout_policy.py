"""Command timeout policy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeoutPolicy:
    default_seconds: int = 60
    max_seconds: int = 600
    min_seconds: int = 1

    def normalize(self, seconds: int | None) -> int:
        if seconds is None:
            return self.default_seconds
        if seconds < self.min_seconds:
            return self.min_seconds
        if seconds > self.max_seconds:
            return self.max_seconds
        return seconds

    def to_dict(self) -> dict:
        return {"default_seconds": self.default_seconds, "max_seconds": self.max_seconds, "min_seconds": self.min_seconds}
