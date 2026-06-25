"""Export adapter foundation.

Adapters return a plan or files dictionary. They do not call external services.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ExportPlan:
    adapter: str
    dry_run: bool = True
    files: Dict[str, str] = field(default_factory=dict)
    commands: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "adapter": self.adapter,
            "dry_run": self.dry_run,
            "files": dict(self.files),
            "commands": list(self.commands),
            "warnings": list(self.warnings),
        }


def phaser_export_plan(game_slug: str, title: str) -> ExportPlan:
    slug = game_slug or "game"
    return ExportPlan(
        adapter="phaser",
        files={
            f"{slug}/package.json": json.dumps({
                "name": slug,
                "private": True,
                "scripts": {"dev": "vite --host 127.0.0.1", "build": "vite build"},
                "dependencies": {"@vitejs/plugin-react": "latest", "vite": "latest", "typescript": "latest", "phaser": "latest"},
            }, indent=2),
            f"{slug}/src/main.ts": f"// {title}\n// Phaser bootstrap placeholder.\n",
        },
        commands=["npm install", "npm run dev"],
    )


def godot_export_plan(game_slug: str, title: str) -> ExportPlan:
    slug = game_slug or "game"
    return ExportPlan(
        adapter="godot",
        files={
            f"{slug}/project.godot": f"; Engine configuration file\nconfig/name=\"{title}\"\n",
            f"{slug}/scenes/Main.tscn": "[gd_scene format=3]\n",
        },
        warnings=["Godot export is a scaffold only; open with Godot editor to complete setup."],
    )


def document_export_plan(title: str, markdown: str) -> ExportPlan:
    safe_title = (title or "document").replace(" ", "-").lower()
    return ExportPlan(
        adapter="document",
        files={
            f"docs/{safe_title}.md": markdown,
            f"docs/{safe_title}.html": "<!doctype html><meta charset='utf-8'><pre>" + markdown.replace("&", "&amp;").replace("<", "&lt;") + "</pre>\n",
        },
        warnings=["DOCX/PDF adapters are placeholders in this package."],
    )


def movie_export_plan(title: str, treatment: str) -> ExportPlan:
    safe_title = (title or "movie").replace(" ", "-").lower()
    return ExportPlan(
        adapter="movie",
        files={
            f"movie/{safe_title}-treatment.md": treatment,
            f"movie/{safe_title}-storyboard.json": json.dumps({"title": title, "shots": []}, indent=2),
            f"movie/{safe_title}.srt": "1\n00:00:00,000 --> 00:00:03,000\nOpening title.\n",
        },
        commands=["ffmpeg -version", "npm create vite@latest remotion-placeholder"],
        warnings=["FFmpeg/Remotion commands are informational and dry-run only."],
    )
