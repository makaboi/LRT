import tempfile
import unittest
from pathlib import Path

from roads_beneath_shadow.app import Game
from roads_beneath_shadow.content import ORIGINS
from roads_beneath_shadow.models import Character, GameState
from roads_beneath_shadow.profile import PlayerProfile, ProfileManager
from roads_beneath_shadow.ui import TerminalUI


class PlayerProfileTests(unittest.TestCase):
    def test_completed_run_unlocks_matching_achievements(self) -> None:
        state = GameState(Character.from_origin("Arin", ORIGINS[0]))
        state.ending = "fellowship"
        state.character.hope = 5
        state.character.corruption = 1
        state.flags.update(
            {
                "ned_survived": True,
                "mara_chose_to_continue": True,
                "tobin_chose_to_continue": True,
            }
        )
        state.journal = [f"Clue {index}" for index in range(12)]

        profile = PlayerProfile()
        unlocked = profile.record(state)

        self.assertIn("part_one", unlocked)
        self.assertIn("none_left_behind", unlocked)
        self.assertIn("unbroken_hope", unlocked)
        self.assertIn("road_scholar", unlocked)
        self.assertEqual(profile.endings, {"fellowship": 1})

    def test_profile_manager_round_trip_does_not_duplicate_a_completed_journey(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manager = ProfileManager(Path(temporary) / "profile.json")
            state = GameState(Character.from_origin("Arin", ORIGINS[1]))
            state.ending = "shadow_claim"
            state.character.corruption = 4

            first = manager.record(state)
            second = manager.record(state)
            loaded = manager.load()

            self.assertIn("shadow_touched", first)
            self.assertNotIn("shadow_touched", second)
            self.assertEqual(loaded.completed_runs, 1)
            self.assertEqual(loaded.endings["shadow_claim"], 1)

    def test_incomplete_journey_cannot_be_recorded(self) -> None:
        state = GameState(Character.from_origin("Arin", ORIGINS[2]))
        with self.assertRaises(ValueError):
            PlayerProfile().record(state)

    def test_damaged_or_hostile_profile_labels_are_ignored(self) -> None:
        profile = PlayerProfile.from_dict(
            {
                "completed_runs": 2,
                "endings": {"fellowship": 1, "\x1b[31mspoof": 99},
                "origins_completed": ["bree_wayfarer", "invented_origin"],
                "recorded_journeys": ["safe-id", "bad\nline", "x" * 200],
            }
        )

        self.assertEqual(profile.endings, {"fellowship": 1})
        self.assertEqual(profile.origins_completed, ["bree_wayfarer"])
        self.assertEqual(profile.recorded_journeys, ["safe-id"])

    def test_ending_screen_records_once_and_chronicle_reads_the_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manager = ProfileManager(Path(temporary) / "profile.json")
            output: list[str] = []
            ui = TerminalUI(
                color=False,
                fast=True,
                input_fn=lambda _: "2",
                output_fn=output.append,
            )
            game = Game(ui, profile=manager)
            game.state = GameState(Character.from_origin("Arin", ORIGINS[0]))
            game.state.ending = "fellowship"
            game.state.flags.update(
                {"defeated_ghorak": True, "ned_survived": True, "part_two_hidden_route_known": False}
            )

            game._show_ending()
            game._show_ending()
            game._show_chronicle()

            loaded = manager.load()
            transcript = "\n".join(output)
            self.assertEqual(loaded.completed_runs, 1)
            self.assertIn("The Road Opens", transcript)
            self.assertIn("Completed journeys: 1", transcript)


if __name__ == "__main__":
    unittest.main()
