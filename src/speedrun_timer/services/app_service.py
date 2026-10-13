"""Top-level application service.

Wires config → capture adapter → detectors → timer → UI. This is the
only place that knows about all the layers; everything else is a
dependency-injected leaf.
"""

from __future__ import annotations

import logging
from pathlib import Path

from speedrun_timer.capture.base import CaptureAdapter
from speedrun_timer.capture.dxcam_adapter import DxcamAdapter
from speedrun_timer.capture.stub_adapter import StubAdapter
from speedrun_timer.models.config_model import AppConfig
from speedrun_timer.models.split_model import RunState
from speedrun_timer.services.detector_service import DetectorService
from speedrun_timer.services.timer_service import TimerService

log = logging.getLogger(__name__)


class AppService:
    def __init__(self, config: AppConfig, data_dir: Path) -> None:
        self._config = config
        self._data_dir = data_dir

    def _build_capture(self) -> CaptureAdapter:
        backend = self._config.capture.backend
        if backend == "dxcam":
            try:
                return DxcamAdapter(self._config.capture)
            except Exception as exc:
                log.warning("dxcam unavailable (%s); falling back to stub", exc)
        return StubAdapter()

    def run(self) -> int:
        # Import here so headless environments (CI, tests) never touch Qt.
        from speedrun_timer.ui.main_window import MainWindow

        state = RunState(game_id=self._config.detector.game_id, category="any%")
        timer = TimerService(state)
        detector_service = DetectorService(
            capture=self._build_capture(),
            timer=timer,
            poll_interval_ms=self._config.detector.poll_interval_ms,
        )
        window = MainWindow(
            config=self._config,
            timer=timer,
            detector_service=detector_service,
        )
        return window.run()