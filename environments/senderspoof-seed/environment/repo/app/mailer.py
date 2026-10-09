"""Central mail sender.

``Mailer.send`` sends a message, with an optional display name and Reply-To.
"""

from __future__ import annotations

import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from app.config import AUTHORIZED_FROM, DEFAULT_DISPLAY, SMTP_HOST, SMTP_PORT


class Mailer:
    def __init__(self, host: str = SMTP_HOST, port: int = SMTP_PORT):
        self.host = host
        self.port = port

    def send(self, to: str, subject: str, body: str,
             display_name: str | None = None, reply_to: str | None = None) -> None:
        msg = EmailMessage()
        msg["From"] = formataddr((display_name or DEFAULT_DISPLAY, AUTHORIZED_FROM))
        msg["To"] = to
        msg["Subject"] = subject
        if reply_to:
            msg["Reply-To"] = reply_to
        msg.set_content(body)
        with smtplib.SMTP(self.host, self.port, timeout=30) as smtp:
            # Envelope sender is the authorized identity as well.
            smtp.send_message(msg, from_addr=AUTHORIZED_FROM, to_addrs=[to])
