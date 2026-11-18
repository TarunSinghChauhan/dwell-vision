import numpy as np
import pytest

from dwell import DwellTimeTracker


def test_counts_seconds_inside_zone():
    t = DwellTimeTracker(fps=10)
    for _ in range(25):
        out = t.update(np.array([1]), np.array([True]))
    assert out[1] == pytest.approx(2.5)


def test_ignores_frames_outside_zone():
    t = DwellTimeTracker(fps=10)
    t.update(np.array([1]), np.array([False]))
    assert t.summary() == {}


def test_multiple_ids_tracked_independently():
    t = DwellTimeTracker(fps=5)
    for _ in range(5):
        t.update(np.array([1, 2]), np.array([True, False]))
    assert t.summary() == {1: 1.0}


def test_invalid_inputs():
    with pytest.raises(ValueError):
        DwellTimeTracker(fps=0)
    with pytest.raises(ValueError):
        DwellTimeTracker(1).update(np.array([1]), np.array([True, False]))
