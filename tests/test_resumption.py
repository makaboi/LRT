import random
import tempfile
import unittest
from pathlib import Path

from roads_beneath_shadow.app import Game
from roads_beneath_shadow.content import ORIGINS
from roads_beneath_shadow.models import Character, GameState
from roads_beneath_shadow.savegame import SaveManager
from roads_beneath_shadow.ui import TerminalUI


class ResumptionTests(unittest.TestCase):
    def test_aftermath_reward_is_idempotent_across_save_load(self) -> None:
        output: list[str] = []
        with tempfile.TemporaryDirectory() as temporary:
            saves = SaveManager(Path(temporary))
            state = GameState(Character.from_origin("Arin", ORIGINS[0]), scene="aftermath")
            state.character.hp = 5
            first_ui = TerminalUI(color=False, fast=True, input_fn=lambda _: "m", output_fn=output.append)
            first = Game(first_ui, saves=saves, rng=random.Random(1))
            first.state = state

            self.assertFalse(first._aftermath())
            hp_after_setup = state.character.hp
            self.assertTrue(state.flags["aftermath_setup"])
            saves.save(1, state)

            resumed_state = saves.load(1)
            second_ui = TerminalUI(color=False, fast=True, input_fn=lambda _: "m", output_fn=output.append)
            second = Game(second_ui, saves=saves, rng=random.Random(1))
            second.state = resumed_state

            self.assertFalse(second._aftermath())
            self.assertEqual(resumed_state.character.hp, hp_after_setup)
            self.assertEqual(resumed_state.character.inventory["orc_cleaver"], 1)

    def test_cliffhanger_consequences_are_idempotent_across_reentry(self) -> None:
        output: list[str] = []
        state = GameState(Character.from_origin("Arin", ORIGINS[0]), scene="cliffhanger")
        state.character.hope = 3
        state.character.mara_trust = 2
        state.character.tobin_trust = 2
        state.flags.update({"defeated_ghorak": True, "ned_survived": True})
        game = Game(
            TerminalUI(color=False, fast=True, input_fn=lambda _: "2", output_fn=output.append),
            rng=random.Random(2),
        )
        game.state = state

        game._cliffhanger()
        minutes_after_first_resolution = state.play_minutes
        journal_after_first_resolution = list(state.journal)
        quests_after_first_resolution = list(state.quests)
        ending_after_first_resolution = state.ending

        game._cliffhanger()

        self.assertEqual(state.play_minutes, minutes_after_first_resolution)
        self.assertEqual(state.journal, journal_after_first_resolution)
        self.assertEqual(state.quests, quests_after_first_resolution)
        self.assertEqual(state.ending, ending_after_first_resolution)
        self.assertTrue(state.flags["cliffhanger_resolved"])


if __name__ == "__main__":
    unittest.main()
