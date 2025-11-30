# src/controller/main_controller.py

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QFileDialog
import threading
import time 

# Importaciones de las otras capas
from model.audio_file import AudioFile
from model.feature_extractor import FeatureExtractor
from model.playlist_analyzer import PlaylistAnalyzer, SingleTrackResult

class MainController(QObject):
    """
    El Controlador (Controller): Orquesta la comunicación entre Model y View.
    Hereda de QObject para utilizar Signals y Slots de PySide6.
    """
    # Signals internos para actualizar la View desde el hilo principal de Qt
    signal_status_update = Signal(str, str)
    signal_summary_update = Signal(dict)
    signal_graph_update = Signal(dict)
    signal_filepath_update = Signal(str)

    def __init__(self, model_audio: AudioFile, model_extractor: FeatureExtractor, view_window):
        super().__init__()
        
        self.model_audio = model_audio
        self.model_extractor = model_extractor
        self.model_playlist = PlaylistAnalyzer()
        self.view_window = view_window
        
        self._connect_signals_to_slots()
        
    def _connect_signals_to_slots(self):
        """Conecta los Signals de la View y los Signals internos a los Slots."""
        
        # 1. View -> Controller: La View pide iniciar el análisis
        self.view_window.signal_analyze_request.connect(self.handle_analyze_request)
        
        # 2. Controller (interno) -> View: Actualizaciones de estado/datos
        self.signal_status_update.connect(self.view_window.update_status)
        self.signal_summary_update.connect(self.view_window.display_summary)
        self.signal_graph_update.connect(self.view_window.display_analysis)
        self.signal_filepath_update.connect(self.view_window.update_filepath)

    @Slot(str)
    def handle_analyze_request(self, dummy_path):
        """
        Slot principal: Maneja la petición del usuario, inicia el diálogo 
        de archivo (lógica de I/O) y delega el procesamiento al Model.
        """
        
        # Lógica de I/O gestionada por el Controller: Apertura de diálogo de archivo
        filepath, _ = QFileDialog.getOpenFileName(
            self.view_window, 
            "Seleccionar Archivo de Audio", 
            "", 
            "Audio Files (*.mp3 *.wav *.flac)"
        )

        if not filepath:
            self.signal_status_update.emit("Selección cancelada.", "orange")
            return
        
        # Muestra la ruta del archivo inmediatamente
        self.signal_filepath_update.emit(filepath)
        self.signal_status_update.emit("Cargando y analizando...", "blue")

        # Inicia el procesamiento pesado en un hilo separado
        analysis_thread = threading.Thread(target=self._run_analysis_async, args=(filepath,))
        analysis_thread.start()

    def _run_analysis_async(self, filepath):
        """
        Ejecuta la lógica de negocio (Model) en un hilo secundario 
        para no bloquear la interfaz gráfica.
        """
        try:
            # 1. Model: Cargar audio (Encapsulamiento)
            if not self.model_audio.load_audio(filepath):
                self.signal_status_update.emit("ERROR: No se pudo cargar el archivo de audio.", "red")
                return

            # 2. Model: Extraer características (Abstracción)
            features = self.model_extractor.extract_all_features(self.model_audio)

            if features.get("error"):
                self.signal_status_update.emit(f"ERROR: {features['error']}", "red")
                return
                
            # 3. Model: Crear objeto de resultado (Polimorfismo)
            result_obj = SingleTrackResult(features)
            self.model_playlist.add_analysis(features) # Agregar a la lista para futura agregación
            
            # 4. Controller -> View: Emitir los resultados al hilo principal para actualización
            self.signal_summary_update.emit(result_obj.get_summary())
            self.signal_graph_update.emit(features)
            self.signal_status_update.emit("Análisis completado exitosamente.", "green")

        except Exception as e:
            self.signal_status_update.emit(f"Error inesperado durante el análisis: {e}", "red")