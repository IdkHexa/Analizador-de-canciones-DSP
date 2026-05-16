"""Playlist-level analysis and result aggregation.

Provides a hierarchy of result classes that showcase **inheritance**
and **polymorphism**:

- :class:`AnalysisResultBase` — abstract base.
- :class:`SingleTrackResult` — detailed per-track summary.
- :class:`AggregatePlaylistResult` — statistical aggregation.
- :class:`PlaylistAnalyzer` — collection manager.
"""

from __future__ import annotations

from typing import Any

import numpy as np


class AnalysisResultBase:
    """Abstract base class for analysis results.

    Subclasses **must** override :meth:`get_summary`.
    """

    def __init__(self, raw_data: Any) -> None:
        self._raw_data = raw_data

    def get_summary(self) -> dict[str, Any]:
        """Return a human-readable summary of the analysis.

        Raises:
            NotImplementedError: Subclasses must implement this.
        """
        raise NotImplementedError("El método get_summary() debe ser implementado.")


class SingleTrackResult(AnalysisResultBase):
    """Detailed results for a single audio track.

    Demonstrates **inheritance** from :class:`AnalysisResultBase` and
    **polymorphism** via :meth:`get_summary`.
    """

    def get_summary(self) -> dict[str, str]:
        """Return a dictionary with ``File``, ``BPM``, and ``Key`` entries."""
        return {
            "File": str(self._raw_data.get("path", "N/A")).split("/")[-1],
            "BPM": f"{self._raw_data['tempo']:.2f}",
            "Key": str(self._raw_data.get("key", "N/A")),
        }


class AggregatePlaylistResult(AnalysisResultBase):
    """Aggregate statistics computed from a list of per-track results.

    Demonstrates **inheritance** and **polymorphism** — the same
    ``get_summary()`` interface returns structurally different data.
    """

    def get_summary(self) -> dict[str, Any]:
        """Return aggregate statistics (total tracks, average / std BPM).

        Returns:
            A dict with keys ``Total Tracks``, ``Average BPM``, and
            ``Std Dev BPM`` (or ``N/A`` when no data is available).
        """
        tempos = [
            d._raw_data.get("tempo")  # noqa: SLF001 — intentional for educational example
            for d in self._raw_data
            if d._raw_data.get("tempo") is not None
        ]

        if not tempos:
            return {"Total Tracks": 0, "Average BPM": "N/A"}

        return {
            "Total Tracks": len(tempos),
            "Average BPM": f"{np.mean(tempos):.2f}",
            "Std Dev BPM": f"{np.std(tempos):.2f}",
        }


class PlaylistAnalyzer:
    """Manages a collection of per-track analysis results.

    The primary Model class for playlist-level operations: add results,
    query aggregates.
    """

    def __init__(self) -> None:
        self._results: list[SingleTrackResult] = []

    def add_analysis(self, result_data: dict[str, Any]) -> SingleTrackResult:
        """Wrap *result_data* in a :class:`SingleTrackResult` and store it.

        Args:
            result_data: A features dict (as returned by
                         :meth:`FeatureExtractor.extract_all_features`).

        Returns:
            The newly created :class:`SingleTrackResult`.
        """
        track_result = SingleTrackResult(result_data)
        self._results.append(track_result)
        return track_result

    def get_aggregate_results(self) -> AggregatePlaylistResult:
        """Return an :class:`AggregatePlaylistResult` over all stored tracks."""
        return AggregatePlaylistResult(self._results)
