from pathlib import Path
from zai_coder.data_import_export_migration_center.models import DataSourceSpec, MigrationJob, SchemaField, DataMapping
from zai_coder.data_import_export_migration_center.core import *
from zai_coder.data_import_export_migration_center.routes import *

def test_models_validation():
    assert DataSourceSpec("s","Source","json","fixtures/a.json").validate() == []
    assert DataSourceSpec("","","bad","secret token", mode="bad", status="bad").validate()
    assert MigrationJob("j","Job","s","target").validate() == []
    assert MigrationJob("","","","", job_type="bad", status="bad", dry_run=False).validate()
    assert SchemaField("f","dataset","name","string").validate() == []
    assert SchemaField("","","","bad").validate()
    assert DataMapping("m","src","dst","copy").validate() == []
    assert DataMapping("","","", transform="bad", status="bad").validate()

def test_core_migration():
    assert source_catalog()
    assert migration_jobs()
    assert schema_catalog()
    assert mapping_catalog()
    assert validation_report()["ok"]
    assert import_plan()["dry_run"]
    assert export_plan()["external_upload"] is False
    assert schema_compatibility_check()["dry_run"]
    assert rollback_preview()["apply_rollback"] is False
    assert migration_evidence_bundle()["requires_review"] is True

def test_exports(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert Path(write_migration_export(tmp_path)).exists()
    assert Path(write_migration_report(tmp_path)).exists()
    demo = migration_demo(str(tmp_path))
    assert Path(demo["export_path"]).exists()
    assert Path(demo["report_path"]).exists()

def test_routes():
    assert route_migration_status()["ok"]
    assert route_migration_overview()["validation"]["ok"]
    assert route_import_plan()["dry_run"]
    assert route_export_plan()["external_upload"] is False
    assert route_schema_check()["dry_run"]
    assert route_mapping_catalog()["mappings"]
    assert route_rollback_preview()["apply_rollback"] is False
    assert "export_path" in route_migration_export()
    assert "export_path" in route_migration_demo()
    assert route_migration_page()["content_type"] == "text/html"
    assert route_migration_import_page()["content_type"] == "text/html"
    assert route_migration_export_page()["content_type"] == "text/html"
    assert route_migration_schema_page()["content_type"] == "text/html"
    assert route_migration_rollback_page()["content_type"] == "text/html"

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/migration-center/migration-status.sh",
        "scripts/migration-center/import-plan.sh",
        "scripts/migration-center/export-plan.sh",
        "scripts/migration-center/schema-check.sh",
        "scripts/migration-center/mapping-catalog.sh",
        "scripts/migration-center/rollback-preview.sh",
        "scripts/migration-center/migration-export.sh",
        "scripts/migration-center/migration-demo.sh",
        "scripts/migration-center/migration-dashboard-export.sh",
        "docs/migration-center/DATA_IMPORT_EXPORT_MIGRATION_CENTER_GUIDE.md",
        "docs/migration-center/IMPORT_EXPORT_POLICY.md",
        "docs/migration-center/SCHEMA_COMPATIBILITY.md",
        "docs/migration-center/ROLLBACK_PREVIEW.md",
        "docs/migration-center/DATA_MAPPING_CATALOG.md",
        "docs/requirements/NEXT_V44_DATA_IMPORT_EXPORT_MIGRATION_CENTER_REQUIREMENTS.md",
        "assets/migration-center/data_import_export_migration_center_features.json",
    ]:
        assert (root / rel).exists(), rel
