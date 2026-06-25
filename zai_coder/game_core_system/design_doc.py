"""Game design document generation helpers."""

from __future__ import annotations

from .models import GameProject


def validate_game_project(project: GameProject) -> list[str]:
    issues: list[str] = []
    if not project.slug:
        issues.append("missing slug")
    if not project.title:
        issues.append("missing title")
    if not project.genre:
        issues.append("missing genre")
    if not project.platform:
        issues.append("missing platform")
    scene_slugs = set()
    for scene in project.scenes:
        if scene.slug in scene_slugs:
            issues.append(f"duplicate scene slug: {scene.slug}")
        scene_slugs.add(scene.slug)
        if not scene.objective:
            issues.append(f"missing scene objective: {scene.slug}")
    return issues


def render_game_design_doc(project: GameProject) -> str:
    lines = [
        f"# {project.title}",
        "",
        "## Game Overview",
        f"- Slug: `{project.slug}`",
        f"- Genre: {project.genre}",
        f"- Platform: {project.platform}",
        "",
        "## Scenes",
    ]
    if not project.scenes:
        lines.append("- No scenes defined yet.")
    for scene in project.scenes:
        lines.extend([
            f"### {scene.title}",
            f"- Slug: `{scene.slug}`",
            f"- Objective: {scene.objective}",
            f"- Entities: {', '.join(scene.entities) if scene.entities else 'none'}",
            "",
        ])
    lines.append("## Assets")
    if not project.assets:
        lines.append("- No assets defined yet.")
    for asset in project.assets:
        lines.append(f"- `{asset.path}` ({asset.kind})")
    return "\n".join(lines).rstrip() + "\n"
