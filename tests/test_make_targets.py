import pytest
import subprocess

def test_make_targets_exist():
    required_targets = [
        "repo-check",
        "secret-scan",
        "stage-manifest-check",
        "package-check",
        "web-check",
        "web-migration-report",
        "self-doctor",
        "self-list",
        "self-plan",
        "self-requirement-next"
    ]
    
    for target in required_targets:
        res = subprocess.run(["make", "-n", target], capture_output=True, text=True)
        assert res.returncode == 0, f"Makefile target {target} does not exist or failed: {res.stderr}"
