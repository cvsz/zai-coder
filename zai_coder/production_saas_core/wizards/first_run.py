"""First-run setup wizard plan."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FirstRunPlan:
    admin_email: str
    org_slug: str
    workspace_slug: str
    steps: list[str] = field(default_factory=list)
    dry_run: bool = True

    def to_dict(self) -> dict:
        return {
            "admin_email": self.admin_email,
            "org_slug": self.org_slug,
            "workspace_slug": self.workspace_slug,
            "steps": list(self.steps),
            "dry_run": self.dry_run,
        }


def build_first_run_plan(admin_email: str, org_slug: str = "default-org", workspace_slug: str = "default") -> FirstRunPlan:
    if "@" not in admin_email:
        raise ValueError("admin_email must be valid")
    return FirstRunPlan(
        admin_email=admin_email,
        org_slug=org_slug,
        workspace_slug=workspace_slug,
        steps=[
            "run migrations",
            "bootstrap admin API key",
            "create admin user",
            "create organization",
            "create default workspace",
            "assign owner role",
            "review Cloudflare/Auth exposure",
        ],
    )
