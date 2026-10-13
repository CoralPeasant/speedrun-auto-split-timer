"""Read and write the project's native split file format.

The format is JSON with a version field. We also read LiveSplit ``.lss``
XML for import, but we never write it — too many quirks to round-trip
safely.
"""

from __future__ import annotations

import json
import logging
from datetime import timedelta
from pathlib import Path

from speedrun_timer.models.split_model import SplitDefinition