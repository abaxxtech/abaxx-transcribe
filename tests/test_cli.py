"""Tests for CLI argument parsing. Uses click's CliRunner (no real audio needed)."""

import pytest
from click.testing import CliRunner

from transcribe_and_diarize import __version__
from transcribe_and_diarize.__main__ import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_version(runner):
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "--model" in result.output
    assert "--format" in result.output
    assert "--speakers" in result.output
    assert "--verbose" in result.output or "-v" in result.output
    assert "--output-dir" in result.output or "-o" in result.output


def test_missing_audio_file(runner):
    result = runner.invoke(cli, ["nonexistent_file.mp3"])
    assert result.exit_code != 0


def test_unsupported_format(runner, tmp_path):
    bad_file = tmp_path / "meeting.xyz"
    bad_file.write_text("fake audio content")
    result = runner.invoke(cli, [str(bad_file)])
    assert result.exit_code != 0
    output = result.output.lower()
    assert "unsupported" in output or "xyz" in output or "format" in output


def test_valid_mp3_reaches_pipeline(runner, tmp_path):
    # .mp3 passes validation, then fails at Transcriber stub (NotImplementedError)
    # That's expected: exit_code should be 1 (error), NOT 2 (click arg error)
    fake_mp3 = tmp_path / "meeting.mp3"
    fake_mp3.write_bytes(b"\xff\xfb" + b"\x00" * 100)
    out_dir = tmp_path / "output"
    result = runner.invoke(cli, [str(fake_mp3), "-o", str(out_dir)])
    assert result.exit_code != 2, f"Got click arg error (exit 2). Output: {result.output}"


def test_invalid_model_choice(runner, tmp_path):
    fake_mp3 = tmp_path / "test.mp3"
    fake_mp3.write_bytes(b"\xff\xfb" + b"\x00" * 100)
    result = runner.invoke(cli, [str(fake_mp3), "--model", "xlarge"])
    assert result.exit_code != 0


def test_invalid_format_choice(runner, tmp_path):
    fake_mp3 = tmp_path / "test.mp3"
    fake_mp3.write_bytes(b"\xff\xfb" + b"\x00" * 100)
    result = runner.invoke(cli, [str(fake_mp3), "--format", "xml"])
    assert result.exit_code != 0


def test_verbose_flag_accepted(runner, tmp_path):
    fake_mp3 = tmp_path / "test.mp3"
    fake_mp3.write_bytes(b"\xff\xfb" + b"\x00" * 100)
    # -v flag should be accepted; pipeline fails at stub (exit 1), NOT arg error (exit 2)
    result = runner.invoke(cli, [str(fake_mp3), "-v"])
    assert result.exit_code != 2, f"Got click arg error. Output: {result.output}"
