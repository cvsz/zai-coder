from __future__ import annotations
from zai_coder.real_provider_adapters.models import ProviderOperation

def github_create_repo_operation(repo_name: str, visibility: str = 'public') -> ProviderOperation:
    if not repo_name or '/' in repo_name or '..' in repo_name:
        raise ValueError('repo_name must be a simple repository name')
    if visibility not in {'public', 'private'}:
        raise ValueError('visibility must be public or private')
    flag = '--private' if visibility == 'private' else '--public'
    return ProviderOperation('github', 'create_repo', repo_name, (f'gh repo create {repo_name} {flag} --source=. --remote=origin',), {'repo_name': repo_name, 'visibility': visibility}, True)

def github_release_operation(version: str = 'v0.17.0') -> ProviderOperation:
    if not version.startswith('v'):
        raise ValueError('version must start with v')
    return ProviderOperation('github', 'create_release', version, (f"gh release create {version} --draft --title 'ZAI Coder Control Plane {version}' --notes-file docs/release/RELEASE_NOTES_v0.12.0.md",), {'version': version}, True)
