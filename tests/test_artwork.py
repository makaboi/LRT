import unittest
import textwrap

from roads_beneath_shadow import artwork


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
                self.assertGreaterEqual(density, 0.18)
                self.assertLessEqual(density, 0.55)

    def test_action_art_preserves_recognition_landmarks(self) -> None:
        # These landmarks encode the simple visual grammar used by the sprites:
        # O heads for heroes, pointed ears and tusks for Orcs, detached weapons,
        # canine ears and teeth for the warg, and a full cloaked Rider.
        self.assertEqual(artwork.ORC_ATTACK_ART.count("/^^\\"), 3)
        self.assertIn("X", artwork.ORC_ATTACK_ART)
        self.assertIn("O", artwork.ORC_ATTACK_ART)

        self.assertIn("/^^^^\\", artwork.ORC_TRACKER_INTRO_ART)
        self.assertIn("V  V", artwork.ORC_TRACKER_INTRO_ART)
        self.assertIn("===========>", artwork.ORC_TRACKER_INTRO_ART)

        self.assertGreaterEqual(artwork.MARSH_WARG_INTRO_ART.count("/\\"), 2)
        self.assertIn("/ o\\", artwork.MARSH_WARG_INTRO_ART)
        self.assertIn("/o \\", artwork.MARSH_WARG_INTRO_ART)
        self.assertIn("V V V V", artwork.MARSH_WARG_INTRO_ART)

        self.assertIn("/^^^^\\", artwork.GHORAK_ASH_HAND_INTRO_ART)
        self.assertIn("(@)", artwork.GHORAK_ASH_HAND_INTRO_ART)
        self.assertIn("o======\\_______________", artwork.GHORAK_ASH_HAND_INTRO_ART)

        self.assertGreaterEqual(artwork.FINAL_RUINS_BATTLE_ART.count("O"), 3)
        self.assertIn("/^^\\", artwork.FINAL_RUINS_BATTLE_ART)
        self.assertIn("*", artwork.FINAL_RUINS_BATTLE_ART)

        for frame in artwork.BLACK_RIDER_CLIFFHANGER_FRAMES:
            with self.subTest(frame=frame.strip().splitlines()[0]):
                self.assertIn("##___##", frame)
                self.assertIn("o================>", frame)
                self.assertIn("/ # | # \\", frame)

    def test_animated_accents_have_exactly_two_frames(self) -> None:
        self.assertEqual(len(artwork.PRANCING_PONY_EXTERIOR_FRAMES), 2)
        self.assertEqual(len(artwork.BLACK_RIDER_CLIFFHANGER_FRAMES), 2)
        self.assertEqual(artwork.PRANCING_PONY_EXTERIOR_ART.frames, artwork.PRANCING_PONY_EXTERIOR_FRAMES)
        self.assertEqual(artwork.BLACK_RIDER_CLIFFHANGER_ART.frames, artwork.BLACK_RIDER_CLIFFHANGER_FRAMES)


if __name__ == "__main__":
    unittest.main()
