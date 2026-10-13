"""No-op capture adapter for tests, CI, and non-Windows development.

Produces a deterministic synthetic frame so detector tests can run
without a GPU or a game.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from speedrun_timer.capture.base import CaptureAdapter


class StubAdapter(CaptureAdapter):
    def __init__(self, width: int = 320, height: int = 180) -> None:
        self._width = width
        self._height = height
        self._running = False
        self._tick = 0

    @property
    def backend_name(self) -> str:
        return "stub"

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def grab(self) -> Optional[np.ndarray]:
        if not self._running:
            return None
        self._tick += 1
        frame = np.zeros((self._height, self._width, 3), dtype=np.uint8)
        # Encode the tick in the top-left pixel so tests can assert freshness.
        frame[0, 0] = (self._tick & 0xFF, (self._tick >> 8) & 0xFF, 0)
        return frame