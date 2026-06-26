import pytest
from zai_coder.core.patcher import PatchRuntime
from zai_coder.core.safety import SafetyPolicy
import os

def test_patch_runtime_check_mode(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("Hello\n")
    patch = tmp_path / "test.diff"
    patch_text = "--- a/test.txt\n+++ b/test.txt\n@@ -1,1 +1,1 @@\n-Hello\n+World\n"
    patch.write_text(patch_text)

    runtime = PatchRuntime(workspace=str(tmp_path), checkpoint_dir=str(tmp_path / "checkpoints"), safety=SafetyPolicy())
    res = runtime.apply_file(str(patch), check_only=True)
    assert res.ok
    assert f.read_text() == "Hello\n"  # unchanged in check mode

def test_patch_runtime_apply_mode(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("Hello\n")
    patch = tmp_path / "test.diff"
    patch_text = "--- a/test.txt\n+++ b/test.txt\n@@ -1,1 +1,1 @@\n-Hello\n+World\n"
    patch.write_text(patch_text)

    runtime = PatchRuntime(workspace=str(tmp_path), checkpoint_dir=str(tmp_path / "checkpoints"), safety=SafetyPolicy())
    res = runtime.apply_file(str(patch), check_only=False)
    assert res.ok
    assert f.read_text() == "World\n"
    assert res.checkpoint is not None

def test_patch_runtime_blocked_secret(tmp_path):
    secret_dir = tmp_path / "apps" / "zlms"
    secret_dir.mkdir(parents=True)
    f = secret_dir / "secret.txt"
    f.write_text("Secret\n")

    patch = tmp_path / "secret.diff"
    patch_text = "--- a/apps/zlms/secret.txt\n+++ b/apps/zlms/secret.txt\n@@ -1,1 +1,1 @@\n-Secret\n+Hacked\n"
    patch.write_text(patch_text)

    runtime = PatchRuntime(workspace=str(tmp_path), checkpoint_dir=str(tmp_path / "checkpoints"), safety=SafetyPolicy(allow_apps_zlms=False))
    res = runtime.apply_file(str(patch), check_only=False)
    assert not res.ok
    assert "Blocked" in res.blocked_reason or "not allowed" in res.blocked_reason

def test_patch_runtime_path_traversal(tmp_path):
    patch = tmp_path / "trav.diff"
    patch_text = "--- a/../../../etc/passwd\n+++ b/../../../etc/passwd\n@@ -1,1 +1,1 @@\n-root:x\n+hacked\n"
    patch.write_text(patch_text)

    runtime = PatchRuntime(workspace=str(tmp_path), checkpoint_dir=str(tmp_path / "checkpoints"), safety=SafetyPolicy())
    res = runtime.apply_file(str(patch), check_only=False)
    assert not res.ok
    assert "Blocked" in res.blocked_reason or "not allowed" in res.blocked_reason or "outside workspace" in res.blocked_reason.lower() or "No such file or directory" in res.stderr

