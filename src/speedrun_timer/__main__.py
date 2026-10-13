"""Entry point for the ``srast`` console script and GUI launcher.

Bootstraps logging, loads user config, spins up the Qt application, and
hands control to the main window. All real work happens in services.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from speedrun_timer.config.loader import load_config
from speedrun_timer.config.paths import user_data_dir
from speedrun_timer.services.app_service import AppService


def _configure_logging(log_dir: Path, verbose: bool) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "srast.log", encoding="utf-8"),
            logging.StreamHandler(sys.stderr),
        ],
    )


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv if argv is None else argv)
    verbose = "--verbose" in argv or "-v" in argv

    data_dir = user_data_dir()
    _configure_logging(data_dir / "logs", verbose)

    log = logging.getLogger("speedrun_timer")
    log.info("speedrun-auto-split-timer starting (data dir=%s)", data_dir)

    config = load_config(data_dir)
    service = AppService(config=config, data_dir=data_dir)
    return service.run()


if __name__ == "__main__":
    raise SystemExit(main())