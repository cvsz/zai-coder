from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class EnvRequirement:
    name: str
    required_for_apply: bool = True
    description: str = ''

PROVIDER_ENV_REQUIREMENTS: dict[str, tuple[EnvRequirement, ...]] = {
    'github': (EnvRequirement('GITHUB_TOKEN', True, 'GitHub token or authenticated gh session'), EnvRequirement('GITHUB_OWNER', False, 'GitHub owner/user/org')),
    'cloudflare': (EnvRequirement('CLOUDFLARE_API_TOKEN', True, 'Cloudflare API token'), EnvRequirement('CLOUDFLARE_ACCOUNT_ID', True, 'Cloudflare account ID'), EnvRequirement('CLOUDFLARE_ZONE_ID', False, 'Cloudflare zone ID')),
    'docker': (EnvRequirement('DOCKER_HOST', False, 'Docker host socket/endpoint'),),
    'postgres': (EnvRequirement('DATABASE_URL', True, 'PostgreSQL DSN'),),
}

def required_env_for(provider: str, apply: bool = False) -> list[str]:
    return [req.name for req in PROVIDER_ENV_REQUIREMENTS.get(provider, ()) if apply and req.required_for_apply]

def validate_provider_env(provider: str, env: dict[str, str] | None = None, apply: bool = False) -> dict:
    env = env or {}
    reqs = PROVIDER_ENV_REQUIREMENTS.get(provider)
    if reqs is None:
        return {'ok': False, 'provider': provider, 'missing': [], 'issues': [f'unknown provider: {provider}'], 'safe_env_keys': sorted(env.keys())}
    missing = [req.name for req in reqs if apply and req.required_for_apply and not env.get(req.name)]
    issues: list[str] = []
    for key, value in env.items():
        if ('TOKEN' in key or 'SECRET' in key or 'PASSWORD' in key) and value and len(value) < 12:
            issues.append(f'{key} appears too short')
    return {'ok': not missing and not issues, 'provider': provider, 'missing': missing, 'issues': issues, 'safe_env_keys': sorted(env.keys())}
