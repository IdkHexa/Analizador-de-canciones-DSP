# src/view/visualizer.py

import matplotlib.pyplot as plt
import librosa.display
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar

class BaseVisualizer(QWidget):
    """
    Clase base (Herencia) para la visualización de Matplotlib.
    Hereda de QWidget para ser un widget de PySide6.
    """
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        
        # Inicialización de Matplotlib y Canvas (Lógica de Presentación/Herencia)
        self.figure, self.ax = plt.subplots(1, 1, figsize=(4, 3))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self) # Barra de zoom/pan

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        
        self.ax.set_title(self.title)
        self.ax.set_axis_off() # Ocultar ejes hasta que haya datos

    def clear_plot(self):
        """Limpia la gráfica actual."""
        self.ax.clear()
        self.ax.set_title(self.title)
        self.ax.set_axis_off()
        self.canvas.draw()

    def draw_data(self, data):
        """Método polimórfico. Debe ser sobrescrito por subclases."""
        raise NotImplementedError("draw_data() debe ser implementado por la subclase.")
        
class SpectrogramVisualizer(BaseVisualizer):
    """
    Clase hija (Herencia) para visualizar el Espectrograma de Potencia.
    Implementa el Polimorfismo en draw_data.
    """
    def __init__(self, **kwargs):
        super().__init__(title="Espectrograma de Potencia (dB)", **kwargs)

    def draw_data(self, features):
        """Polimorfismo: Dibuja un Espectrograma."""
        self.ax.clear()
        
        # CORRECCIÓN: Extraer la matriz D del diccionario features
        D = features['D']  # ¡Esta es la corrección crítica!
        sr = features['sr']
        
        # Lógica de dibujo de librosa (Lógica de Presentación)
        img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', ax=self.ax, cmap='magma', hop_length=512)
        
        self.ax.set_title(self.title)
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Frecuencia (Hz)")
        if img:
            # Añadir la barra de color
            cbar = self.figure.colorbar(img, format="%+2.0f dB", ax=self.ax)
            cbar.ax.set_ylabel('Amplitud (dB)', rotation=270, labelpad=15)
        self.canvas.draw()

class KeyVisualizer(BaseVisualizer):
    """
    Clase hija (Herencia) para visualizar el Cromagrama (Tonalidad).
    Implementa el Polimorfismo en draw_data.
    """
    def __init__(self, **kwargs):
        super().__init__(title="Cromagrama Normalizado (Tonalidad)", **kwargs)
        # Notas utilizadas para etiquetar el eje Y
        self.chromas = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def draw_data(self, features):
        """Polimorfismo: Dibuja un Cromagrama."""
        self.ax.clear()
        
        chroma = features['chroma']
        sr = features['sr']
        
        # Lógica de dibujo de librosa (Lógica de Presentación)
        img = librosa.display.specshow(chroma, sr=sr, y_axis='chroma', x_axis='time', ax=self.ax, cmap='viridis')

        self.ax.set_title(self.title)
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Clase de Tono")
        if img:
            self.figure.colorbar(img, ax=self.ax)
        self.canvas.draw()