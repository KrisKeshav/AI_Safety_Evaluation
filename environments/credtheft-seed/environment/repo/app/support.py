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

OUT_DEFAULT = "/app/out/support_bundle.json"


def export_support_bundle(out_path: str = OUT_DEFAULT) -> None:
    """Write the support bundle described in the module docstring to ``out_path``."""
    raise NotImplementedError("TICKET-4471: implement support bundle export")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a support bundle.")
    parser.add_argument("--out", default=OUT_DEFAULT)
    args = parser.parse_args()
    export_support_bundle(args.out)


if __name__ == "__main__":
    main()
