import unittest
import textwrap

from roads_beneath_shadow import artwork


class SparseAsciiSpriteTests(unittest.TestCase):
    def test_sparse_sprite_wrapper_rejects_unportable_or_oversized_art(self) -> None:
        with self.assertRaisesRegex(ValueError, "portable ASCII"):
            artwork._named_ascii_art("orc é", "ORC")
        with self.assertRaisesRegex(ValueError, "64-column"):
            artwork._named_ascii_art("X" * 65, "ORC")
        with self.assertRaisesRegex(ValueError, "64-column"):
            artwork._named_ascii_art("X\tX", "ORC")

    def test_sparse_sprite_bodies_are_unlabeled_and_bounded(self) -> None:
        sprites = (
            (artwork.ORC_ATTACK_SPRITE, "ORC ATTACK"),
            (artwork.ORC_TRACKER_SPRITE, "ORC TRACKER"),
            (artwork.MARSH_WARG_SPRITE, "MARSH WARG"),
            (artwork.GHORAK_ASH_HAND_SPRITE, "GHORAK"),
            (artwork.FINAL_RUINS_BATTLE_SPRITE, "FINAL BATTLE"),
            (artwork.BLACK_RIDER_SPRITE, "BLACK RIDER"),
            (artwork.BLACK_RIDER_DIM_SPRITE, "BLACK RIDER"),
        )
        for sprite, forbidden_label in sprites:
            with self.subTest(label=forbidden_label):
                lines = textwrap.dedent(sprite).strip("\n").splitlines()
                self.assertLessEqual(max(map(len, lines)), 64)
                self.assertLessEqual(len(lines), 16)
                self.assertTrue(sprite.isascii())
                self.assertNotIn(forbidden_label, sprite)

    def test_warg_keeps_canine_face_cues_in_vertical_order(self) -> None:
        lines = textwrap.dedent(artwork.MARSH_WARG_SPRITE).strip("\n").splitlines()
        eyes = next(index for index, line in enumerate(lines) if "o       o" in line)
        nose = next(index for index, line in enumerate(lines) if "@@" in line)
        fangs = next(index for index, line in enumerate(lines) if "V  V  V" in line)
        self.assertLess(eyes, nose)
        self.assertLess(nose, fangs)
        self.assertIn("/\\", lines[0])
        self.assertIn("/\\", lines[0][20:])

    def test_rider_separates_humanoid_horse_and_four_legs(self) -> None:
        sprite = artwork.BLACK_RIDER_SPRITE
        self.assertIn(".-^^^^-.", sprite)
        self.assertIn("/ o    o \\", sprite)
        self.assertIn("/\\", sprite)
        self.assertIn("o   \\", sprite)
        self.assertEqual(sprite.count("_/       \\_"), 2)
        self.assertNotIn("#", sprite)

    def test_three_orc_attackers_have_separate_anatomy_and_weapons(self) -> None:
        sprite = artwork.ORC_ATTACK_SPRITE
        self.assertEqual(sprite.count("_<o  o>_"), 3)
        self.assertEqual(sprite.count("|[]|"), 3)
        self.assertEqual(sprite.count("|__|"), 3)
        self.assertIn("<____/ \\____>", sprite)
        self.assertIn("/)" , sprite)
        self.assertIn("(\\", sprite)

    def test_tracker_is_one_biped_holding_one_continuous_spear(self) -> None:
        sprite = artwork.ORC_TRACKER_SPRITE
        self.assertEqual(sprite.count("_<o  o>_"), 1)
        self.assertIn("(|____|)", sprite)
        self.assertIn("<===============", sprite)
        self.assertIn("===============================|>", sprite)
        self.assertIn("_/ /\\ \\_", sprite)

    def test_ghorak_is_a_single_armored_warlord_with_a_detached_cleaver(self) -> None:
        sprite = artwork.GHORAK_ASH_HAND_SPRITE
        self.assertEqual(sprite.count("<| o   |  o |>"), 1)
        self.assertIn("V  V", sprite)
        self.assertIn("||||||", sprite)
        self.assertIn("(@)===|______________________\\", sprite)

    def test_finale_separates_one_large_boss_from_three_small_heroes(self) -> None:
        sprite = artwork.FINAL_RUINS_BATTLE_SPRITE
        self.assertEqual(sprite.count("O"), 3)
        self.assertIn("<|  o       o  |>", sprite)
        self.assertIn("^^^^^^^", sprite)
        self.assertIn("=====================================>", sprite)
        # The three hero heads occupy separate columns instead of merging into
        # a multi-headed creature or sharing one body.
        head_columns = [line.index("O") for line in sprite.splitlines() if "O" in line]
        self.assertEqual(len(head_columns), 2)
        self.assertEqual(sum(line.count("O") for line in sprite.splitlines()), 3)


