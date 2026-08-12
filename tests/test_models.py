import unittest

from roads_beneath_shadow.content import ITEMS, ORIGINS
from roads_beneath_shadow.models import Character, GameState


class CharacterTests(unittest.TestCase):
    def test_origin_builds_inventory_and_equipment(self) -> None:
        character = Character.from_origin("Arin", ORIGINS[0])

        self.assertEqual(character.hp, character.max_hp)
        self.assertEqual(character.weapon, "ash_staff")
        self.assertEqual(character.armor, "patched_leather")
        self.assertEqual(character.inventory["healing_herb"], 1)

    def test_every_origin_exposes_a_distinct_combat_ability(self) -> None:
        self.assertEqual(
            {origin.ability_id for origin in ORIGINS},
            {"stand_fast", "flanking_strike", "field_remedy"},
        )
        self.assertTrue(all(origin.ability_name and origin.ability_description for origin in ORIGINS))

    def test_inventory_can_equip_and_consume_items(self) -> None:
        character = Character.from_origin("Arin", ORIGINS[0])
        character.add_item("orc_cleaver")
        character.equip(ITEMS["orc_cleaver"])

        self.assertEqual(character.weapon, "orc_cleaver")
        self.assertTrue(character.remove_item("healing_herb"))
        self.assertNotIn("healing_herb", character.inventory)

    def test_state_round_trip_preserves_consequences(self) -> None:
        state = GameState(Character.from_origin("Arin", ORIGINS[2]))
        state.flags["found_ranger_cipher"] = True
        state.add_quest("Find the third stone")
        state.character.corruption = 2

        restored = GameState.from_dict(state.to_dict())

        self.assertEqual(restored.character.name, "Arin")
        self.assertEqual(restored.character.corruption, 2)
        self.assertTrue(restored.flags["found_ranger_cipher"])
        self.assertEqual(restored.quests, ["Find the third stone"])


if __name__ == "__main__":
    unittest.main()
