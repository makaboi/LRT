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

    def test_art_contains_no_embedded_scene_captions(self) -> None:
        captions = (
            "PRANCING PONY",
            "ORC TRACKER",
            "MARSH WARG",
            "GHORAK",
            "BLACK RIDER",
            "BREE",
            "NORTH GATE",
            "MIDGEWATER",
            "ROAD BELOW",
        )
        combined = "\n".join(
            value
            for name, value in vars(artwork).items()
            if (name.endswith("_ART") or name == "TITLE_ART_EXPANDED")
            and isinstance(value, str)
        )
        for caption in captions:
            with self.subTest(caption=caption):
                self.assertNotIn(caption, combined.upper())

    def test_art_remains_portable_ascii(self) -> None:
        art_values = (
            value
            for name, value in vars(artwork).items()
            if name.endswith("_ART") or name == "TITLE_ART_EXPANDED"
        )
        for value in art_values:
            with self.subTest(opening=value.strip().splitlines()[0]):
                self.assertTrue(value.isascii())

    def test_animated_accents_have_exactly_two_frames(self) -> None:
        self.assertEqual(len(artwork.PRANCING_PONY_EXTERIOR_FRAMES), 2)
        self.assertEqual(len(artwork.BLACK_RIDER_CLIFFHANGER_FRAMES), 2)
        self.assertEqual(artwork.PRANCING_PONY_EXTERIOR_ART.frames, artwork.PRANCING_PONY_EXTERIOR_FRAMES)
        self.assertEqual(artwork.BLACK_RIDER_CLIFFHANGER_ART.frames, artwork.BLACK_RIDER_CLIFFHANGER_FRAMES)


if __name__ == "__main__":
    unittest.main()
