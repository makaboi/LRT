# The Lord of the Rings: Roads Beneath the Shadow

*Roads Beneath the Shadow* is a story-driven terminal RPG set in Middle-earth during the War of the Ring. You play an unknown traveler whose guardian has vanished and whose quiet life ends when a dying messenger delivers a broken silver star.

This repository contains the complete playable opening episode: **Part I — The Black Rider's Letter**. A normal playthrough is designed for roughly 45–70 minutes depending on reading speed, exploration, and combat choices.

## Quick start on macOS

### What you need

- macOS
- Python 3.10 or newer
- No extra packages or installation commands

Check your Python version by opening Terminal and entering:

```bash
python3 --version
```

### 1. Download the game

1. Click the green **Code** button near the top of this GitHub page.
2. Click **Download ZIP**.
3. Open the downloaded ZIP file to create the `LRT-main` folder.

### 2. Launch the game

Open the `LRT-main` folder, then double-click:

```text
Play Roads Beneath the Shadow.command
```

A Terminal window will open at the game title screen. Choose **1** to begin a new journey.

If macOS blocks the launcher the first time, Control-click the file, choose **Open**, then choose **Open** again.

### Run from Terminal instead

If you downloaded the ZIP file, open Terminal and enter:

```bash
cd ~/Downloads/LRT-main
python3 -m roads_beneath_shadow
```

If you use Git, you can clone and launch the game with:

```bash
git clone https://github.com/makaboi/LRT.git
cd LRT
python3 -m roads_beneath_shadow
```

### Optional launch settings

Add one of these options when launching from Terminal:

```bash
python3 -m roads_beneath_shadow --sound     # turn on terminal bell sound cues
python3 -m roads_beneath_shadow --no-color  # use plain text without ANSI colors
python3 -m roads_beneath_shadow --fast      # remove dramatic text pauses
```

### Troubleshooting

- **`python3: command not found`** — install Python 3.10 or newer, then reopen Terminal.
- **The launcher says “Permission denied”** — run `chmod +x "Play Roads Beneath the Shadow.command"` inside the game folder, then open it again.
- **The downloaded folder has a different name** — type `cd ` in Terminal, drag the folder into the Terminal window, press Return, then run `python3 -m roads_beneath_shadow`.
- **Text colors are difficult to read** — launch with `python3 -m roads_beneath_shadow --no-color`.

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
