"""Hostname validation helpers."""

from __future__ import annotations

from .models import HOSTNAME_RE


def validate_hostname(hostname: str) -> dict:
    hostname = (hostname or "").strip().lower()
    issues: list[str] = []
    if not hostname:
        issues.append("hostname required")
    if hostname.startswith("*."):
        issues.append("wildcard hostname is not allowed for go-live target")
    if not HOSTNAME_RE.match(hostname):
        issues.append("hostname must be a valid DNS name")
    if hostname.endswith(".local") or hostname.endswith(".internal"):
        issues.append("public go-live hostname cannot be .local or .internal")
    return {"ok": not issues, "hostname": hostname, "issues": issues}
