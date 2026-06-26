from pathlib import Path
import subprocess


def test_release_process_guardrail_docs_exist():
    assert Path("docs/ops/release-process-guardrails.md").exists()
    assert Path("docs/ops/release-branch-checklist-template.md").exists()


def test_ci_pytest_setup_guard_script_exists_and_is_executable():
    script = Path("scripts/repo/check-ci-pytest-setup.sh")
    assert script.exists()
    assert script.stat().st_mode & 0o111


def test_ci_pytest_setup_guard_passes():
    result = subprocess.run(
        ["bash", "scripts/repo/check-ci-pytest-setup.sh"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
