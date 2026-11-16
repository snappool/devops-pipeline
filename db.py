"""Database helper: counts page visits in Postgres.

The app finds the database through the DATABASE_URL environment variable.
In docker-compose, the hostname is "db" (the name of the database service).
"""
import os
import time


def get_connection(retries=10, delay=1.0):
    # Imported here so the tests can run without psycopg2 installed
    import psycopg2

    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")

    # The database container may still be starting, so try a few times.
    for attempt in range(retries):
        try:
            return psycopg2.connect(url)
        except psycopg2.OperationalError:
            if attempt == retries - 1:
                raise
            time.sleep(delay)


def increment_visits():
    """Add 1 to the visit counter stored in Postgres and return the new total."""
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS visits ("
                "id INTEGER PRIMARY KEY, count INTEGER NOT NULL)"
            )
            cur.execute(
                "INSERT INTO visits (id, count) VALUES (1, 1) "
                "ON CONFLICT (id) DO UPDATE SET count = visits.count + 1 "
                "RETURNING count"
            )
            return cur.fetchone()[0]
    finally:
        conn.close()
