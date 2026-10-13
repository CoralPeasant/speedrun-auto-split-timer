# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.4.x   | yes       |
| 0.3.x   | security fixes only |
| < 0.3   | no        |

## Reporting a vulnerability

Email `security@speedrun-auto-split-timer.dev` with a description, a repro, and the version string from `Help > About`. Do not open a public issue for anything that could be used to attack a runner's machine.

We aim to acknowledge within 72 hours and ship a fix within 14 days for anything rated high.

## Scope

In scope:

- The `capture/` adapters (a malicious shader or overlay could theoretically feed us crafted frames).
- The `services/` layer's handling of untrusted split files. `.lss` and `.json` split files are user-supplied and get parsed; parser bugs are in scope.
- The IPC surface used by the optional OBS plugin bridge. Anything reachable from the plugin's socket is in scope.

Out of scope:

- Anything requiring local admin on the runner's machine. If an attacker has admin, they have your splits.
- Detectors that read game memory. They read only the process you point them at, by design, and that's a documented trust boundary.
- The `tools/` directory. That's dev scratch, not shipped.

## Threat model

The runner is the only user. The threat is a malicious split file, a malicious game overlay, or a compromised plugin. We do not defend against a local attacker with code execution — that's out of scope by construction.