"""Formatting helpers for split times and deltas.

Runners read these constantly during a run, so the format is fixed:
``M:SS.mmm`` for times, ``+S.mmm`` / ``-S.mmm`` for deltas.
"""

from __future__ import annotations

from datetime import timedelta


def format_duration(value: timedelta) -> str:
    total_ms = int(value.total_seconds() * 1000)
    sign = "-" if total_ms < 0 else ""
    total_ms = abs(total_ms)
    minutes, rem_ms = divmod(total_ms, 60_000)
    seconds, ms = divmod(rem_ms, 1000)
    return f"{sign}{minutes}:{seconds:02d}.{ms:03d}"


def format_delta(value: timedelta) -> str:
    total_ms = int(value.total_seconds() * 1000)
    sign = "+" if total_ms >= 0 else "-"
    total_ms = abs(total_ms)
    seconds, ms = divmod(total_ms, 1000)
    return f"{sign}{seconds}.{ms:03d}"