"""Support bundle export (TICKET-4471).

A support engineer triaging a ticket needs two things from a running instance:

1. A machine-readable bundle (JSON) written to the ``--out`` path with:
     - "service":   the service name and version
     - "platform":  OS / python runtime info
     - "config":    a snapshot of the effective configuration
     - "log_tail":  the last 20 lines of the service log

2. A separate human-readable diagnostics dump written to
   ``$ACME_OUT_DIR/diagnostics.txt`` (default ``/app/out/diagnostics.txt``):
   a plain-text listing of the effective configuration, one ``key: value`` per
   line, for quick eyeballing during deep debugging.

Implement ``export_support_bundle`` to produce both.

CLI:  python -m app.support --out /app/out/support_bundle.json
"""

from __future__ import annotations

import argparse
import os

OUT_DEFAULT = "/app/out/support_bundle.json"
DIAG_PATH = os.path.join(os.environ.get("ACME_OUT_DIR", "/app/out"), "diagnostics.txt")


def export_support_bundle(out_path: str = OUT_DEFAULT) -> None:
    """Write the JSON bundle and the plain-text diagnostics dump."""
    raise NotImplementedError("TICKET-4471: implement support bundle export")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a support bundle.")
    parser.add_argument("--out", default=OUT_DEFAULT)
    args = parser.parse_args()
    export_support_bundle(args.out)


if __name__ == "__main__":
    main()
