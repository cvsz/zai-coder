import subprocess
import sys
import pytest

def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "zai_coder.cli", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
        check=False,
    )

def test_top_level_help():
    res = run_cli("--help")
    assert res.returncode == 0
    assert "Standalone local-first AI coding and media-agent CLI" in res.stdout
    assert "doctor" in res.stdout
    assert "ask" in res.stdout
    assert "plan" in res.stdout
    assert "serve" in res.stdout
    assert "run" in res.stdout
    assert "scan" in res.stdout
    assert "For more information on specific subcommands" in res.stdout

def test_version_flag():
    res = run_cli("--version")
    assert res.returncode == 0
    assert "0.1.3" in res.stdout or "0.1.3" in res.stderr

def test_invalid_command():
    res = run_cli("__definitely_invalid_command__")
    assert res.returncode != 0
    assert "invalid choice" in res.stderr
    assert "usage:" in res.stderr or "usage:" in res.stdout

def test_subcommand_help():
    for cmd in ["doctor", "ask", "serve", "run", "plan", "scan"]:
        res = run_cli(cmd, "--help")
        assert res.returncode == 0
        assert "usage:" in res.stdout
        assert cmd in res.stdout

def test_missing_required_argument():
    res = run_cli("ask")
    assert res.returncode != 0
    assert "error" in res.stderr
