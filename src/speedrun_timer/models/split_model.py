"""Split definitions and run state.

A ``SplitDefinition`` is static: it describes one segment of a run.
A ``RunState`` is dynamic: it tracks where we are in the run right now.
"""

from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SplitStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    DONE = "done"
    SKIPPED = "skipped"


class SplitDefinition(BaseModel):
    name: str
    detector_id: str
    ideal_time: Optional[timedelta] = None
    best_time: Optional[timedelta] = None
    notes: str = ""


class SplitRecord(BaseModel):
    definition: SplitDefinition
    status: SplitStatus = SplitStatus.PENDING
    elapsed: Optional[timedelta] = None
    delta_to_best: Optional[timedelta] = None


class RunState(BaseModel):
    game_id: str
    category: str
    splits: list[SplitRecord] = Field(default_factory=list)
    started_at_monotonic: Optional[float] = None
    finished_at_monotonic: Optional[float] = None
    current_index: int = 0

    @property
    def is_running(self) -> bool:
        return self.started_at_monotonic is not None and self.finished_at_monotonic is None