"""Command-line entry point."""

from __future__ import annotations

import argparse

from .app import Game
from .audio import SoundPlayer
from .profile import ProfileManager
from .settings import SettingsManager
from .ui import InputClosed, TerminalUI


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Play The Lord of the Rings: Roads Beneath the Shadow")
    parser.add_argument("--no-color", action="store_true", help="disable ANSI terminal colors")
    parser.add_argument("--sound", action="store_true", help="enable the original retro sound cues")
    parser.add_argument("--fast", action="store_true", help="remove dramatic pauses (useful for testing)")
    parser.add_argument(
        "--text-speed",
        choices=("slow", "normal", "fast", "instant"),
        help="override the saved narration speed for this launch",
    )
    parser.add_argument("--reduced-motion", action="store_true", help="disable terminal animation")
    parser.add_argument(
        "--screen-reader",
        action="store_true",
        help="replace decorative art with concise scene descriptions",
    )
    parser.add_argument(
        "--difficulty",
        choices=("story", "ranger", "shadow"),
        help="choose story, intended Ranger, or hard Shadow combat",
    )
    parser.add_argument("--check-install", action="store_true", help=argparse.SUPPRESS)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.check_install:
        missing = SoundPlayer.missing_cues()
        if missing:
            raise SystemExit(f"Installation check failed; missing sound cues: {', '.join(missing)}")
        print(f"Installation verified: {len(SoundPlayer.CUES)} sound cues are available.")
        return
    settings_manager = SettingsManager()
    settings = settings_manager.load()
    if args.no_color:
        settings.color_mode = "off"
    if args.sound:
        settings.sound = True
    if args.text_speed:
        settings.text_speed = args.text_speed
    if args.reduced_motion:
        settings.reduced_motion = True
    if args.screen_reader:
        settings.screen_reader = True
    if args.difficulty:
        settings.difficulty = args.difficulty

    color = {"auto": None, "on": True, "off": False}[settings.color_mode]
    sound_player = SoundPlayer()
    ui = TerminalUI(
        color=color,
        sound=settings.sound,
        fast=args.fast,
        text_speed=settings.text_speed,
        reduced_motion=settings.reduced_motion,
        screen_reader=settings.screen_reader,
        sound_fn=sound_player.play,
    )
    try:
        Game(
            ui,
            settings_manager=settings_manager,
            user_settings=settings,
            profile=ProfileManager(),
        ).run()
    except (KeyboardInterrupt, InputClosed):
        ui.write("\nYour journey has paused. Unsaved progress was not kept.")


if __name__ == "__main__":
    main()
