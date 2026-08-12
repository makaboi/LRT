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

    def test_discoveries_unlock_hidden_road_instead_of_obsolete_early_exit(self) -> None:
        state, transcript = self._resolve_cliffhanger(
            hope=4,
            corruption=0,
            mara_trust=3,
            tobin_trust=3,
            flags={
                "defeated_ghorak": True,
                "ned_survived": True,
                "learned_dead_road_map": True,
                "found_ranger_cipher": True,
            },
        )

        self.assertEqual(state.ending, "hidden_road")
        self.assertTrue(state.flags["part_two_hidden_route_known"])
        self.assertIn("unmarked stair opens beneath the broken crown", transcript)
        self.assertIn("archive clues revealed a hidden descent", transcript)

    def test_companion_bonds_and_ned_rescue_create_fellowship_ending(self) -> None:
        state, transcript = self._resolve_cliffhanger(
            hope=4,
            corruption=1,
            mara_trust=2,
            tobin_trust=2,
            flags={"defeated_ghorak": True, "ned_survived": True},
        )

        self.assertEqual(state.ending, "fellowship")
        self.assertTrue(state.flags["part_two_companions_united"])
        self.assertTrue(state.flags["part_two_ned_safe"])
        self.assertIn("Ned lives, and Tobin follows", transcript)
        self.assertIn("She follows by choice", transcript)

    def test_broken_trust_and_neds_death_create_keeper_ending(self) -> None:
        state, transcript = self._resolve_cliffhanger(
            hope=3,
            corruption=1,
            mara_trust=-2,
            tobin_trust=0,
            flags={"defeated_ghorak": True, "ned_survived": False},
        )

        self.assertEqual(state.ending, "keeper_of_secrets")
        self.assertTrue(state.flags["part_two_mara_distrusts_player"])
        self.assertFalse(state.flags["part_two_ned_safe"])
        self.assertIn("Ned fell", transcript)
        self.assertIn("no longer trusts", transcript)

    def test_repeated_use_of_star_power_can_claim_an_otherwise_victorious_route(self) -> None:
        state, transcript = self._resolve_cliffhanger(
            hope=0,
            corruption=2,
            mara_trust=3,
            tobin_trust=3,
            flags={
                "defeated_ghorak": True,
                "ned_survived": True,
                "accepted_star_power": True,
                "used_star_in_final": True,
            },
        )

        self.assertEqual(state.ending, "shadow_claim")
        self.assertTrue(state.flags["part_two_shadow_foothold"])
        self.assertIn("star found a foothold", transcript)

    @staticmethod
    def _resolve_cliffhanger(
        *,
        hope: int,
        corruption: int,
        mara_trust: int,
        tobin_trust: int,
        flags: dict[str, bool],
    ) -> tuple[GameState, str]:
        output: list[str] = []
        ui = TerminalUI(color=False, fast=True, input_fn=lambda _: "2", output_fn=output.append)
        game = Game(ui, rng=random.Random(9))
        character = Character.from_origin("Arin", ORIGINS[0])
        character.hope = hope
        character.corruption = corruption
        character.mara_trust = mara_trust
        character.tobin_trust = tobin_trust
        game.state = GameState(character, scene="cliffhanger", flags=dict(flags))

        game._cliffhanger()
        game._show_ending()
        return game.state, "\n".join(output)


if __name__ == "__main__":
    unittest.main()
