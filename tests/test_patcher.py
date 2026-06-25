from pathlib import Path
import subprocess

from zai_coder.core.patcher import PatchRuntime


def test_patch_blocks_secret_path(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)
    patch = """diff --git a/.env b/.env\nnew file mode 100644\n--- /dev/null\n+++ b/.env\n@@ -0,0 +1 @@\n+SECRET=1\n"""
    res = PatchRuntime(tmp_path, ".zai-coder/checkpoints").apply(patch)
    assert not res.ok
    assert "secret" in res.blocked_reason.lower()


def test_patch_check_can_validate(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)
    (tmp_path / "a.txt").write_text("hello\n", encoding="utf-8")
    subprocess.run(["git", "add", "a.txt"], cwd=tmp_path, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    patch = """diff --git a/a.txt b/a.txt\n--- a/a.txt\n+++ b/a.txt\n@@ -1 +1 @@\n-hello\n+hello world\n"""
    res = PatchRuntime(tmp_path, ".zai-coder/checkpoints").apply(patch, check_only=True)
    assert res.ok or "No valid patches" not in res.stderr
