"""Shared fixtures for the test suite."""

from __future__ import annotations

import os
import sys
from typing import Any
from unittest.mock import MagicMock

import numpy as np
import pytest

# Ensure the ``src/`` directory is on the module path so that
# production imports (``from model.xxx``, ``from config import ...``)
# resolve correctly during tests.
_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
if _src not in sys.path:
    sys.path.insert(0, _src)


@pytest.fixture
def sine_wav() -> np.ndarray:
    """Generate a 2-second 440 Hz sine wave at 22 050 Hz sample rate.

    Useful for integration-testing the DSP pipeline without real audio
    files.
    """
    sr = 22050
    duration = 2.0
    t = np.linspace(0.0, duration, int(sr * duration), endpoint=False)
    return np.sin(2.0 * np.pi * 440.0 * t).astype(np.float32)


@pytest.fixture
def mock_librosa_load() -> MagicMock:
    """Return a ``MagicMock`` that stands in for ``librosa.load``.

    The mock returns ``(np.ndarray, int)`` — a 1-second silent array
    at 22 050 Hz — so that ``AudioFile.load_audio`` can be tested
    without touching the filesystem.
    """
    mock = MagicMock()
    mock.return_value = (np.zeros(22050, dtype=np.float32), 22050)
    return mock


@pytest.fixture
def valid_features() -> dict[str, Any]:
    """Return a realistic feature dictionary as produced by the DSP pipeline."""
    return {
        "path": "/music/test.wav",
        "tempo": 120.0,
        "key": "C Mayor",
        "D": np.random.rand(128, 100),
        "chroma": np.random.rand(12, 100),
        "y": np.zeros(22050, dtype=np.float32),
        "sr": 22050,
        "times": np.linspace(0, 5, 100),
    }
