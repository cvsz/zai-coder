from __future__ import annotations
from zai_coder.real_provider_adapters.models import ProviderOperation
from zai_coder.production_hardening_core.db.postgres_adapter import PostgresSettings

def postgres_migration_operation(dsn: str = 'postgresql://zai@127.0.0.1:5432/zai') -> ProviderOperation:
    settings = PostgresSettings(dsn)
    issues = settings.validate()
    if issues:
        raise ValueError('; '.join(issues))
    safe = settings.safe_dict()
    return ProviderOperation('postgres', 'migrate', f"{safe['host']}:{safe['port']}/{safe['database']}", ('make production-migrate-plan', 'make production-migrate-apply APPLY=1'), {'safe_dsn': safe}, True)

def postgres_health_operation(dsn: str = 'postgresql://zai@127.0.0.1:5432/zai') -> ProviderOperation:
    settings = PostgresSettings(dsn)
    issues = settings.validate()
    if issues:
        raise ValueError('; '.join(issues))
    return ProviderOperation('postgres', 'health_check', settings.safe_dict()['database'], ('make postgres-check',), {'safe_dsn': settings.safe_dict()}, False)
