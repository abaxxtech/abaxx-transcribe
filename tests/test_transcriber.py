import pytest
from transcribe_and_diarize.transcriber import Transcriber


def test_transcriber_init():
    t = Transcriber(model_size="base")
    assert t.model_size == "base"
    assert t.device == "auto"


def test_transcriber_transcribe_not_implemented():
    t = Transcriber()
    with pytest.raises(NotImplementedError):
        t.transcribe("dummy.mp3")
