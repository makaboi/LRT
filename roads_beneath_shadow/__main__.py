"""Command-line entry point."""

from __future__ import annotations

import argparse

from .app import Game
from .ui import InputClosed, TerminalUI


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Play The Lord of the Rings: Roads Beneath the Shadow")
    parser.add_argument("--no-color", action="store_true", help="disable ANSI terminal colors")
    parser.add_argument("--sound", action="store_true", help="enable optional terminal bell cues")
    parser.add_argument("--fast", action="store_true", help="remove dramatic pauses (useful for testing)")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    ui = TerminalUI(color=False if args.no_color else None, sound=args.sound, fast=args.fast)
    try:
        Game(ui).run()
    except (KeyboardInterrupt, InputClosed):
        ui.write("\nYour journey has paused. Unsaved progress was not kept.")


if __name__ == "__main__":
    main()
