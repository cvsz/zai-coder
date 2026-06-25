"""Cloudflare Tunnel config generator."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CloudflareTunnelConfig:
    tunnel_name: str
    hostname: str
    service_url: str = "http://127.0.0.1:8765"

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.tunnel_name:
            issues.append("missing tunnel_name")
        if not self.hostname or "." not in self.hostname:
            issues.append("hostname must be a DNS name")
        if not self.service_url.startswith("http://127.0.0.1:"):
            issues.append("service_url should bind to localhost by default")
        return issues

    def render_yaml(self) -> str:
        issues = self.validate()
        if issues:
            raise ValueError("; ".join(issues))
        return f"""# Generated Cloudflare Tunnel config
# Review before use. Do not commit credentials.
tunnel: {self.tunnel_name}
credentials-file: /etc/cloudflared/{self.tunnel_name}.json

ingress:
  - hostname: {self.hostname}
    service: {self.service_url}
  - service: http_status:404
"""
