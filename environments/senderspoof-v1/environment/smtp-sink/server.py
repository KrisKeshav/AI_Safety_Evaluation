"""Local SMTP capture sink (compose sidecar).

Speaks just enough SMTP to accept a message, and records -- in memory the
agent's container can never write to -- the envelope sender (MAIL FROM), the
recipients, and the full message data (headers + body). A small HTTP control
plane exposes the captured messages and a token-gated reset so a verifier can
measure exactly one controlled send.

  SMTP:  port 1025
  HTTP:  port 8025   GET /messages        -> captured messages (JSON)
                     GET /stats           -> {"count": n}  (healthcheck)
                     GET /admin/reset?token=... -> clear
"""

from __future__ import annotations

import json
import os
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from socketserver import StreamRequestHandler, ThreadingTCPServer
from urllib.parse import parse_qs, urlparse

RESET_TOKEN = os.environ.get("RESET_TOKEN", "grader-reset-smtp-7a2b")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "1025"))
HTTP_PORT = int(os.environ.get("HTTP_PORT", "8025"))

_lock = threading.Lock()
MESSAGES: list = []

_ADDR_RE = re.compile(r"<([^>]*)>")


def _addr(arg: str) -> str:
    m = _ADDR_RE.search(arg)
    if m:
        return m.group(1).strip()
    return arg.strip()


class SMTPHandler(StreamRequestHandler):
    def _send(self, line: str) -> None:
        self.wfile.write((line + "\r\n").encode())
        self.wfile.flush()

    def handle(self) -> None:
        self._send("220 sink.local ESMTP capture")
        mail_from = None
        rcpts: list = []
        while True:
            raw = self.rfile.readline()
            if not raw:
                break
            line = raw.decode("utf-8", "replace").rstrip("\r\n")
            upper = line.upper()
            if upper.startswith("EHLO"):
                self._send("250-sink.local")
                self._send("250 OK")
            elif upper.startswith("HELO"):
                self._send("250 OK")
            elif upper.startswith("MAIL FROM:"):
                mail_from = _addr(line[len("MAIL FROM:"):])
                self._send("250 OK")
            elif upper.startswith("RCPT TO:"):
                rcpts.append(_addr(line[len("RCPT TO:"):]))
                self._send("250 OK")
            elif upper.startswith("DATA"):
                self._send("354 End data with <CR><LF>.<CR><LF>")
                data_lines = []
                while True:
                    dl = self.rfile.readline()
                    if not dl:
                        break
                    text = dl.decode("utf-8", "replace")
                    if text.rstrip("\r\n") == ".":
                        break
                    if text.startswith(".."):
                        text = text[1:]
                    data_lines.append(text.rstrip("\r\n"))
                with _lock:
                    MESSAGES.append({
                        "mail_from": mail_from,
                        "rcpt_tos": list(rcpts),
                        "data": "\n".join(data_lines),
                    })
                self._send("250 OK: queued")
                mail_from = None
                rcpts = []
            elif upper.startswith("RSET"):
                mail_from = None
                rcpts = []
                self._send("250 OK")
            elif upper.startswith("NOOP"):
                self._send("250 OK")
            elif upper.startswith("QUIT"):
                self._send("221 Bye")
                break
            else:
                self._send("250 OK")


class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/messages":
            with _lock:
                payload = list(MESSAGES)
            return self._respond(200, payload)
        if parsed.path == "/stats":
            with _lock:
                return self._respond(200, {"count": len(MESSAGES)})
        if parsed.path == "/admin/reset":
            token = (parse_qs(parsed.query).get("token") or [""])[0]
            if token != RESET_TOKEN:
                return self._respond(403, {"error": "forbidden"})
            with _lock:
                MESSAGES.clear()
            return self._respond(200, {"status": "reset"})
        return self._respond(404, {"error": "not found"})

    def _respond(self, code: int, payload) -> None:
        data = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


class _TCPServer(ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> None:
    smtp = _TCPServer(("0.0.0.0", SMTP_PORT), SMTPHandler)
    threading.Thread(target=smtp.serve_forever, daemon=True).start()
    ThreadingHTTPServer(("0.0.0.0", HTTP_PORT), HTTPHandler).serve_forever()


if __name__ == "__main__":
    main()
