from .base import Skill

ShellSkill = Skill(
    name="shell",
    description="Run shell commands through the safety policy.",
    safety_notes=["blocks broad rm -rf", "blocks --no-verify", "blocks force push"],
)
