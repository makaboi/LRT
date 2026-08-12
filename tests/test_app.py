import random
import tempfile
import unittest
from pathlib import Path

from roads_beneath_shadow.app import Game
from roads_beneath_shadow.savegame import SaveManager
from roads_beneath_shadow.ui import TerminalUI
from tests.helpers import EpisodePlayer, VictoryCombat


class GameFlowTests(unittest.TestCase):
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
        for required in (
            "THE PRANCING PONY",
            "ORCS AT THE DOOR",
            "BREE BEFORE MIDNIGHT",
            "THE THIRD STONE",
            "MIDGEWATER",
            "GHORAK THE ASH-HAND",
            "A BLACK RIDER WAITS",
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
        self.assertIn(game.state.ending, {"fellowship", "shadow_claim"})


if __name__ == "__main__":
    unittest.main()
