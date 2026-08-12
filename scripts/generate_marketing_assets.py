"""Generate deterministic retro marketing art for the GitHub repository."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets"
FONT_PATH = "/System/Library/Fonts/Menlo.ttc"

INK = "#d7ded8"
MUTED = "#819188"
GREEN = "#80c98f"
GOLD = "#d5ad58"
RED = "#d46f6f"
SILVER = "#b9c8d1"
TERMINAL = "#0b1013"
PANEL = "#11191d"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size=size)


def centered(draw: ImageDraw.ImageDraw, text: str, y: int, face, fill: str, width: int) -> None:
    box = draw.textbbox((0, 0), text, font=face)
    draw.text(((width - (box[2] - box[0])) / 2, y), text, font=face, fill=fill)


def add_scanlines(image: Image.Image, spacing: int = 5) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    for y in range(0, image.height, spacing):
        draw.line((0, y, image.width, y), fill=(0, 0, 0, 24), width=1)


def star_points(cx: float, cy: float, outer: float, inner: float) -> list[tuple[float, float]]:
    points = []
    for index in range(16):
        angle = -math.pi / 2 + index * math.pi / 8
        radius = outer if index % 2 == 0 else inner
        points.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
    return points


def social_preview() -> Image.Image:
    width, height = 1280, 640
    image = Image.new("RGB", (width, height), "#080c0f")
    draw = ImageDraw.Draw(image, "RGBA")
    rng = random.Random(1937)

    for _ in range(220):
        x = rng.randrange(width)
        y = rng.randrange(height)
        alpha = rng.randrange(18, 65)
        draw.point((x, y), fill=(181, 199, 189, alpha))

    draw.rectangle((24, 24, width - 25, height - 25), outline=GOLD, width=3)
    draw.rectangle((36, 36, width - 37, height - 37), outline="#304239", width=1)
    draw.line((105, 103, width - 105, 103), fill="#42564b", width=2)
    draw.line((105, 500, width - 105, 500), fill="#42564b", width=2)

    draw.polygon(star_points(640, 156, 42, 14), fill=SILVER, outline="#f0f4f2")
    centered(draw, "A RETRO TERMINAL RPG FOR macOS", 60, font(23), GREEN, width)
    centered(draw, "ROADS", 220, font(92), INK, width)
    centered(draw, "BENEATH THE SHADOW", 326, font(54), GOLD, width)
    centered(draw, "CHOICES LEAVE MARKS.  THE ROAD REMEMBERS.", 422, font(24), SILVER, width)
    centered(draw, "PART I  //  45–70 MINUTES  //  PYTHON 3.10+", 538, font(21), MUTED, width)

    add_scanlines(image, 5)
    return image


SCENES: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "TITLE SCREEN",
        [
            ("                         .  *  .", SILVER),
            ("                         --|--", SILVER),
            ("     ____   ___    _    ____  ____", GOLD),
            ("    |  _ \\ / _ \\  / \\  |  _ \\/ ___|", GOLD),
            ("    | |_) | | | |/ _ \\ | | | \\___ " + "\\", GOLD),
            ("    |  _ <| |_| / ___ \\| |_| |___) |", GOLD),
            ("    |_| \\_\\\\___/_/   \\_\\____/|____/", GOLD),
            ("        BENEATH THE SHADOW", INK),
            ("", INK),
            ("    [1] Begin a new journey", GREEN),
            ("    [2] Load a saved journey", MUTED),
        ],
    ),
    (
        "CHAPTER I — BLOOD AT THE PRANCING PONY",
        [
            ("              ______/   \\______", GOLD),
            ("             /_______________  " + "\\", GOLD),
            ("             |  []   []   [] |  |P|", GOLD),
            ("          ___|_____|    |____|__|_|___", GOLD),
            ("              THE PRANCING PONY", INK),
            ("", INK),
            ("Rain hammers Bree. Inside, nobody sings.", SILVER),
            ("A wounded messenger presses a silver star into your hand.", INK),
            ("\"The star opens the road.\"", GREEN),
        ],
    ),
    (
        "ORCS AT THE DOOR",
        [
            ("    | WINDOW |      ----->      * CRASH *", RED),
            ("    |_\\/\\/__|", RED),
            ("             \\o/       \\o/       \\o/", GOLD),
            ("              |---      |---      |---", GOLD),
            ("             / \\       / \\       / " + "\\", GOLD),
            ("", INK),
            ("WHAT WILL YOU DO?", SILVER),
            ("[1] Draw your weapon and fight beside Mara", GREEN),
            ("[2] Hide the pendant and protect the letter", INK),
            ("[3] Search the fallen messenger for another clue", INK),
            ("[4] Escape through the inn's kitchen", INK),
        ],
    ),
    (
        "ENCOUNTER — MIDGEWATER AMBUSH",
        [
            ("YOU        HP 24/30   FOCUS 2/3", GREEN),
            ("MARA       HP 18/22   TRUST  +2", SILVER),
            ("", INK),
            ("TARGET     MARSH WARG   HP 15/21", RED),
            ("           [========----]", RED),
            ("", INK),
            ("[1] Attack          [4] Defend", INK),
            ("[2] Power attack    [5] Use item", GOLD),
            ("[3] Change target   [6] Command Mara", INK),
            ("", INK),
            ("Mara: \"Left flank. I will draw its teeth.\"", GREEN),
        ],
    ),
    (
        "THE THIRD STONE OPENS",
        [
            ("             [ 1 ]   [ 2 ]   [ 3 ]", GOLD),
            ("             |   |   |   |   | * |", GOLD),
            ("       ______|___|___|___|___|_|_|______", GOLD),
            ("                               /|\\", SILVER),
            ("                            --- * ---", SILVER),
            ("                               \\|/", SILVER),
            ("", INK),
            ("QUEST UPDATED: THE MISSING WATCHMAN", GREEN),
            ("Hope +1  |  Mara trust +1  |  New clue discovered", MUTED),
            ("A map beneath the dust shows a road that should not exist.", INK),
        ],
    ),
    (
        "THE BLACK RIDER",
        [
            ("                       .-^-.", SILVER),
            ("                      /_|||_\\", SILVER),
            ("                     /  |||  " + "\\", SILVER),
            ("                    /___|||___\\", SILVER),
            ("                       / " + "\\", SILVER),
            ("", INK),
            ("A horn answers from the eastern road.", RED),
            ("The rider turns its hood toward you — and speaks your name.", INK),
            ("", INK),
            ("END OF PART I", GOLD),
            ("Your choices carry into Part II: THE DEAD ROAD", GREEN),
        ],
    ),
]


def gameplay_frame(scene_index: int, reveal: float, cursor: bool) -> Image.Image:
    width, height = 960, 600
    image = Image.new("RGB", (width, height), "#070a0c")
    draw = ImageDraw.Draw(image, "RGBA")

    draw.rounded_rectangle((20, 20, width - 20, height - 20), radius=13, fill=PANEL, outline="#3d4c45", width=2)
    draw.rectangle((21, 21, width - 21, 61), fill="#182126")
    for x, color in ((42, "#d46f6f"), (66, GOLD), (90, GREEN)):
        draw.ellipse((x - 6, 35, x + 6, 47), fill=color)
    draw.text((124, 31), "Roads Beneath the Shadow — Terminal", font=font(17), fill=MUTED)

    title, lines = SCENES[scene_index]
    draw.text((48, 79), title, font=font(21), fill=GOLD)
    draw.line((48, 111, width - 48, 111), fill="#34463c", width=1)

    visible = max(1, math.ceil(len(lines) * reveal))
    y = 132
    face = font(17)
    for text, color in lines[:visible]:
        draw.text((53, y), text, font=face, fill=color)
        y += 36

    if cursor:
        draw.rectangle((53, 548, 65, 570), fill=GREEN)
    else:
        draw.text((53, 544), ">", font=face, fill=MUTED)

    draw.text((width - 120, 548), f"{scene_index + 1}/6", font=font(15), fill=MUTED)
    add_scanlines(image, 4)
    return image


def gameplay_gif() -> tuple[list[Image.Image], list[int]]:
    frames: list[Image.Image] = []
    durations: list[int] = []
    for index in range(len(SCENES)):
        for reveal, cursor, duration in ((0.58, False, 520), (1.0, True, 620), (1.0, False, 1500)):
            frame = gameplay_frame(index, reveal, cursor)
            frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=96))
            durations.append(duration)
    durations[-1] = 2600
    return frames, durations


def contact_sheet(frames: list[Image.Image]) -> Image.Image:
    selected = [frames[index * 3 + 2].convert("RGB").resize((480, 300)) for index in range(6)]
    sheet = Image.new("RGB", (1440, 600), "#070a0c")
    for index, frame in enumerate(selected):
        sheet.paste(frame, ((index % 3) * 480, (index // 3) * 300))
    return sheet


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    social_preview().save(OUTPUT_DIR / "social-preview.png", optimize=True)

    frames, durations = gameplay_gif()
    frames[0].save(
        OUTPUT_DIR / "gameplay-demo.gif",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    contact_sheet(frames).save("/private/tmp/roads-gameplay-contact-sheet.png", optimize=True)


if __name__ == "__main__":
    main()
