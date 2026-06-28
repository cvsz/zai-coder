from __future__ import annotations

import logging
import queue
from dataclasses import dataclass
from typing import BinaryIO, Optional

try:
    import sounddevice as sd
    import soundfile as sf
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False

@dataclass
class AudioStreamConfig:
    sample_rate: int = 16000
    channels: int = 1
    format: str = "wav"

class AudioCaptureInterface:
    def __init__(self, config: AudioStreamConfig | None = None):
        self.config = config or AudioStreamConfig()
        self.is_recording = False
        self.logger = logging.getLogger(__name__)
        self.q = queue.Queue()
        self.stream = None
        self.recorded_data = []

    def _callback(self, indata, frames, time, status):
        if status:
            self.logger.warning(f"Audio status: {status}")
        self.q.put(indata.copy())

    def start_recording(self) -> bool:
        if self.is_recording:
            self.logger.warning("Already recording.")
            return False
        
        if not HAS_SOUNDDEVICE:
            self.logger.error("sounddevice is not installed. Cannot start recording.")
            return False

        self.logger.info(f"Started audio capture: {self.config}")
        self.is_recording = True
        self.recorded_data = []
        
        self.stream = sd.InputStream(
            samplerate=self.config.sample_rate,
            channels=self.config.channels,
            callback=self._callback
        )
        self.stream.start()
        return True

    def stop_recording(self) -> bytes:
        if not self.is_recording:
            return b""
        
        self.is_recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        self.logger.info("Stopped audio capture.")
        
        if not HAS_SOUNDDEVICE:
             return b""

        import io
        import numpy as np

        if self.q.empty():
            return b""

        while not self.q.empty():
            self.recorded_data.append(self.q.get())

        data = np.concatenate(self.recorded_data, axis=0)
        buffer = io.BytesIO()
        sf.write(buffer, data, self.config.sample_rate, format=self.config.format)
        return buffer.getvalue()

    def status(self) -> str:
        if self.is_recording:
            return f"Recording ({self.config.sample_rate}Hz, {self.config.channels}ch)"
        return "Idle"
