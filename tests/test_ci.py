import pytest
import subprocess
import os

def test_ci_target_existence():
    # Make sure Makefile exposes required targets
    res = subprocess.run(["make", "-n", "repo-check"], capture_output=True, text=True)
    assert res.returncode == 0
    
    res = subprocess.run(["make", "-n", "secret-scan"], capture_output=True, text=True)
    assert res.returncode == 0
    
    res = subprocess.run(["make", "-n", "stage-manifest-check"], capture_output=True, text=True)
    assert res.returncode == 0
    
    res = subprocess.run(["make", "-n", "final-release-status"], capture_output=True, text=True)
    assert res.returncode == 0
