"""DSP feature extraction from audio signals.

The :class:`FeatureExtractor` hides the complexity of ``librosa`` behind
a simple ``extract_all_features()`` API (abstraction pattern).  Key detection
uses the **Krumhansl-Schmuckler** algorithm.
"""

from __future__ import annotations

import logging
from typing import Any

import librosa
import numpy as np

from config import CHROMA_NAMES, K_MAJOR, K_MINOR
from model.audio_file import AudioFile

logger = logging.getLogger(__name__)


class FeatureExtractor:
    """High-level DSP feature extraction.

    Uses ``librosa`` under the hood but exposes only intent-revealing
    methods so that callers never touch the DSP library directly.
    """

    def _determine_key(self, chroma_mean: np.ndarray) -> str:
        """Determine the musical key from a normalised chroma vector.

        Implements the **Krumhansl-Schmuckler** algorithm: the 12-bin
        chroma profile is correlated against rotated major and minor
        templates; the rotation with the highest score wins.

        Args:
            chroma_mean: 12-element array of mean chroma energy.

        Returns:
            A string like ``"C Mayor"`` or ``"A Menor"``.
        """
        chroma_mean = chroma_mean / np.sum(chroma_mean)  # normalise

        best_match: float = -1.0
        best_key: str = "Desconocida"

        for i in range(12):
            major_score = float(np.dot(chroma_mean, np.roll(K_MAJOR, i)))
            minor_score = float(np.dot(chroma_mean, np.roll(K_MINOR, i)))

            if major_score > best_match:
                best_match = major_score
                best_key = f"{CHROMA_NAMES[i]} Mayor"

            if minor_score > best_match:
                best_match = minor_score
                best_key = f"{CHROMA_NAMES[i]} Menor"

        return best_key

    def extract_all_features(self, audio_file: AudioFile) -> dict[str, Any]:
        """Run the full DSP pipeline on a loaded audio file.

        Extracts **tempo** (BPM), **musical key**, an STFT-based
        **spectrogram** (in dB), and a **chromagram**.

        Args:
            audio_file: An already-loaded :class:`AudioFile` instance.

        Returns:
            A dictionary with keys ``path``, ``tempo``, ``key``, ``D``,
            ``chroma``, ``sr``, and ``times`` — or ``{"error": ...}`` if
            no audio is loaded.
        """
        y = audio_file.get_signal()
        sr = audio_file.get_sample_rate()

        if y is None or sr is None:
            logger.warning("extract_all_features called with no audio loaded")
            return {"error": "Archivo de audio no cargado."}

        logger.info("Starting DSP pipeline on %s", audio_file.get_path())

        # 1. Tempo (BPM)
        # Use the modern API path (librosa >= 0.10).  Fall back to the
        # old path for very old installations.
        try:
            (tempo,) = librosa.feature.rhythm.tempo(y=y, sr=sr)  # type: ignore[attr-defined]
        except AttributeError:
            (tempo,) = librosa.beat.tempo(y=y, sr=sr)

        # 2. Key (chroma-based)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        key = self._determine_key(chroma_mean)

        # 3. Power spectrogram
        spec_db = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        times = librosa.times_like(spec_db, sr=sr)

        features: dict[str, Any] = {
            "path": audio_file.get_path(),
            "tempo": float(tempo),
            "key": key,
            "D": spec_db,
            "chroma": chroma,
            "y": y,  # raw signal for waveform visualization
            "sr": sr,
            "times": times,
        }

        audio_file.set_features_cache(features)
        logger.info("DSP pipeline complete — BPM=%.1f, Key=%s", tempo, key)
        return features
