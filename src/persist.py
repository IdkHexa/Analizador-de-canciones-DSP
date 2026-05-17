"""History persistence — save/load analysis history to disk.

Stores only scalar results (file, bpm, key) to keep the file small.
Full feature arrays (spectrograms, chromagrams) are NOT persisted.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_HISTORY_DIR = Path.home() / ".music-analyzer"
_HISTORY_FILE = _HISTORY_DIR / "history.json"


def _ensure_dir() -> None:
    """Create the history directory if it does not exist."""
    _HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def save_entry(entry: dict[str, Any]) -> None:
    """Append a single analysis entry to the history file.

    Args:
        entry: Dictionary with keys ``file``, ``bpm``, ``key``, etc.
               May include extra metadata (but NOT full signal arrays).
    """
    _ensure_dir()
    history = []
    if _HISTORY_FILE.exists():
        try:
            history = json.loads(_HISTORY_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Corrupt history file, starting fresh: %s", exc)

    # Keep only scalar entries for persistence
    scalar = {k: v for k, v in entry.items() if isinstance(v, (str, float, int, bool))}
    history.append(scalar)

    _HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.debug("History saved (%d entries)", len(history))


def load_history() -> list[dict[str, Any]]:
    """Load all analysis entries from the history file.

    Returns:
        A list of scalar-only feature dictionaries.
    """
    if not _HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(_HISTORY_FILE.read_text(encoding="utf-8"))
        logger.info("Loaded %d history entries", len(data))
        return data
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to load history: %s", exc)
        return []
