from __future__ import annotations


class Formatter:
    def format_json(self, segments: list, metadata: dict) -> str:
        raise NotImplementedError("Formatter.format_json() — implemented in task-013")

    def format_markdown(self, segments: list, metadata: dict) -> str:
        raise NotImplementedError("Formatter.format_markdown() — implemented in task-013")
