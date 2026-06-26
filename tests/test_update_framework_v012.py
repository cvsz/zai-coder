import pytest
from pathlib import Path
from zai_coder.update_system.manager import UpdateManager, UpdatePlan
from zai_coder.update_system.manifest import UpdateManifest

def test_update_manifest_and_plan(tmp_path):
    manager = UpdateManager(project_root=tmp_path)
    
    # 1. Test validate_paths for safe/unsafe paths
    warnings = manager.validate_paths(["safe_file.txt", "sub/dir/safe.py"])
    assert len(warnings) == 0
    
    unsafe_warnings = manager.validate_paths([
        "/absolute/path.py",
        "../outside.py",
        "apps/zlms/conf.py",
        "node_modules/package/index.js",
        "dist/archive.tgz"
    ])
    assert len(unsafe_warnings) == 5
    assert "unsafe path" in unsafe_warnings[0]
    assert "blocked apps/zlms" in unsafe_warnings[2]
    assert "blocked generated/secret" in unsafe_warnings[3]

def test_update_manager_apply_dry_run(tmp_path):
    proj_root = tmp_path / "project"
    source_dir = tmp_path / "source"
    proj_root.mkdir()
    source_dir.mkdir()
    
    # Create test source file
    src_file = source_dir / "update.py"
    src_file.write_text("print('hello')", encoding="utf-8")
    
    manifest = UpdateManifest(
        version="1.2.3",
        channel="stable",
        files=["update.py"]
    )
    
    manager = UpdateManager(project_root=proj_root)
    
    # Dry-run plan (apply=False) should not copy files
    plan = manager.apply_from_dir(source_dir, manifest, apply=False)
    assert plan.version == "1.2.3"
    assert len(plan.warnings) == 0
    assert not (proj_root / "update.py").exists()
    
    # Real apply (apply=True) should copy files
    plan_apply = manager.apply_from_dir(source_dir, manifest, apply=True)
    assert len(plan_apply.warnings) == 0
    assert (proj_root / "update.py").exists()
    assert (proj_root / "update.py").read_text(encoding="utf-8") == "print('hello')"
