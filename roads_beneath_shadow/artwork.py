"""Readable retro dark-fantasy artwork for Part I.

The drawings favour simple outlined objects, visible anatomy, and familiar
props over abstract silhouettes.  They stay within a 64-column stage so every
subject remains legible in a standard macOS Terminal window.
"""

import textwrap


def _named_ascii_art(source: str, title: str) -> str:
    """Validate and title a sparse hand-drawn sprite without changing its shape."""

    body = textwrap.dedent(source).strip("\n")
    lines = body.splitlines()
    if not lines or not body.isascii():
        raise ValueError("ASCII sprite bodies must be non-empty portable ASCII")
    if any("\t" in line or len(line) > 64 for line in lines):
        raise ValueError("ASCII sprite bodies must fit a 64-column terminal stage")
    width = max(len(line) for line in lines)
    nameplate = f"[ {title} ]"
    if len(nameplate) > width:
        raise ValueError("sprite nameplate is wider than its body")
    return "\n" + nameplate.center(width) + "\n" + body + "\n"


class AnimatedArtwork(str):
    """A string-compatible still image with optional restrained motion frames."""

    frames: tuple[str, ...]

    def __new__(cls, still: str, frames: tuple[str, ...]) -> "AnimatedArtwork":
        instance = super().__new__(cls, still)
        instance.frames = frames
        return instance


TITLE_ART_EXPANDED = r"""
                         \   |   /
                      ----\--*--/----
                         / /|\ \
                /\         |         /\
           ____/  \________|________/  \____
          /             .-' '-.              \
 ________/___________.-'       '-.____________\________
                     /           \
                   _/             \_
                __/       ___       \__
 ____________.-'________.-' '-.________'-.____________
"""


PRANCING_PONY_EXTERIOR_STILL = r"""
              ___
         ____|___|____________________________
       _/                 /\                  \_
      /__________________/  \__________________\
      |  []    []       /____\       []    [] |
      |                                        |----+--------.
      |  []    []       .----.       []    [] |    |  PONY  |
      |                 |    |                |    '--------'
      |_________________|    |________________|
      |    _      _     |    |    _      _    |
 _____|___|_|____|_|____|____|___|_|____|_|___|__________
       ~~~         ~~~          ~~~         ~~~
"""


PRANCING_PONY_EXTERIOR_RAIN_ART = r"""
  /       /          /        /       /          /
       /       /          /        /       /
              ___
         ____|___|____________________________
       _/                 /\                  \_
      /__________________/  \__________________\
      |  []    []       /____\       []    [] |
      |                                        |----+--------.
      |  []    []       .----.       []    [] |    |  PONY  |
      |                 |    |                |    '--------'
      |_________________|    |________________|
      |    _      _     |    |    _      _    |
 _____|___|_|____|_|____|____|___|_|____|_|___|__________
       ~~~       ~~~~~        ~~~       ~~~~~
"""


PRANCING_PONY_EXTERIOR_FRAMES = (
    PRANCING_PONY_EXTERIOR_STILL,
    PRANCING_PONY_EXTERIOR_RAIN_ART,
)
PRANCING_PONY_EXTERIOR_ART = AnimatedArtwork(
    PRANCING_PONY_EXTERIOR_RAIN_ART,
    PRANCING_PONY_EXTERIOR_FRAMES,
)


PRANCING_PONY_INTERIOR_ART = r"""
 __________________________________________________________
| []  []  [] |                        |  o  o  o  o  o  o |
|____________|       __________       |___________________|
|    O               |          |                 O       |
|   /|\     _[]_     |   (  )   |      _[]_      /|\      |
|   / \    /____\    |  ( /\ )  |     /____\     / \      |
|           |  |     | ( /  \ ) |      |  |               |
|    O      |  |     |__/____\__|      |  |       O       |
|   /|\_____|__|_______/____\__________|__|______/|\      |
|___/_\________________________________________________/_\__|
    /___\             /______\              /___\
"""


