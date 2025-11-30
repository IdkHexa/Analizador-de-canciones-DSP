Analizador de Música DSP

Aplicación de escritorio para análisis de audio mediante Procesamiento Digital de Señales (DSP). Extrae características musicales como BPM, tonalidad y genera visualizaciones de espectrogramas y cromagramas.

Características

Análisis de Tempo (BPM): Detección automática del tempo musical
Detección de Tonalidad: Identifica la clave musical (Mayor/Menor) usando el algoritmo Krumhansl-Schmuckler
Espectrograma de Potencia: Visualización frecuencia-tiempo en escala logarítmica
Cromagrama: Representación visual de la distribución de clases de tonos
Interfaz Gráfica Moderna: Construida con PySide6 (Qt for Python)
Arquitectura MVC: Modelo-Vista-Controlador para código mantenible

Tecnologías

Python 3.8+
PySide6: Framework de interfaz gráfica
librosa: Biblioteca de análisis de audio y música
NumPy: Computación numérica
Matplotlib: Visualización de datos

1. Clonar el repositorio

git clone https://github.com/tu-usuario/music-analyzer.git
cd music-analyzer

2. Crear entorno virtual (recomendado)

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

3. Instalar dependencias

pip install -r requirements.txt

requirements.txt:

PySide6>=6.5.0
librosa>=0.9.0
numpy>=1.21.0
matplotlib>=3.5.0
soundfile>=0.11.0

 Uso
Ejecutar la aplicación

python main.py

Pasos para analizar audio

Click en "Cargar y Analizar Audio..."
Selecciona un archivo de audio (MP3, WAV, FLAC)
Espera a que se complete el análisis
Visualiza los resultados:

Panel izquierdo: BPM, Tonalidad, Nombre del archivo
Panel derecho: Espectrograma y Cromagrama interactivos

Estructura del Proyecto

music-analyzer/
│
├── main.py                          # Punto de entrada de la aplicación
│
├── src/
│   ├── model/                       # Capa de Modelo (Lógica de negocio)
│   │   ├── __init__.py
│   │   ├── audio_file.py           # Encapsulamiento de datos de audio
│   │   ├── feature_extractor.py    # Extracción de características DSP
│   │   └── playlist_analyzer.py    # Análisis agregado de playlists
│   │
│   ├── view/                        # Capa de Vista (Interfaz gráfica)
│   │   ├── __init__.py
│   │   ├── main_window.py          # Ventana principal
│   │   └── visualizer.py           # Visualizadores Matplotlib
│   │
│   └── controller/                  # Capa de Controlador (Orquestación)
│       ├── __init__.py
│       └── main_controller.py      # Controlador principal MVC
│
├── requirements.txt                 # Dependencias del proyecto
└── README.md                        # Este archivo

Principios de POO Implementados
Este proyecto demuestra los siguientes conceptos de Programación Orientada a Objetos:
1. Encapsulamiento

AudioFile: Protege atributos privados (_y, _sr) con métodos getter/setter
Separación clara entre datos internos y API pública

2. Abstracción

FeatureExtractor: Oculta la complejidad del DSP de librosa
Expone métodos simples como extract_all_features()

3. Herencia

BaseVisualizer → SpectrogramVisualizer, KeyVisualizer
AnalysisResultBase → SingleTrackResult, AggregatePlaylistResult

4. Polimorfismo

Método draw_data() implementado de forma diferente en cada visualizador
Método get_summary() con comportamiento específico por tipo de resultado

5. Patrón MVC (Model-View-Controller)

Model: Lógica de negocio y procesamiento DSP
View: Interfaz gráfica PySide6
Controller: Orquestación y comunicación via Signals/Slots

Algoritmos DSP Utilizados
Detección de Tempo

tempo = librosa.beat.tempo(y=y, sr=sr)

Utiliza análisis de onset y autocorrelación para detectar BPM.
Detección de Tonalidad
Implementa el algoritmo Krumhansl-Schmuckler:

Extrae características cromáticas con STFT
Calcula vector promedio de 12 clases de tonos
Compara con plantillas Mayor/Menor rotadas
Selecciona la clave con mayor correlación

Espectrograma

D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

Transformada de Fourier de Tiempo Corto (STFT) convertida a escala de decibelios.

Error: "ModuleNotFoundError: No module named 'model'"
Solución: Asegúrate de que existen los archivos __init__.py en cada carpeta:

touch src/model/__init__.py
touch src/view/__init__.py
touch src/controller/__init__.py

Error: "dict object has no attribute 'dtype'"
Solución: Ya corregido en visualizer.py línea 59. Actualiza el archivo.

Warning: "librosa.beat.tempo FutureWarning"
Solución: Puedes ignorarlo o actualizar librosa:

pip install --upgrade librosa

Audio no se carga
Verificar:

El archivo está en formato soportado (MP3, WAV, FLAC)
soundfile o audioread están instalados correctamente
El archivo no está corrupto

Ejemplos de Salida
Análisis de una pista:
Archivo: cancion.mp3
BPM: 120.00
Key: C Mayor
Espectrograma: Muestra la distribución de energía en frecuencias a lo largo del tiempo
Cromagrama: Visualiza la distribución de las 12 clases de tonos (C, C#, D, ..., B)

Autor
Desarrollado como proyecto educativo para demostrar conceptos de:

Programación Orientada a Objetos
Arquitectura MVC
Procesamiento Digital de Señales
Desarrollo de aplicaciones GUI con Python

Referencias

https://librosa.org/doc/latest/index.html
https://doc.qt.io/qtforpython-6/
https://rnhart.net/articles/key-finding/
https://www.dspguide.com/