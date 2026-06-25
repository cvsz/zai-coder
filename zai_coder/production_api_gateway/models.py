"""Production API Gateway models.

The gateway is local-first and policy-first. It provides route, auth, tenant,
rate-limit, response-envelope, CORS, security header, and upstream registry
scaffolding without exposing public services by default.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class GatewayRequest:
    method: str
    path: str
    headers: dict[str, str] = field(default_factory=dict)
    query: dict[str, str] = field(default_factory=dict)
    body: dict[str, Any] | None = None
    remote_addr: str = "127.0.0.1"
    received_at: str = field(default_factory=now_iso)

    def normalized_method(self) -> str:
        return self.method.upper()

    def to_safe_dict(self) -> dict:
        redacted_headers = {}
        for key, value in self.headers.items():
            lower = key.lower()
            if lower in {"authorization", "cookie", "x-api-key"}:
                redacted_headers[key] = "<redacted>"
            else:
                redacted_headers[key] = value
        return {
            "method": self.normalized_method(),
            "path": self.path,
            "headers": redacted_headers,
            "query": dict(self.query),
            "body_present": self.body is not None,
            "remote_addr": self.remote_addr,
            "received_at": self.received_at,
        }


@dataclass(frozen=True)
class GatewayResponse:
    status: int
    body: dict[str, Any]
    headers: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"status": self.status, "body": dict(self.body), "headers": dict(self.headers)}


@dataclass(frozen=True)
class GatewayRoute:
    id: str
    method: str
    path: str
    upstream: str
    auth_required: bool = True
    tenant_required: bool = True
    rate_limit_key: str = "standard"
    description: str = ""

    def validate(self) -> list[str]:
        issues: list[str] = []
        if self.method.upper() not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
            issues.append("unsupported method")
        if not self.path.startswith("/"):
            issues.append("path must start with /")
        if not self.upstream:
            issues.append("upstream required")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "method": self.method.upper(),
            "path": self.path,
            "upstream": self.upstream,
            "auth_required": self.auth_required,
            "tenant_required": self.tenant_required,
            "rate_limit_key": self.rate_limit_key,
            "description": self.description,
        }


@dataclass(frozen=True)
class UpstreamService:
    id: str
    name: str
    base_url: str
    health_path: str = "/healthz"
    timeout_seconds: int = 30
    enabled: bool = True

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name:
            issues.append("upstream id/name required")
        if not (self.base_url.startswith("http://127.0.0.1") or self.base_url.startswith("http://localhost")):
            issues.append("upstream must be localhost-first")
        if self.timeout_seconds <= 0:
            issues.append("timeout must be positive")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class GatewayAuditEvent:
    id: str
    actor: str
    org_id: str
    workspace_id: str
    action: str
    target: str
    status: int
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "actor": self.actor,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "action": self.action,
            "target": self.target,
            "status": self.status,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }
