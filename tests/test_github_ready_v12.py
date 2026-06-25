from pathlib import Path

from zai_coder.github_ready_core.repo_policy import is_safe_stage_path, find_forbidden_command_text
from zai_coder.github_ready_core.stage_manifest import load_stage_manifest, validate_stage_manifest, render_git_add_commands
from zai_coder.github_ready_core.secret_scan import scan_text
from zai_coder.github_ready_core.repo_check import check_required_files, repo_ready_report
from zai_coder.github_ready_core.release_notes import render_release_notes


def test_stage_path_policy():
    assert is_safe_stage_path("README.md")
    assert not is_safe_stage_path("apps/zlms/noise.md")
    assert not is_safe_stage_path("../secret")
    assert not is_safe_stage_path(".env")
    assert not is_safe_stage_path("secret.pem")


def test_forbidden_command_detection():
    assert "git add ." in find_forbidden_command_text("never run git add .")
    assert "git add -A" in find_forbidden_command_text("never run git add -A")
    assert find_forbidden_command_text("git add -- README.md") == []


def test_stage_manifest_validation():
    root = Path(__file__).resolve().parents[1]
    items = load_stage_manifest(root / "docs/github/STAGE_MANIFEST.v12-github-ready.txt")
    result = validate_stage_manifest(items)
    assert result["ok"], result
    commands = render_git_add_commands(items)
    assert commands
    assert all(cmd.startswith("git add -- ") for cmd in commands)


def test_required_files_and_report():
    root = Path(__file__).resolve().parents[1]
    assert check_required_files(root)["ok"]
    report = repo_ready_report(root)
    assert report["required_files"]["ok"] is True
    assert report["forbidden_commands"]["ok"] is True


def test_release_notes():
    notes = render_release_notes("v0.12.0")
    assert "ZAI Coder Control Plane v0.12.0" in notes
    assert "python3 -m pytest -q" in notes


def test_github_files_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        ".github/workflows/ci.yml",
        ".github/workflows/release.yml",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/dependabot.yml",
        "LICENSE",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "SUPPORT.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "RELEASE.md",
        "scripts/github/gh-create-repo-safe.sh",
        "scripts/github/gh-stage-manifest-safe.sh",
        "scripts/repo/repo-check.sh",
        "scripts/repo/secret-scan-safe.sh",
    ]:
        assert (root / rel).exists(), rel
