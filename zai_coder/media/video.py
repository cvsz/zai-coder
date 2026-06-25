from __future__ import annotations

import json
from .common import ensure_out, safe_text


def generate_video_storyboard(prompt: str, out: str = "out/video_storyboard.json") -> str:
    p = ensure_out(out)
    title = safe_text(prompt, 80)
    storyboard = {
        "title": title,
        "format": "storyboard-v1",
        "note": "Offline storyboard metadata. Use ffmpeg/renderer pipeline to turn scenes into video.",
        "scenes": [
            {"seconds": 0, "visual": "dark terminal boot", "voice": "ZAI Coder online.", "music": "soft pulse"},
            {"seconds": 4, "visual": "multi-agent graph appears", "voice": "Planner, coder, reviewer, and media agents coordinate safely.", "music": "rising synth"},
            {"seconds": 9, "visual": "code patch and validation checklist", "voice": "Exact paths. Minimal patches. Validation first.", "music": "focused beat"},
            {"seconds": 14, "visual": "ship screen with green checks", "voice": "Standalone local-first automation complete.", "music": "resolution"},
        ],
        "optional_ffmpeg_command": "ffmpeg -loop 1 -i image.svg -i music.wav -shortest out/demo.mp4",
    }
    p.write_text(json.dumps(storyboard, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(p)
