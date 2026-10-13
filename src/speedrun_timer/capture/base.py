"""Abstract capture adapter.

Adapters are hot-path code. ``grab()`` is called at up to 360 Hz and must
not allocate more than necessary. Return ``None`` when no new frame is
available rather than blocking.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


class CaptureAdapter(ABC):
    """Uniform interface over screen capture backends."""

    @abstractmethod
    def start(self) -> None:
        """Begin capturing. Idempotent."""

    @abstractmethod
    def stop(self) -> None:
        """Stop capturing and release resources. Idempotent."""

    @abstractmethod
    def grab(self) -> Optional[np.ndarray]:
        """Return the latest frame as HxWx3 uint8 BGR, or None if none ready."""

    @property
    @abstractmethod
    def backend_name(self) -> str:
        """Stable identifier used in logs and the About dialog."""