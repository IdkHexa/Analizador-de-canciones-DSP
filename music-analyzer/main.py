# main.py (en la raíz del proyecto: music-analyzer/)

import sys
import os

# Añadir la carpeta src/ al path de Python
# __file__ es main.py en music-analyzer/, así que añadimos music-analyzer/src/
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from PySide6.QtWidgets import QApplication

# Importar capas (ahora funcionarán correctamente)
from model.audio_file import AudioFile
from model.feature_extractor import FeatureExtractor
from view.main_window import MainWindow
from controller.main_controller import MainController

def main():
    # Inicialización de la aplicación PySide6
    app = QApplication(sys.argv)
    
    # 1. Inicializar Modelos (Datos y Lógica de Negocio)
    model_audio = AudioFile()
    model_extractor = FeatureExtractor()
    
    # 2. Inicializar Vista (Interfaz)
    main_window = MainWindow()
    
    # 3. Inicializar Controller (Orquestación)
    controller = MainController(model_audio, model_extractor, main_window)
    
    # Mostrar la ventana y ejecutar el bucle de eventos
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()