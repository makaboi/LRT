"""Terminal rendering, prompts, colors, and small sound cues."""

from __future__ import annotations

import os
import shutil
import sys
import textwrap
import time
from collections.abc import Callable, Sequence


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    SILVER = "\033[38;5;250m"


class InputClosed(Exception):
    """Raised when the terminal input stream is closed."""


class TerminalUI:
    def __init__(
        self,
        *,
        color: bool | None = None,
        sound: bool = False,
        fast: bool = False,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[[str], None] = print,
    ) -> None:
        self.color = self._supports_color() if color is None else color
        self.sound_enabled = sound
        self.fast = fast
        self.input_fn = input_fn
        self.output_fn = output_fn

    @staticmethod
    def _supports_color() -> bool:
        return sys.stdout.isatty() and os.environ.get("TERM", "dumb") != "dumb" and "NO_COLOR" not in os.environ

    @property
    def width(self) -> int:
        return max(60, min(92, shutil.get_terminal_size((78, 24)).columns))

    def style(self, text: str, *codes: str) -> str:
        if not self.color:
            return text
        return "".join(codes) + text + Color.RESET

    def clear(self) -> None:
        if not self.fast and sys.stdout.isatty():
            self.output_fn("\033[2J\033[H")

    def write(self, text: str = "", *, color: str | None = None, bold: bool = False) -> None:
        codes: list[str] = []
        if color:
            codes.append(color)
        if bold:
            codes.append(Color.BOLD)
        self.output_fn(self.style(text, *codes))

    def rule(self, char: str = "=") -> None:
        self.write(char * min(72, self.width), color=Color.DIM)

    def title(self, text: str) -> None:
        self.rule()
        self.write(text.center(min(72, self.width)), color=Color.YELLOW, bold=True)
        self.rule()

    def art(self, text: str, color: str = Color.SILVER) -> None:
        for line in text.strip("\n").splitlines():
            self.write(line, color=color)

    def narrate(self, text: str, *, color: str | None = None) -> None:
        paragraphs = text.strip().split("\n")
        for paragraph in paragraphs:
            if not paragraph.strip():
                self.write()
                continue
            for line in textwrap.wrap(paragraph, width=min(78, self.width)):
                self.write(line, color=color)
            if not self.fast:
                time.sleep(0.12)

    def prompt(self, label: str = "> ") -> str:
        try:
            return self.input_fn(self.style(label, Color.CYAN, Color.BOLD)).strip()
        except EOFError:
            raise InputClosed from None

    def choose(self, title: str, options: Sequence[str], *, allow_back: bool = False) -> int | None:
        while True:
            self.write()
            self.write(title, color=Color.YELLOW, bold=True)
            for index, option in enumerate(options, 1):
                self.write(f"[{index}] {option}")
            if allow_back:
                self.write("[B] Back", color=Color.DIM)
            answer = self.prompt("Enter your choice: ").lower()
            if allow_back and answer in {"b", "back", "q"}:
                return None
            if answer.isdigit() and 1 <= int(answer) <= len(options):
                return int(answer)
            self.write("Choose one of the listed options.", color=Color.RED)

    def pause(self, message: str = "Press Return to continue...") -> None:
        if not self.fast:
            self.prompt(message)

    def sound(self, cue: str = "notice") -> None:
        if not self.sound_enabled:
            return
        patterns = {"danger": 2, "victory": 3, "notice": 1}
        self.output_fn("\a" * patterns.get(cue, 1))

    def meter(self, label: str, value: int, maximum: int, *, color: str = Color.GREEN) -> str:
        maximum = max(1, maximum)
        filled = max(0, min(16, round((value / maximum) * 16)))
        bar = "#" * filled + "-" * (16 - filled)
        return self.style(f"{label:<7} [{bar}] {value}/{maximum}", color)
