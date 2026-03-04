__version__ = "0.1.0"
__author__ = "Abaxx Technologies"
__email__ = "dev@abaxx.tech"

from transcribe_and_diarize.exceptions import (
    TranscribeError,
    AudioFileNotFoundError,
    UnsupportedAudioFormatError,
    AuthenticationError,
    DiskSpaceError,
)

__all__ = [
    "__version__",
    "TranscribeError",
    "AudioFileNotFoundError",
    "UnsupportedAudioFormatError",
    "AuthenticationError",
    "DiskSpaceError",
]
