"""Main application window — the View layer.

Provides the :class:`MainWindow` (a :class:`QMainWindow`) with controls
on the left (load button, file info, scalar results, history list, status)
and Matplotlib-based visualisations on the right.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from config import (
    CONTROL_PANEL_WIDTH,
    STYLE_FILEPATH_LABEL,
    STYLE_STATUS_ERROR,
    STYLE_STATUS_INFO,
    STYLE_STATUS_OK,
    STYLE_STATUS_WARN,
    STYLE_SUMMARY_OUTPUT,
    SUMMARY_ICONS,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_TITLE,
)

from .visualizer import KeyVisualizer, SpectrogramVisualizer

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Desktop window for the Music Analyzer application.

    Signals
    -------
    signal_analyze_request:
        Emitted when the user clicks *Load & Analyse*.  Connected
        by the Controller to its :meth:`handle_analyze_request` slot.
    signal_history_item_selected(int):
        Emitted when the user clicks a past analysis entry in the
        history :class:`QListWidget`.
    """

    signal_analyze_request = Signal(str)
    signal_history_item_selected = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Cache of the latest feature dict (used for history restore)
        self._last_features: dict[str, Any] | None = None

        self.setup_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def setup_ui(self) -> None:
        """Build the entire window layout."""
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # ---- Left panel: controls & summary ----
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_panel.setFixedWidth(CONTROL_PANEL_WIDTH)

        self._build_control_area(control_layout)

        # ---- Right panel: graphs ----
        self._build_graph_area(main_layout)

        main_layout.addWidget(control_panel)
        self.setCentralWidget(central_widget)

    def _build_control_area(self, layout: QVBoxLayout) -> None:
        """Populate the left control panel."""
        # 1. Load button
        self.load_button = QPushButton("Cargar y Analizar Audio...")
        self.load_button.clicked.connect(self._on_load_clicked)
        self.load_button.setMinimumHeight(40)

        # 2. File path label
        self.filepath_label = QLabel("Archivo: Ninguno cargado.")
        self.filepath_label.setWordWrap(True)
        self.filepath_label.setStyleSheet(STYLE_FILEPATH_LABEL)

        # 3. Summary title
        summary_title = QLabel("--- Resultados Escalares ---")
        summary_title.setAlignment(Qt.AlignCenter)
        font_title = QFont()
        font_title.setBold(True)
        font_title.setPointSize(11)
        summary_title.setFont(font_title)

        # 4. Summary output
        self.summary_output = QLabel()
        self.summary_output.setWordWrap(True)
        self.summary_output.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.summary_output.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.summary_output.setStyleSheet(STYLE_SUMMARY_OUTPUT)
        self._set_default_summary()

        # 5. History section
        history_title = QLabel("--- Historial de Análisis ---")
        history_title.setAlignment(Qt.AlignCenter)
        history_title.setFont(font_title)

        self.history_list = QListWidget()
        self.history_list.setMaximumHeight(120)
        self.history_list.itemClicked.connect(self._on_history_clicked)

        # 6. Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        # 7. Status
        self.status_label = QLabel("Listo para cargar.")
        self.status_label.setStyleSheet(STYLE_STATUS_OK)

        # Assemble
        layout.addWidget(self.load_button)
        layout.addSpacing(10)
        layout.addWidget(self.filepath_label)
        layout.addSpacing(15)
        layout.addWidget(summary_title)
        layout.addSpacing(5)
        layout.addWidget(self.summary_output)
        layout.addSpacing(10)
        layout.addWidget(history_title)
        layout.addSpacing(5)
        layout.addWidget(self.history_list)
        layout.addStretch()
        layout.addWidget(line)
        layout.addWidget(self.status_label)

    def _build_graph_area(self, main_layout: QHBoxLayout) -> None:
        """Populate the right panel with Matplotlib canvases."""
        self.graph_container = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_container)

        self.spectrogram_viz = SpectrogramVisualizer()
        self.key_viz = KeyVisualizer()

        self.graph_layout.addWidget(self.spectrogram_viz)
        self.graph_layout.addWidget(self.key_viz)

        main_layout.addWidget(self.graph_container)

    # ------------------------------------------------------------------
    # Default state
    # ------------------------------------------------------------------

    def _set_default_summary(self) -> None:
        """Show the placeholder summary before any analysis."""
        default_text = (
            "<p style='margin-bottom: 12px;'><b>📁 Archivo:</b> N/A</p>\n"
            "<p style='margin-bottom: 12px;'><b>🎵 BPM:</b> N/A</p>\n"
            "<p style='margin-bottom: 12px;'><b>🎹 Key:</b> N/A</p>"
        )
        self.summary_output.setText(default_text)

    # ------------------------------------------------------------------
    # User interaction handlers (emit signals → controller)
    # ------------------------------------------------------------------

    def _on_load_clicked(self) -> None:
        """Emit ``signal_analyze_request`` so the Controller opens the dialog."""
        self.signal_analyze_request.emit("")

    def _on_history_clicked(self, item: QListWidgetItem) -> None:
        """Emit the index of the clicked history entry."""
        row = self.history_list.row(item)
        self.signal_history_item_selected.emit(row)

    # ------------------------------------------------------------------
    # Slots  (called by the Controller, possibly via signals)
    # ------------------------------------------------------------------

    def update_filepath(self, path: str) -> None:
        """Update the file-path label with the loaded file name."""
        filename = os.path.basename(path)
        self.filepath_label.setText(f"📂 Archivo: {filename}")

    def update_status(self, message: str, style: str = "green") -> None:
        """Update the status label with colour-coded feedback.

        Args:
            message: Text to display.
            style: CSS colour name (``green``, ``red``, ``blue``, ``orange``).
        """
        style_map = {
            "green": STYLE_STATUS_OK,
            "red": STYLE_STATUS_ERROR,
            "blue": STYLE_STATUS_INFO,
            "orange": STYLE_STATUS_WARN,
        }
        self.status_label.setStyleSheet(style_map.get(style, STYLE_STATUS_OK))
        self.status_label.setText(message)

    def display_summary(self, summary_data: dict[str, str]) -> None:
        """Render scalar results as styled HTML.

        Args:
            summary_data: Dictionary with ``File``, ``BPM``, ``Key`` etc.
        """
        html_parts = [
            "<p style='margin-bottom: 15px;'>"
            f"<b>{SUMMARY_ICONS.get(key, '•')} {key}:</b> {value}</p>"
            for key, value in summary_data.items()
        ]
        self.summary_output.setText("".join(html_parts))

    def display_analysis(self, features: dict[str, Any]) -> None:
        """Pass feature data to each visualiser widget.

        Each visualiser's ``draw_data()`` is called — **polymorphism**
        in action since every subclass implements it differently.
        """
        self._last_features = features
        self.spectrogram_viz.draw_data(features)
        self.key_viz.draw_data(features)

    def update_history_list(self, names: list[str]) -> None:
        """Replace the history :class:`QListWidget` contents with *names*.

        Args:
            names: Display labels for each analysed track.
        """
        self.history_list.clear()
        for name in names:
            QListWidgetItem(name, self.history_list)

    def highlight_history_item(self, index: int) -> None:
        """Select and scroll to the *index*-th history entry."""
        item = self.history_list.item(index)
        if item:
            self.history_list.setCurrentItem(item)
