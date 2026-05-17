"""Integration tests — run the DSP pipeline against a real audio file."""

from __future__ import annotations

from pathlib import Path

import pytest

from model.audio_file import AudioFile
from model.feature_extractor import FeatureExtractor

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
SINE_WAV = FIXTURE_DIR / "sine_440.wav"


class TestEndToEnd:
    """Full pipeline: load a real WAV → extract features → verify."""

    @pytest.fixture
    def extractor(self) -> FeatureExtractor:
        return FeatureExtractor()

    def test_sine_wav_exists(self) -> None:
        """The synthetic fixture file must be present."""
        assert SINE_WAV.exists(), (
            f"Fixture not found at {SINE_WAV}. Run `python tests/fixtures/generate_wav.py` first."
        )

    def test_full_pipeline_on_sine_wav(self, extractor: FeatureExtractor) -> None:
        """Load a real WAV file and verify the DSP output.

        The 440 Hz sine produces a detectable tempo and a key
        (mostly centered on chroma bin corresponding to A).
        """
        audio = AudioFile()
        assert audio.load_audio(str(SINE_WAV)), "Failed to load WAV fixture"

        features = extractor.extract_all_features(audio)

        assert "error" not in features, f"Pipeline returned error: {features.get('error')}"
        assert isinstance(features["tempo"], float)
        assert features["tempo"] > 0, f"Expected positive tempo, got {features['tempo']}"
        assert isinstance(features["key"], str)
        assert "Desconocida" not in features["key"]
        # Chromagram should have the expected shape
        assert features["chroma"].shape[0] == 12
        assert features["chroma"].ndim == 2
        # Spectrogram should be 2D
        assert features["D"].ndim == 2

    def test_pipeline_rejects_unloaded_audio(self, extractor: FeatureExtractor) -> None:
        """Calling extract without loading should return an error."""
        audio = AudioFile()
        result = extractor.extract_all_features(audio)
        assert "error" in result
