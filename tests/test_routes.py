import random
import tempfile
import unittest
from pathlib import Path

from roads_beneath_shadow.app import Game
from roads_beneath_shadow.savegame import SaveManager
from roads_beneath_shadow.ui import TerminalUI
from tests.helpers import EpisodePlayer, VictoryCombat


class OpeningRouteTests(unittest.TestCase):
    EXPECTED_FLAGS = {
        1: "stood_with_mara",
        2: "pendant_hidden",
        3: "found_ranger_cipher",
        4: "returned_for_mara",
        5: "calenor_may_live",
    }

    def test_all_five_opening_choices_reach_final_cliffhanger(self) -> None:
        for opening_choice, expected_flag in self.EXPECTED_FLAGS.items():
            with self.subTest(opening_choice=opening_choice), tempfile.TemporaryDirectory() as temporary:
                player = EpisodePlayer(opening_choice=opening_choice)
                ui = TerminalUI(color=False, fast=True, input_fn=player.read, output_fn=player.write)
                game = Game(ui, saves=SaveManager(Path(temporary)), rng=random.Random(50 + opening_choice))
                combat = VictoryCombat()
                game.combat = combat
                game.run()

                self.assertTrue(game.state.flags[expected_flag])
                self.assertTrue(game.state.flags["part_one_complete"])
                self.assertTrue(game.state.flags["defeated_ghorak"])
                self.assertEqual(len(combat.encounters), 3)

    def test_each_origin_has_a_complete_viable_route(self) -> None:
        for origin_choice in (1, 2, 3):
            with self.subTest(origin=origin_choice), tempfile.TemporaryDirectory() as temporary:
                player = EpisodePlayer(origin_choice=origin_choice)
                ui = TerminalUI(color=False, fast=True, input_fn=player.read, output_fn=player.write)
                game = Game(ui, saves=SaveManager(Path(temporary)), rng=random.Random(100 + origin_choice))
                game.combat = VictoryCombat()
                game.run()

                self.assertTrue(game.state.flags["part_one_complete"])
                self.assertTrue(game.state.flags["ned_stabilized"])


if __name__ == "__main__":
    unittest.main()
