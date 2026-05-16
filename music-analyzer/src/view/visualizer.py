"""Matplotlib-based visualisation widgets for audio analysis.

Provides an inheritance hierarchy:

- :class:`BaseVisualizer` — abstract widget with a Matplotlib canvas.
- :class:`SpectrogramVisualizer` — power spectrogram (dB).
- :class:`KeyVisualizer` — normalised chromagram.

Each subclass implements :meth:`draw_data` **polymorphically**.
"""

from __future__ import annotations

from typing import Any

import librosa.display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QVBoxLayout, QWidget


class BaseVisualizer(QWidget):
    """Abstract widget that hosts a Matplotlib figure and toolbar.

    Subclasses **must** override :meth:`draw_data`.

    Args:
        title: Plot title displayed above the axes.
    """

    def __init__(self, title: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.title = title

        self.figure, self.ax = plt.subplots(1, 1, figsize=(4, 3))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.ax.set_title(self.title)
        self.ax.set_axis_off()

    def clear_plot(self) -> None:
        """Clear the current axes and redraw the empty canvas."""
        self.ax.clear()
        self.ax.set_title(self.title)
        self.ax.set_axis_off()
        self.canvas.draw()

    def draw_data(self, data: Any) -> None:
        """Render *data* onto the canvas.

        Raises:
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError(
            "draw_data() debe ser implementado por la subclase."
        )


class SpectrogramVisualizer(BaseVisualizer):
    """Displays a power spectrogram (dB) over time.

    Uses ``librosa.display.specshow`` with a logarithmic frequency axis
    and the ``magma`` colour map.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(title="Espectrograma de Potencia (dB)", **kwargs)

    def draw_data(self, features: dict[str, Any]) -> None:
        """Render the spectrogram from *features['D']*.

        Args:
            features: Dictionary with keys ``D`` (spectrogram matrix),
                      ``sr`` (sample rate).
        """
        self.ax.clear()

        spec_data: Any = features["D"]
        sr: int = features["sr"]

        img = librosa.display.specshow(
            spec_data,
            sr=sr,
            x_axis="time",
            y_axis="log",
            ax=self.ax,
            cmap="magma",
            hop_length=512,
        )

        self.ax.set_title(self.title)
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Frecuencia (Hz)")

        if img:
            cbar = self.figure.colorbar(img, format="%+2.0f dB", ax=self.ax)
            cbar.ax.set_ylabel("Amplitud (dB)", rotation=270, labelpad=15)

        self.canvas.draw()


class KeyVisualizer(BaseVisualizer):
    """Displays a normalised chromagram (pitch-class distribution).

    The y-axis shows the 12 chroma bins (``C`` … ``B``) and the colour
    map uses ``viridis``.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(title="Cromagrama Normalizado (Tonalidad)", **kwargs)
        self.chromas: list[str] = [
            "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
        ]

    def draw_data(self, features: dict[str, Any]) -> None:
        """Render the chromagram from *features['chroma']*.

        Args:
            features: Dictionary with keys ``chroma`` (12×n array),
                      ``sr`` (sample rate).
        """
        self.ax.clear()

        chroma: Any = features["chroma"]
        sr: int = features["sr"]

        img = librosa.display.specshow(
            chroma,
            sr=sr,
            y_axis="chroma",
            x_axis="time",
            ax=self.ax,
            cmap="viridis",
        )

        self.ax.set_title(self.title)
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Clase de Tono")

        if img:
            self.figure.colorbar(img, ax=self.ax)

        self.canvas.draw()
