"""Skill pack builder."""

from __future__ import annotations

import json
from pathlib import Path

from .catalog import find_skill


def build_skill_pack(skill_ids: list[str], root: str | Path = ".", out: str = "marketplace/skills/skill-pack.json") -> str:
    root = Path(root)
    skills = [find_skill(skill_id).to_dict() for skill_id in skill_ids]
    payload = {"kind": "zai-skill-pack", "version": "1.0", "skills": skills, "safe_mode": True}
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return str(path)


def skill_pack_plan(skill_ids: list[str]) -> dict:
    skills = [find_skill(skill_id).to_dict() for skill_id in skill_ids]
    return {"dry_run": True, "kind": "zai-skill-pack", "skills": skills, "safe_mode": True}
