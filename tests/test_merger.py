import pytest
from transcribe_and_diarize.merger import Merger


def test_merger_init():
    m = Merger()
    assert m is not None


def test_merger_merge_not_implemented():
    m = Merger()
    with pytest.raises(NotImplementedError):
        m.merge({}, {})
