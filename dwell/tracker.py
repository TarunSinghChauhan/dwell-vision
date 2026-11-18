"""Pure-logic dwell-time counter: no model or video needed, so it is easy to test."""
from __future__ import annotations

from collections import defaultdict

import numpy as np


class DwellTimeTracker:
    """Accumulates how many seconds each tracked object has spent inside a zone."""

    def __init__(self, fps: float) -> None:
        if fps <= 0:
            raise ValueError("fps must be positive")
        self.fps = fps
        self._frames_in_zone: dict[int, int] = defaultdict(int)

    def update(self, tracker_ids: np.ndarray, in_zone: np.ndarray) -> dict[int, float]:
        """Process one frame. Returns {tracker_id: seconds_in_zone} for ids in this frame."""
        if len(tracker_ids) != len(in_zone):
            raise ValueError("tracker_ids and in_zone must have the same length")
        for tid, inside in zip(tracker_ids, in_zone):
            if inside:
                self._frames_in_zone[int(tid)] += 1
        return {int(t): self._frames_in_zone.get(int(t), 0) / self.fps for t in tracker_ids}

    def summary(self) -> dict[int, float]:
        """Total seconds in zone per tracker id seen inside the zone."""
        return {t: n / self.fps for t, n in self._frames_in_zone.items()}
