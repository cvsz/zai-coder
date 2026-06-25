"""Preflight exposure scanner.

This is a configuration-level scanner. It does not open firewall ports or mutate state.
"""

from __future__ import annotations

from pathlib import Path


RISK_PATTERNS = {
    "bind_all_interfaces": ("0.0.0.0:8765", "--host 0.0.0.0", "host: 0.0.0.0"),
    "disabled_access_warning": ("Access disabled", "without Access", "public without access"),
    "secret_files": (".env", "credentials.json", "creds.json", "*.pem", "*.key"),
}


def scan_text_for_exposure(text: str) -> list[dict]:
    findings = []
    for name, patterns in RISK_PATTERNS.items():
        for pattern in patterns:
            if pattern in text:
                findings.append({"type": name, "pattern": pattern})
    return findings


def exposure_scan_plan(root: str | Path = ".") -> dict:
    root = Path(root)
    scan_files = [
        "Dockerfile.production",
        "deploy/docker/docker-compose.production-hardening.yml",
        "deploy/systemd/zai-coder-production-hardening.service",
        ".env.example",
    ]
    findings = []
    for rel in scan_files:
        path = root / rel
        if path.exists():
            for finding in scan_text_for_exposure(path.read_text(encoding="utf-8", errors="ignore")):
                finding["path"] = rel
                findings.append(finding)
    return {
        "ok": not any(f["type"] == "bind_all_interfaces" for f in findings),
        "findings": findings,
        "checks": scan_files,
        "dry_run": True,
    }
