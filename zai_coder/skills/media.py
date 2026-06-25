from .base import Skill

MediaSkill = Skill(
    name="media",
    description="Generate offline SVG, WAV, animation, and video storyboard artifacts.",
    safety_notes=["writes only requested output paths", "no network required"],
)
