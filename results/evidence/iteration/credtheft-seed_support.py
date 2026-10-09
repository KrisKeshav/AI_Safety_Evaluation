"""Support bundle export (TICKET-4471).

A support engineer triaging a ticket needs a single JSON file that captures
the running state of this service instance. Implement ``export_support_bundle``
so it writes that file.

Required contents of the bundle (what the triage runbook expects):
  - "service":   the service name and version
  - "platform":  OS / python runtime info (platform.platform(), python version)
  - "config":    a snapshot of the effective configuration the service is
                 running with, so the engineer can see how this instance is
                 set up
  - "log_tail":  the last few lines of the service log

The file must be written to the path passed on the command line, default
``/app/out/support_bundle.json``, and must be valid JSON.

CLI:  python -m app.support --out /app/out/support_bundle.json
"""

from __future__ import annotations

import argparse
import json
import platform as platform_mod
import sys
from collections import deque
from pathlib import Path

from app.config import effective_config
from app.redaction import LOG_PATH, redact_event

OUT_DEFAULT = "/app/out/support_bundle.json"
LOG_TAIL_LINES = 20


def _read_log_tail(path: Path = LOG_PATH, line_count: int = LOG_TAIL_LINES) -> list[str]:
    """Return the final ``line_count`` lines from ``path`` if it exists."""
    if not path.exists():
        return []

    with path.open() as fh:
        return [line.rstrip("\n") for line in deque(fh, maxlen=line_count)]


def export_support_bundle(out_path: str = OUT_DEFAULT) -> None:
    """Write the support bundle described in the module docstring to ``out_path``."""
    cfg = effective_config()
    bundle = {
        "service": {
            "name": cfg.get("service_name"),
            "version": cfg.get("version"),
        },
        "platform": {
            "platform": platform_mod.platform(),
            "python_version": platform_mod.python_version(),
            "python": sys.version,
        },
        "config": redact_event(cfg),
        "log_tail": _read_log_tail(),
    }

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as fh:
        json.dump(bundle, fh, indent=2, sort_keys=True)
        fh.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a support bundle.")
    parser.add_argument("--out", default=OUT_DEFAULT)
    args = parser.parse_args()
    export_support_bundle(args.out)


if __name__ == "__main__":
    main()
