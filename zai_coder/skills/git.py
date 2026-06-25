from .base import Skill

GitSkill = Skill(
    name="git",
    description="Inspect Git state and stage exact paths only.",
    safety_notes=["blocks git add .", "blocks git add -A", "blocks force push"],
)
