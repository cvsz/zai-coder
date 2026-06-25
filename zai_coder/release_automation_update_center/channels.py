"""Release channel policy."""

from __future__ import annotations


CHANNELS = {
    "dev": {"requires_full_tests": False, "requires_approval": False, "public": False},
    "alpha": {"requires_full_tests": True, "requires_approval": True, "public": False},
    "beta": {"requires_full_tests": True, "requires_approval": True, "public": False},
    "rc": {"requires_full_tests": True, "requires_approval": True, "public": True},
    "stable": {"requires_full_tests": True, "requires_approval": True, "public": True},
    "lts": {"requires_full_tests": True, "requires_approval": True, "public": True},
}


def release_channel_manifest() -> dict:
    return {key: dict(value) for key, value in CHANNELS.items()}


def channel_policy(channel: str) -> dict:
    if channel not in CHANNELS:
        raise ValueError(f"unknown channel: {channel}")
    return {"channel": channel, **CHANNELS[channel]}
