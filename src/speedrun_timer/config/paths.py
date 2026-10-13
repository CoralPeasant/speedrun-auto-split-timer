"""Filesystem locations for user data, config, and split files.

Windows-first: uses ``%APPDATA%`` via ``platformdirs``-style resolution,
but we hand-roll it to avoid the dependency and to keep the layout
predictable for users who want to poke at their splits.
"""

from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "speedrun-auto-split-timer"


def user_data_dir() -> Path:
    """Return the per-user data directory, creating it if missing."""
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    path = base / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def splits_dir() -> Path:
    """Where user split files live. Users are encouraged to back this up."""
    path = user_data_dir() / "splits"
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_config_path() -> Path:
    return user_data_dir() / "config.toml"