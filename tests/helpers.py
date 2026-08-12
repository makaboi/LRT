"""Reusable scripted players for full-episode tests."""

from __future__ import annotations

import re

from roads_beneath_shadow.combat import CombatResult


class VictoryCombat:
    def __init__(self) -> None:
        self.encounters = []

    def run(self, state, enemies, config=None):
        self.encounters.append({"enemies": [enemy.name for enemy in enemies], "config": config})
        for enemy in enemies:
            enemy.hp = 0
        return CombatResult.VICTORY


class EpisodePlayer:
    """Reads rendered headings and chooses a coherent completionist route."""

    def __init__(self, opening_choice: int = 1, origin_choice: int = 1, *, real_combat: bool = False) -> None:
        self.opening_choice = opening_choice
        self.origin_choice = origin_choice
        self.real_combat = real_combat
        self.output: list[str] = []
        self.cursor = 0
        self.main_menu_visits = 0
        self.prompt_count = 0

    def write(self, line: str) -> None:
        self.output.append(line)

    def read(self, prompt: str) -> str:
        self.prompt_count += 1
        if self.prompt_count > 500:
            raise AssertionError("Script exceeded 500 prompts; likely stuck in a loop")
        context = "\n".join(self.output[self.cursor :])
        self.cursor = len(self.output)

        if "Traveler's name" in prompt:
            return "Arin"
        if "MAIN MENU" in context:
            self.main_menu_visits += 1
            return "1" if self.main_menu_visits == 1 else "6"
        if "Choose your background" in context:
            return str(self.origin_choice)
        if "Accept this background" in context:
            return "1"
        if "What lesson from Calenor do you carry?" in context:
            return "1"
        if "WHAT WILL YOU DO?" in context:
            return str(self.opening_choice)
        if "IN THE KITCHEN" in context:
            return "1"
        if "PRESS YOUR QUESTION" in context:
            return "1"
        if "MARA WARNS YOU" in context:
            return "1"
        if "Choose your action" in context:
            return self._combat_action(context)
        if "Use which item?" in context:
            return "1"
        if "MARA WAITS FOR YOUR ANSWER" in context:
            return "1"
        if "WHERE WILL YOU INVESTIGATE?" in context:
            return "1"
        if "WHAT DO YOU EXAMINE?" in context:
            return "1"
        if "TOBIN LOOKS TO YOU" in context:
            return "1"
        if "CHOOSE ONE BUNDLE" in context:
            return "1"
        if "WHAT DO YOU ASK?" in context:
            return "2"
        if "TOBIN ASKS WHAT THE ORCS WERE SEEKING" in context:
            return "1"
        if "HOW WILL YOU OPEN CALENOR'S CACHE?" in context:
            return "1"
        if "TOBIN READS NED'S NAME" in context:
            return "1"
        if "CHOOSE THE APPROACH TO MIDGEWATER" in context:
            return "1"
        if "WHILE TOBIN SLEEPS" in context:
            return "2"
        if "WHO TAKES THE LAST WATCH?" in context:
            return "1"
        if "HOW DO YOU REACH NED?" in context:
            return "1"
        if "NED IS FADING" in context:
            return "1"
        if "THE WAYHOUSE DEMANDS A WARDEN'S OATH" in context:
            return "1"
        if "EXPLORE THE BURIED WAYHOUSE" in context:
            return "1"
        if "THE OLD BLADE IS BALANCED" in context:
            return "1"
        if "THE REFLECTION OFFERS STRENGTH" in context:
            return "1"
        if "THE FINAL BATTLE" in context:
            return "1"
        if "What next?" in context:
            return "2"
        raise AssertionError(f"Unexpected prompt: {prompt!r}\nContext:\n{context}")

    @staticmethod
    def _combat_action(context: str) -> str:
        health_matches = re.findall(r"Health\s+\[[#-]+\]\s+(\d+)/(\d+)", context)
        focus_matches = re.findall(r"Focus\s+\[[#-]+\]\s+(\d+)/(\d+)", context)
        if health_matches:
            current, maximum = map(int, health_matches[-1])
            if (
                current <= max(7, maximum // 3)
                and "Use an item" in context
                and "You have no usable items." not in context
            ):
                return "4"
        if focus_matches and int(focus_matches[-1][0]) > 0:
            return "2"
        return "1"
