"""Generate a small synthetic WAV file for integration testing.

Usage::

    python tests/fixtures/generate_wav.py

Produces ``tests/fixtures/sine_440.wav`` — a 2-second 440 Hz sine tone
at 22 050 Hz sample rate (mono, PCM-16).
"""

from __future__ import annotations

import numpy as np
from scipy.io.wavfile import write

SR = 22050
DURATION = 2.0
FREQUENCY = 440.0  # Hz — concert A
OUTPUT = "tests/fixtures/sine_440.wav"

t = np.linspace(0.0, DURATION, int(SR * DURATION), endpoint=False)
signal = np.sin(2.0 * np.pi * FREQUENCY * t).astype(np.float32)

# scipy expects int16 for PCM-16
write(OUTPUT, SR, (signal * 32767).astype(np.int16))
print(f"Generated {OUTPUT} ({len(signal)} samples @ {SR} Hz)")
