from __future__ import annotations

import math
import wave
import struct

from .common import ensure_out


def generate_music_wav(prompt: str, out: str = "out/music.wav", seconds: float = 6.0, sample_rate: int = 44100) -> str:
    p = ensure_out(out)
    notes = [261.63, 329.63, 392.00, 523.25]
    mood_shift = sum(ord(c) for c in prompt) % len(notes)
    frames = int(seconds * sample_rate)
    with wave.open(str(p), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for i in range(frames):
            t = i / sample_rate
            note = notes[(int(t * 2) + mood_shift) % len(notes)]
            env = min(1.0, t * 5) * min(1.0, max(0.0, seconds - t) * 5)
            sample = 0.25 * env * math.sin(2 * math.pi * note * t)
            sample += 0.10 * env * math.sin(2 * math.pi * note * 2 * t)
            wav.writeframes(struct.pack("<h", int(max(-1, min(1, sample)) * 32767)))
    return str(p)
