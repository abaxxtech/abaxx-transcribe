class TranscribeError(Exception):
    pass

class AudioFileNotFoundError(TranscribeError):
    def __init__(self, path: str):
        self.path = path
        super().__init__(f"Audio file not found: {path}")

class UnsupportedAudioFormatError(TranscribeError):
    SUPPORTED = ["mp3", "wav", "m4a", "flac", "ogg", "mp4", "webm"]
    def __init__(self, path: str):
        self.path = path
        ext = path.rsplit(".", 1)[-1].lower() if "." in path else "unknown"
        super().__init__(f"Unsupported audio format: .{ext}. Supported: {', '.join('.' + e for e in self.SUPPORTED)}")

class AuthenticationError(TranscribeError):
    def __init__(self, message: str = "HuggingFace authentication failed. Run setup wizard."):
        super().__init__(message)

class DiskSpaceError(TranscribeError):
    def __init__(self, required_gb: float):
        super().__init__(f"Insufficient disk space. Need ~{required_gb:.1f}GB free for models.")

class ModelDownloadError(TranscribeError):
    def __init__(self, model_name: str):
        super().__init__(f"Cannot download model '{model_name}'. Check internet connection.")
