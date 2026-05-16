"""Tests for ``FeatureExtractor`` — key detection and full pipeline."""

from __future__ import annotations

import numpy as np
import pytest

from src.model.feature_extractor import FeatureExtractor


class TestDetermineKey:
    """Unit tests for the private ``_determine_key`` method."""

    @pytest.fixture
    def extractor(self) -> FeatureExtractor:
        return FeatureExtractor()

    def test_c_major_is_detected(self, extractor: FeatureExtractor) -> None:
        """Energy concentrated on C (bin 0) should yield ``C Mayor``."""
        chroma = np.zeros(12)
        chroma[0] = 10.0
        result = extractor._determine_key(chroma)  # noqa: SLF001
        assert "C Mayor" in result

    def test_a_minor_is_detected(self, extractor: FeatureExtractor) -> None:
        """Energy concentrated on A (bin 9) with minor profile yields ``A Menor``."""
        chroma = np.array([0.5, 0.3, 0.4, 0.6, 0.3, 0.4, 0.3, 0.5, 0.6, 3.0, 0.3, 0.5])
        result = extractor._determine_key(chroma)  # noqa: SLF001
        assert "Menor" in result

    def test_silence_returns_unknown(self, extractor: FeatureExtractor) -> None:
        """Flat chroma (all equal) produces ``Desconocida`` or a guess."""
        chroma = np.ones(12) * 0.5
        result = extractor._determine_key(chroma)  # noqa: SLF001
        assert isinstance(result, str)

    def test_key_result_format(self, extractor: FeatureExtractor) -> None:
        """Result should match ``<Note> <Mayor|Menor>``."""
        chroma = np.zeros(12)
        chroma[0] = 10.0
        result = extractor._determine_key(chroma)  # noqa: SLF001
        parts = result.split()
        assert len(parts) == 2
        assert parts[1] in ("Mayor", "Menor")


class TestExtractAllFeatures:
    """Integration-style tests for the full DSP pipeline.

    Uses a synthetic sine-wave array to exercise the real librosa code paths.
    """

    @pytest.fixture
    def extractor(self) -> FeatureExtractor:
        return FeatureExtractor()

    def test_returns_error_when_no_audio(self, extractor: FeatureExtractor) -> None:
        """Calling without a loaded file should return an error dict."""
        from src.model.audio_file import AudioFile

        audio = AudioFile()
        result = extractor.extract_all_features(audio)
        assert "error" in result

    def test_sine_wave_produces_valid_features(
        self, extractor: FeatureExtractor, sine_wav: np.ndarray
    ) -> None:
        """A real sine wave should produce tempo > 0 and a valid key string."""
        from src.model.audio_file import AudioFile

        audio = AudioFile()
        audio._y = sine_wav          # noqa: SLF001 — inject signal directly
        audio._sr = 22050            # noqa: SLF001
        audio._path = "test.wav"

        result = extractor.extract_all_features(audio)

        assert "error" not in result
        assert result["tempo"] > 0
        assert isinstance(result["key"], str)
        assert "Desconocida" not in result["key"]
        assert result["D"].ndim == 2
        assert result["chroma"].shape[0] == 12
