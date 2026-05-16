"""Controller layer — orchestrates Model and View communication.

Provides the :class:`MainController` (Qt :class:`QObject`) that wires
user gestures from the View to Model operations and pushes results back.
"""

from __future__ import annotations

import logging
from typing import Any

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QFileDialog, QWidget

from config import AUDIO_FILE_PATTERNS
from model.audio_file import AudioFile
from model.feature_extractor import FeatureExtractor
from model.playlist_analyzer import PlaylistAnalyzer, SingleTrackResult
from view.main_window import MainWindow

logger = logging.getLogger(__name__)


class WorkerObject(QObject):
    """Performs DSP analysis in a background :class:`QThread`.

    Signals
    -------
    finished(features: dict):
        Emitted when analysis completes successfully.
    error(message: str):
        Emitted when any error occurs during loading or analysis.
    """

    finished = Signal(dict)
    error = Signal(str)

    def __init__(
        self,
        model_audio: AudioFile,
        model_extractor: FeatureExtractor,
        filepath: str,
    ) -> None:
        super().__init__()
        self._audio = model_audio
        self._extractor = model_extractor
        self._filepath = filepath

    @Slot()
    def run(self) -> None:
        """Load audio and run the DSP pipeline.

        This method runs **on the worker thread** — it must not touch
        the UI directly.  Results are delivered via Qt signals.
        """
        logger.info("Worker started for %s", self._filepath)
        try:
            if not self._audio.load_audio(self._filepath):
                self.error.emit("ERROR: No se pudo cargar el archivo de audio.")
                return

            features = self._extractor.extract_all_features(self._audio)
            if features.get("error"):
                self.error.emit(f"ERROR: {features['error']}")
                return

            logger.info("Worker finished — emitting results")
            self.finished.emit(features)

        except Exception as exc:
            logger.exception("Worker crashed")
            self.error.emit(f"Error inesperado durante el análisis: {exc}")


class MainController(QObject):
    """Orchestrates Model ↔ View communication.

    Responsible for
    - Handling UI requests (file dialog → analysis).
    - Running DSP on a background thread via :class:`WorkerObject`.
    - Maintaining an analysis history (:class:`PlaylistAnalyzer`).
    - Pushing results back to the View thread-safely via Qt signals.
    """

    # Signals used to push data from the worker thread back to the UI
    signal_status_update = Signal(str, str)
    signal_summary_update = Signal(dict)
    signal_graph_update = Signal(dict)
    signal_filepath_update = Signal(str)
    signal_history_update = Signal(list)
    signal_history_restore = Signal(int)

    def __init__(
        self,
        model_audio: AudioFile,
        model_extractor: FeatureExtractor,
        view_window: MainWindow,
    ) -> None:
        super().__init__()
        self.model_audio = model_audio
        self.model_extractor = model_extractor
        self.model_playlist = PlaylistAnalyzer()
        self.view_window = view_window

        # Keep track of each result's features keyed by list index
        self._history_features: list[dict[str, Any]] = []

        self._connect_signals_to_slots()

    # ------------------------------------------------------------------
    # Signal wiring
    # ------------------------------------------------------------------

    def _connect_signals_to_slots(self) -> None:
        """Wire internal and view signals to the appropriate slots."""
        # View → Controller
        self.view_window.signal_analyze_request.connect(self.handle_analyze_request)
        self.view_window.signal_history_item_selected.connect(self._restore_from_history)

        # Controller → View
        self.signal_status_update.connect(self.view_window.update_status)
        self.signal_summary_update.connect(self.view_window.display_summary)
        self.signal_graph_update.connect(self.view_window.display_analysis)
        self.signal_filepath_update.connect(self.view_window.update_filepath)
        self.signal_history_update.connect(self.view_window.update_history_list)
        self.signal_history_restore.connect(self.view_window.highlight_history_item)

    # ------------------------------------------------------------------
    # Entry point: user wants to analyse a file
    # ------------------------------------------------------------------

    @Slot(str)
    def handle_analyze_request(self, _dummy: str = "") -> None:
        """Open a file dialog and start background analysis.

        The actual file dialog lives in the Controller (not the View)
        to keep the View free of I/O logic.
        """
        filepath, _ = QFileDialog.getOpenFileName(
            QWidget(self.view_window),
            "Seleccionar Archivo de Audio",
            "",
            AUDIO_FILE_PATTERNS,
        )
        if not filepath:
            self.signal_status_update.emit("Selección cancelada.", "orange")
            return

        self.signal_filepath_update.emit(filepath)
        self.signal_status_update.emit("Cargando y analizando...", "blue")

        self._start_worker(filepath)

    # ------------------------------------------------------------------
    # QThread worker management
    # ------------------------------------------------------------------

    def _start_worker(self, filepath: str) -> None:
        """Create a :class:`WorkerObject`, move it to a :class:`QThread`,
        and start processing."""
        self._thread = QThread(self)
        self._worker = WorkerObject(self.model_audio, self.model_extractor, filepath)
        self._worker.moveToThread(self._thread)

        # Wire worker signals
        self._worker.finished.connect(self._on_analysis_finished)
        self._worker.error.connect(self._on_analysis_error)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)

        # Clean up when done
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

    def _on_analysis_finished(self, features: dict[str, Any]) -> None:
        """Handle a successful DSP result: store, summarise, display."""
        result_obj = SingleTrackResult(features)
        self.model_playlist.add_analysis(features)
        self._history_features.append(features)

        self.signal_summary_update.emit(result_obj.get_summary())
        self.signal_graph_update.emit(features)
        self.signal_status_update.emit("Análisis completado exitosamente.", "green")

        # Notify the View to refresh the history list
        history_names = [
            str(r.get_summary().get("File", f"Track {i}"))
            for i, r in enumerate(self.model_playlist._results)  # noqa: SLF001
        ]
        self.signal_history_update.emit(history_names)

    def _on_analysis_error(self, message: str) -> None:
        """Handle an error from the worker thread."""
        self.signal_status_update.emit(message, "red")

    # ------------------------------------------------------------------
    # History navigation
    # ------------------------------------------------------------------

    @Slot(int)
    def _restore_from_history(self, index: int) -> None:
        """Restore the summary and graphs for a previously analysed track.

        Args:
            index: Position of the track in the history list.
        """
        if index < 0 or index >= len(self._history_features):
            logger.warning("Invalid history index: %d", index)
            return

        features = self._history_features[index]
        result_obj = SingleTrackResult(features)

        self.signal_summary_update.emit(result_obj.get_summary())
        self.signal_graph_update.emit(features)
        self.signal_status_update.emit(
            f"Restaurado: {result_obj.get_summary().get('File', 'Track')}",
            "blue",
        )
        self.signal_history_restore.emit(index)
