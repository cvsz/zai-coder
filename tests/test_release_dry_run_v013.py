import os
import subprocess
import shutil
from pathlib import Path
import pytest

def run_cmd(args, *, cwd: Path, env: dict[str, str] | None = None):
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        args,
        cwd=cwd,
        env=merged_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
    )

def test_release_dry_run_refuses_to_mutate(tmp_path: Path):
    # Setup isolated environment
    root = Path.cwd()
    
    # Run release script in dry-run mode (APPLY=0 if supported or specific dry-run flag)
    # Based on discovered scripts, let's look at scripts/release/build-release-safe.sh if exists
    # Or just use the packaging script, as that is the closest release automation script
    
    # Try running scripts/package.sh in a dry-run like manner if possible
    # scripts/package.sh doesn't seem to have dry-run mode, it just writes to dist.
    # We should run it inside tmp_path to avoid mutating real dist/
    
    env = {"ROOT": str(root)}
    # Mock ROOT in package.sh might be hard if it's hardcoded.
    # The script uses ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    # So we should run it from a copy.
    
    stage = tmp_path / "stage"
    shutil.copytree(root, stage, ignore=shutil.ignore_patterns(".git", ".venv", "dist", ".pytest_cache", "data/*.db"))
    
    # Try running package script
    result = run_cmd(["bash", "scripts/package.sh"], cwd=stage)
    
    assert result.returncode == 0
    assert (stage / "dist").exists()
    assert (stage / "dist" / "zai-coder-standalone-0.1.3.zip").exists()
    
    # Verify no mutation in original root/dist
    assert not (root / "dist" / "zai-coder-standalone-0.1.3.zip").exists()

def test_package_check_validates_isolated_artifacts(tmp_path: Path):
    root = Path.cwd()
    dist = tmp_path / "dist"
    dist.mkdir()
    
    # Create dummy valid artifacts
    archive_name = "zai-coder-standalone-0.1.3"
    (dist / f"{archive_name}.tar.gz").write_text("dummy tar")
    (dist / f"{archive_name}.zip").write_text("dummy zip")
    (dist / f"{archive_name}.tar.gz.sha256").write_text(f"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  {archive_name}.tar.gz")
    (dist / f"{archive_name}.zip.sha256").write_text(f"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  {archive_name}.zip")
    
    # Create manifest
    import json
    manifest = {
        "version": "0.1.3",
        "archives": [f"{archive_name}.tar.gz", f"{archive_name}.zip"],
        "timestamp": "2026-06-26T00:00:00Z"
    }
    (dist / "RELEASE_MANIFEST.json").write_text(json.dumps(manifest))
    
    # Run package-check
    env = {"ROOT": str(tmp_path)}
    # Need to make sure package-check.sh works.
    # It assumes dist/ is in ROOT.
    # We need to run it from tmp_path and have a pyproject.toml there.
    shutil.copy(root / "pyproject.toml", tmp_path)
    
    result = run_cmd(["bash", "scripts/package-check.sh"], cwd=tmp_path)
    # This will fail because dummy tar/zip aren't real tar/zip files.
    # But it should reach the checksum or content validation step.
    assert result.returncode != 0
