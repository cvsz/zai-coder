from __future__ import annotations
import json, uuid
from pathlib import Path
from .models import DataSourceSpec, MigrationJob, SchemaField, DataMapping

SOURCES = [
    DataSourceSpec("src_customer_json", "Customer JSON Export", "json", "fixtures/customer-export.json", "read_only", "validated"),
    DataSourceSpec("src_usage_csv", "Usage Analytics CSV", "csv", "fixtures/usage-analytics.csv", "read_only", "planned"),
    DataSourceSpec("src_local_sqlite", "Local SQLite Demo", "sqlite", "data/demo.sqlite", "read_only", "validated"),
]

SCHEMA = [
    SchemaField("sf_customer_id", "customers", "customer_id", "string", True),
    SchemaField("sf_email_hash", "customers", "email_hash", "string", False),
    SchemaField("sf_created_at", "customers", "created_at", "datetime", True),
    SchemaField("sf_usage_count", "usage", "usage_count", "integer", False),
]

MAPPINGS = [
    DataMapping("map_customer_id", "customer_id", "id", "rename", "validated"),
    DataMapping("map_email", "email", "email_hash", "redact", "validated"),
    DataMapping("map_created", "created_at", "created_at", "copy", "validated"),
    DataMapping("map_usage", "usage_count", "events_count", "rename", "planned"),
]

JOBS = [
    MigrationJob("job_import_customers", "Import customer JSON plan", "src_customer_json", "local/customers", "import_plan", "review", True),
    MigrationJob("job_export_usage", "Export usage analytics plan", "src_usage_csv", "local/usage-export", "export_plan", "draft", True),
    MigrationJob("job_schema_check", "Customer schema compatibility check", "src_customer_json", "local/customers", "schema_check", "review", True),
    MigrationJob("job_rollback_preview", "Rollback preview for customer import", "src_customer_json", "local/customers", "rollback_preview", "draft", True),
]

def source_catalog(): return [s.to_dict() for s in SOURCES]
def migration_jobs(): return [j.to_dict() for j in JOBS]
def schema_catalog(): return [s.to_dict() for s in SCHEMA]
def mapping_catalog(): return [m.to_dict() for m in MAPPINGS]

def validation_report() -> dict:
    rows = [*SOURCES, *JOBS, *SCHEMA, *MAPPINGS]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def import_plan(source_id="src_customer_json") -> dict:
    source = next((s for s in SOURCES if s.id == source_id), None)
    if not source: raise ValueError(f"unknown source: {source_id}")
    return {"dry_run": True, "source": source.to_dict(), "steps": ["validate source", "map fields", "preview row counts", "write local import report"], "write_data": False}

def export_plan(source_id="src_usage_csv") -> dict:
    source = next((s for s in SOURCES if s.id == source_id), None)
    if not source: raise ValueError(f"unknown source: {source_id}")
    return {"dry_run": True, "source": source.to_dict(), "format": "json", "destination": "migration/exports", "external_upload": False}

def schema_compatibility_check() -> dict:
    required = [f for f in SCHEMA if f.required]
    mappings = {m.source_field for m in MAPPINGS}
    missing = [f.name for f in required if f.name not in mappings]
    return {"ok": not missing, "missing_required_mappings": missing, "required_fields": [f.to_dict() for f in required], "dry_run": True}

def rollback_preview(job_id="job_import_customers") -> dict:
    job = next((j for j in JOBS if j.id == job_id), None)
    if not job: raise ValueError(f"unknown job: {job_id}")
    return {"dry_run": True, "job": job.to_dict(), "steps": ["snapshot local state", "reverse mapped records", "verify counts", "produce rollback report"], "apply_rollback": False}

def migration_evidence_bundle() -> dict:
    return {
        "kind": "zai-migration-evidence-bundle",
        "version": "1.0",
        "sources": source_catalog(),
        "jobs": migration_jobs(),
        "schema": schema_catalog(),
        "mappings": mapping_catalog(),
        "validation": validation_report(),
        "schema_check": schema_compatibility_check(),
        "rollback_preview": rollback_preview(),
        "external_upload": False,
        "requires_review": True,
    }

def write_migration_export(root=".", out="migration/exports/migration-evidence.json") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(migration_evidence_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_migration_report(root=".", out="migration/reports/migration-center-report.md") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    jobs = "\n".join(f"- {j.title} [{j.job_type} / {j.status} / dry_run={j.dry_run}]" for j in JOBS)
    path.write_text(f"# Data Import Export and Migration Center Report\n\n## Jobs\n\n{jobs}\n\n## Safety\n\n- Dry-run migration planning by default.\n- No direct production database access.\n- Rollback previews only.\n", encoding="utf-8")
    return str(path)

def migration_status():
    return {"ok": True, "systems": ["source_catalog","import_plan","export_plan","migration_jobs","schema_check","mapping_catalog","rollback_preview","evidence_export","dashboard_routes"]}

def migration_overview():
    return {"status": migration_status(), "sources": source_catalog(), "jobs": migration_jobs(), "schema": schema_catalog(), "mappings": mapping_catalog(), "validation": validation_report(), "schema_check": schema_compatibility_check()}

def migration_demo(root="."):
    export_path = write_migration_export(root)
    report_path = write_migration_report(root)
    return {"export_path": export_path, "report_path": report_path, "import_plan": import_plan(), "export_plan": export_plan(), "rollback_preview": rollback_preview(), "bundle": migration_evidence_bundle()}