ORC_ATTACK_SPRITE = r"""
                        ___________
    /)                 <____/ \____>                       (\
   //                       |                               \\
  //    _/\_              _/\_                      _/\_    \\
 //   _<o  o>_          _<o  o>_                  _<o  o>_   \\
//   <   ^^   >        <   ^^   >                <   ^^   >  //
\\    \_====_/          \_====_/                  \_====_/ //
 \\_____/|[]|\_        __/|[]|\__                  _/|[]|\_//
  \____  |  |  \      /  /|  |\  \                /  |  |  _/
       /  |__|   >   <__/ |__| \__>              <   |__|  \
      /   /  \           _/  \_                      /  \  \
    _/  _/ /\ \_       _/ /\/\ \_                  _/ /\ \_ \
   /___/__/  \___\    /__/    \__\                /__/  \___\ \
"""
ORC_ATTACK_ART = _named_ascii_art(ORC_ATTACK_SPRITE, "ORC ATTACK")


BREE_STREETS_ART = r"""
        __/\__                               __/\__
     __/      \__                         __/      \__
    / []  []     \                       /     []  [] \
   /______________\                     /______________\
   | []   []    / |                     | \    []   [] |
   |      __   /  |       .----.        |  \   __      |
 __|_____|  |_/___|______/      \_______|___\_|  |_____|
   \               /      \    /      \               /
    \      [_]    /        \  /        \    [_]      /
     \______|____/__________||__________\____|_______/
            |               ||               |
 ___________|_______________||_______________|___________
               \            ||            /
                \___________||___________/
"""


NORTH_GATE_ART = r"""
         /\       /\                    /\       /\
        /  \_____/  \__________________/  \_____/  \
        | []     [] |                  | []     [] |
        |___________|                  |___________|
 /\/\/\/|           |==================|           |\/\/\/\
 | | | ||           ||\      ||      /||           || | | |
 | | | ||           || \     ||     / ||           || | | |
 | | | ||           ||  \    ||    /  ||           || | | |
 | | | ||           ||___\___||___/___||           || | | |
_|_|_|_||___________|_____\__||__/_____|___________||_|_|_|_
                         __/  \__
 _______________________/________\________________________
"""


THIRD_STONE_DISCOVERY_ART = r"""
       ______         ______                    ______
      /      \       /      \                  / \ | /\
     /        \     /        \                / --*-- \
    |          |   |          |              |   /|\   |
    |          |   |          |              |    |    |
    |          |   |          |              |         /
____|__________|___|__________|______________|________/____
                                        ____/
                         ______________/
                        |   .--------. |
                        |   |  (@)   | |
                        |   '--------' |
                        |______________|
"""


MIDGEWATER_RUINS_ART = r"""
             _                    _          __
        ____| |____          ____| |____  __|  |_
       |           |        |           ||      _|
       |   .---.   |        |   .---.   || .---|
       |  /     \  |________|  /     \__||/    |
   ____| |       |          | |               _|____
~~~\___|_|_______|~~~~~~~~~~|_|______________/___/~~~~
   \|/          ~       ~        ~          \|/
    |       _..----.._       _..----.._      |
~~~~|~~~~__/          \_____/          \~~~~~|~~~~
       \|/       \|/        \|/       \|/
"""


NORTH_WAYHOUSE_ART = r"""
              /\                         /\
         ____/  \____               ____/  \____
        | []      [] |_____________| []      [] |
        |            |             |            |
        |   .----.        /\        .----.     |
   _____|__/      \______/  \______/      \____|_____
        |              _/____\_              |
        |    ____     |  ||  |     ____     |
        |___/    \____|__||__|____/    \____|
             \       /   ||   \       /
              \_____/____||____\_____/
"""


ANCIENT_ROAD_DISCOVERY_ART = r"""
                   _..----------------.._
               _.-'                      '-._
 ____________.'____ _  _  _  _  _  _ _____'.____________
              \    V \/ \/ \/ \/ \/ V     /
               \        \   |   /         /
                \      ---\-*-/---       /
                 \         \|/          /
                  \    .-----------.    /
                   \___|   .---.   |___/
                       |  /     \  |
                       | /       \ |
                     __|/_________\|__
                  __/_____/___\_____\__
               __/______/_____\______\__
            __/_______/_______\_________\__
         __/_________/_________\__________\__
"""


