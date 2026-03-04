import pytest
from transcribe_and_diarize.diarizer import Diarizer


def test_diarizer_init():
    d = Diarizer()
    assert d.device == "auto"


def test_diarizer_diarize_not_implemented():
    d = Diarizer()
    with pytest.raises(NotImplementedError):
        d.diarize("dummy.mp3")
