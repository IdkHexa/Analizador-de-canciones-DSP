# DSP Music Analyzer

![CI](https://github.com/IdkHexa/Analizador-de-canciones-DSP/actions/workflows/ci.yml/badge.svg)

> [**Leer en español**](README.es.md)

A desktop application for audio analysis through **Digital Signal Processing (DSP)**. Extracts musical features like **BPM** and **key/tonality**, and generates interactive visualizations of **spectrograms**, **chromagrams**, and **waveforms**.

![Main window preview](assets/waveform.png)

## Features

- **Tempo (BPM) Detection**: Automatic musical tempo estimation
- **Key Detection**: Identifies major/minor keys using the Krumhansl-Schmuckler algorithm
- **Power Spectrogram**: Frequency-time visualization in logarithmic scale
- **Chromagram**: Pitch-class distribution visualization
- **Waveform**: Time-domain signal display
- **Analysis History**: Navigate previously analyzed tracks with one click
- **Export Results**: Save analysis as JSON or CSV
- **Background Processing**: UI never freezes thanks to QThread
- **Drag & Drop**: Drop audio files directly onto the window
- **Batch Analysis**: Process multiple files sequentially
- **Modern GUI**: Built with PySide6 (Qt for Python)
- **MVC Architecture**: Model-View-Controller with signals/slots

## Demo

### Generated Visualizations

Each analysis produces three interactive plots (zoom & pan enabled):

| Spectrogram | Chromagram |
|:---:|:---:|
| ![Spectrogram](assets/spectrogram.png) | ![Chromagram](assets/chromagram.png) |

| Waveform |
|:---:|
| ![Waveform](assets/waveform.png) |

### Usage Flow

```
1. Click "Cargar y Analizar Audio..." (or drag a file)
       │
       ▼
2. Progress bar shows analysis status
       │
       ▼
3. Scalar results: BPM, Key
       │
       ▼
4. Visualizations: Waveform → Spectrogram → Chromagram
       │
       ▼
5. Export to JSON/CSV or browse history
```

## Technologies

| Technology | Min. version | Purpose |
|-----------|-------------|---------|
| Python | 3.10+ | Language |
| PySide6 | 6.5.0 | GUI framework |
| librosa | 0.9.0 | Audio & music analysis |
| NumPy | 1.21.0 | Numerical computation |
| Matplotlib | 3.5.0 | Data visualization |
| SciPy | 1.7.0 | Test signal generation |
| pytest | — | Automated testing |
| ruff | — | Linter & formatter |
| mypy | — | Static type checker |

## Installation

```bash
# 1. Clone
git clone https://github.com/IdkHexa/Analizador-de-canciones-DSP.git
cd Analizador-de-canciones-DSP

# 2. Virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Steps to analyze audio:

1. Click **"Cargar y Analizar Audio..."** (or drag a file onto the window)
2. Select an audio file (MP3, WAV, FLAC)
3. Wait for the analysis to complete
4. View the results:
   - **Left panel**: BPM, Key, analysis history
   - **Right panel**: Interactive waveform, spectrogram, and chromagram
5. Click any history entry to restore a previous analysis

## Project Structure

```
Analizador-de-canciones-DSP/
│
├── main.py                              # Entry point
├── pyproject.toml                       # Packaging & tool config
├── .pre-commit-config.yaml              # ruff, black, mypy hooks
├── requirements.txt                     # Dependencies
├── README.md                            # This file (English)
├── README.es.md                         # Spanish version
│
├── src/
│   ├── config/                          # Centralized configuration
│   │   └── __init__.py                  # DSP constants, UI styles, settings
│   │
│   ├── model/                           # Model layer (business logic)
│   │   ├── __init__.py
│   │   ├── audio_file.py               # Audio data encapsulation
│   │   ├── feature_extractor.py        # DSP feature extraction
│   │   └── playlist_analyzer.py        # Aggregated playlist analysis
│   │
│   ├── view/                            # View layer (GUI)
│   │   ├── __init__.py
│   │   ├── main_window.py              # Main window with history
│   │   └── visualizer.py               # Matplotlib visualizers
│   │
│   ├── controller/                      # Controller layer (orchestration)
│   │   ├── __init__.py
│   │   └── main_controller.py           # WorkerObject + QThread + history
│   │
│   └── persist.py                       # History persistence to disk
│
├── tests/                               # Automated tests
│   ├── conftest.py                      # Shared fixtures
│   ├── fixtures/
│   │   ├── generate_wav.py             # Synthetic WAV generator
│   │   └── sine_440.wav                # Test WAV (440 Hz, 2s)
│   ├── test_audio_file.py              # AudioFile tests (mocked)
│   ├── test_feature_extractor.py       # Key detection + pipeline tests
│   ├── test_integration.py             # End-to-end tests with real WAV
│   └── test_results.py                 # Result class tests
│
├── assets/                              # README images
│   ├── spectrogram.png
│   ├── chromagram.png
│   └── waveform.png
│
└── .github/workflows/
    └── ci.yml                           # CI matrix (3.10, 3.11, 3.12)
```

## Testing & Quality

```bash
# Tests
pytest                     # 22 tests, 0 failures expected

# Linter
ruff check src/ tests/     # 0 errors

# Formatting
ruff format --check src/ tests/

# Type checking
mypy src/                  # Success: no issues found

# Coverage
pytest --cov=src tests/    # Coverage report

# Pre-commit (optional)
pre-commit install
pre-commit run --all-files
```

The project runs **automated CI** on GitHub Actions for Python 3.10, 3.11, and 3.12 on every push and pull request.

## Engineering Principles

### MVC Pattern (Model-View-Controller)
- **Model**: Business logic and DSP processing
- **View**: PySide6 GUI with Qt signals
- **Controller**: Orchestration via QThread + signals/slots

### Object-Oriented Programming
- **Encapsulation**: `AudioFile` protects `_y` and `_sr` with getters
- **Abstraction**: `FeatureExtractor` hides librosa complexity
- **Inheritance**: `BaseVisualizer → SpectrogramVisualizer, KeyVisualizer`
- **Polymorphism**: `draw_data()` implemented differently per visualizer

### Best Practices
- ✅ **Type hints** across the entire codebase (verified by mypy)
- ✅ **Google-style docstrings** on all public classes and methods
- ✅ **Structured logging** instead of print()
- ✅ **QThread** for async operations (non-blocking UI)
- ✅ **Centralized config** (src/config/) — no hardcoded constants
- ✅ **22 automated tests** (unit + integration)
- ✅ **CI/CD** with GitHub Actions
- ✅ **Pre-commit hooks** (ruff, black, mypy)
- ✅ **Modern packaging** (pyproject.toml)

## DSP Algorithms

### Tempo Detection
Uses `librosa.feature.rhythm.tempo` with onset detection and autocorrelation.

### Key Detection
Implements the **Krumhansl-Schmuckler algorithm**:

1. Extract chroma features via STFT
2. Compute average 12-bin chroma vector
3. Correlate with rotated major/minor templates
4. Select the key with the highest correlation score

### Power Spectrogram
STFT (Short-Time Fourier Transform) converted to decibel scale with `librosa.amplitude_to_db`.

## Troubleshooting

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'librosa'` | `pip install -r requirements.txt` |
| `FutureWarning: librosa.beat.tempo` | Harmless — code uses try/except for both APIs |
| Audio won't load | Check format (MP3, WAV, FLAC) and that `soundfile` is installed |

## Sample Output

```
File: cancion.mp3
BPM: 120.00
Key: C Major
```

- **Spectrogram**: Energy distribution across frequencies over time
- **Chromagram**: Distribution of the 12 pitch classes (C, C#, D, ..., B)

## Author

Developed as an educational project demonstrating:

- Object-Oriented Programming
- MVC Architecture
- Digital Signal Processing
- Automated Testing & CI/CD
- Python GUI Development

## References

- [librosa](https://librosa.org/doc/latest/index.html)
- [PySide6](https://doc.qt.io/qtforpython-6/)
- [Krumhansl-Schmuckler key-finding](https://rnhart.net/articles/key-finding/)
- [The Scientist and Engineer's Guide to DSP](https://www.dspguide.com/)
