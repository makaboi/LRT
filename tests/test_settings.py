import json
import tempfile
import unittest
from pathlib import Path

from roads_beneath_shadow.app import Game
from roads_beneath_shadow.combat import CombatDifficulty
from roads_beneath_shadow.settings import SettingsManager, UserSettings
from roads_beneath_shadow.ui import TerminalUI


class SettingsManagerTests(unittest.TestCase):
    def test_preferences_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manager = SettingsManager(Path(temporary) / "settings.json")
            expected = UserSettings(
                color_mode="off",
                sound=True,
                text_speed="fast",
                reduced_motion=True,
                screen_reader=True,
                difficulty="story",
            )

            manager.save(expected)
            loaded = manager.load()

            self.assertEqual(loaded, expected)

    def test_missing_or_damaged_settings_use_safe_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "settings.json"
            manager = SettingsManager(path)
            self.assertEqual(manager.load(), UserSettings())

            path.write_text("not json", encoding="utf-8")
            self.assertEqual(manager.load(), UserSettings())

    def test_unknown_values_are_repaired_and_extra_keys_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "settings.json"
            path.write_text(
                json.dumps(
                    {
                        "color_mode": "neon",
                        "text_speed": "warp",
                        "difficulty": "impossible",
                        "sound": "yes",
                        "reduced_motion": 1,
                        "future_option": True,
                    }
                ),
                encoding="utf-8",
            )

            loaded = SettingsManager(path).load()

            self.assertEqual(loaded.color_mode, "auto")
            self.assertEqual(loaded.text_speed, "normal")
            self.assertEqual(loaded.difficulty, "ranger")
            self.assertFalse(loaded.sound)
            self.assertFalse(loaded.reduced_motion)

    def test_game_settings_menu_applies_and_persists_player_preferences(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manager = SettingsManager(Path(temporary) / "settings.json")
            settings = UserSettings(color_mode="off")
            choices = iter(["1", "3", "4", "5", "6", "7"])
            ui = TerminalUI(
                color=False,
                fast=True,
                input_fn=lambda _: next(choices),
                output_fn=lambda _: None,
                sound_fn=lambda _: True,
            )
            game = Game(ui, settings_manager=manager, user_settings=settings)

            game._settings()

            loaded = manager.load()
            self.assertTrue(loaded.sound)
            self.assertEqual(loaded.text_speed, "fast")
            self.assertTrue(loaded.reduced_motion)
            self.assertTrue(loaded.screen_reader)
            self.assertEqual(loaded.difficulty, "shadow")
            self.assertEqual(game.combat.default_difficulty, CombatDifficulty.HARD)


if __name__ == "__main__":
    unittest.main()
