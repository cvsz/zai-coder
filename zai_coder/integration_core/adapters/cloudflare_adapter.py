"""Cloudflare integration adapter."""

from __future__ import annotations

from dataclasses import dataclass

from zai_coder.integration_core.models import IntegrationPlan


@dataclass(frozen=True)
class CloudflareDnsRecord:
    name: str
    record_type: str
    target: str
    proxied: bool = True

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.name or "." not in self.name:
            issues.append("record name must be a DNS name")
        if self.record_type not in {"A", "AAAA", "CNAME", "TXT"}:
            issues.append(f"unsupported record type: {self.record_type}")
        if not self.target:
            issues.append("missing target")
        return issues

    def to_dict(self) -> dict:
        return {"name": self.name, "record_type": self.record_type, "target": self.target, "proxied": self.proxied}


def tunnel_validate_plan(config_path: str = "deploy/cloudflare/generated-tunnel.example.yml") -> IntegrationPlan:
    return IntegrationPlan(
        provider="cloudflare",
        action="tunnel_validate",
        commands=[f"cloudflared tunnel ingress validate {config_path}", "cloudflared tunnel list"],
        payload={"config_path": config_path},
        warnings=["Validation only. Do not commit Cloudflare credentials."],
    )


def dns_plan(records: list[CloudflareDnsRecord]) -> IntegrationPlan:
    issues = []
    payload = []
    for record in records:
        payload.append(record.to_dict())
        issues.extend([f"{record.name}: {issue}" for issue in record.validate()])
    return IntegrationPlan(
        provider="cloudflare",
        action="dns_plan",
        commands=["# Review DNS records before applying through Cloudflare dashboard or Terraform."],
        payload={"records": payload},
        warnings=issues,
    )


def pages_deploy_plan(project_name: str, directory: str = "dist") -> IntegrationPlan:
    return IntegrationPlan(
        provider="cloudflare",
        action="pages_deploy_plan",
        commands=[f"wrangler pages deploy {directory} --project-name {project_name}"],
        payload={"project_name": project_name, "directory": directory},
        warnings=["Dry-run plan only. Requires wrangler auth and explicit operator approval."],
    )
