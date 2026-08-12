import random
import tempfile
import unittest
from pathlib import Path

from roads_beneath_shadow.app import Game
from roads_beneath_shadow.content import ORIGINS
from roads_beneath_shadow.models import Character, GameState
from roads_beneath_shadow.savegame import SaveManager
from roads_beneath_shadow.ui import TerminalUI
from tests.helpers import EpisodePlayer, VictoryCombat


class GameFlowTests(unittest.TestCase):
    def test_initial_new_journey_still_starts_without_discard_confirmation(self) -> None:
        answers = iter(["Arin", "1", "1", "1"])
        output: list[str] = []
        ui = TerminalUI(
            color=False,
            fast=True,
            input_fn=lambda _: next(answers),
            output_fn=output.append,
        )
        game = Game(ui, rng=random.Random(1))

        self.assertTrue(game._new_journey())
        self.assertEqual(game.state.character.name, "Arin")
        self.assertNotIn("unfinished journey", "\n".join(output))

    def test_new_journey_requires_confirmation_before_discarding_progress(self) -> None:
        original = GameState(Character.from_origin("Mira", ORIGINS[0]), scene="wayhouse")
        output: list[str] = []
        ui = TerminalUI(
            color=False,
            fast=True,
            input_fn=lambda _: "1",
            output_fn=output.append,
        )
        game = Game(ui, rng=random.Random(2))
        game.state = original

        self.assertFalse(game._new_journey())
        self.assertIs(game.state, original)
        self.assertIn("Your current journey has been kept.", output)

    def test_confirmed_discard_replaces_the_unfinished_journey(self) -> None:
        original = GameState(Character.from_origin("Mira", ORIGINS[0]), scene="wayhouse")
        answers = iter(["2", "Arin", "1", "1", "1"])
        ui = TerminalUI(
            color=False,
            fast=True,
            input_fn=lambda _: next(answers),
            output_fn=lambda _: None,
        )
        game = Game(ui, rng=random.Random(3))
        game.state = original

        self.assertTrue(game._new_journey())
        self.assertEqual(game.state.character.name, "Arin")
        self.assertNotEqual(game.state.journey_id, original.journey_id)

    def test_load_menu_handles_validation_failure_without_replacing_current_state(self) -> None:
        class InvalidLoad:
            @staticmethod
            def all_slots():
                return [
                    {"name": "Spoof", "chapter": 1, "ending": None},
                    None,
                    None,
                ]

            @staticmethod
            def slot_metadata(_slot):
                return {"name": "Spoof", "chapter": 1, "ending": None}

            @staticmethod
            def load(_slot):
                raise ValueError("scene must not contain control characters")

        original = GameState(Character.from_origin("Mira", ORIGINS[0]), scene="wayhouse")
        output: list[str] = []
        ui = TerminalUI(
            color=False,
            fast=True,
            input_fn=lambda _: "1",
            output_fn=output.append,
        )
        game = Game(ui, saves=InvalidLoad(), rng=random.Random(4))
        game.state = original

        self.assertFalse(game._load_menu())
        self.assertIs(game.state, original)
        self.assertIn(
            "Could not load the journey: scene must not contain control characters",
            output,
        )

    def test_full_part_one_contains_required_episode_beats(self) -> None:
        player = EpisodePlayer(opening_choice=1)
        ui = TerminalUI(color=False, fast=True, input_fn=player.read, output_fn=player.write)
        with tempfile.TemporaryDirectory() as temporary:
            game = Game(ui, saves=SaveManager(Path(temporary)), rng=random.Random(12))
            combat = VictoryCombat()
            game.combat = combat
            game.run()

        state = game.state
        transcript = "\n".join(player.output)
        self.assertTrue(state.flags["part_one_complete"])
        self.assertTrue(state.flags["defeated_ghorak"])
        self.assertTrue(state.flags["ned_survived"])
        self.assertIn("Find missing watchman Ned Barley in the Midgewater fringe", state.completed_quests)
        self.assertEqual(len(combat.encounters), 3)
        self.assertGreaterEqual(state.play_minutes, 55)
        self.assertGreaterEqual(player.prompt_count, 20)
        self.assertTrue(state.flags["part_two_hidden_route_known"])
        self.assertIn(state.ending, {"hidden_road", "shadow_claim"})
        for required in (
            "PART I — THE BLACK RIDER'S LETTER",
            '"The silver star. Take its bearer alive."',
            "BREE BEFORE MIDNIGHT",
            "THE THIRD STONE",
            "THE LOST WHISTLE",
            "THE FINAL BATTLE",
            "THE EIGHTH HORN",
            "THE ROAD YOU MADE",
            "Tobin and Ned:",
            "These consequences are carried into Part II.",
            "PART I COMPLETE",
        ):
            self.assertIn(required, transcript)

    def test_real_combat_route_completes_episode(self) -> None:
        player = EpisodePlayer(opening_choice=1, origin_choice=1, real_combat=True)
        ui = TerminalUI(color=False, fast=True, input_fn=player.read, output_fn=player.write)
        with tempfile.TemporaryDirectory() as temporary:
            game = Game(ui, saves=SaveManager(Path(temporary)), rng=random.Random(8))
            game.run()

        self.assertTrue(game.state.flags["part_one_complete"])
        self.assertTrue(game.state.character.alive)
        self.assertIn(game.state.ending, {"hidden_road", "shadow_claim"})


if __name__ == "__main__":
    unittest.main()
