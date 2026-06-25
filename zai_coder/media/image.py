from __future__ import annotations

from .common import ensure_out, safe_text


def generate_svg_image(prompt: str, out: str = "out/image.svg", width: int = 1024, height: int = 1024) -> str:
    p = ensure_out(out)
    title = safe_text(prompt, 80)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="45%" stop-color="#1d4ed8"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="100%" height="100%" fill="url(#g)"/>
  <circle cx="512" cy="420" r="180" fill="none" stroke="#a7f3d0" stroke-width="10" filter="url(#glow)"/>
  <path d="M320 650 C420 540 600 540 704 650" fill="none" stroke="#ffffff" stroke-width="16" stroke-linecap="round"/>
  <text x="512" y="150" text-anchor="middle" font-family="monospace" font-size="46" fill="#fff">ZAI CODER</text>
  <text x="512" y="870" text-anchor="middle" font-family="monospace" font-size="30" fill="#e0f2fe">{title}</text>
</svg>"""
    p.write_text(svg, encoding="utf-8")
    return str(p)
