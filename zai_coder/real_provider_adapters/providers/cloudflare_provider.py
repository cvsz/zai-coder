from __future__ import annotations
from zai_coder.real_provider_adapters.models import ProviderOperation
from zai_coder.cloudflare_go_live.models import CloudflareGoLiveConfig
from zai_coder.cloudflare_go_live.tunnel import render_tunnel_config

def cloudflare_tunnel_operation(hostname: str, tunnel_name: str = 'zai-coder-control-plane') -> ProviderOperation:
    config = CloudflareGoLiveConfig(hostname=hostname, tunnel_name=tunnel_name)
    issues = config.validate()
    if issues:
        raise ValueError('; '.join(issues))
    return ProviderOperation('cloudflare', 'create_tunnel_route', hostname, (f'cloudflared tunnel create {tunnel_name}', f'cloudflared tunnel route dns {tunnel_name} {hostname}', f'cloudflared tunnel ingress validate deploy/cloudflare/generated/{tunnel_name}.yml'), {'hostname': hostname, 'tunnel_name': tunnel_name, 'config_yaml': render_tunnel_config(config)}, True)

def cloudflare_access_operation(hostname: str) -> ProviderOperation:
    return ProviderOperation('cloudflare', 'configure_access', hostname, ('# Configure Cloudflare Access application and deny-by-default policy before public DNS.',), {'hostname': hostname, 'requires_dashboard_or_api': True}, True)
