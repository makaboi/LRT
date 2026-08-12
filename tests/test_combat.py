import random
import unittest

from roads_beneath_shadow.combat import CombatEngine, CombatResult
from roads_beneath_shadow.content import ORIGINS
from roads_beneath_shadow.models import Character, Enemy, GameState
from roads_beneath_shadow.ui import TerminalUI


class CombatTests(unittest.TestCase):
    def test_attack_can_win_encounter(self) -> None:
        answers = iter(["1"])
        output: list[str] = []
        ui = TerminalUI(color=False, fast=True, input_fn=lambda _: next(answers), output_fn=output.append)
        state = GameState(Character.from_origin("Arin", ORIGINS[0]))
        enemy = Enemy("Practice Orc", 1, 1, 1, 1)

        result = CombatEngine(ui, random.Random(4)).run(state, [enemy])

        self.assertEqual(result, CombatResult.VICTORY)
        self.assertTrue(state.character.alive)
        self.assertEqual(enemy.hp, 0)

    def test_healing_item_recovers_health(self) -> None:
        answers = iter(["1"])
        output: list[str] = []
        ui = TerminalUI(color=False, fast=True, input_fn=lambda _: next(answers), output_fn=output.append)
        state = GameState(Character.from_origin("Arin", ORIGINS[0]))
        state.character.hp = 5
        engine = CombatEngine(ui, random.Random(1))

        consumed_turn = engine.use_item(state)

        self.assertTrue(consumed_turn)
        self.assertEqual(state.character.hp, 14)
        self.assertNotIn("healing_herb", state.character.inventory)

    def test_player_can_change_target_without_spending_turn(self) -> None:
        answers = iter(["6", "2", "1", "1"])
        output: list[str] = []
        ui = TerminalUI(color=False, fast=True, input_fn=lambda _: next(answers), output_fn=output.append)
        state = GameState(Character.from_origin("Arin", ORIGINS[0]))
        first = Enemy("First Orc", 1, 1, 1, 1)
        second = Enemy("Second Orc", 1, 1, 1, 1)

        result = CombatEngine(ui, random.Random(2)).run(state, [first, second])

        self.assertEqual(result, CombatResult.VICTORY)
        self.assertTrue(any("attention to Second Orc" in line for line in output))


if __name__ == "__main__":
    unittest.main()
