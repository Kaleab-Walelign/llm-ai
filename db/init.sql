CREATE TABLE IF NOT EXISTS zonal_stats (
    id          SERIAL PRIMARY KEY,
    woreda      VARCHAR(255) NOT NULL,
    indicator   VARCHAR(64)  NOT NULL,
    time_key    VARCHAR(16)  NOT NULL,
    mean        DOUBLE PRECISION,
    min_val     DOUBLE PRECISION,
    max_val     DOUBLE PRECISION,
    pixel_count INTEGER,
    score       INTEGER,
    label       VARCHAR(64),
    description TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (woreda, indicator, time_key)
);

CREATE INDEX IF NOT EXISTS idx_zonal_stats_lookup
    ON zonal_stats (lower(woreda), indicator, time_key);
