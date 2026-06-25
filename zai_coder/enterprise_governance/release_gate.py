"""Release readiness gate."""

from __future__ import annotations

from .compliance import compliance_summary
from .risk_register import risk_summary
from .policy_engine import governance_gate


def release_readiness_gate(status: dict | None = None) -> dict:
    status = status or {}
    compliance = compliance_summary(status.get("compliance", {}))
    risk = risk_summary()
    governance = governance_gate(status.get("operation", {"mutating": False, "apply": False}))
    required_checks = {
        "tests_passed": bool(status.get("tests_passed", False)),
        "repo_check_ok": bool(status.get("repo_check_ok", False)),
        "secret_scan_ok": bool(status.get("secret_scan_ok", False)),
        "backup_ok": bool(status.get("backup_ok", False)),
        "cloudflare_access_ok": bool(status.get("cloudflare_access_ok", False)),
    }
    blocked = [name for name, ok in required_checks.items() if not ok]
    allowed = not blocked and compliance["ok"] and risk["ok"] and governance["allowed"]
    return {
        "allowed": allowed,
        "blocked": blocked,
        "required_checks": required_checks,
        "compliance": compliance,
        "risk": risk,
        "governance": governance,
    }


def sample_release_status() -> dict:
    return {
        "tests_passed": True,
        "repo_check_ok": True,
        "secret_scan_ok": True,
        "backup_ok": True,
        "cloudflare_access_ok": True,
        "compliance": {f"cmp-{i:03d}": True for i in range(1, 9)},
        "operation": {"mutating": False, "apply": False, "secret_scan_ok": True},
    }
