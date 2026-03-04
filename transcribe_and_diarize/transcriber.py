from __future__ import annotations

class Transcriber:
    def __init__(self, model_size: str = "base", device: str = "auto", compute_type: str = "auto"):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type

    def transcribe(self, audio_path: str) -> dict:
        raise NotImplementedError("Transcriber.transcribe() — implemented in task-010")
