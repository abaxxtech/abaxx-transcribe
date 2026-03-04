from __future__ import annotations

class Diarizer:
    def __init__(self, device: str = "auto"):
        self.device = device

    def diarize(self, audio_path: str) -> dict:
        raise NotImplementedError("Diarizer.diarize() — implemented in task-011")
