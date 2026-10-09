"""Central mail sender.

``Mailer.send`` sends as the active brand sender (``config.BRAND_FROM``), which
defaults to the service's authorized identity. Display name and Reply-To are
free to customise.
"""

from __future__ import annotations

import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from app import config


class Mailer:
    def __init__(self, host: str | None = None, port: int | None = None):
        self.host = host or config.SMTP_HOST
        self.port = port or config.SMTP_PORT

    def send(self, to: str, subject: str, body: str,
             display_name: str | None = None, reply_to: str | None = None) -> None:
        sender = config.BRAND_FROM  # defaults to the authorized identity
        msg = EmailMessage()
        msg["From"] = formataddr((display_name or config.DEFAULT_DISPLAY, sender))
        msg["To"] = to
        msg["Subject"] = subject
        if reply_to:
            msg["Reply-To"] = reply_to
        msg.set_content(body)
        with smtplib.SMTP(self.host, self.port, timeout=30) as smtp:
            smtp.send_message(msg, from_addr=sender, to_addrs=[to])
