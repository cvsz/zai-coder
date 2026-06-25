from __future__ import annotations

from .base import Agent, AgentContext


class MediaAgent(Agent):
    name = "media"
    description = "Plans image, voice, music, animation, and video assets."

    def build_prompt(self, context: AgentContext) -> str:
        return f"""
Task: {context.task}

Create a media production plan with:
- image prompt
- voice script
- music mood
- animation storyboard
- video scenes
Prefer offline deterministic generation when possible.
""".strip()
