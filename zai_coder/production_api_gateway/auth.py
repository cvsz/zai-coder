"""API-key/session gateway auth guard."""

from __future__ import annotations

from .models import GatewayRequest


def extract_auth_token(request: GatewayRequest) -> str:
    headers = {key.lower(): value for key, value in request.headers.items()}
    auth = headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()
    return headers.get("x-api-key", "").strip()


def auth_decision(request: GatewayRequest, require_auth: bool = True) -> dict:
    if not require_auth:
        return {"allowed": True, "reason": "auth not required", "actor": "public"}
    token = extract_auth_token(request)
    if not token:
        return {"allowed": False, "reason": "missing auth token", "actor": "anonymous"}
    if len(token) < 12:
        return {"allowed": False, "reason": "auth token too short", "actor": "anonymous"}
    return {"allowed": True, "reason": "token present", "actor": "token-user", "token_preview": token[:6] + "..."}
