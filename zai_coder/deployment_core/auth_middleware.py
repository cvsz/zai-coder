"""API auth middleware foundation.

This module is framework-neutral. It verifies local requests or API keys.
"""

from __future__ import annotations

from dataclasses import dataclass
from ipaddress import ip_address


LOCALHOSTS = {"127.0.0.1", "::1", "localhost"}


@dataclass(frozen=True)
class AuthDecision:
    allowed: bool
    reason: str
    actor: str = ""

    def to_dict(self) -> dict:
        return {"allowed": self.allowed, "reason": self.reason, "actor": self.actor}


def is_local_host(host: str) -> bool:
    host = (host or "").split(":", 1)[0].strip().lower()
    if host in LOCALHOSTS:
        return True
    try:
        return ip_address(host).is_loopback
    except ValueError:
        return False


def authorize_request(
    client_host: str,
    bind_host: str,
    api_key: str = "",
    verify_key=None,
    allow_localhost_without_key: bool = True,
) -> AuthDecision:
    if allow_localhost_without_key and is_local_host(client_host) and is_local_host(bind_host):
        return AuthDecision(True, "localhost-dev", "local")

    if not api_key:
        return AuthDecision(False, "missing-api-key")

    if verify_key is None:
        return AuthDecision(False, "no-verifier-configured")

    record = verify_key(api_key)
    if record:
        return AuthDecision(True, "api-key", getattr(record, "name", "api-key"))

    return AuthDecision(False, "invalid-api-key")
