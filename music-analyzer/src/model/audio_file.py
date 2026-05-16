"""Audio file data encapsulation.

Provides the :class:`AudioFile` class which wraps a loaded audio signal
and its sample rate behind a controlled API (encapsulation pattern).
"""

from __future__ import annotations

import logging
from typing import Any

import librosa
import numpy as np

logger = logging.getLogger(__name__)


class AudioFile:
    """Encapsulates the raw audio signal and sample rate of a loaded file.

    Attributes are kept private (``_y``, ``_sr``) and exposed through
    getter methods.  A feature cache is maintained so that analysis
    results can be reused without re-computation.
    """

    def __init__(self) -> None:
        self._path: str | None = None
        self._y: np.ndarray | None = None  # Audio signal (protected)
        self._sr: int | None = None  # Sample rate (protected)
        self._features_cache: dict[str, Any] = {}

    def load_audio(self, path: str) -> bool:
        """Load an audio file via ``librosa.load``.

        Args:
            path: Absolute or relative path to a supported audio file
                  (``.mp3``, ``.wav``, ``.flac``, etc.).

        Returns:
            ``True`` on success, ``False`` if loading failed.
        """
        self._path = path
        self._features_cache = {}
        try:
            y, sr = librosa.load(path, sr=None, mono=True)
            self._y = y
            self._sr = int(sr)
            logger.info("Loaded audio: %s (%d samples @ %d Hz)", path, len(self._y), self._sr)
            return True
        except Exception as exc:
            logger.error("Failed to load audio: %s", exc, exc_info=True)
            self._y = None
            self._sr = None
            return False

    # ------------------------------------------------------------------
    # Getters  (encapsulation)
    # ------------------------------------------------------------------

    def get_signal(self) -> np.ndarray | None:
        """Return the raw audio signal array, or ``None`` if not loaded."""
        return self._y

    def get_sample_rate(self) -> int | None:
        """Return the sample rate in Hz, or ``None`` if not loaded."""
        return self._sr

    def get_path(self) -> str | None:
        """Return the file path of the loaded audio, or ``None``."""
        return self._path

    def get_features_cache(self) -> dict[str, Any]:
        """Return the internal feature cache dictionary."""
        return self._features_cache

    def set_features_cache(self, features: dict[str, Any]) -> None:
        """Replace the internal feature cache with *features*."""
        self._features_cache = features
