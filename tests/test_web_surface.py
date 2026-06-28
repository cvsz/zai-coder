from __future__ import annotations

import json
import subprocess
from pathlib import Path


def test_web_surface_contract():
    root = Path(__file__).resolve().parents[1]
    web = root / "web"

    package = json.loads((web / "package.json").read_text(encoding="utf-8"))
    scripts = package["scripts"]

    assert package["name"] == "open-webui"
    assert package["private"] is True
    assert scripts["build"] == "npm run pyodide:fetch && vite build"
    assert scripts["check"] == "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json"
    assert scripts["test:frontend"] == "vitest --passWithNoTests"

    pyproject = (web / "pyproject.toml").read_text(encoding="utf-8")
    start_sh = (web / "backend" / "start.sh").read_text(encoding="utf-8")
    env_example = (web / ".env.example").read_text(encoding="utf-8")

    assert 'open-webui = "open_webui:app"' in pyproject
    assert 'requires-python = ">= 3.11, < 3.13.0a1"' in pyproject
    assert 'curl -sf "http://localhost:${PORT}/health"' in start_sh
    assert 'uvicorn open_webui.main:app' in start_sh
    assert "OLLAMA_BASE_URL" in env_example
    assert "CORS_ALLOW_ORIGIN" in env_example


def test_zai_web_migration_surface_is_owned_and_routable():
    root = Path(__file__).resolve().parents[1]
    web = root / "web"

    expected_paths = [
        web / "src" / "lib" / "zai" / "migration-manifest.json",
        web / "src" / "lib" / "zai" / "migration.ts",
        web / "src" / "lib" / "zai" / "openui.ts",
        web / "src" / "lib" / "components" / "zai" / "OpenUIRenderer.svelte",
        web / "src" / "routes" / "(app)" / "zai" / "+page.svelte",
    ]

    assert not (web / ".git").exists(), "web/ must be owned by the root repository, not nested git"
    for path in expected_paths:
        assert path.exists(), f"missing ZAI web migration file: {path}"

    sidebar = (web / "src" / "lib" / "components" / "layout" / "Sidebar.svelte").read_text(
        encoding="utf-8"
    )
    assert "ZAI Command Center" in sidebar
    assert "href: '/zai'" in sidebar


def test_zai_migration_manifest_tracks_real_files_without_deferred_language():
    root = Path(__file__).resolve().parents[1]
    manifest_path = root / "web" / "src" / "lib" / "zai" / "migration-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["releaseState"]["primarySurface"] == "/web"
    assert manifest["releaseState"]["localReleaseReady"] is True
    assert manifest["releaseState"]["externalGoLiveReady"] is True
    assert manifest["releaseState"]["coveragePercent"] >= 50
    assert any(epic["id"] == "zai-openui-runtime" for epic in manifest["epics"])
    assert any(gate["command"] == "make web-migration-report" for gate in manifest["qualityGates"])

    serialized = json.dumps(manifest).lower()
    forbidden = ["todo", "placeholder", "pseudocode", "implement later"]
    assert not any(term in serialized for term in forbidden)

    missing = []
    for epic in manifest["epics"]:
        for file_name in epic["files"]:
            path = root / file_name
            if not path.exists() and not any(
                (root / parent).exists() for parent in Path(file_name).parents if str(parent) != "."
            ):
                missing.append(file_name)

    assert missing == []


def test_web_migration_report_command_is_strict_json():
    result = subprocess.run(
        [
            "python3",
            "scripts/repo/web-migration-report.py",
            "--format",
            "json",
            "--strict",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["hygiene"]["nestedGitMetadata"] is False
    assert payload["hygiene"]["missingManifestPaths"] == []
    assert payload["inventory"]["routes"] >= 1
