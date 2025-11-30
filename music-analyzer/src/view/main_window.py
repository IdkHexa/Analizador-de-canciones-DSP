# src/view/main_window.py

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QFrame) 
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont
from .visualizer import SpectrogramVisualizer, KeyVisualizer 
import os

class MainWindow(QMainWindow):
    """
    La Vista (View): Define la interfaz gráfica.
    Emite signals a través de QObject para comunicar eventos al Controller.
    """
    # Signals que serán conectados al Controller (PySide6/Qt)
    signal_analyze_request = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizador de Canciones DSP (PySide6 MVC)")
        self.setMinimumSize(1000, 650)
        
        self.controller = None
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        # --- Panel Izquierdo: Controles y Resumen ---
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_panel.setFixedWidth(350)
        
        # 1. Selector de Archivo (Botón que dispara el Signal)
        self.load_button = QPushButton("Cargar y Analizar Audio...")
        self.load_button.clicked.connect(self._handle_load_button_clicked)
        self.load_button.setMinimumHeight(40)
        
        # 2. Etiqueta del archivo con mejor formato
        self.filepath_label = QLabel("Archivo: Ninguno cargado.")
        self.filepath_label.setWordWrap(True)
        self.filepath_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                background-color: #2b2b2b;
                border-radius: 5px;
                color: #ffffff;
            }
        """)

        # 3. Título de Resultados
        summary_title = QLabel("--- Resultados Escalares ---")
        summary_title.setAlignment(Qt.AlignCenter)
        font_title = QFont()
        font_title.setBold(True)
        font_title.setPointSize(11)
        summary_title.setFont(font_title)
        
        # 4. Resumen Escalar con mejor formato y separadores
        self.summary_output = QLabel()
        self.summary_output.setWordWrap(True)
        self.summary_output.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.summary_output.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.summary_output.setStyleSheet("""
            QLabel {
                padding: 15px;
                background-color: #1e1e1e;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                color: #ffffff;
                font-size: 12pt;
                line-height: 1.8;
            }
        """)
        self._set_default_summary()

        # 5. Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        # 6. Estado
        self.status_label = QLabel("Listo para cargar.")
        self.status_label.setStyleSheet("color: green; font-weight: bold; padding: 5px;")

        # Agregar widgets al layout
        control_layout.addWidget(self.load_button)
        control_layout.addSpacing(10)
        control_layout.addWidget(self.filepath_label)
        control_layout.addSpacing(15)
        control_layout.addWidget(summary_title)
        control_layout.addSpacing(5)
        control_layout.addWidget(self.summary_output)
        control_layout.addStretch()
        control_layout.addWidget(line)
        control_layout.addWidget(self.status_label)
        
        # --- Panel Derecho: Visualizaciones Matplotlib ---
        self.graph_container = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_container)
        
        # Instanciar Visualizadores (Clases que usan Herencia y Polimorfismo)
        self.spectrogram_viz = SpectrogramVisualizer()
        self.key_viz = KeyVisualizer()
        
        self.graph_layout.addWidget(self.spectrogram_viz)
        self.graph_layout.addWidget(self.key_viz)

        # Configurar Layout Principal
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.graph_container)
        self.setCentralWidget(central_widget)

    def _set_default_summary(self):
        """Establece el texto por defecto del resumen."""
        default_text = """
<p style='margin-bottom: 12px;'><b>📁 Archivo:</b> N/A</p>
<p style='margin-bottom: 12px;'><b>🎵 BPM:</b> N/A</p>
<p style='margin-bottom: 12px;'><b>🎹 Key:</b> N/A</p>
        """.strip()
        self.summary_output.setText(default_text)

    # --- Métodos de Interacción (Solo captura el evento) ---

    def _handle_load_button_clicked(self):
        """
        Captura el click y pide al Controller que inicie el diálogo de archivo,
        manteniendo la lógica de I/O fuera de la View.
        """
        # La View emite un signal. El Controller lo interceptará y abrirá el QFileDialog.
        self.signal_analyze_request.emit("")

    # --- Slots de Actualización (El Controller llama a estos) ---

    def update_filepath(self, path):
        """Actualiza la etiqueta del archivo cargado."""
        filename = os.path.basename(path)
        self.filepath_label.setText(f"📂 Archivo: {filename}")

    def update_status(self, message, style="green"):
        """Actualiza el mensaje de estado."""
        self.status_label.setStyleSheet(f"color: {style}; font-weight: bold; padding: 5px;")
        self.status_label.setText(message)

    def display_summary(self, summary_data):
        """
        Actualiza los resultados escalares con formato HTML mejorado.
        Ahora con espaciado adecuado entre elementos.
        """
        # Mapeo de iconos para cada campo
        icons = {
            "File": "📁",
            "BPM": "🎵",
            "Key": "🎹"
        }
        
        # Construir el texto con HTML para mejor formato
        html_parts = []
        for key, value in summary_data.items():
            icon = icons.get(key, "•")
            # Cada elemento con margen inferior para separación
            html_parts.append(
                f"<p style='margin-bottom: 15px;'><b>{icon} {key}:</b> {value}</p>"
            )
        
        html_text = "".join(html_parts)
        self.summary_output.setText(html_text)

    def display_analysis(self, features):
        """Ordena a los visualizadores (clases hijas) que se dibujen."""
        
        # Uso de Polimorfismo: Se llama al mismo método draw_data()
        # pero cada clase hija sabe cómo dibujar sus datos específicos.
        self.spectrogram_viz.draw_data(features)
        self.key_viz.draw_data(features)