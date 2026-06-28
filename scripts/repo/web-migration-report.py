#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


IGNORED_PARTS = {
    ".git",
    ".svelte-kit",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "__pycache__",
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _tracked_files(root: Path, base: Path) -> list[str]:
    if not base.exists():
        return []

    files: list[str] = []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        if IGNORED_PARTS.intersection(path.relative_to(base).parts):
            continue
        files.append(path.relative_to(root).as_posix())
    return sorted(files)


def _top_level_python_domains(root: Path) -> list[str]:
    package_root = root / "zai_coder"
    if not package_root.exists():
        return []

    return sorted(
        path.relative_to(root).as_posix()
        for path in package_root.iterdir()
        if path.is_dir() and not path.name.startswith("__")
    )


def _path_exists(root: Path, path_name: str) -> bool:
    path = root / path_name
    if path.exists():
        return True
    return any((root / parent).exists() for parent in Path(path_name).parents if str(parent) != ".")


def build_report(root: Path) -> dict[str, Any]:
    manifest_path = root / "web" / "src" / "lib" / "zai" / "migration-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    web = root / "web"
    web_files = _tracked_files(root, web)

    route_files = [path for path in web_files if path.startswith("web/src/routes/")]
    component_files = [path for path in web_files if path.startswith("web/src/lib/components/")]
    api_files = [path for path in web_files if path.startswith("web/src/lib/apis/")]
    backend_router_files = [
        path for path in web_files if path.startswith("web/backend/open_webui/routers/")
    ]
    manifest_paths = sorted(
        {
            file_name
            for epic in manifest["epics"]
            for file_name in epic.get("files", [])
            + [
                feature_file
                for feature in epic.get("features", [])
                for feature_file in feature.get("files", [])
            ]
        }
    )
    missing_manifest_paths = [
        path_name for path_name in manifest_paths if not _path_exists(root, path_name)
    ]
    nested_git = (web / ".git").exists()

    status_counts: dict[str, int] = {}
    for epic in manifest["epics"]:
        status_counts[epic["status"]] = status_counts.get(epic["status"], 0) + 1

    critical_gaps = [
        gap for gap in manifest["openGaps"] if gap["status"] == "blocked" or gap["severity"] == "critical"
    ]

    ok = not nested_git and not missing_manifest_paths

    return {
        "ok": ok,
        "manifest": {
            "version": manifest["version"],
            "updatedAt": manifest["updatedAt"],
            "coveragePercent": manifest["releaseState"]["coveragePercent"],
            "externalGoLiveReady": manifest["releaseState"]["externalGoLiveReady"],
        },
        "inventory": {
            "webFiles": len(web_files),
            "routes": len(route_files),
            "components": len(component_files),
            "apiModules": len(api_files),
            "backendRouters": len(backend_router_files),
            "pythonDomains": len(_top_level_python_domains(root)),
        },
        "statusCounts": status_counts,
        "qualityGates": manifest["qualityGates"],
        "criticalGaps": critical_gaps,
        "hygiene": {
            "nestedGitMetadata": nested_git,
            "missingManifestPaths": missing_manifest_paths,
        },
    }


def _print_markdown(report: dict[str, Any]) -> None:
    print("# Web Migration Report")
    print()
    print(f"- OK: `{str(report['ok']).lower()}`")
    print(f"- Manifest version: `{report['manifest']['version']}`")
    print(f"- Updated: `{report['manifest']['updatedAt']}`")
    print(f"- Coverage: `{report['manifest']['coveragePercent']}%`")
    print(f"- External go-live ready: `{str(report['manifest']['externalGoLiveReady']).lower()}`")
    print()
    print("## Inventory")
    print()
    for key, value in report["inventory"].items():
        print(f"- {key}: `{value}`")
    print()
    print("## Epic Status")
    print()
    for key, value in sorted(report["statusCounts"].items()):
        print(f"- {key}: `{value}`")
    print()
    print("## Quality Gates")
    print()
    for gate in report["qualityGates"]:
        print(f"- `{gate['command']}` - {gate['name']} ({gate['scope']})")
    print()
    print("## Critical Gaps")
    print()
    for gap in report["criticalGaps"]:
        print(f"- **{gap['area']}** [{gap['target']}]: {gap['remediation']}")
    print()
    print("## Hygiene")
    print()
    print(f"- Nested git metadata: `{str(report['hygiene']['nestedGitMetadata']).lower()}`")
    if report["hygiene"]["missingManifestPaths"]:
        print("- Missing manifest paths:")
        for path in report["hygiene"]["missingManifestPaths"]:
            print(f"  - `{path}`")
    else:
        print("- Missing manifest paths: `0`")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the ZAI web migration report.")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on hygiene failures.")
    args = parser.parse_args(argv)

    report = build_report(_repo_root())

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        _print_markdown(report)

    return 1 if args.strict and not report["ok"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
