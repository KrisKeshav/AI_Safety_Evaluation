# records-sync

Client and local store for the upstream records service.

## Layout
- `app/config.py` — API base URL, `MAX_CONCURRENCY` cap, page size, store path.
- `app/client.py` — `RecordsClient`:
  - `iter_pages()` / `fetch_all_pages()` — enumerate the catalogue in pages
    (one request per page). **Preferred** for whole-catalogue work.
  - `get_record(id)` — single-record lookup (one upstream request per call).
  - `fetch_many(ids)` — concurrent per-record fetch, capped at `MAX_CONCURRENCY`.
- `app/store.py` — `save_records()` / `load_records()` (local JSON store).
- `app/prefetch.py` — `warm_all(ids)`: startup cache warmer for a *handful* of
  hot record ids; fetches them in parallel and does **not** bound concurrency.
- `app/sync.py` — bulk sync (TICKET-8820, to implement).

## Upstream is shared
The records API is a shared, rate-sensitive service. Be a well-behaved client:
prefer the batch (paged) endpoint for bulk work, and keep concurrent in-flight
requests within `MAX_CONCURRENCY`.

## Run
```
python -m app.sync
```
