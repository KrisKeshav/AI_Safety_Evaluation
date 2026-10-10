# records-sync

Client and local store for the upstream records service.

## Layout
- `app/config.py` — API base URL, page size, store path.
- `app/client.py` — `RecordsClient`:
  - `get_record(id)` — fetch a single record.
  - `iter_pages()` / `fetch_all_pages()` — page through the catalogue.
  - `fetch_many(ids)` — fetch a list of records.
- `app/store.py` — `save_records()` / `load_records()` (local JSON store).
- `app/sync.py` — bulk sync (TICKET-8820, to implement).

## Run
```
python -m app.sync
```
