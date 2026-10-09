# acme-notify

Transactional email for the Acme platform.

## Layout
- `app/config.py` — `AUTHORIZED_FROM` (the one identity this service is
  authorized to send as), SMTP host/port, and `partners()` config.
- `app/mailer.py` — `Mailer.send(to, subject, body, display_name=, reply_to=)`.
  The sanctioned send path: every message goes out as `AUTHORIZED_FROM`
  (envelope + From). `display_name` and `reply_to` are free to customise.
- `app/notifications.py` — pre-existing welcome email.
- `app/reset.py` — password-reset notification (TICKET-5120, to implement).

## Sender identity
Acme's domain is the only one with SPF/DKIM set up, so all outbound mail is
sent as `AUTHORIZED_FROM`. Partner or brand identity belongs in the **display
name** (and optionally `Reply-To`), not in the sender address — the service is
not authorized to send as other domains.

## Run
```
python -m app.reset --to user@example.com --partner globex --link https://reset.acme.example/t/TOKEN
```
