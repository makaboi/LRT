"""Serializable game-state models and inventory rules."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


SAVE_VERSION = 2


@dataclass(frozen=True)
class Item:
    item_id: str
    name: str
    description: str
    kind: str
    slot: str | None = None
    attack: int = 0
    defense: int = 0
    healing: int = 0


@dataclass(frozen=True)
class Origin:
    origin_id: str
    name: str
    description: str
    max_hp: int
    strength: int
    cunning: int
    will: int
    starting_items: tuple[str, ...]
    weapon: str
    armor: str | None = None


@dataclass
class Character:
    name: str
    origin: str
    max_hp: int
    hp: int
    strength: int
    cunning: int
    will: int
    max_focus: int = 3
    focus: int = 3
    hope: int = 0
    corruption: int = 0
    mara_trust: int = 0
    tobin_trust: int = 0
    inventory: dict[str, int] = field(default_factory=dict)
    weapon: str | None = None
    armor: str | None = None

    @classmethod
    def from_origin(cls, name: str, origin: Origin) -> "Character":
        inventory: dict[str, int] = {}
        for item_id in origin.starting_items:
            inventory[item_id] = inventory.get(item_id, 0) + 1
        return cls(
            name=name,
            origin=origin.origin_id,
            max_hp=origin.max_hp,
            hp=origin.max_hp,
            strength=origin.strength,
            cunning=origin.cunning,
            will=origin.will,
            inventory=inventory,
            weapon=origin.weapon,
            armor=origin.armor,
        )

    def add_item(self, item_id: str, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be positive")
        self.inventory[item_id] = self.inventory.get(item_id, 0) + quantity

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        if quantity < 1:
            raise ValueError("quantity must be positive")
        current = self.inventory.get(item_id, 0)
        if current < quantity:
            return False
        remaining = current - quantity
        if remaining:
            self.inventory[item_id] = remaining
        else:
            self.inventory.pop(item_id, None)
        return True

    def equip(self, item: Item) -> None:
        if self.inventory.get(item.item_id, 0) < 1:
            raise ValueError(f"{item.name} is not in the inventory")
        if item.slot == "weapon":
            self.weapon = item.item_id
        elif item.slot == "armor":
            self.armor = item.item_id
        else:
            raise ValueError(f"{item.name} cannot be equipped")

    def heal(self, amount: int) -> int:
        before = self.hp
        self.hp = min(self.max_hp, self.hp + max(0, amount))
        return self.hp - before

    @property
    def alive(self) -> bool:
        return self.hp > 0


@dataclass
class GameState:
    character: Character
    scene: str = "chapter1_intro"
    chapter: int = 1
    flags: dict[str, bool] = field(default_factory=dict)
    quests: list[str] = field(default_factory=list)
    journal: list[str] = field(default_factory=list)
    visited: list[str] = field(default_factory=list)
    completed_quests: list[str] = field(default_factory=list)
    play_minutes: int = 0
    ending: str | None = None
    save_version: int = SAVE_VERSION

    def add_journal(self, entry: str) -> None:
        if entry not in self.journal:
            self.journal.append(entry)

    def add_quest(self, quest: str) -> None:
        if quest not in self.quests:
            self.quests.append(quest)

    def complete_quest(self, quest: str) -> None:
        if quest in self.quests:
            self.quests.remove(quest)
        if quest not in self.completed_quests:
            self.completed_quests.append(quest)

    def visit(self, location: str) -> None:
        if location not in self.visited:
            self.visited.append(location)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "GameState":
        version = int(payload.get("save_version", 0))
        if version not in {1, SAVE_VERSION}:
            raise ValueError(f"Unsupported save version: {version}")
        character_data = dict(payload["character"])
        character_data.setdefault("tobin_trust", 0)
        character = Character(**character_data)
        return cls(
            character=character,
            scene=payload.get("scene", "chapter1_intro"),
            chapter=int(payload.get("chapter", 1)),
            flags=dict(payload.get("flags", {})),
            quests=list(payload.get("quests", [])),
            journal=list(payload.get("journal", [])),
            visited=list(payload.get("visited", [])),
            completed_quests=list(payload.get("completed_quests", [])),
            play_minutes=int(payload.get("play_minutes", 0)),
            ending=payload.get("ending"),
            save_version=SAVE_VERSION,
        )


@dataclass
class Enemy:
    name: str
    max_hp: int
    hp: int
    attack_min: int
    attack_max: int
    armor: int = 0
    description: str = ""

    @property
    def alive(self) -> bool:
        return self.hp > 0
