import os
import subprocess
import shutil
from pathlib import Path
import pytest

def run_cmd(args, *, env: dict[str, str] | None = None):
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        args,
        env=merged_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

def test_installer_safe_sandbox(tmp_path: Path):
    # Setup sandbox
    sandbox = tmp_path / "sandbox"
    prefix = sandbox / "share/zai-coder"
    venv_dir = sandbox / "venvs/zai-coder"
    bin_dir = sandbox / "bin"
    launcher = bin_dir / "zai-coder"
    
    bin_dir.mkdir(parents=True)
    
    env = {
        "PREFIX": str(prefix),
        "VENV_DIR": str(venv_dir),
        "BIN_DIR": str(bin_dir),
        "LAUNCHER": str(launcher),
        "APPLY": "1"
    }
    
    # Run installer
    script = Path("scripts/install/install-local-safe.sh")
    result = run_cmd(["bash", str(script)], env=env)
    
    assert result.returncode == 0
    assert prefix.exists()
    assert venv_dir.exists()
    assert launcher.exists()
    
    # Run post-install check
    post_check = Path("scripts/install/post-install-check.sh")
    check_result = run_cmd(["bash", str(post_check)], env=env)
    
    assert check_result.returncode == 0
    assert "Check: PASSED" in check_result.stdout
