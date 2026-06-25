"""Go-live checklist."""

from __future__ import annotations


def go_live_checklist() -> list[dict]:
    return [
        {"area": "tests", "item": "python3 -m pytest -q", "required": True},
        {"area": "repo", "item": "make repo-check && make secret-scan", "required": True},
        {"area": "env", "item": ".env exists and is not committed", "required": True},
        {"area": "auth", "item": "session auth enabled for protected APIs", "required": True},
        {"area": "database", "item": "migrations applied and backup created", "required": True},
        {"area": "service", "item": "systemd or Docker service starts on localhost", "required": True},
        {"area": "health", "item": "/healthz and /readyz pass", "required": True},
        {"area": "cloudflare", "item": "Cloudflare Access enabled before public DNS", "required": True},
        {"area": "backup", "item": "restore test completed", "required": True},
        {"area": "release", "item": "release artifact checksums and SBOM generated", "required": True},
    ]
