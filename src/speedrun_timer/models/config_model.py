"""Typed configuration model. Every field has a default so a partial
config file still produces a usable AppConfig.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class CaptureConfig(BaseModel):
    backend: Literal["dxcam", "mss", "stub"] = "dxcam"
    monitor_index: int = 0
    target_fps: int = Field(default=60, ge=1, le=360)
    region: tuple[int, int, int, int] | None = None


class DetectorConfig(BaseModel):
    game_id: str = "generic"
    poll_interval_ms: int = Field(default=16, ge=1, le=250)
    memory_reads_enabled: bool = False
    process_name: str | None = None


class TimerConfig(BaseModel):
    countdown_seconds: int = Field(default=3, ge=0, le=30)
    auto_start: bool = True
    auto_stop: bool = True
    hotkey_split: str = "F1"
    hotkey_reset: str = "F3"
    hotkey_skip: str = "F2"


class AppConfig(BaseModel):
    capture: CaptureConfig = Field(default_factory=CaptureConfig)
    detector: DetectorConfig = Field(default_factory=DetectorConfig)
    timer: TimerConfig = Field(default_factory=TimerConfig)
    theme: Literal["dark", "light"] = "dark"