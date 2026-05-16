"""Entry point for the Music Analyzer desktop application.

Configures structured logging, wires up the **MVC** layers
(Model / View / Controller), and starts the PySide6 event loop.
"""

from __future__ import annotations

import logging
import os
import sys

# ---------------------------------------------------------------------------
# Logging configuration  (runs once at startup)
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# Add the ``src/`` package to the module search path so that
# ``from model.xxx`` / ``from view.xxx`` / ``from controller.xxx``
# resolve correctly.
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from PySide6.QtWidgets import QApplication

from model.audio_file import AudioFile
from model.feature_extractor import FeatureExtractor
from view.main_window import MainWindow
from controller.main_controller import MainController


def main() -> None:
    """Application entry point.

    Steps
    1. Create the PySide6 application object.
    2. Instantiate the Model layer (``AudioFile``, ``FeatureExtractor``).
    3. Instantiate the View layer (``MainWindow``).
    4. Wire everything together with the Controller (``MainController``).
    5. Show the window and start the Qt event loop.
    """
    app = QApplication(sys.argv)

    # Model
    model_audio = AudioFile()
    model_extractor = FeatureExtractor()

    # View
    main_window = MainWindow()

    # Controller
    controller = MainController(model_audio, model_extractor, main_window)  # noqa: F841

    logger.info("Application started — main window displayed")
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

if __name__ == '__main__':
    main()