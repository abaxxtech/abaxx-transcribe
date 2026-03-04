import pytest
from transcribe_and_diarize.formatter import Formatter

def test_formatter_init():
    f = Formatter()
    assert f is not None

def test_formatter_json_not_implemented():
    f = Formatter()
    with pytest.raises(NotImplementedError):
        f.format_json([], {})

def test_formatter_markdown_not_implemented():
    f = Formatter()
    with pytest.raises(NotImplementedError):
        f.format_markdown([], {})
