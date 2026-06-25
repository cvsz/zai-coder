"""Rollback hook registry."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RollbackHook:
    name: str
    action: str
    command: tuple[str, ...]
    requires_backup: bool = True

    def to_dict(self) -> dict:
        return {"name": self.name, "action": self.action, "command": list(self.command), "requires_backup": self.requires_backup}


DEFAULT_ROLLBACK_HOOKS = {
    "docker_compose_up": RollbackHook("docker-compose-down", "docker_compose_up", ("docker", "compose", "-f", "deploy/docker/docker-compose.production-hardening.yml", "ps"), False),
    "cloudflare_dns": RollbackHook("cloudflare-dns-rollback-plan", "cloudflare_dns", ("make", "cloudflare-dns-rollback-plan"), True),
    "postgres_migrate": RollbackHook("postgres-backup-restore-plan", "postgres_migrate", ("make", "restore-plan"), True),
}


def list_rollback_hooks() -> list[dict]:
    return [hook.to_dict() for hook in DEFAULT_ROLLBACK_HOOKS.values()]


def rollback_hook_for(action: str) -> dict | None:
    hook = DEFAULT_ROLLBACK_HOOKS.get(action)
    return hook.to_dict() if hook else None
