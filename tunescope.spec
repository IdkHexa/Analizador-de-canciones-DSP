# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for TuneScope — Music Analyzer."""

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

BLOCK_CIPHER_LIST = None

all_pil = collect_submodules("PIL")
pil_data = collect_data_files("PIL", include_py_files=True)

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("src", "src"),
    ] + pil_data,
    hiddenimports=[
        "PySide6.QtCore",
        "PySide6.QtWidgets",
        "PySide6.QtGui",
        "librosa",
        "numpy",
        "matplotlib",
        "matplotlib.backends.backend_qt5agg",
        "matplotlib.backends.backend_qt",
        "scipy.io.wavfile",
        "soundfile",
    ] + all_pil,
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
