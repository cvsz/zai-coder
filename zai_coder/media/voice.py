from __future__ import annotations

import math
import wave
import struct

from .common import ensure_out


def generate_voice_wav(text: str, out: str = "out/voice.wav", sample_rate: int = 22050) -> str:
    """Generate a small robot-style speech placeholder WAV.

    This is not natural TTS. It is an offline fallback artifact that encodes text rhythm as tones.
    """
    p = ensure_out(out)
    cleaned = text.strip() or "ZAI Coder"
    seconds_per_char = 0.045
    silence = 0.012
    frames: list[int] = []
    for ch in cleaned[:240]:
        freq = 360 + (ord(ch) % 32) * 16
        n = int(seconds_per_char * sample_rate)
        for i in range(n):
            t = i / sample_rate
            env = min(1.0, i / max(1, n * 0.15)) * min(1.0, (n - i) / max(1, n * 0.15))
            val = 0.22 * env * math.sin(2 * math.pi * freq * t)
            frames.append(int(val * 32767))
        frames.extend([0] * int(silence * sample_rate))
    with wave.open(str(p), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for s in frames:
            wav.writeframes(struct.pack("<h", s))
    return str(p)
