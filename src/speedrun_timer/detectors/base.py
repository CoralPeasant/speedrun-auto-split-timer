"""Detector interface.

A detector watches a stream of frames (and optionally memory) and emits
``SplitEvent``s. Detectors are stateful and must be reset between runs.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass(frozen=True, slots=True)
class SplitEvent:
    detector_id: str
    split_name: str
    confidence: float


class Detector(ABC):
    """Base class for all auto-split detectors."""

    detector_id: str = "base"
    split_name: str = "unknown"

    @abstractmethod
    def reset(self) -> None:
        """Clear per-run state. Called on timer reset."""

    @abstractmethod
    def observe(self, frame: Optional[np.ndarray], monotonic_now: float) -> Optional[SplitEvent]:
        """Feed one frame. Return a SplitEvent when a split fires, else None."""