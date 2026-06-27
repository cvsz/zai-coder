from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import BinaryIO


@dataclass
class AudioStreamConfig:
    sample_rate: int = 16000
    channels: int = 1
    format: str = "wav"


class AudioCaptureInterface:
    def __init__(self, config: AudioStreamConfig | None = None):
        self.config = config or AudioStreamConfig()
        self.is_recording = False
        self._stream: BinaryIO | None = None
        self.logger = logging.getLogger(__name__)

    def start_recording(self) -> bool:
        if self.is_recording:
            self.logger.warning("Already recording.")
            return False
        
        self.logger.info(f"Started audio capture: {self.config}")
        self.is_recording = True
        # In a full implementation, we'd open a PyAudio or SoundDevice stream here
        return True

    def stop_recording(self) -> bytes:
        if not self.is_recording:
            return b""
        
        self.is_recording = False
        self.logger.info("Stopped audio capture.")
        # Return a mock empty wave header for now to satisfy safe abstraction
        return b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x00\x7d\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00"

    def status(self) -> str:
        if self.is_recording:
            return f"Recording ({self.config.sample_rate}Hz, {self.config.channels}ch)"
        return "Idle"
