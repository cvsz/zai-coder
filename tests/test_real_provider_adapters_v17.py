from pathlib import Path
import tempfile
from zai_coder.real_provider_adapters.models import ProviderContext
from zai_coder.real_provider_adapters.env_validation import validate_provider_env, required_env_for
from zai_coder.real_provider_adapters.permissions import permission_decision, has_provider_permission
from zai_coder.real_provider_adapters.approval_guard import approval_decision
from zai_coder.real_provider_adapters.audit import ProviderAuditLog
from zai_coder.real_provider_adapters.executor import ProviderExecutor
from zai_coder.real_provider_adapters.providers.github_provider import github_create_repo_operation, github_release_operation
from zai_coder.real_provider_adapters.providers.cloudflare_provider import cloudflare_tunnel_operation, cloudflare_access_operation
from zai_coder.real_provider_adapters.providers.docker_provider import docker_compose_up_operation, docker_status_operation
from zai_coder.real_provider_adapters.providers.postgres_runtime_provider import postgres_migration_operation, postgres_health_operation
from zai_coder.real_provider_adapters.registry import list_provider_actions, build_demo_operations
from zai_coder.real_provider_adapters.routes import route_providers_status, route_provider_actions, route_provider_env_check, route_github_create_repo_plan, route_github_release_plan, route_cloudflare_tunnel_plan, route_docker_compose_plan, route_postgres_migration_plan, route_provider_audit, route_providers_page, route_provider_audit_page

def test_env_validation():
    assert required_env_for('github', apply=True) == ['GITHUB_TOKEN']
    assert validate_provider_env('github', {}, apply=False)['ok'] is True
    assert validate_provider_env('github', {}, apply=True)['ok'] is False
    assert validate_provider_env('github', {'GITHUB_TOKEN': 'x' * 20}, apply=True)['ok'] is True
    assert validate_provider_env('unknown', {}, apply=False)['ok'] is False

def test_permissions_and_approval():
    assert has_provider_permission(('admin',), (), 'providers:apply')
    assert permission_decision(('viewer',), (), apply=True)['allowed'] is False
    assert approval_decision(False)['allowed'] is True
    assert approval_decision(True, '')['allowed'] is False
    assert approval_decision(True, 'approved_manual_001')['allowed'] is True

def test_provider_operations():
    assert github_create_repo_operation('demo').provider == 'github'
    assert github_release_operation('v0.17.0').action == 'create_release'
    assert cloudflare_tunnel_operation('zai.example.com').provider == 'cloudflare'
    assert cloudflare_access_operation('zai.example.com').mutating is True
    assert docker_compose_up_operation().provider == 'docker'
    assert docker_status_operation().mutating is False
    assert postgres_migration_operation().provider == 'postgres'
    assert postgres_health_operation().mutating is False

def test_executor_dry_run_and_blocked_apply():
    with tempfile.TemporaryDirectory() as td:
        audit = ProviderAuditLog(Path(td) / 'audit.db')
        executor = ProviderExecutor(audit)
        result = executor.execute(ProviderContext(provider='github', apply=False), github_create_repo_operation('demo'))
        assert result.ok is True and result.dry_run is True and result.audit_id
        blocked = executor.execute(ProviderContext(provider='github', apply=True, scopes=('providers:apply',)), github_create_repo_operation('demo'))
        assert blocked.ok is False and blocked.blocked_reasons and audit.list_events()

def test_executor_apply_allowed_with_env_permission_approval():
    with tempfile.TemporaryDirectory() as td:
        executor = ProviderExecutor(ProviderAuditLog(Path(td) / 'audit.db'))
        ctx = ProviderContext(provider='github', apply=True, roles=('admin',), scopes=('providers:apply',), approval_id='approved_manual_001', env={'GITHUB_TOKEN': 'x' * 20})
        result = executor.execute(ctx, github_create_repo_operation('demo'))
        assert result.ok is True and result.dry_run is False

def test_registry():
    assert len(list_provider_actions()) >= 8
    assert len(build_demo_operations()) >= 8

def test_routes():
    assert route_providers_status()['ok'] is True
    assert route_provider_actions()['actions']
    assert route_provider_env_check({'provider': 'github'})['ok'] is True
    assert route_github_create_repo_plan({'repo_name': 'demo'})['dry_run'] is True
    assert route_github_release_plan({'version': 'v0.17.0'})['dry_run'] is True
    assert route_cloudflare_tunnel_plan({'hostname': 'zai.example.com'})['dry_run'] is True
    assert route_docker_compose_plan({})['dry_run'] is True
    assert route_postgres_migration_plan({})['dry_run'] is True
    assert 'events' in route_provider_audit()
    assert route_providers_page()['content_type'] == 'text/html'
    assert route_provider_audit_page()['content_type'] == 'text/html'

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in ['scripts/providers/provider-status.sh','scripts/providers/provider-env-check.sh','scripts/providers/github-plan.sh','scripts/providers/cloudflare-plan.sh','scripts/providers/docker-plan.sh','scripts/providers/postgres-plan.sh','scripts/providers/provider-audit.sh','docs/providers/REAL_PROVIDER_ADAPTERS_GUIDE.md','docs/providers/PROVIDER_ENVIRONMENT.md','docs/providers/PROVIDER_AUDIT_AND_APPROVAL.md','docs/requirements/NEXT_V17_REAL_PROVIDER_ADAPTERS_REQUIREMENTS.md','assets/providers/real_provider_adapters_features.json']:
        assert (root / rel).exists(), rel
