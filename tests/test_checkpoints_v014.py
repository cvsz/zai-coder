import pytest
from pathlib import Path
from zai_coder.core.checkpoints import CheckpointManager

def test_checkpoint_list_and_metadata(tmp_path):
    # Setup mock checkpoint
    cp_dir = tmp_path / ".zai-coder" / "checkpoints" / "patch-20230101-120000-abcd"
    cp_dir.mkdir(parents=True)
    (cp_dir / "test.txt").write_text("content")

    cm = CheckpointManager(tmp_path, checkpoint_dir=".zai-coder/checkpoints")
    cps = cm.list_checkpoints()
    assert len(cps) == 1
    assert cps[0]["id"] == "patch-20230101-120000-abcd"
    assert "test.txt" in cps[0]["files"]

def test_restore_checkpoint_dry_run(tmp_path):
    cp_dir = tmp_path / ".zai-coder" / "checkpoints" / "patch-test"
    cp_dir.mkdir(parents=True)
    (cp_dir / "file1.txt").write_text("v1")

    cm = CheckpointManager(tmp_path, checkpoint_dir=".zai-coder/checkpoints")
    result = cm.restore_checkpoint("patch-test", dry_run=True)
    assert result["dry_run"] is True
    assert result["restored"] is False
    assert not (tmp_path / "file1.txt").exists()

def test_restore_checkpoint_apply(tmp_path):
    cp_dir = tmp_path / ".zai-coder" / "checkpoints" / "patch-test"
    cp_dir.mkdir(parents=True)
    (cp_dir / "file1.txt").write_text("v1")

    cm = CheckpointManager(tmp_path, checkpoint_dir=".zai-coder/checkpoints")
    result = cm.restore_checkpoint("patch-test", dry_run=False)
    assert result["dry_run"] is False
    assert result["restored"] is True
    assert (tmp_path / "file1.txt").exists()
    assert (tmp_path / "file1.txt").read_text() == "v1"

def test_restore_checkpoint_secret_blocked(tmp_path):
    cp_dir = tmp_path / ".zai-coder" / "checkpoints" / "patch-test"
    cp_dir.mkdir(parents=True)
    (cp_dir / "secret.env").write_text("v1")

    cm = CheckpointManager(tmp_path, checkpoint_dir=".zai-coder/checkpoints")
    with pytest.raises(ValueError, match="Safety violation: Blocked possible secret file"):
        cm.restore_checkpoint("patch-test", dry_run=False)

def test_path_traversal_blocked(tmp_path):
    cm = CheckpointManager(tmp_path, checkpoint_dir=".zai-coder/checkpoints")
    with pytest.raises(ValueError, match="path traversal blocked"):
        cm._get_checkpoint_path("../outside")
