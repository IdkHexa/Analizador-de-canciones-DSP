# src/model/feature_extractor.py

import librosa
import numpy as np
from .audio_file import AudioFile

class FeatureExtractor:
    """
    Clase que implementa la Abstracción, ocultando la complejidad del DSP de librosa.
    Expone métodos simples para obtener características.
    """
    def __init__(self):
        # Plantillas Krumhansl-Schmuckler (para detección de tonalidad)
        self.K_MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        self.K_MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
        # Se completa la lista de notas para detección de clave
        self.CHROMAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def _determine_key(self, chroma_mean):
        """Calcula la tonalidad musical comparando el vector croma con plantillas."""
        chroma_mean = chroma_mean / np.sum(chroma_mean) # Normalización
        
        best_match = -1
        best_key = "Desconocida"

        for i in range(12): 
            # Rotar las plantillas para todas las claves (C, C#, D, etc.)
            major_score = np.dot(chroma_mean, np.roll(self.K_MAJOR, i))
            minor_score = np.dot(chroma_mean, np.roll(self.K_MINOR, i))

            if major_score > best_match:
                best_match = major_score
                best_key = f"{self.CHROMAS[i]} Mayor"
            
            if minor_score > best_match:
                best_match = minor_score
                best_key = f"{self.CHROMAS[i]} Menor"
                
        return best_key
    
    def extract_all_features(self, audio_file: AudioFile):
        """Método de Abstracción: Ejecuta todo el DSP."""
        y = audio_file.get_signal()
        sr = audio_file.get_sample_rate()

        if y is None or sr is None:
            return {"error": "Archivo de audio no cargado."}

        # 1. Tempo (BPM) - Usando sintaxis compatible con versiones antiguas
        tempo, = librosa.beat.tempo(y=y, sr=sr) 

        # 2. Tonalidad (Chroma)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        key = self._determine_key(chroma_mean)

        # 3. Espectrograma de Potencia (Para visualización)
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        times = librosa.times_like(D, sr=sr)
        
        features = {
            "path": audio_file.get_path(),
            "tempo": float(tempo),
            "key": key,
            "D": D,
            "chroma": chroma,
            "sr": sr,
            "times": times
        }
        
        # Guardar en caché (uso interno del Model)
        audio_file.set_features_cache(features)
        return features