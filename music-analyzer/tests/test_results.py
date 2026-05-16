"""Tests for ``SingleTrackResult`` and ``AggregatePlaylistResult``."""

from __future__ import annotations

import numpy as np
import pytest

from src.model.playlist_analyzer import (
    AggregatePlaylistResult,
    AnalysisResultBase,
    SingleTrackResult,
)


class TestAnalysisResultBase:
    """Verifies that the base class enforces the contract."""

    def test_get_summary_raises_not_implemented(self) -> None:
        result = AnalysisResultBase({"dummy": True})
        with pytest.raises(NotImplementedError):
            result.get_summary()


class TestSingleTrackResult:
    """Unit tests for ``SingleTrackResult.get_summary``."""

    @pytest.fixture
    def features(self) -> dict:
        return {
            "path": "/music/track.wav",
            "tempo": 120.5,
            "key": "C Mayor",
        }

    def test_summary_contains_expected_keys(self, features: dict) -> None:
        result = SingleTrackResult(features)
        summary = result.get_summary()
        assert set(summary.keys()) == {"File", "BPM", "Key"}

    def test_bpm_formatting(self, features: dict) -> None:
        result = SingleTrackResult(features)
        assert result.get_summary()["BPM"] == "120.50"

    def test_key_formatting(self, features: dict) -> None:
        result = SingleTrackResult(features)
        assert result.get_summary()["Key"] == "C Mayor"

    def test_filename_is_basename(self, features: dict) -> None:
        result = SingleTrackResult(features)
        assert result.get_summary()["File"] == "track.wav"

    def test_missing_key_returns_n_a(self) -> None:
        result = SingleTrackResult({"tempo": 100.0})
        assert result.get_summary()["Key"] == "N/A"


class TestAggregatePlaylistResult:
    """Unit tests for ``AggregatePlaylistResult.get_summary``."""

    def test_empty_list(self) -> None:
        result = AggregatePlaylistResult([])
        summary = result.get_summary()
        assert summary["Total Tracks"] == 0
        assert summary["Average BPM"] == "N/A"

    def test_single_track(self) -> None:
        track = SingleTrackResult({"tempo": 120.0})
        result = AggregatePlaylistResult([track])
        summary = result.get_summary()
        assert summary["Total Tracks"] == 1
        assert float(summary["Average BPM"]) == pytest.approx(120.0)

    def test_multiple_tracks(self) -> None:
        tracks = [
            SingleTrackResult({"tempo": 100.0}),
            SingleTrackResult({"tempo": 120.0}),
            SingleTrackResult({"tempo": 140.0}),
        ]
        result = AggregatePlaylistResult(tracks)
        summary = result.get_summary()
        assert summary["Total Tracks"] == 3
        assert float(summary["Average BPM"]) == pytest.approx(120.0)
        assert float(summary["Std Dev BPM"]) == pytest.approx(
            float(np.std([100.0, 120.0, 140.0]))
        )
