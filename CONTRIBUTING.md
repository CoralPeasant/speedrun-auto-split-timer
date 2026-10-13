# Contributing to speedrun-auto-split-timer

Thanks for wanting to help make auto-splitting less cursed. This project exists because manually hitting split keys at 3am on a 4-hour category is a war crime against wrists.

## Getting set up

```bash
git clone https://github.com/speedrun-auto-split-timer/speedrun-auto-split-timer.git
cd speedrun-auto-split-timer
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

You need Python 3.11+ on Windows. The capture backend uses the Windows Graphics Capture API through `dxcam`; on Linux/macOS the project falls back to a stub backend and the timer runs in manual mode.

## What we want

- **New auto-split detectors.** The `detectors/` package is where game-specific logic lives. If you can describe a memory value, a pixel region, or a log line that reliably fires on a split event, we want it.
- **New capture adapters.** `capture/` is a thin layer over whatever grabs frames. If you've got a faster path on a specific GPU, send it.
- **Bug fixes with a repro.** "It doesn't work" is not a bug report. "It doesn't work on Celeste 1.4.0.0 with the framerate unlocked, here's the log" is a bug report.

## What we don't want

- Detectors that read memory from a process you don't own. This tool is for the runner's own game on the runner's own machine.
- Anything that touches anti-cheat. If your game has kernel anti-cheat, this tool will not work with it and we will not help you make it work.
- Pull requests that reformat the whole repo. We use `ruff` and `black`, run them, don't argue with them.

## Style

- Type hints on every public function. `mypy --strict` is the bar.
- No `print()` in library code. Use the `logging` module, logger name = module name.
- Tests live next to the code they test under `tests/`. If you add a detector, add a test with a recorded frame fixture.

## Commit messages

Conventional commits, please. `feat(detectors): add Celeste chapter 7 split`, `fix(capture): handle monitor hotplug`. Not "fixed stuff".

## Reviewing

Two approvals for anything in `core/`. One approval for everything else. If your PR sits for a week, ping the maintainers — we're runners too, we're probably mid-run.