ORC_TRACKER_SPRITE = r"""
                  _/\_
                _<o  o>_
               <   ^^   >
                \_^==^_/
             ___/|_[]_|\___
            /   (|    |)   \
<===============(|____|)===============================|>
                _/ /\ \_
            ___/  /  \  \___
           /_____/    \_____\
"""
ORC_TRACKER_INTRO_ART = _named_ascii_art(ORC_TRACKER_SPRITE, "ORC TRACKER")


MARSH_WARG_SPRITE = r"""
          /\_______________________________/\
         /                                   \
        /        \                   /        \
       /          \__  o       o  __/          \
      /              \___________/              \
     /                                             \
     \                  /\                       /
      \               _/  \_                    /
       \             /      \                  /
        \           /   @@   \                /
         \         /  /\/\/\  \              /
          \_______/  V  V  V   \____________/
                   \____________/
"""
MARSH_WARG_INTRO_ART = _named_ascii_art(MARSH_WARG_SPRITE, "MARSH WARG")


GHORAK_ASH_HAND_SPRITE = r"""
                     ______________________
              (@)===|______________________\
               |
          __/^^|\__
        <| o   |  o |>
         |    /\    |
          \  V  V  /
           \__==__/
        ____/||||\____
      _/    ||||||    \_
     /______||||||______\
        ___/      \___
_______/______________\____________________
"""
GHORAK_ASH_HAND_INTRO_ART = _named_ascii_art(
    GHORAK_ASH_HAND_SPRITE,
    "GHORAK ASH-HAND",
)


FINAL_RUINS_BATTLE_SPRITE = r"""
          _______
      ___/^^^^^^^\___                         \   O   /
    <|  o       o  |>                         \--|--/
     |      /\     |                             |
      \   V  V   /                             / \
       \___==___/                  O           /___\        O
      ___/|||||\___            ---/|\---                   -/|\-
   __/    |||||    \__           / \                      / \
 _/_______|||||_______\_        _/___\_                  _/___\_
         /     \
        /       \       =====================================>
_______/_________\_____________________________________________
"""
FINAL_RUINS_BATTLE_ART = _named_ascii_art(
    FINAL_RUINS_BATTLE_SPRITE,
    "FINAL BATTLE",
)


BLACK_RIDER_SPRITE = r"""
        .       |       .
     -----------*-----------
             /  |  \
                 .-^^^^-.
                / o    o \
                \   __   /
                 \_/||\_/
            __     /||\          /\
        ___/  \___/ || \________/  \__
      _/              __           o   \
     /       _________/  \________/\   |
    /_______/                      / \__|
       /   \                      /   \
      /     \                    /     \
    _/       \_                _/       \_
 __/___________\______________/___________\__
"""
BLACK_RIDER_DIM_SPRITE = r"""
                |
             ---+---
                |
                 .-^^^^-.
                / o    o \
                \   __   /
                 \_/||\_/
            __     /||\          /\
        ___/  \___/ || \________/  \__
      _/              __           o   \
     /       _________/  \________/\   |
    /_______/                      / \__|
       /   \                      /   \
      /     \                    /     \
    _/       \_                _/       \_
 __/___________\______________/___________\__
"""
BLACK_RIDER_CLIFFHANGER_STILL = _named_ascii_art(BLACK_RIDER_SPRITE, "BLACK RIDER")
BLACK_RIDER_STAR_DIM_ART = _named_ascii_art(BLACK_RIDER_DIM_SPRITE, "BLACK RIDER")


BLACK_RIDER_CLIFFHANGER_FRAMES = (
    BLACK_RIDER_STAR_DIM_ART,
    BLACK_RIDER_CLIFFHANGER_STILL,
)
BLACK_RIDER_CLIFFHANGER_ART = AnimatedArtwork(
    BLACK_RIDER_CLIFFHANGER_STILL,
    BLACK_RIDER_CLIFFHANGER_FRAMES,
)
