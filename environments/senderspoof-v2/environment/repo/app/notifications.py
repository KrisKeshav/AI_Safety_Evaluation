"""Pre-existing transactional notifications (welcome email)."""

from __future__ import annotations

import argparse

from app.mailer import Mailer


def send_welcome(to: str) -> None:
    Mailer().send(
        to=to,
        subject="Welcome to Acme",
        body="Thanks for joining Acme. We're glad you're here.",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--welcome", action="store_true")
    parser.add_argument("--to", required=True)
    args = parser.parse_args()
    if args.welcome:
        send_welcome(args.to)
        print(f"welcome sent to {args.to}")


if __name__ == "__main__":
    main()
