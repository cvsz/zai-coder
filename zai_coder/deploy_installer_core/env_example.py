"""Environment example generator."""

from __future__ import annotations

from .config import DeployInstallConfig


def render_env_example(config: DeployInstallConfig | None = None) -> str:
    config = config or DeployInstallConfig()
    return f"""# ZAI Coder Control Plane environment example
# Copy to .env and edit values before production use.

ZAI_ENV=production
ZAI_HOST={config.host}
ZAI_PORT={config.port}
ZAI_DOMAIN={config.domain}

# Use PostgreSQL for production. Keep credentials outside git.
DATABASE_URL=postgresql://zai:change-me@127.0.0.1:5432/zai

# Session secret should be generated locally. Do not commit real value.
ZAI_SESSION_SECRET=replace-with-generated-secret

# Cloudflare optional
CLOUDFLARE_TUNNEL_NAME=zai-coder
CLOUDFLARE_HOSTNAME={config.domain}

# Runtime paths
ZAI_DATA_DIR={config.data_dir}
ZAI_LOGS_DIR={config.logs_dir}
ZAI_BACKUP_DIR={config.backup_dir}
ZAI_STORAGE_DIR={config.storage_dir}
"""
