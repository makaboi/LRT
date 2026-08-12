"""Turn-based combat for terminal encounters."""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum

from .content import ITEMS
from .models import Enemy, GameState
from .ui import Color, TerminalUI


class CombatResult(str, Enum):
    VICTORY = "victory"
    DEFEAT = "defeat"
    ESCAPED = "escaped"


@dataclass
class CombatConfig:
    allow_flee: bool = False
    surprise_round: bool = False
    mara_aid: bool = False
    tobin_aid: bool = False
    location_text: str = "Steel clears leather. Rain hisses through the broken window."
    objective: str | None = None
    max_rounds: int | None = None


class CombatEngine:
    def __init__(self, ui: TerminalUI, rng: random.Random | None = None) -> None:
        self.ui = ui
        self.rng = rng or random.Random()

    def run(self, state: GameState, enemies: list[Enemy], config: CombatConfig | None = None) -> CombatResult:
        config = config or CombatConfig()
        character = state.character
        character.focus = character.max_focus
        self.ui.sound("danger")
        self.ui.title("COMBAT")
        self.ui.narrate(config.location_text, color=Color.RED)
        if config.objective:
            self.ui.write(f"Objective: {config.objective}", color=Color.YELLOW, bold=True)

        if config.surprise_round and enemies:
            damage = self._player_damage(state, enemies[0], power=False)
            enemies[0].hp = max(0, enemies[0].hp - damage)
            self.ui.write(f"You seize the opening and strike {enemies[0].name} for {damage} damage!", color=Color.GREEN)

        round_number = 1
        active = next(enemy for enemy in enemies if enemy.alive)
        while character.alive and any(enemy.alive for enemy in enemies):
            if not active.alive:
                active = next(enemy for enemy in enemies if enemy.alive)
            self._show_status(state, enemies, round_number, active)
            actions = ["attack", "power", "defend", "item", "inspect"]
            options = ["Attack", "Power attack (-1 Focus)", "Defend", "Use an item", "Inspect enemy"]
            if sum(enemy.alive for enemy in enemies) > 1:
                actions.append("target")
                options.append(f"Change target (current: {active.name})")
            if config.mara_aid:
                actions.append("mara")
                options.append("Call to Mara (-1 Focus)")
            if config.tobin_aid:
                actions.append("tobin")
                options.append("Call to Tobin (-1 Focus)")
            if config.allow_flee:
                actions.append("flee")
                options.append("Attempt to flee")
            selected = self.ui.choose("Choose your action", options)
            if selected is None:
                continue
            action = actions[selected - 1]

            defended = False
            consumes_turn = True
            if action == "attack":
                damage = self._player_damage(state, active, power=False)
                active.hp = max(0, active.hp - damage)
                self.ui.write(f"You strike {active.name} for {damage} damage.", color=Color.GREEN)
            elif action == "power":
                if character.focus <= 0:
                    self.ui.write("You have no Focus left. Choose another action.", color=Color.YELLOW)
                    continue
                character.focus -= 1
                damage = self._player_damage(state, active, power=True)
                active.hp = max(0, active.hp - damage)
                self.ui.write(f"Your heavy blow deals {damage} damage to {active.name}!", color=Color.GREEN, bold=True)
            elif action == "defend":
                defended = True
                restored = 1 if character.focus < character.max_focus else 0
                character.focus = min(character.max_focus, character.focus + restored)
                message = "You set your feet and raise your guard."
                if restored:
                    message += " You recover 1 Focus."
                self.ui.write(message, color=Color.CYAN)
            elif action == "item":
                consumes_turn = self.use_item(state)
                if not consumes_turn:
                    continue
            elif action == "inspect":
                self._inspect(active)
                consumes_turn = False
            elif action == "target":
                living = [enemy for enemy in enemies if enemy.alive]
                target = self.ui.choose("Choose a target", [f"{enemy.name} ({enemy.hp}/{enemy.max_hp} Health)" for enemy in living], allow_back=True)
                if target is not None:
                    active = living[target - 1]
                    self.ui.write(f"You turn your attention to {active.name}.", color=Color.CYAN)
                consumes_turn = False
            elif action == "mara":
                if character.focus <= 0:
                    self.ui.write("You have no Focus left. Choose another action.", color=Color.YELLOW)
                    continue
                character.focus -= 1
                damage = self.rng.randint(3, 5) + max(0, character.mara_trust)
                active.hp = max(0, active.hp - damage)
                self.ui.write(f"Mara crosses your attack and deals {damage} damage to {active.name}.", color=Color.MAGENTA)
            elif action == "tobin":
                if character.focus <= 0:
                    self.ui.write("You have no Focus left. Choose another action.", color=Color.YELLOW)
                    continue
                character.focus -= 1
                damage = self.rng.randint(2, 4) + max(0, character.tobin_trust)
                active.hp = max(0, active.hp - damage)
                self.ui.write(f"Tobin's arrow deals {damage} damage to {active.name}.", color=Color.CYAN)
            elif action == "flee":
                if self.rng.randint(1, 6) + character.cunning >= 6:
                    self.ui.write("You overturn a table and vanish through the smoke.", color=Color.CYAN)
                    return CombatResult.ESCAPED
                self.ui.write("The enemy cuts off your escape.", color=Color.RED)

            if not consumes_turn:
                continue
            if not active.alive:
                self.ui.write(f"{active.name} falls.", color=Color.YELLOW, bold=True)
                if not any(enemy.alive for enemy in enemies):
                    break
                active = next(enemy for enemy in enemies if enemy.alive)
                self.ui.write(f"{active.name} steps over the body and attacks!", color=Color.RED)

            incoming = self.rng.randint(active.attack_min, active.attack_max)
            armor = ITEMS[character.armor].defense if character.armor else 0
            incoming = max(1, incoming - armor)
            if defended:
                incoming = max(1, incoming // 2)
            if config.mara_aid and self.rng.random() < 0.25:
                incoming = max(0, incoming - 2)
                self.ui.write("Mara turns part of the blow with her second blade.", color=Color.MAGENTA)
            character.hp = max(0, character.hp - incoming)
            self.ui.write(f"{active.name} hits you for {incoming} damage.", color=Color.RED)
            round_number += 1
            if config.max_rounds and round_number > config.max_rounds and character.alive:
                self.ui.write("Your objective is complete—the surviving enemies lose their chance to stop you.", color=Color.GREEN)
                return CombatResult.VICTORY

        if character.alive:
            self.ui.sound("victory")
            self.ui.write("The last enemy crashes to the floor.", color=Color.GREEN, bold=True)
            return CombatResult.VICTORY
        self.ui.write("Your strength fails. Black shapes close around you.", color=Color.RED, bold=True)
        return CombatResult.DEFEAT

    def _player_damage(self, state: GameState, enemy: Enemy, *, power: bool) -> int:
        character = state.character
        weapon_attack = ITEMS[character.weapon].attack if character.weapon else 0
        roll = self.rng.randint(1, 3)
        bonus = 3 if power else 0
        return max(1, roll + character.strength + weapon_attack + bonus - enemy.armor)

    def use_item(self, state: GameState) -> bool:
        character = state.character
        consumables = [item_id for item_id, quantity in character.inventory.items() if quantity and ITEMS[item_id].healing]
        if not consumables:
            self.ui.write("You have no usable items.", color=Color.YELLOW)
            return False
        labels = [f"{ITEMS[item_id].name} x{character.inventory[item_id]}" for item_id in consumables]
        choice = self.ui.choose("Use which item?", labels, allow_back=True)
        if choice is None:
            return False
        item = ITEMS[consumables[choice - 1]]
        if character.hp >= character.max_hp:
            self.ui.write("You are already at full health.", color=Color.YELLOW)
            return False
        character.remove_item(item.item_id)
        healed = character.heal(item.healing)
        self.ui.write(f"You use {item.name} and recover {healed} Health.", color=Color.GREEN)
        return True

    def _inspect(self, enemy: Enemy) -> None:
        self.ui.write(f"{enemy.name}: {enemy.hp}/{enemy.max_hp} Health, {enemy.armor} Armor", color=Color.CYAN)
        if enemy.description:
            self.ui.narrate(enemy.description, color=Color.DIM)

    def _show_status(self, state: GameState, enemies: list[Enemy], round_number: int, target: Enemy) -> None:
        character = state.character
        self.ui.write()
        self.ui.write(f"-- Round {round_number} --", color=Color.YELLOW, bold=True)
        self.ui.write(self.ui.meter("Health", character.hp, character.max_hp))
        self.ui.write(self.ui.meter("Focus", character.focus, character.max_focus, color=Color.CYAN))
        for enemy in enemies:
            if enemy.alive:
                marker = " < TARGET" if enemy is target else ""
                self.ui.write(self.ui.meter(enemy.name[:7], enemy.hp, enemy.max_hp, color=Color.RED) + marker)


def orc_scout(name: str = "Orc Scout") -> Enemy:
    return Enemy(name, max_hp=9, hp=9, attack_min=3, attack_max=6, armor=0, description="Lean, rain-blackened, and eager to prove itself.")


def orc_captain(*, wounded: bool = False) -> Enemy:
    hp = 12 if wounded else 16
    return Enemy("Orc Captain", max_hp=16, hp=hp, attack_min=4, attack_max=7, armor=1, description="A scarred Uruk with a curved sword and the red-eye brand.")


def marsh_warg() -> Enemy:
    return Enemy(
        "Marsh Warg",
        max_hp=14,
        hp=14,
        attack_min=4,
        attack_max=7,
        armor=0,
        description="A huge grey hunter, ribs striped with old spear scars and muzzle wet with marsh water.",
    )


def ghorak() -> Enemy:
    return Enemy(
        "Ghorak Ash-Hand",
        max_hp=25,
        hp=25,
        attack_min=5,
        attack_max=8,
        armor=2,
        description="The Orc commander who hunted Calenor. One gauntlet is crusted with pale ash and silver dust.",
    )
