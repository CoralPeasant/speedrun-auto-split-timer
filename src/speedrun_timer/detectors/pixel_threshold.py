"""Generic pixel-threshold detector.

Watches a small region for a colour transition. Useful for games whose
split condition is "this HUD element changes colour" — surprisingly many.
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np

from speedrun_timer.detectors.base import Detector, SplitEvent

log = logging.getLogger(__name__)


class PixelThresholdDetector(Detector):
    def __init__(
        self,
        detector_id: str,
        split_name: str,
        region: tuple[int, int, int, int],
        target_bgr: tuple[int, int, int],
        tolerance: int = 24,
        min_consecutive: int = 3,
    ) -> None:
        self.detector_id = detector_id
        self.split_name = split_name
        self._region = region
        self._target = np.array(target_bgr, dtype=np.int16)
        self._tolerance = tolerance
        self._min_consecutive = min_consecutive
        self._streak = 0
        self._fired = False

    def reset(self) -> None:
        self._streak = 0
        self._fired = False

    def observe(self, frame: Optional[np.ndarray], monotonic_now: float) -> Optional[SplitEvent]:
        if frame is None or self._fired:
            return None

        x0, y0, x1, y1 = self._region
        patch = frame[y0:y1, x0:x1]
        if patch.size == 0:
            return None

        mean = patch.reshape(-1, 3).mean(axis=0).astype(np.int16)
        if int(np.abs(mean - self._target).max()) <= self._tolerance:
            self._streak += 1
        else:
            self._streak = 0

        if self._streak >= self._min_consecutive:
            self._fired = True
            confidence = min(1.0, self._streak / (self._min_consecutive * 2))
            log.debug("detector %s fired split=%s", self.detector_id, self.split_name)
            return SplitEvent(self.detector_id, self.split_name, confidence)
        return None