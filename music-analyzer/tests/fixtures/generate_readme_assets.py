"""Generate example output images for the README.

Produces PNG files of the spectrogram, chromagram, and waveform
using the same DSP pipeline as the main application.
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

# Ensure src/ is on the path
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.insert(0, src)

# Configure matplotlib for dark theme
plt.style.use("dark_background")

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate a synthetic audio signal (A4 = 440 Hz + harmonics)
SR = 22050
DURATION = 3.0
t = np.linspace(0.0, DURATION, int(SR * DURATION), endpoint=False)
y = (
    np.sin(2.0 * np.pi * 440.0 * t)
    + 0.5 * np.sin(2.0 * np.pi * 880.0 * t)
    + 0.25 * np.sin(2.0 * np.pi * 1320.0 * t)
).astype(np.float32)

# --- 1. Waveform ---
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(t[:2000], y[:2000], color="steelblue", linewidth=0.5)
ax.set_title("Forma de Onda (Waveform)", fontsize=14)
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Amplitud")
ax.set_xlim(0, 0.09)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "waveform.png"), dpi=120, bbox_inches="tight")
plt.close(fig)
print("OK - waveform.png")

# --- 2. Spectrogram ---
import librosa
import librosa.display

D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
fig, ax = plt.subplots(figsize=(10, 4))
img = librosa.display.specshow(
    D, sr=SR, x_axis="time", y_axis="log", ax=ax, cmap="magma", hop_length=512
)
ax.set_title("Espectrograma de Potencia (dB)", fontsize=14)
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Frecuencia (Hz)")
cbar = fig.colorbar(img, format="%+2.0f dB", ax=ax)
cbar.ax.set_ylabel("Amplitud (dB)", rotation=270, labelpad=15)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "spectrogram.png"), dpi=120, bbox_inches="tight")
plt.close(fig)
print("OK - spectrogram.png")

# --- 3. Chromagram ---
chroma = librosa.feature.chroma_stft(y=y, sr=SR)
fig, ax = plt.subplots(figsize=(10, 3))
img = librosa.display.specshow(
    chroma, sr=SR, y_axis="chroma", x_axis="time", ax=ax, cmap="viridis"
)
ax.set_title("Cromagrama Normalizado (Tonalidad)", fontsize=14)
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Clase de Tono")
fig.colorbar(img, ax=ax)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "chromagram.png"), dpi=120, bbox_inches="tight")
plt.close(fig)
print("OK - chromagram.png")

# --- 4. Output summary ---
print("\n== All images generated in assets/ ==")
print(f"Directory: {OUTPUT_DIR}")
