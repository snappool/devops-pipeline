# Phase 2: Add Postgres with docker-compose

## What changed

| File | Change |
|------|--------|
| `db.py` (new) | Connects to Postgres and counts visits |
| `app.py` | New `/visits` page |
| `requirements.txt` | Added `psycopg2-binary` (the Python driver for Postgres) |
| `Dockerfile` | Now also copies `db.py` into the image |
| `docker-compose.yml` | New `db` service, a volume, and a health check |
| `tests/test_app.py` | 2 new tests using a fake database |

## New ideas

- **Two containers, one network.** Compose puts `web` and `db` on a private network.
  `web` reaches the database at the hostname `db`: the service name.
- **Environment variable config.** The app reads `DATABASE_URL`, so the same image
  can talk to any database without changing code.
- **Volume.** A container's files disappear when it is removed. A volume
  (`pgdata`) is storage that lives outside the container, so data survives.
- **depends_on + healthcheck.** Postgres takes a few seconds to start. `web` waits
  until `pg_isready` succeeds.
- **Mocking in tests.** CI has no database, so tests replace the database function
  with a fake one. This keeps tests fast and independent.

## Try it

```
docker compose up --build
```

Open http://localhost:5000/visits and refresh a few times. The number goes up.

**Prove the data is saved:**
1. Press Ctrl+C, then run `docker compose down`.
2. Run `docker compose up` again and open `/visits`. The count continues.
3. Now run `docker compose down -v` (the `-v` deletes the volume) and start again.
   The count resets to 1. That's the volume at work.

**Look inside the database:**
```
docker compose exec db psql -U appuser -d appdb -c "SELECT * FROM visits;"
```

## Push it

```
git add .
git commit -m "Add Postgres and visits counter"
git push
```
