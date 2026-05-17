# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for TuneScope — Music Analyzer."""

import os
import sys
from pathlib import Path

BLOCK_CIPHER_LIST = None

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        # Include the src package recursively
        ("src", "src"),
    ],
    hiddenimports=[
        "PySide6.QtCore",
        "PySide6.QtWidgets",
        "PySide6.QtGui",
        "librosa",
        "numpy",
        "matplotlib",
        "PIL",
        "PIL.Image",
        "scipy.io.wavfile",
        "soundfile",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "cv2",
        "tensorflow",
        "torch",
        "jupyter",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="TuneScope",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
