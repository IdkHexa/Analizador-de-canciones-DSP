#!/usr/bin/env bash
# Build TuneScope executable for Linux
# Requires: pip install pyinstaller

set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Building executable..."
pyinstaller --clean tunescope.spec

echo "Done! Executable at dist/TuneScope"
