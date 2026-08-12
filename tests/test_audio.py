import unittest
from unittest import mock

from roads_beneath_shadow.audio import SoundPlayer


class SoundPlayerTests(unittest.TestCase):
    def test_every_original_cue_is_packaged(self) -> None:
        self.assertEqual(SoundPlayer.missing_cues(), [])

    def test_missing_platform_player_is_a_safe_noop(self) -> None:
        player = SoundPlayer()
        player._player = None
        self.assertFalse(player.play("danger"))

    def test_known_cue_uses_nonblocking_platform_player(self) -> None:
        player = SoundPlayer()
        player._player = "/usr/bin/afplay"
        with mock.patch("roads_beneath_shadow.audio.subprocess.Popen") as popen:
            self.assertTrue(player.play("victory"))
        command = popen.call_args.args[0]
        self.assertEqual(command[0], "/usr/bin/afplay")
        self.assertTrue(command[1].endswith("victory.wav"))


if __name__ == "__main__":
    unittest.main()
