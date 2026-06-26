from zai_coder.core.repair import RepairManager
import os

def test_repair_check_empty(tmp_path):
    manager = RepairManager(tmp_path)
    # Empty patch text fails parsing paths in our simple patcher, so it returns False
    assert manager.check_patch("") is False

def test_repair_apply_dry(tmp_path):
    manager = RepairManager(tmp_path)
    patch = "--- a/file\n+++ b/file\n"
    # Even if valid format, if file doesn't exist git apply --check will fail (or our mocked subset)
    # This just ensures we don't crash
    manager.check_patch(patch)
