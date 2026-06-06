# NRMS AI Assistant API — production image
FROM python:3.11-slim-bookworm

WORKDIR /app

# GDAL + build tools for rasterio / rasterstats
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    libspatialindex-dev \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV GDAL_CONFIG=/usr/bin/gdal-config
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY static ./static

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
# Overridden in docker-compose / .env
ENV NRMS_DATA_DIR=/data/rangeland
ENV DATABASE_URL=postgresql://nrms:nrms@postgres:5432/nrms
ENV REDIS_URL=redis://redis:6379/0
ENV GEOSERVER_URL=https://nrms.ati.gov.et/geoserver

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://127.0.0.1:8001/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "1"]
