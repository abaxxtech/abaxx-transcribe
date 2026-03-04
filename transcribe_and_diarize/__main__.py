"""CLI entry point for transcribe-and-diarize."""

import sys
import time
from pathlib import Path

import click

from transcribe_and_diarize import __version__
from transcribe_and_diarize.config import DEFAULTS, MODEL_SIZES, OUTPUT_FORMATS, SUPPORTED_FORMATS
from transcribe_and_diarize.exceptions import TranscribeError
from transcribe_and_diarize.logger import setup_logger


def validate_audio_file(ctx, param, value):
    """Validate audio file exists and has a supported extension."""
    path = Path(value)
    if not path.exists():
        raise click.BadParameter(f"File not found: {value}")
    if not path.is_file():
        raise click.BadParameter(f"Not a file: {value}")
    ext = path.suffix.lstrip(".").lower()
    if ext not in SUPPORTED_FORMATS:
        supported_str = ", ".join(f".{f}" for f in SUPPORTED_FORMATS)
        raise click.BadParameter(f"Unsupported format: .{ext}. Supported formats: {supported_str}")
    return value


@click.command()
@click.argument("audio_file", callback=validate_audio_file)
@click.option(
    "-o",
    "--output-dir",
    default=DEFAULTS["output_dir"],
    show_default=True,
    help="Output directory for transcript files.",
    type=click.Path(file_okay=False, writable=True),
)
@click.option(
    "--model",
    default=DEFAULTS["model_size"],
    show_default=True,
    type=click.Choice(MODEL_SIZES),
    help="Whisper model size (trades speed for accuracy).",
)
@click.option(
    "--format",
    "output_format",
    default=DEFAULTS["output_format"],
    show_default=True,
    type=click.Choice(OUTPUT_FORMATS),
    help="Output format.",
)
@click.option(
    "--speakers",
    default=None,
    help='Comma-separated speaker names in order of appearance. E.g. "Ian,Alice,Bob"',
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=DEFAULTS["verbose"],
    help="Print detailed progress information.",
)
@click.version_option(version=__version__, prog_name="transcribe-and-diarize")
def cli(audio_file, output_dir, model, output_format, speakers, verbose):
    """Transcribe and diarize an audio file.

    Converts AUDIO_FILE to a speaker-labeled transcript in JSON and/or Markdown.
    Models are downloaded automatically on first run (~530MB for default setup).

    Examples:

      transcribe-and-diarize meeting.mp3

      transcribe-and-diarize meeting.mp3 -o ~/transcripts/ --model small

      transcribe-and-diarize meeting.mp3 --speakers "Ian,Alice,Bob" -v
    """
    logger = setup_logger(verbose=verbose)
    start_time = time.perf_counter()

    audio_path = Path(audio_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    speaker_names = None
    if speakers:
        speaker_names = [s.strip() for s in speakers.split(",") if s.strip()]

    stem = audio_path.stem

    if verbose:
        click.echo(f"transcribe-and-diarize v{__version__}")
        size_mb = audio_path.stat().st_size / 1024 / 1024
        click.echo(f"Audio: {audio_path.name} ({size_mb:.1f} MB)")
        click.echo(f"Model: {model}")
        click.echo(f"Output: {output_path}/")
        click.echo("")

    try:
        logger.info("[1/4] Transcribing audio...")
        from transcribe_and_diarize.transcriber import Transcriber

        transcriber = Transcriber(model_size=model)
        transcript_data = transcriber.transcribe(str(audio_path))

        if verbose:
            lang = transcript_data.get("language", "unknown")
            duration = transcript_data.get("duration", 0)
            mins, secs = divmod(int(duration), 60)
            nseg = len(transcript_data.get("segments", []))
            logger.info(f"  Language: {lang}")
            logger.info(f"  Duration: {mins}:{secs:02d}")
            logger.info(f"  Segments: {nseg}")

        logger.info("[2/4] Diarizing speakers...")
        from transcribe_and_diarize.diarizer import Diarizer

        diarization_data = Diarizer().diarize(str(audio_path))

        if verbose:
            n_speakers = len(set(s["speaker"] for s in diarization_data.get("speakers", [])))
            logger.info(f"  Speakers detected: {n_speakers}")

        logger.info("[3/4] Merging transcript + speakers...")
        from transcribe_and_diarize.merger import Merger

        segments = Merger().merge(transcript_data, diarization_data)

        if speaker_names:
            unique_speakers = sorted(set(s["speaker"] for s in segments))
            name_map = {
                spk: speaker_names[i]
                for i, spk in enumerate(unique_speakers)
                if i < len(speaker_names)
            }
            for seg in segments:
                seg["speaker"] = name_map.get(seg["speaker"], seg["speaker"])

        if verbose:
            logger.info(f"  Segments merged: {len(segments)}")

        logger.info("[4/4] Formatting output...")
        from transcribe_and_diarize.formatter import Formatter

        fmt = Formatter()
        metadata = {
            "audio_file": audio_path.name,
            "language": transcript_data.get("language", "unknown"),
            "duration_seconds": transcript_data.get("duration", 0),
            "speakers_identified": len(set(s["speaker"] for s in segments)),
            "segments_count": len(segments),
        }

        output_files = []

        if output_format in ("json", "both"):
            json_path = output_path / f"{stem}_transcript.json"
            json_path.write_text(fmt.format_json(segments, metadata), encoding="utf-8")
            output_files.append(json_path)
            if verbose:
                kb = json_path.stat().st_size / 1024
                logger.info(f"  JSON: {json_path} ({kb:.0f} KB)")

        if output_format in ("markdown", "both"):
            md_path = output_path / f"{stem}_transcript.md"
            md_path.write_text(fmt.format_markdown(segments, metadata), encoding="utf-8")
            output_files.append(md_path)
            if verbose:
                kb = md_path.stat().st_size / 1024
                logger.info(f"  Markdown: {md_path} ({kb:.0f} KB)")

        elapsed = time.perf_counter() - start_time
        mins_e, secs_e = divmod(int(elapsed), 60)
        click.echo(f"Done in {mins_e}m {secs_e:02d}s")
        for f in output_files:
            click.echo(f"  -> {f}")

        sys.exit(0)

    except TranscribeError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("Cancelled.", err=True)
        sys.exit(130)
    except Exception as e:
        if verbose:
            import traceback

            traceback.print_exc()
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
