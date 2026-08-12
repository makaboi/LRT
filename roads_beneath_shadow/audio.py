"""Small optional sound-cue player with graceful terminal fallbacks."""

from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path


AUDIO_DIRECTORY = Path(__file__).with_name("audio_assets")


class SoundPlayer:
    """Play bundled, original cues without making audio a runtime requirement."""

    CUES = {
        "notice": "notice.wav",
        "danger": "danger.wav",
        "victory": "victory.wav",
        "discovery": "discovery.wav",
        "corruption": "corruption.wav",
    }

    def __init__(self) -> None:
        self._player = self._find_player()

    @staticmethod
    def _find_player() -> str | None:
        if platform.system() == "Darwin":
            return shutil.which("afplay")
        return None

    @property
    def available(self) -> bool:
        return self._player is not None and AUDIO_DIRECTORY.is_dir()

    @classmethod
    def missing_cues(cls) -> list[str]:
        """Return packaged cue names whose WAV data is unavailable."""

        return [cue for cue, filename in cls.CUES.items() if not (AUDIO_DIRECTORY / filename).is_file()]

    def play(self, cue: str) -> bool:
        filename = self.CUES.get(cue, self.CUES["notice"])
        path = AUDIO_DIRECTORY / filename
        if not self._player or not path.is_file():
            return False
        try:
            subprocess.Popen(
                [self._player, str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        except OSError:
            return False
        return True
