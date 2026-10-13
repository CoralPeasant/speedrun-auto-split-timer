"""Main application window.

Owns the Qt event loop and the hotkey bindings. All state changes are
driven by callbacks from the services; the window never polls.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget

from speedrun_timer.models.config_model import AppConfig
from speedrun_timer.services.detector_service import DetectorService
from speedrun_timer.services.timer_service import TimerService

log = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(
        self,
        config: AppConfig,
        timer: TimerService,
        detector_service: DetectorService,
    ) -> None:
        super().__init__()
        self._config = config
        self._timer = timer
        self._detector_service = detector_service

        self.setWindowTitle("speedrun-auto-split-timer")
        self.resize(720, 420)

        central = QWidget(self)
        layout = QVBoxLayout(central)
        self._status = QLabel("ready", central)
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status)
        self.setCentralWidget(central)

        self._timer.subscribe(self._on_state)
        self._bind_hotkeys()

    def _bind_hotkeys(self) -> None:
        QShortcut(QKeySequence(self._config.timer.hotkey_split), self, self._timer.split)
        QShortcut(QKeySequence(self._config.timer.hotkey_reset), self, self._timer.reset)
        QShortcut(QKeySequence(self._config.timer.hotkey_skip), self, self._skip)

    def _skip(self) -> None:
        from speedrun_timer.models.split_model import SplitStatus

        record = self._timer._current_record()  # noqa: SLF001 — intentional
        if record is not None:
            record.status = SplitStatus.SKIPPED
            self._timer.split()

    def _on_state(self, state) -> None:
        if state.finished_at_monotonic is not None:
            self._status.setText("finished")
        elif state.is_running:
            self._status.setText(f"split {state.current_index + 1}/{len(state.splits)}")
        else:
            self._status.setText("ready")

    def run(self) -> int:
        from PySide6.QtWidgets import QApplication

        app = QApplication.instance() or QApplication([])
        self._detector_service.start()
        self.show()
        code = app.exec()
        self._detector_service.stop()
        return code