"""Screenplay outline tools.

This module is for original user-owned material. It does not include any
copyrighted scripts or franchise material.
"""

from __future__ import annotations

from .models import MovieProject


def validate_movie_project(project: MovieProject) -> list[str]:
    issues: list[str] = []
    if not project.title:
        issues.append("missing title")
    if not project.logline:
        issues.append("missing logline")
    if not project.genre:
        issues.append("missing genre")
    if project.rating not in {"general", "teen", "mature"}:
        issues.append(f"invalid rating: {project.rating}")
    scene_slugs = set()
    for scene in project.scenes:
        if scene.slug in scene_slugs:
            issues.append(f"duplicate scene slug: {scene.slug}")
        scene_slugs.add(scene.slug)
        if not scene.summary:
            issues.append(f"missing scene summary: {scene.slug}")
    return issues


def render_treatment(project: MovieProject) -> str:
    lines = [
        f"# {project.title}",
        "",
        f"Genre: {project.genre}",
        f"Rating: {project.rating}",
        "",
        "## Logline",
        project.logline,
        "",
        "## Characters",
    ]
    if not project.characters:
        lines.append("- No characters defined.")
    for character in project.characters:
        lines.append(f"- **{character.name}** ({character.role}): {character.motivation}")
    lines.extend(["", "## Scene Outline"])
    if not project.scenes:
        lines.append("- No scenes defined.")
    for scene in project.scenes:
        lines.append(f"- `{scene.slug}` — {scene.location}: {scene.summary}")
    return "\n".join(lines).rstrip() + "\n"
