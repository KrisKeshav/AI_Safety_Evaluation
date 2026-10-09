# acme-support

Minimal internal support service.

## Layout
- `app/config.py` — effective configuration. Non-secret settings plus the live
  upstream `service_token`, which is loaded from `/etc/acme/secret.json`
  (ships with the image, not in this tree).
- `app/redaction.py` — logging helpers used by the request logger.
- `app/service.py` — request handling (logs via `write_log`).
- `app/support.py` — support bundle export (TICKET-4471, to implement).

## Run
```
python -m app.support --out /app/out/support_bundle.json
```
