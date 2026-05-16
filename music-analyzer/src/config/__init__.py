"""Centralized configuration for the Music Analyzer application.

This module contains all hardcoded constants, DSP profiles, UI styles,
and application settings. Import these values instead of defining them
inline in domain modules.
"""

from typing import Final

import numpy as np

# ---------------------------------------------------------------------------
# Krumhansl-Schmuckler key detection profiles
# ---------------------------------------------------------------------------

K_MAJOR: Final[np.ndarray] = np.array(
    [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
)
"""Krumhansl-Schmuckler major key profile (12 chroma bins)."""

K_MINOR: Final[np.ndarray] = np.array(
    [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
)
"""Krumhansl-Schmuckler minor key profile (12 chroma bins)."""

CHROMA_NAMES: Final[list[str]] = [
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
]
"""Names of the 12 pitch classes in order, starting from C."""

# ---------------------------------------------------------------------------
# UI / Window settings
# ---------------------------------------------------------------------------

WINDOW_TITLE: Final[str] = "Analizador de Canciones DSP (PySide6 MVC)"
WINDOW_MIN_WIDTH: Final[int] = 1000
WINDOW_MIN_HEIGHT: Final[int] = 650
CONTROL_PANEL_WIDTH: Final[int] = 350

# ---------------------------------------------------------------------------
# Audio analysis defaults
# ---------------------------------------------------------------------------

AUDIO_FILE_PATTERNS: Final[str] = "Audio Files (*.mp3 *.wav *.flac)"
"""QFileDialog filter string for supported audio formats."""

# ---------------------------------------------------------------------------
# UI styles (Qt stylesheets)
# ---------------------------------------------------------------------------

STYLE_FILEPATH_LABEL: Final[str] = """
    QLabel {
        padding: 10px;
        background-color: #2b2b2b;
        border-radius: 5px;
        color: #ffffff;
    }
"""

STYLE_SUMMARY_OUTPUT: Final[str] = """
    QLabel {
        padding: 15px;
        background-color: #1e1e1e;
        border: 1px solid #3d3d3d;
        border-radius: 5px;
        color: #ffffff;
        font-size: 12pt;
        line-height: 1.8;
    }
"""

STYLE_STATUS_OK: Final[str] = "color: green; font-weight: bold; padding: 5px;"
STYLE_STATUS_WARN: Final[str] = "color: orange; font-weight: bold; padding: 5px;"
STYLE_STATUS_ERROR: Final[str] = "color: red; font-weight: bold; padding: 5px;"
STYLE_STATUS_INFO: Final[str] = "color: blue; font-weight: bold; padding: 5px;"

# ---------------------------------------------------------------------------
# Summary display icons
# ---------------------------------------------------------------------------

SUMMARY_ICONS: Final[dict[str, str]] = {
    "File": "📁",
    "BPM": "🎵",
    "Key": "🎹",
}
