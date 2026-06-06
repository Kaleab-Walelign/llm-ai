"""PostgreSQL persistence for zonal statistics."""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Any, Generator

import psycopg2
import psycopg2.extras

from app.config import DATABASE_URL

logger = logging.getLogger(__name__)


@contextmanager
def _conn() -> Generator[Any, None, None]:
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_stats(woreda: str, indicator: str, time_key: str) -> dict | None:
    try:
        with _conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT woreda, indicator, time_key, mean, min_val, max_val,
                           pixel_count, score, label, description
                    FROM zonal_stats
                    WHERE lower(woreda) = lower(%s)
                      AND indicator = %s
                      AND time_key = %s
                    """,
                    (woreda, indicator, time_key),
                )
                row = cur.fetchone()
                return dict(row) if row else None
    except Exception as exc:
        logger.warning("PostgreSQL get failed: %s", exc)
        return None


def save_stats(data: dict[str, Any]) -> None:
    try:
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO zonal_stats (
                        woreda, indicator, time_key, mean, min_val, max_val,
                        pixel_count, score, label, description
                    ) VALUES (%(woreda)s, %(indicator)s, %(time_key)s,
                              %(mean)s, %(min_val)s, %(max_val)s,
                              %(pixel_count)s, %(score)s, %(label)s, %(description)s)
                    ON CONFLICT (woreda, indicator, time_key)
                    DO UPDATE SET
                        mean = EXCLUDED.mean,
                        min_val = EXCLUDED.min_val,
                        max_val = EXCLUDED.max_val,
                        pixel_count = EXCLUDED.pixel_count,
                        score = EXCLUDED.score,
                        label = EXCLUDED.label,
                        description = EXCLUDED.description,
                        updated_at = NOW()
                    """,
                    data,
                )
    except Exception as exc:
        logger.warning("PostgreSQL save failed: %s", exc)


def ping() -> bool:
    try:
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                return cur.fetchone() is not None
    except Exception:
        return False
