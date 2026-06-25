from __future__ import annotations

from .common import ensure_out, safe_text


def generate_animation_svg(prompt: str, out: str = "out/animation.svg", width: int = 1280, height: int = 720) -> str:
    p = ensure_out(out)
    title = safe_text(prompt, 90)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#020617"/>
  <text x="{width/2}" y="90" text-anchor="middle" font-family="monospace" font-size="38" fill="#e0f2fe">{title}</text>
  <circle r="32" fill="#22d3ee">
    <animateMotion dur="5s" repeatCount="indefinite" path="M120,360 C320,80 520,640 700,360 S1000,80 1160,360" />
  </circle>
  <g stroke="#94a3b8" stroke-width="3" fill="none" opacity="0.75">
    <path d="M120,360 C320,80 520,640 700,360 S1000,80 1160,360"/>
  </g>
  <text x="{width/2}" y="650" text-anchor="middle" font-family="monospace" font-size="24" fill="#94a3b8">planner → coder → reviewer → media → ship</text>
</svg>"""
    p.write_text(svg, encoding="utf-8")
    return str(p)
