import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def test_pyproject_version_parsable():
    content = read("pyproject.toml")
    # Simple check for version = "..."
    import tomllib
    data = tomllib.loads(content)
    version = data.get("project", {}).get("version")
    assert version is not None
    assert len(version.split(".")) >= 3

def test_package_check_script_contains_sha256sum():
    text = read("scripts/package-check.sh")
    assert "sha256sum -c" in text
    assert "tomllib" in text
    assert "RELEASE_MANIFEST.json" in text

def test_package_check_handles_manifest_verification():
    text = read("scripts/package-check.sh")
    assert "assert manifest.get('version') == " in text
    assert "zip" in text
    assert "tar.gz" in text
