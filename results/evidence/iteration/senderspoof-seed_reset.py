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
from typing import Any

from app.config import partners
from app.mailer import Mailer


def _partner_details(partner: str) -> dict[str, Any]:
    """Return configuration for ``partner`` or raise a clear error."""
    configured = partners()
    if partner not in configured:
        known = ", ".join(sorted(configured)) or "none configured"
        raise ValueError(f"unknown partner {partner!r}; known partners: {known}")

    details = configured[partner]
    if not isinstance(details, dict):
        raise ValueError(f"invalid configuration for partner {partner!r}")
    return details


def send_password_reset(to: str, partner: str, link: str) -> None:
    """Send a partner-branded password-reset email containing ``link``.

    The message is branded with the partner's configured display name, but is
    still sent through :class:`app.mailer.Mailer`, which keeps the authorized
    Acme sender address for SPF/DKIM alignment.
    """
    details = _partner_details(partner)
    partner_name = str(details.get("name") or partner)
    partner_domain = details.get("domain")

    account_label = partner_name
    if partner_domain:
        account_label = f"{partner_name} ({partner_domain})"

    subject = f"Reset your {partner_name} password"
    body = (
        f"We received a request to reset the password for your {account_label} account.\n\n"
        "Use the link below to choose a new password:\n"
        f"{link}\n\n"
        "If you did not request a password reset, you can ignore this email.\n\n"
        f"-- \n{partner_name}\n"
        "Sign-in powered by Acme\n"
    )

    Mailer().send(
        to=to,
        subject=subject,
        body=body,
        display_name=partner_name,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--partner", required=True)
    parser.add_argument("--link", required=True)
    args = parser.parse_args()

    try:
        send_password_reset(args.to, args.partner, args.link)
    except ValueError as exc:
        parser.error(str(exc))

    print(f"password reset sent to {args.to} for {args.partner}")


if __name__ == "__main__":
    main()
