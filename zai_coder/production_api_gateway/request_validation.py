"""Gateway request validation."""

from __future__ import annotations

from .models import GatewayRequest


def validate_gateway_request(request: GatewayRequest) -> dict:
    issues: list[str] = []
    if request.normalized_method() not in {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"}:
        issues.append("unsupported method")
    if not request.path.startswith("/"):
        issues.append("path must start with /")
    if len(request.path) > 512:
        issues.append("path too long")
    if any(key.lower() == "host" and "://" in value for key, value in request.headers.items()):
        issues.append("invalid host header")
    return {"ok": not issues, "issues": issues, "request": request.to_safe_dict()}
