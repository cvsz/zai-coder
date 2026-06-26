import os
import subprocess
import sys
from pathlib import Path
import json

def check_import_health():
    try:
        import zai_coder
        import zai_coder.github_ready_core
        return {"ok": True, "message": "Import health OK"}
    except Exception as e:
        return {"ok": False, "message": f"Import failed: {e}"}

def check_cli_parser():
    try:
        # Avoid shelling out for the CLI if we can just import its parser
        # Actually, let's just use subprocess bounded by timeout
        res = subprocess.run(["./zai-coder", "--help"], capture_output=True, timeout=5, text=True)
        return {"ok": res.returncode == 0, "message": "CLI parser OK" if res.returncode == 0 else "CLI parser failed"}
    except Exception as e:
        return {"ok": False, "message": f"CLI execution failed: {e}"}

def check_required_files():
    root = Path(".")
    required = ["README.md", "Makefile", "zai-coder", ".github/workflows/ci.yml"]
    missing = [f for f in required if not (root / f).exists()]
    if missing:
        return {"ok": False, "message": f"Missing: {missing}"}
    return {"ok": True, "message": "Required files present"}

def check_safety_rules():
    root = Path(".")
    safety_script = root / "scripts" / "safety-check.sh"
    if not safety_script.exists():
        return {"ok": False, "message": "Safety check script missing"}
    try:
        res = subprocess.run(["bash", str(safety_script), "."], capture_output=True, timeout=10, text=True)
        return {"ok": res.returncode == 0, "message": "Safety rules OK" if res.returncode == 0 else "Safety rules failed"}
    except Exception as e:
        return {"ok": False, "message": f"Safety check failed: {e}"}

def check_tests_directory():
    root = Path(".")
    tests_dir = root / "tests"
    if not tests_dir.is_dir():
        return {"ok": False, "message": "tests directory missing"}
    return {"ok": True, "message": "tests directory exists"}

def check_makefile_targets():
    root = Path(".")
    makefile = root / "Makefile"
    if not makefile.exists():
        return {"ok": False, "message": "Makefile missing"}
    content = makefile.read_text(encoding="utf-8")
    targets = ["repo-check:", "secret-scan:", "stage-manifest-check:", "final-release-status:"]
    missing = [t for t in targets if t not in content]
    if missing:
        return {"ok": False, "message": f"Missing targets: {missing}"}
    return {"ok": True, "message": "Makefile targets OK"}

def check_scripts_executable():
    root = Path(".")
    scripts_dir = root / "scripts"
    if not scripts_dir.is_dir():
        return {"ok": False, "message": "scripts directory missing"}
    # check if files ending in .sh are executable
    not_exec = []
    for sh_file in scripts_dir.rglob("*.sh"):
        if not os.access(sh_file, os.X_OK):
            not_exec.append(str(sh_file))
    if not_exec:
        return {"ok": False, "message": f"Not executable: {not_exec}"}
    return {"ok": True, "message": "Scripts executable OK"}

def check_package_metadata():
    root = Path(".")
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return {"ok": False, "message": "pyproject.toml missing"}
    # rudimentary check for metadata
    content = pyproject.read_text(encoding="utf-8")
    if "name" not in content or "version" not in content:
        return {"ok": False, "message": "Package metadata missing name/version"}
    return {"ok": True, "message": "Package metadata OK"}
