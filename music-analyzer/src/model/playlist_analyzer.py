# src/model/playlist_analyzer.py

import numpy as np

class AnalysisResultBase: 
    """Clase base (Abstracción) para resultados."""
    def __init__(self, raw_data):
        self._raw_data = raw_data
        
    def get_summary(self):
        """Método polimórfico. Debe ser implementado."""
        raise NotImplementedError("El método get_summary() debe ser implementado.")

class SingleTrackResult(AnalysisResultBase):
    """Herencia 1: Resultados detallados de una única pista."""
    def get_summary(self):
        """Polimorfismo: Devuelve el resumen escalar detallado."""
        return {
            "File": self._raw_data.get("path", "N/A").split('/')[-1],
            "BPM": f"{self._raw_data['tempo']:.2f}",
            "Key": self._raw_data.get('key', 'N/A'),
        }

class AggregatePlaylistResult(AnalysisResultBase):
    """Herencia 2: Resultados estadísticos agregados de una lista de análisis."""
    def get_summary(self):
        """Polimorfismo: Calcula y devuelve estadísticas agregadas (Promedio de BPM)."""
        tempos = [d._raw_data.get('tempo') for d in self._raw_data if d._raw_data.get('tempo') is not None]
        
        if not tempos:
            return {"Total Tracks": 0, "Average BPM": "N/A"}
            
        return {
            "Total Tracks": len(tempos),
            "Average BPM": f"{np.mean(tempos):.2f}",
            "Std Dev BPM": f"{np.std(tempos):.2f}",
        }

class PlaylistAnalyzer:
    """Clase que gestiona la colección de resultados de análisis (Model principal)."""
    def __init__(self):
        self._results = []

    def add_analysis(self, result_data):
        """Añade un resultado individual a la colección."""
        track_result = SingleTrackResult(result_data)
        self._results.append(track_result)
        return track_result

    def get_aggregate_results(self):
        """Devuelve un objeto de resultados agregados, usando el polimorfismo."""
        return AggregatePlaylistResult(self._results)