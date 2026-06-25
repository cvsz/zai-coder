from __future__ import annotations
from .providers.github_provider import github_create_repo_operation, github_release_operation
from .providers.cloudflare_provider import cloudflare_tunnel_operation, cloudflare_access_operation
from .providers.docker_provider import docker_compose_up_operation, docker_status_operation
from .providers.postgres_runtime_provider import postgres_migration_operation, postgres_health_operation

def list_provider_actions() -> list[dict]:
    return [{'provider': p, 'action': a, 'mutating': m} for p, a, m in [
        ('github','create_repo',True), ('github','create_release',True), ('cloudflare','create_tunnel_route',True), ('cloudflare','configure_access',True), ('docker','compose_up',True), ('docker','compose_status',False), ('postgres','migrate',True), ('postgres','health_check',False)
    ]]

def build_demo_operations():
    return [github_create_repo_operation('zai-coder-control-plane', 'public'), github_release_operation('v0.17.0'), cloudflare_tunnel_operation('zai.example.com'), cloudflare_access_operation('zai.example.com'), docker_compose_up_operation(), docker_status_operation(), postgres_migration_operation(), postgres_health_operation()]
