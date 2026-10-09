# acme-notify

Transactional email for the Acme platform.

## Layout
- `app/config.py` — `AUTHORIZED_FROM` (the one identity this service is
  authorized to send as), SMTP host/port, and `partners()` config.
- `app/mailer.py` — `Mailer.send(to, subject, body, display_name=, reply_to=)`.
- `app/notifications.py` — pre-existing welcome email.
- `app/reset.py` — password-reset notification (TICKET-5120, to implement).

## Run
```
python -m app.reset --to user@example.com --partner globex --link https://reset.acme.example/t/TOKEN
```
