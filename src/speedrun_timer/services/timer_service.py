"""Run timing service.

Owns the monotonic clock, the split cursor, and the delta-to-best math.
Uses ``time.monotonic`` exclusively — wall-clock time is for display only.
"""

from __future__ import annotations

import logging
import time
from datetime import timedelta
from typing import Callable, Optional

from speedrun_timer.models.split_model import (
    RunState,
    SplitRecord,
    SplitStatus,
)

log = logging.getLogger(__name__)

StateListener = Callable[[RunState], None]


class TimerService:
    def __init__(self, state: RunState) -> None:
        self._state = state
        self._listeners: list[StateListener] = []

    @property
    def state(self) -> RunState:
        return self._state

    def subscribe(self, listener: StateListener) -> None:
        self._listeners.append(listener)

    def _emit(self) -> None:
        for listener in self._listeners:
            try:
                listener(self._state)
            except Exception:
                log.exception("state listener raised; continuing")

    def start(self, countdown: float = 0.0) -> None:
        if self._state.is_running:
            return
        self._state.started_at_monotonic = time.monotonic() + countdown
        self._state.finished_at_monotonic = None
        self._advance_to_first_pending()
        self._emit()

    def split(self) -> Optional[SplitRecord]:
        if not self._state.is_running:
            return None
        now = time.monotonic()
        record = self._current_record()
        if record is None:
            return None
        record.elapsed = timedelta(seconds=now - self._state.started_at_monotonic)  # type: ignore[operator]
        record.status = SplitStatus.DONE
        if record.definition.best_time is not None:
            record.delta_to_best = record.elapsed - record.definition.best_time
        self._state.current_index += 1
        if self._state.current_index >= len(self._state.splits):
            self._state.finished_at_monotonic = now
        else:
            self._advance_to_first_pending()
        self._emit()
        return record

    def reset(self) -> None:
        self._state.started_at_monotonic = None
        self._state.finished_at_monotonic = None
        self._state.current_index = 0
        for record in self._state.splits:
            record.status = SplitStatus.PENDING
            record.elapsed = None
            record.delta_to_best = None
        self._emit()

    def _current_record(self) -> Optional[SplitRecord]:
        if self._state.current_index >= len(self._state.splits):
            return None
        return self._state.splits[self._state.current_index]

    def _advance_to_first_pending(self) -> None:
        while self._state.current_index < len(self._state.splits):
            record = self._state.splits[self._state.current_index]
            if record.status == SplitStatus.SKIPPED:
                self._state.current_index += 1
                continue
            record.status = SplitStatus.ACTIVE
            return