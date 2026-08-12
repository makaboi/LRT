"""JSON save slots with atomic writes and lightweight metadata."""

from __future__ import annotations

import json
import os
import platform
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import GameState


def default_save_directory() -> Path:
    override = os.environ.get("RBS_SAVE_DIR")
    if override:
        return Path(override).expanduser()
    if platform.system() == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Roads Beneath the Shadow" / "saves"
    return Path.home() / ".roads_beneath_shadow" / "saves"


class SaveManager:
    SLOT_COUNT = 3

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or default_save_directory()

    def _path(self, slot: int) -> Path:
        if not 1 <= slot <= self.SLOT_COUNT:
            raise ValueError(f"Save slot must be between 1 and {self.SLOT_COUNT}")
        return self.root / f"slot_{slot}.json"

    def save(self, slot: int, state: GameState) -> Path:
        path = self._path(slot)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "state": state.to_dict(),
        }
        handle, temporary_name = tempfile.mkstemp(prefix=f"slot_{slot}_", suffix=".tmp", dir=path.parent)
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as temporary:
                json.dump(payload, temporary, ensure_ascii=False, indent=2)
                temporary.write("\n")
            os.replace(temporary_name, path)
        except Exception:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
            raise
        return path

    def load(self, slot: int) -> GameState:
        path = self._path(slot)
        with path.open("r", encoding="utf-8") as source:
            payload = json.load(source)
        if not isinstance(payload, dict) or not isinstance(payload.get("state"), dict):
            raise ValueError("Save file is malformed")
        return GameState.from_dict(payload["state"])

    def delete(self, slot: int) -> None:
        self._path(slot).unlink(missing_ok=True)

    def slot_metadata(self, slot: int) -> dict[str, Any] | None:
        path = self._path(slot)
        if not path.exists():
            return None
        try:
            with path.open("r", encoding="utf-8") as source:
                payload = json.load(source)
            state = payload["state"]
            character = state["character"]
            return {
                "slot": slot,
                "name": character["name"],
                "origin": character["origin"],
                "chapter": state.get("chapter", 1),
                "scene": state.get("scene", "unknown"),
                "ending": state.get("ending"),
                "saved_at": payload.get("saved_at", "unknown"),
            }
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
            return {"slot": slot, "corrupt": True}

    def all_slots(self) -> list[dict[str, Any] | None]:
        return [self.slot_metadata(slot) for slot in range(1, self.SLOT_COUNT + 1)]
