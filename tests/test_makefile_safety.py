from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str):
    return subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_makefile_exists():
    assert (ROOT / "Makefile").exists()


def test_makefile_defaults_to_dry_run():
    res = run("make", "doctor")
    assert res.returncode == 0
    assert "[DRY-RUN]" in res.stdout


def test_safety_wrapper_blocks_git_add_dot():
    res = run("./scripts/safety-dry-run.sh", "--", "git", "add", ".")
    assert res.returncode == 126
    assert "SAFETY BLOCKED" in res.stderr


def test_safety_check_runs():
    res = run("make", "safety-check")
    assert res.returncode == 0
    assert "safety-check" in res.stdout or "Safety check" in res.stdout
