"""Connector env and secret guard."""

from __future__ import annotations

SECRET_PATTERNS = ("TOKEN", "SECRET", "KEY", "PASSWORD")


def redact_env(env: dict[str, str]) -> dict[str, str]:
    redacted = {}
    for key, value in env.items():
        if any(pattern in key.upper() for pattern in SECRET_PATTERNS):
            redacted[key] = "<redacted>" if value else ""
        else:
            redacted[key] = value
    return redacted


def validate_connector_env(required_env: tuple[str, ...], env: dict[str, str] | None = None) -> dict:
    env = env or {}
    missing = [key for key in required_env if not env.get(key)]
    blocked = [key for key in env if key.startswith("LIVE_") or key.endswith("_LIVE_SECRET")]
    return {
        "ok": not missing and not blocked,
        "missing": missing,
        "blocked": blocked,
        "safe_env": redact_env({key: env.get(key, "") for key in required_env}),
    }
