"""Gateway response envelope."""

from __future__ import annotations

import uuid

from .models import GatewayResponse


def success_response(data: dict, status: int = 200, request_id: str | None = None) -> GatewayResponse:
    request_id = request_id or f"req_{uuid.uuid4().hex[:12]}"
    return GatewayResponse(
        status=status,
        body={"ok": True, "request_id": request_id, "data": data, "error": None},
        headers={"X-Request-Id": request_id},
    )


def error_response(code: str, message: str, status: int = 400, request_id: str | None = None) -> GatewayResponse:
    request_id = request_id or f"req_{uuid.uuid4().hex[:12]}"
    return GatewayResponse(
        status=status,
        body={"ok": False, "request_id": request_id, "data": None, "error": {"code": code, "message": message}},
        headers={"X-Request-Id": request_id},
    )