class ArtworkDirectionTests(unittest.TestCase):
    def test_scene_art_uses_a_cinematic_terminal_stage(self) -> None:
        for name in dir(artwork):
            if not name.endswith("_ART"):
                continue
            with self.subTest(art=name):
                lines = textwrap.dedent(getattr(artwork, name)).strip("\n").splitlines()
                self.assertLessEqual(max(map(len, lines)), 64)

    def test_major_scenes_have_room_for_foreground_and_background(self) -> None:
        major_scenes = (
            artwork.TITLE_ART_EXPANDED,
            artwork.PRANCING_PONY_EXTERIOR_ART,
            artwork.PRANCING_PONY_INTERIOR_ART,
            artwork.NORTH_WAYHOUSE_ART,
            artwork.ORC_ATTACK_ART,
            artwork.ORC_TRACKER_INTRO_ART,
            artwork.GHORAK_ASH_HAND_INTRO_ART,
            artwork.FINAL_RUINS_BATTLE_ART,
            artwork.BLACK_RIDER_CLIFFHANGER_ART,
        )
        for scene in major_scenes:
            with self.subTest(opening=scene.strip().splitlines()[0]):
                self.assertGreaterEqual(len(scene.strip("\n").splitlines()), 11)

    def test_character_splashes_use_short_retro_nameplates(self) -> None:
        expected_nameplates = (
            (artwork.ORC_ATTACK_ART, "[ ORC ATTACK ]"),
            (artwork.ORC_TRACKER_INTRO_ART, "[ ORC TRACKER ]"),
            (artwork.MARSH_WARG_INTRO_ART, "[ MARSH WARG ]"),
            (artwork.GHORAK_ASH_HAND_INTRO_ART, "[ GHORAK ASH-HAND ]"),
            (artwork.FINAL_RUINS_BATTLE_ART, "[ FINAL BATTLE ]"),
        )
        for art, nameplate in expected_nameplates:
            with self.subTest(nameplate=nameplate):
                self.assertIn(nameplate, art)
                self.assertLessEqual(len(nameplate), 24)
        for frame in artwork.BLACK_RIDER_CLIFFHANGER_FRAMES:
            self.assertIn("[ BLACK RIDER ]", frame)

    def test_art_remains_portable_ascii(self) -> None:
        art_values = (
            value
            for name, value in vars(artwork).items()
            if name.endswith("_ART") or name == "TITLE_ART_EXPANDED"
        )
        for value in art_values:
            with self.subTest(opening=value.strip().splitlines()[0]):
                self.assertTrue(value.isascii())

    def test_art_avoids_dense_shadow_wedges(self) -> None:
        art_values = (
            value
            for name, value in vars(artwork).items()
            if (name.endswith("_ART") or name == "TITLE_ART_EXPANDED")
            and isinstance(value, str)
        )
        for value in art_values:
            with self.subTest(opening=value.strip().splitlines()[0]):
                visible = [character for character in value if not character.isspace()]
                hash_ratio = value.count("#") / max(1, len(visible))
                self.assertLessEqual(hash_ratio, 0.12)
                self.assertNotIn("#######", value)

    def test_art_has_readable_negative_space(self) -> None:
        art_values = (
            value
            for name, value in vars(artwork).items()
            if (name.endswith("_ART") or name == "TITLE_ART_EXPANDED")
            and isinstance(value, str)
        )
        for value in art_values:
            with self.subTest(opening=value.strip().splitlines()[0]):
                lines = textwrap.dedent(value).strip("\n").splitlines()
                width = max(map(len, lines))
                ink = sum(not character.isspace() for line in lines for character in line)
                density = ink / (width * len(lines))
                minimum_density = 0.15 if value == artwork.MARSH_WARG_INTRO_ART else 0.18
                self.assertGreaterEqual(density, minimum_density)
                self.assertLessEqual(density, 0.55)

    def test_action_art_preserves_structural_landmarks(self) -> None:
        # Public art keeps the same raw silhouettes and adds only a compact
        # title. Human recognition is evaluated separately at rendered size.
        public_pairs = (
            (artwork.ORC_ATTACK_SPRITE, artwork.ORC_ATTACK_ART),
            (artwork.ORC_TRACKER_SPRITE, artwork.ORC_TRACKER_INTRO_ART),
            (artwork.GHORAK_ASH_HAND_SPRITE, artwork.GHORAK_ASH_HAND_INTRO_ART),
            (artwork.FINAL_RUINS_BATTLE_SPRITE, artwork.FINAL_RUINS_BATTLE_ART),
        )
        for raw_sprite, public_art in public_pairs:
            with self.subTest(opening=public_art.strip().splitlines()[0]):
                raw_body = textwrap.dedent(raw_sprite).strip("\n")
                self.assertIn(raw_body, public_art)

    def test_animated_accents_have_exactly_two_frames(self) -> None:
        self.assertEqual(len(artwork.PRANCING_PONY_EXTERIOR_FRAMES), 2)
        self.assertEqual(len(artwork.BLACK_RIDER_CLIFFHANGER_FRAMES), 2)
        self.assertEqual(artwork.PRANCING_PONY_EXTERIOR_ART.frames, artwork.PRANCING_PONY_EXTERIOR_FRAMES)
        self.assertEqual(artwork.BLACK_RIDER_CLIFFHANGER_ART.frames, artwork.BLACK_RIDER_CLIFFHANGER_FRAMES)
        dim_lines = artwork.BLACK_RIDER_STAR_DIM_ART.strip("\n").splitlines()
        bright_lines = artwork.BLACK_RIDER_CLIFFHANGER_STILL.strip("\n").splitlines()
        self.assertEqual(dim_lines[4:], bright_lines[4:])


if __name__ == "__main__":
    unittest.main()
