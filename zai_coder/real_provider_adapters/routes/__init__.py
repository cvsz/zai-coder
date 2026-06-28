from __future__ import annotations
from zai_coder.core.booleans import coerce_bool
from zai_coder.real_provider_adapters.models import ProviderContext
from zai_coder.real_provider_adapters.executor import ProviderExecutor
from zai_coder.real_provider_adapters.audit import ProviderAuditLog
from zai_coder.real_provider_adapters.registry import list_provider_actions
from zai_coder.real_provider_adapters.env_validation import validate_provider_env
from zai_coder.real_provider_adapters.providers.github_provider import github_create_repo_operation, github_release_operation
from zai_coder.real_provider_adapters.providers.cloudflare_provider import cloudflare_tunnel_operation
from zai_coder.real_provider_adapters.providers.docker_provider import docker_compose_up_operation
from zai_coder.real_provider_adapters.providers.postgres_runtime_provider import postgres_migration_operation
from zai_coder.real_provider_adapters.ui.pages import render_providers_page, render_provider_audit_page

def route_providers_status() -> dict:
    return {'ok': True, 'service': 'zai-real-provider-adapters', 'systems': ['github_adapter_wrapper','cloudflare_adapter_wrapper','docker_adapter_wrapper','postgres_runtime_adapter','provider_env_validation','provider_permission_checks','dry_run_apply_switch','provider_audit_log','approval_guard']}

def _ctx(payload: dict | None = None) -> ProviderContext:
    payload = payload or {}
    return ProviderContext(provider=payload.get('provider', 'github'), actor=payload.get('actor', 'local-operator'), roles=tuple(payload.get('roles', ['admin'])), scopes=tuple(payload.get('scopes', ['providers:plan'])), apply=coerce_bool(payload.get('apply', False)), approval_id=payload.get('approval_id', ''), env=dict(payload.get('env', {})))

def route_provider_actions() -> dict: return {'actions': list_provider_actions()}
def route_provider_env_check(payload: dict | None = None) -> dict:
    payload = payload or {}; return validate_provider_env(payload.get('provider', 'github'), dict(payload.get('env', {})), coerce_bool(payload.get('apply', False)))
def route_github_create_repo_plan(payload: dict | None = None) -> dict:
    payload = payload or {}; ctx = _ctx({**payload, 'provider': 'github'}); op = github_create_repo_operation(payload.get('repo_name', 'zai-coder-control-plane'), payload.get('visibility', 'public')); return ProviderExecutor().execute(ctx, op).to_dict()
def route_github_release_plan(payload: dict | None = None) -> dict:
    payload = payload or {}; ctx = _ctx({**payload, 'provider': 'github'}); op = github_release_operation(payload.get('version', 'v0.17.0')); return ProviderExecutor().execute(ctx, op).to_dict()
def route_cloudflare_tunnel_plan(payload: dict | None = None) -> dict:
    payload = payload or {}; ctx = _ctx({**payload, 'provider': 'cloudflare'}); op = cloudflare_tunnel_operation(payload.get('hostname', 'zai.example.com'), payload.get('tunnel_name', 'zai-coder-control-plane')); return ProviderExecutor().execute(ctx, op).to_dict()
def route_docker_compose_plan(payload: dict | None = None) -> dict:
    payload = payload or {}; ctx = _ctx({**payload, 'provider': 'docker'}); op = docker_compose_up_operation(payload.get('compose_file', 'deploy/docker/docker-compose.production-hardening.yml')); return ProviderExecutor().execute(ctx, op).to_dict()
def route_postgres_migration_plan(payload: dict | None = None) -> dict:
    payload = payload or {}; ctx = _ctx({**payload, 'provider': 'postgres'}); op = postgres_migration_operation(payload.get('dsn', 'postgresql://zai@127.0.0.1:5432/zai')); return ProviderExecutor().execute(ctx, op).to_dict()
def route_provider_audit(limit: int = 50) -> dict: return {'events': ProviderAuditLog().list_events(limit)}
def route_providers_page() -> dict: return {'content_type': 'text/html', 'html': render_providers_page()}
def route_provider_audit_page() -> dict: return {'content_type': 'text/html', 'html': render_provider_audit_page(ProviderAuditLog().list_events())}
