from pathlib import Path
import subprocess


def test_generated_state_guard_script_exists_and_is_executable():
    script = Path("scripts/repo/check-generated-state.sh")
    assert script.exists()
    assert script.stat().st_mode & 0o111


def test_generated_state_candidates_are_not_tracked():
    patterns = [
        "data/*.db",
        "data/**/*.db",
        "*.sqlite",
        "*.sqlite3",
        "**/*.sqlite",
        "**/*.sqlite3",
        "evidence/**/*.json",
        "identity/evidence/**/*.json",
        "marketplace/exports/**/*.json",
        "migration/exports/**/*.json",
        "security/evidence/**/*.json",
    ]

    tracked = []
    for pattern in patterns:
        result = subprocess.run(
            ["git", "ls-files", pattern],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        tracked.extend(line for line in result.stdout.splitlines() if line.strip())

    assert tracked == []
