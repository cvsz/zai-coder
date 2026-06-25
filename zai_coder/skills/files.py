from .base import Skill

FileSkill = Skill(
    name="files",
    description="Read and write workspace files with protected-path checks.",
    safety_notes=["blocks secrets", "blocks generated paths", "blocks apps/zlms/** by default"],
)
