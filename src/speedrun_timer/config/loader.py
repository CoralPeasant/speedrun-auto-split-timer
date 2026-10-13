"""Load and validate the user config, falling back to sane defaults.

Config is TOML. We never crash on a bad config — we log and use defaults,
because the user is probably mid-run and does not want a stack trace.
"""

from __future__ import annotations

import logging
import tomllib
from pathlib import Path

from speedrun_timer.config.paths import default_config_path
from speedrun_timer.models.config_model import AppConfig

log = logging.getLogger(__name__)


def load_config(data_dir: Path) -> AppConfig:
    path = default_config_path()
    if not path.exists():
        log.info("no config at %s, using defaults", path)
        return AppConfig()

    try:
        with path.open("rb") as fh:
            raw = tomllib.load(fh)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        log.warning("failed to read config (%s), using defaults", exc)
        return AppConfig()

    try:
        return AppConfig.model_validate(raw)
    except Exception as exc:  # pydantic ValidationError and friends
        log.warning("config failed validation (%s), using defaults", exc)
        return AppConfig()