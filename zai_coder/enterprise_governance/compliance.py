"""Compliance checklist."""

from __future__ import annotations


COMPLIANCE_CHECKLIST = [
    {"id": "cmp-001", "area": "repo", "item": "repo-check passes", "required": True},
    {"id": "cmp-002", "area": "secrets", "item": "secret-scan passes", "required": True},
    {"id": "cmp-003", "area": "auth", "item": "protected APIs require session or Access", "required": True},
    {"id": "cmp-004", "area": "cloudflare", "item": "Access policy enabled before DNS route", "required": True},
    {"id": "cmp-005", "area": "backup", "item": "backup and restore test completed", "required": True},
    {"id": "cmp-006", "area": "observability", "item": "metrics and health checks available", "required": True},
    {"id": "cmp-007", "area": "audit", "item": "provider/execution audit enabled", "required": True},
    {"id": "cmp-008", "area": "release", "item": "checksums and release notes generated", "required": True},
]


def compliance_checklist() -> list[dict]:
    return list(COMPLIANCE_CHECKLIST)


def compliance_summary(status: dict[str, bool] | None = None) -> dict:
    status = status or {}
    items = []
    for item in COMPLIANCE_CHECKLIST:
        ok = bool(status.get(item["id"], False))
        items.append({**item, "ok": ok})
    required = [item for item in items if item["required"]]
    passed = [item for item in required if item["ok"]]
    return {
        "ok": len(required) == len(passed),
        "required_total": len(required),
        "required_passed": len(passed),
        "items": items,
    }
