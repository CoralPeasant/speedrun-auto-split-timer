"""Windows Graphics Capture adapter via ``dxcam``.

*dxcam's ``grab()`` returns None when the desktop duplication surface has
not produced a new frame since the last call. We pass that through rather
than blocking, because the detector loop is driven by the timer, not by
capture.*
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np

from speedrun_timer.capture.base import CaptureAdapter
from speedrun_timer.models.config_model import CaptureConfig

log = logging.getLogger(__name__)


class DxcamAdapter(CaptureAdapter):
    def __init__(self, config: CaptureConfig) -> None:
        self._config = config
        self._camera = None

    @property
    def backend_name(self) -> str:
        return "dxcam"

    def start(self) -> None:
        if self._camera is not None:
            return
        import dxcam

        self._camera = dxcam.create(
            output_idx=self._config.monitor_index,
            output_color="BGR",
        )
        if self._camera is None:
            raise RuntimeError("dxcam.create returned None; is the monitor index valid?")
        log.info("dxcam capture started on monitor %d", self._config.monitor_index)

    def stop(self) -> None:
        if self._camera is not None:
            self._camera.release()
            self._camera = None
            log.info("dxcam capture stopped")

    def grab(self) -> Optional[np.ndarray]:
        if self._camera is None:
            return None
        region = self._config.region
        frame = self._camera.grab(region=region) if region else self._camera.grab()
        return frame