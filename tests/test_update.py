import pytest
from zai_coder.core.update import check_update, plan_update
import json

def test_package_manifest_check(tmp_path):
    # Mock current manifest
    dist_dir = tmp_path / "dist"
    dist_dir.mkdir()
    current = dist_dir / "RELEASE_MANIFEST.json"
    current.write_text(json.dumps({"version": "0.1.0"}))
    
    # Mock target manifest
    target = tmp_path / "TARGET_MANIFEST.json"
    target.write_text(json.dumps({"version": "0.2.0"}))
    
    res = check_update(str(tmp_path), str(target))
    assert res["current_version"] == "0.1.0"
    assert res["target_version"] == "0.2.0"
    assert res["can_update"] is True
    
    plan = plan_update(str(tmp_path), str(target))
    assert len(plan["steps"]) > 1
    
    # Check no update needed
    target.write_text(json.dumps({"version": "0.1.0"}))
    res2 = check_update(str(tmp_path), str(target))
    assert res2["can_update"] is False
    plan2 = plan_update(str(tmp_path), str(target))
    assert len(plan2["steps"]) == 1
    assert "Already up to date" in plan2["steps"][0]
