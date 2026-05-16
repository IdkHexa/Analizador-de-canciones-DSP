"""Tests for ``AudioFile`` — loading, error handling, and getters."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np

from model.audio_file import AudioFile


class TestLoadAudio:
    """Tests for ``AudioFile.load_audio`` with mocked ``librosa.load``."""

    @patch("model.audio_file.librosa.load")
    def test_successful_load_returns_true(self, mock_load: MagicMock) -> None:
        """When librosa.load succeeds, ``load_audio`` returns ``True``."""
        mock_load.return_value = (np.array([0.1] * 1000, dtype=np.float32), 22050)

        audio = AudioFile()
        result = audio.load_audio("test.wav")

        assert result is True
        assert audio.get_signal() is not None
        assert audio.get_sample_rate() == 22050
        assert audio.get_path() == "test.wav"

    @patch("model.audio_file.librosa.load")
    def test_failed_load_returns_false(self, mock_load: MagicMock) -> None:
        """When librosa.load raises, ``load_audio`` returns ``False``."""
        mock_load.side_effect = FileNotFoundError("File not found")

        audio = AudioFile()
        result = audio.load_audio("nonexistent.wav")

        assert result is False
        assert audio.get_signal() is None
        assert audio.get_sample_rate() is None

    @patch("model.audio_file.librosa.load")
    def test_caches_are_cleared_on_reload(self, mock_load: MagicMock) -> None:
        """Loading a second file clears the previous features cache."""
        mock_load.return_value = (np.zeros(1000, dtype=np.float32), 22050)

        audio = AudioFile()
        audio.set_features_cache({"old": "data"})
        audio.load_audio("second.wav")

        assert audio.get_features_cache() == {}


class TestGetters:
    """Getter behaviour when no file is loaded."""

    def test_default_state(self) -> None:
        audio = AudioFile()
        assert audio.get_signal() is None
        assert audio.get_sample_rate() is None
        assert audio.get_path() is None
        assert audio.get_features_cache() == {}
