import os
from pathlib import Path

SUPPORTED_FORMATS = ["mp3", "wav", "m4a", "flac", "ogg", "mp4", "webm"]
MODEL_SIZES = ["tiny", "base", "small", "medium", "large"]
OUTPUT_FORMATS = ["json", "markdown", "both"]

DEFAULTS = {
    "model_size": os.environ.get("TRANSCRIBE_MODEL_SIZE", "base"),
    "output_format": os.environ.get("TRANSCRIBE_OUTPUT_FORMAT", "both"),
    "output_dir": os.environ.get("TRANSCRIBE_OUTPUT_DIR", "."),
    "device": os.environ.get("TRANSCRIBE_DEVICE", "auto"),
    "compute_type": os.environ.get("TRANSCRIBE_COMPUTE_TYPE", "auto"),
    "verbose": os.environ.get("TRANSCRIBE_VERBOSE", "false").lower() == "true",
}

HF_TOKEN_PATH = Path.home() / ".huggingface" / "token"
HF_TOKEN_ENV = "HUGGING_FACE_HUB_TOKEN"
HF_CACHE_DIR = Path(os.environ.get("HF_HOME", str(Path.home() / ".cache" / "huggingface")))
LOG_DIR = Path.home() / ".transcribe-and-diarize"
LOG_FILE = LOG_DIR / "app.log"
DIARIZATION_MODEL = "pyannote/speaker-diarization-community-1"
MIN_OVERLAP_DURATION = 0.1
