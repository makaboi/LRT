import json
import tempfile
import unittest
from pathlib import Path

from roads_beneath_shadow.content import ORIGINS
from roads_beneath_shadow.models import Character, GameState
from roads_beneath_shadow.savegame import SaveManager


class SaveManagerTests(unittest.TestCase):
    def test_save_load_and_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            saves = SaveManager(Path(temporary))
            state = GameState(Character.from_origin("Mira", ORIGINS[1]))
            state.scene = "branch_search"
            saves.save(2, state)

            loaded = saves.load(2)
            metadata = saves.slot_metadata(2)

            self.assertEqual(loaded.character.name, "Mira")
            self.assertEqual(loaded.scene, "branch_search")
            self.assertEqual(metadata["name"], "Mira")
            self.assertIsNone(saves.slot_metadata(1))

    def test_corrupt_slot_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "slot_1.json").write_text("not json", encoding="utf-8")
            saves = SaveManager(root)

            self.assertTrue(saves.slot_metadata(1)["corrupt"])

    def test_rejects_unknown_save_version(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            payload = {
                "saved_at": "now",
                "state": {
                    "save_version": 999,
                    "character": {},
                },
            }
            (root / "slot_1.json").write_text(json.dumps(payload), encoding="utf-8")
            saves = SaveManager(root)

            with self.assertRaises(ValueError):
                saves.load(1)

    def test_migrates_version_one_save(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state = GameState(Character.from_origin("Old Traveler", ORIGINS[0])).to_dict()
            state["save_version"] = 1
            state["character"].pop("tobin_trust")
            state.pop("visited")
            state.pop("completed_quests")
            state.pop("play_minutes")
            (root / "slot_1.json").write_text(
                json.dumps({"saved_at": "then", "state": state}), encoding="utf-8"
            )

            loaded = SaveManager(root).load(1)

            self.assertEqual(loaded.character.name, "Old Traveler")
            self.assertEqual(loaded.character.tobin_trust, 0)
            self.assertEqual(loaded.save_version, 2)
            self.assertEqual(loaded.visited, [])


if __name__ == "__main__":
    unittest.main()
