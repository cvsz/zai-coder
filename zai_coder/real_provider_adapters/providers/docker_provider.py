from __future__ import annotations
from zai_coder.real_provider_adapters.models import ProviderOperation

def docker_compose_up_operation(compose_file: str = 'deploy/docker/docker-compose.production-hardening.yml') -> ProviderOperation:
    if compose_file.startswith('/') or '..' in compose_file:
        raise ValueError('compose_file must be safe relative path')
    return ProviderOperation('docker', 'compose_up', compose_file, (f'docker compose -f {compose_file} config', f'docker compose -f {compose_file} up --build -d', f'docker compose -f {compose_file} ps'), {'compose_file': compose_file}, True)

def docker_status_operation(compose_file: str = 'deploy/docker/docker-compose.production-hardening.yml') -> ProviderOperation:
    return ProviderOperation('docker', 'compose_status', compose_file, (f'docker compose -f {compose_file} ps',), {'compose_file': compose_file}, False)
