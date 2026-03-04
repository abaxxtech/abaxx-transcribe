# Transcribe and Diarize — Local Meeting Audio Tool

Status: In Development (Sprint 0: Scaffolding)
Owner: Ian Forester / Abaxx Technologies

## Overview
Local, privacy-first CLI tool: converts meeting audio to structured transcripts with speaker identification.
No subscriptions. No cloud uploads. Runs on your machine.

## Install
pip install git+https://github.com/abaxxtech/abaxx-transcribe.git

## Usage
transcribe-and-diarize meeting.mp3

## Architecture
Audio -> Faster-Whisper (transcribe) -> Pyannote (diarize) -> Merge -> JSON + Markdown

## Docs
See ARCHITECTURE.md, USAGE.md, CHANGELOG.md
