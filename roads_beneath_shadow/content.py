"""Static game content for the Chapter One vertical slice."""

from __future__ import annotations

from .models import Item, Origin


TITLE_ART = r"""
          _   _              _     ____  _               _
         | |_| |__   ___    | |   / ___|| |__   __ _  __| | _____      __
         | __| '_ \ / _ \   | |   \___ \| '_ \ / _` |/ _` |/ _ \ \ /\ / /
         | |_| | | |  __/   | |___ ___) | | | | (_| | (_| | (_) \ V  V /
          \__|_| |_|\___|   |_____|____/|_| |_|\__,_|\__,_|\___/ \_/\_/

                     R O A D S   B E N E A T H
"""


PONY_ART = r"""
                       /\
              ________/  \_______
             /                   /\
            /___________________/  \
            |  _   _   _   _   |  |
            | |_| |_| |_| |_|   |  |       THE PRANCING PONY
            |       ______      |  |
            |      |      |     |  |
         ___|______|______|_____|__|___
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


STAR_ART = r"""
                         .
                      .  |  .
                       \ | /
                    ---- * ----
                       / | \
                      '  |  '
                         '
"""


ITEMS: dict[str, Item] = {
    "ash_staff": Item(
        "ash_staff", "Ash Walking Staff", "A sturdy road-worn staff.", "weapon", "weapon", attack=2
    ),
    "hunting_knife": Item(
        "hunting_knife", "Hunting Knife", "Small, quick, and kept keen.", "weapon", "weapon", attack=3
    ),
    "bree_blade": Item(
        "bree_blade", "Bree-forged Sword", "Plain steel with a dependable edge.", "weapon", "weapon", attack=4
    ),
    "orc_cleaver": Item(
        "orc_cleaver", "Orc Cleaver", "Ugly iron, balanced for brutal cuts.", "weapon", "weapon", attack=5
    ),
    "patched_leather": Item(
        "patched_leather", "Patched Leather", "Old armor that still turns a glancing blow.", "armor", "armor", defense=1
    ),
    "healing_herb": Item(
        "healing_herb", "Healing Herb", "A wrapped bundle of yarrow and athelas.", "consumable", healing=9
    ),
    "sealed_letter": Item(
        "sealed_letter", "Calenor's Sealed Letter", "Rain-stained, but its black wax seal is intact.", "quest"
    ),
    "silver_star": Item(
        "silver_star", "Broken Silver Star", "An eight-pointed pendant with one silver ray snapped away.", "quest"
    ),
    "ranger_token": Item(
        "ranger_token", "Ranger's Token", "A small oak-leaf token marked with Calenor's cipher.", "quest"
    ),
    "black_arrowhead": Item(
        "black_arrowhead", "Black Arrowhead", "Its barbs carry the mark of a lidless red eye.", "quest"
    ),
    "calenor_map": Item(
        "calenor_map", "Calenor's Road-map", "A waxed scrap showing a forgotten wayhouse east of Bree.", "quest"
    ),
    "star_key": Item(
        "star_key", "Completed Star-key", "The missing silver ray has joined the pendant, restoring all eight points.", "quest"
    ),
    "watch_badge": Item(
        "watch_badge", "Bree Watch Badge", "Tobin's brass badge; proof that someone in Bree trusts you.", "quest"
    ),
    "smoke_bomb": Item(
        "smoke_bomb", "Dwarf-smoke Flask", "A clay flask that bursts into choking grey smoke.", "consumable"
    ),
    "lembas_scrap": Item(
        "lembas_scrap", "Waybread", "A small wrapped piece of sustaining travel bread.", "consumable", healing=12
    ),
    "ranger_cloak": Item(
        "ranger_cloak", "Weathered Ranger Cloak", "Calenor's grey-green cloak, cut but serviceable.", "armor", "armor", defense=2
    ),
    "numenorean_blade": Item(
        "numenorean_blade", "North-kingdom Blade", "A short leaf-shaped sword recovered from the wayhouse.", "weapon", "weapon", attack=6
    ),
}


ORIGINS: tuple[Origin, ...] = (
    Origin(
        "bree_wayfarer",
        "Bree-land Wayfarer",
        "Balanced and resilient. You know inns, farms, and the people of the road.",
        max_hp=28,
        strength=2,
        cunning=2,
        will=2,
        starting_items=("ash_staff", "patched_leather", "healing_herb"),
        weapon="ash_staff",
        armor="patched_leather",
    ),
    Origin(
        "north_road_scout",
        "North-road Scout",
        "Fast and dangerous. You read tracks well and strike before enemies settle.",
        max_hp=25,
        strength=3,
        cunning=3,
        will=1,
        starting_items=("hunting_knife", "patched_leather", "healing_herb"),
        weapon="hunting_knife",
        armor="patched_leather",
    ),
    Origin(
        "healers_apprentice",
        "Healer's Apprentice",
        "Strong-willed and well supplied. You survive through knowledge and care.",
        max_hp=23,
        strength=1,
        cunning=2,
        will=4,
        starting_items=("ash_staff", "healing_herb", "healing_herb"),
        weapon="ash_staff",
    ),
)


CHAPTER_ONE_CHOICES = (
    "Draw your weapon and fight beside Mara",
    "Hide the pendant and protect the letter",
    "Search the fallen messenger for another clue",
    "Escape through the inn's kitchen",
    "Attempt to question the Orc captain",
)


ENDING_TEXT = {
    "fellowship": (
        "BENEATH THE SHADOW",
        "The buried gate stands open. Beyond it, Calenor's trail descends under the Weather Hills—"
        "and a Black Rider waits above while you, Mara, and Tobin have only one road left: down.",
    ),
    "hidden_road": (
        "THE HIDDEN ROAD",
        "You leave Bree alone beneath a moonless sky. The silver star guides you north while "
        "Mara remains among the wreckage. Whatever bond might have formed between you is left behind.",
    ),
    "keeper_of_secrets": (
        "KEEPER OF THE ROAD",
        "You have opened the lost wayhouse and kept its secret from the Orcs. But the stair beneath "
        "it leads toward Calenor—and something in the dark has begun calling you by name.",
    ),
    "shadow_claim": (
        "SHADOW-MARKED",
        "You descend wounded while the Black Rider claims the threshold behind you. The star-key "
        "burns with a mark it did not bear before, and the Dead Road now knows both your name and your fear.",
    ),
}


QUEST_THIRD_STONE = "Find Calenor's cache behind the north gate's third stone"
QUEST_MISSING_WATCHMAN = "Find missing watchman Ned Barley in the Midgewater fringe"
QUEST_WAYHOUSE = "Reach the forgotten North-kingdom wayhouse before Ghorak"
