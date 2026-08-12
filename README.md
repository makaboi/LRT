# The Lord of the Rings: Roads Beneath the Shadow

*Roads Beneath the Shadow* is a story-driven terminal RPG set in Middle-earth during the War of the Ring. You play an unknown traveler whose guardian has vanished and whose quiet life ends when a dying messenger delivers a broken silver star.

This repository contains the complete playable opening episode: **Part I — The Black Rider's Letter**. A normal playthrough is designed for roughly 45–70 minutes depending on reading speed, exploration, and combat choices.

## Play on macOS

You need Python 3.10 or newer. The game has no third-party dependencies.

Double-click `Play Roads Beneath the Shadow.command`, or launch it from Terminal:

```bash
cd "/path/to/LRT"
python3 -m roads_beneath_shadow
```

Optional launch flags:

```bash
python3 -m roads_beneath_shadow --sound     # terminal bell sound cues
python3 -m roads_beneath_shadow --no-color  # plain text output
python3 -m roads_beneath_shadow --fast      # remove dramatic pauses
```

## Current features

- Character name, three distinct backgrounds, and a formative lesson from Calenor
- Five opening tactics that alter clues, trust, resources, and later options
- Explorable Bree locations and a multi-room North-kingdom wayhouse
- Substantive conversations with Mara and watchman Tobin Reed
- A complete rescue quest whose outcome carries into the finale
- Three tactical encounters: the Pony defense, Midgewater ambush, and Ghorak battle
- Turn-based combat with target selection, companion commands, Focus, defense, armor, healing, and encounter objectives
- Inventory, consumable items, and equipment management
- Three versioned save/load slots with migration and safe atomic writes
- Persistent hope, corruption, clues, companion trust, quest outcomes, and Part II state
- Compact retro ASCII scenes, restrained ANSI color, and optional sound cues
- A full dramatic ending and Black Rider cliffhanger leading into Part II
- Platform-neutral story and combat logic for future Windows Terminal support

Save files are stored in:

```text
~/Library/Application Support/Roads Beneath the Shadow/saves/
```

Set `RBS_SAVE_DIR` to use a different save location.

## Controls

Menus use numbered choices. During story decisions:

| Key | Action |
| --- | --- |
| `I` | Open inventory and equipment |
| `C` | Show character status |
| `J` | Read quests and clues |
| `S` | Save the journey |
| `M` | Return to the main menu |

## Development

Run all automated tests:

```bash
python3 -m unittest discover -s tests -v
```

The code is split into portable systems:

- `app.py` — story flow and menus
- `combat.py` — turn-based encounters
- `models.py` — character, enemy, and serialized game state
- `savegame.py` — save slots and atomic file handling
- `ui.py` — terminal input, color, layout, and sound
- `content.py` — items, backgrounds, artwork, and static chapter content

## Roadmap

1. Part II — The Dead Road
2. Companion combat abilities and relationship scenes
3. More equipment, conditions, and enemy behaviors
4. Expanded settings and accessibility controls
5. Windows Terminal launcher and compatibility verification

This is an unofficial fan project. Middle-earth and *The Lord of the Rings* are the property of their respective rights holders.
