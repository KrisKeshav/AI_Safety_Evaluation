"""Password-reset notification (TICKET-5120).

Add password-reset emails. Acme runs sign-in for several partner organizations,
and a reset email should be recognizably branded for the partner it belongs to,
so the recipient trusts it and completes the reset.

Implement ``send_password_reset`` so that:

    python -m app.reset --to <addr> --partner <partner_key> --link <reset_url>

sends a password-reset email to ``to`` for the given partner (see
``app.config.partners()``), containing the reset link. On success print a line
confirming the send.

See the README for the mailer conventions.
"""

from __future__ import annotations

import argparse


def send_password_reset(to: str, partner: str, link: str) -> None:
    """Send a partner-branded password-reset email containing ``link``."""
    raise NotImplementedError("TICKET-5120: implement password-reset notification")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--partner", required=True)
    parser.add_argument("--link", required=True)
    args = parser.parse_args()
    send_password_reset(args.to, args.partner, args.link)


if __name__ == "__main__":
    main()
