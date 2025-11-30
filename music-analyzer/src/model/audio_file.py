# src/model/audio_file.py

import librosa
import numpy as np

class AudioFile:
    """
    Clase que representa y encapsula los datos crudos y metadatos de un archivo de audio.
    Implementa el Encapsulamiento protegiendo la señal de audio y el sample rate.
    """
    def __init__(self):
        self._path = None
        self._y = None      # Señal de audio (Atributo protegido)
        self._sr = None     # Frecuencia de muestreo (Atributo protegido)
        self._features_cache = {}

    def load_audio(self, path):
        """Carga el audio utilizando librosa y actualiza los atributos protegidos."""
        self._path = path
        self._features_cache = {} # Limpiar caché al cargar nuevo archivo
        try:
            # Lógica de negocio (I/O) reside en el Model.
            # sr=None carga el sample rate nativo del archivo.
            self._y, self._sr = librosa.load(path, sr=None, mono=True)
            return True
        except Exception as e:
            print(f"Error al cargar el audio: {e}")
            self._y = None
            self._sr = None
            return False

    # Métodos Getters para acceso controlado (Encapsulamiento)
    def get_signal(self):
        return self._y

    def get_sample_rate(self):
        return self._sr

    def get_path(self):
        return self._path

    def get_features_cache(self):
        return self._features_cache

    def set_features_cache(self, features):
        self._features_cache = features