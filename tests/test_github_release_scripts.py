from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_github_scripts_exist():
    scripts = [
        "scripts/github/gh-create-repo-safe.sh",
        "scripts/github/gh-init-local-safe.sh",
        "scripts/github/gh-stage-manifest-safe.sh",
        "scripts/github/gh-push-safe.sh",
        "scripts/github/gh-release-safe.sh",
        "scripts/git/gpg-doctor.sh",
        "scripts/git/gpg-list-keys.sh",
        "scripts/git/gpg-loopback.sh",
        "scripts/git/gpg-commit-safe.sh",
        "scripts/git/gpg-tag-safe.sh",
    ]
    for script in scripts:
        assert (ROOT / script).exists(), script


def test_stage_manifest_blocks_unsafe_patterns():
    text = read("scripts/github/gh-stage-manifest-safe.sh")
    assert "apps/zlms" in text
    assert "node_modules" in text
    assert "git add --" in text
    assert "git add ." not in text


def test_gpg_commit_requires_apply():
    text = read("scripts/git/gpg-commit-safe.sh")
    assert 'APPLY' in text
    assert 'git commit -S' in text
    assert '--no-verify' not in text


def test_readme_mentions_no_git_add_dot():
    text = read("README.md")
    assert "No `git add .`" in text or "git add ." in text
    assert "APPLY=1" in text
