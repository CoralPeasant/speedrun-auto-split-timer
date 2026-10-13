"""Detector orchestration.

Pulls frames from a capture adapter, feeds every registered detector,
and forwards fired events to the timer service. Runs on its own thread
so the UI never blocks on capture.
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Optional

from speedrun_timer.capture.base import CaptureAdapter
from speedrun_timer.detectors.base import Detector, SplitEvent
from speedrun_timer.services.timer_service import TimerService

log = logging.getLogger(__name__)


class DetectorService:
    def __init__(
        self,
        capture: CaptureAdapter,
        timer: TimerService,
        poll_interval_ms: int = 16,
    ) -> None:
        self._capture = capture
        self._timer = timer
        self._poll_interval = poll_interval_ms / 1000.0
        self._detectors: list[Detector] = []
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()

    def register(self, detector: Detector) -> None:
        self._detectors.append(detector)

    def start(self) -> None:
        if self._thread is not None:
            return
        self._stop.clear()
        self._capture.start()
        self._thread = threading.Thread(target=self._loop, name="detector-loop", daemon=True)
        self._thread.start()
        log.info("detector service started with %d detectors", len(self._detectors))

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
            self._thread = None
        self._capture.stop()
        log.info("detector service stopped")

    def _loop(self) -> None:
        while not self._stop.is_set():
            loop_start = time.monotonic()
            frame = self._capture.grab()
            now = time.monotonic()
            for detector in self._detectors:
                event = detector.observe(frame, now)
                if event is not None:
                    self._on_event(event)
            elapsed = time.monotonic() - loop_start
            sleep_for = self._poll_interval - elapsed
            if sleep_for > 0:
                self._stop.wait(sleep_for)

    def _on_event(self, event: SplitEvent) -> None:
        log.info(
            "auto-split fired: %s/%s (conf=%.2f)",
            event.detector_id,
            event.split_name,
            event.confidence,
        )
        self._timer.split()