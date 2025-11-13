# syntax=docker/dockerfile:1

FROM python:3.10-slim

# System deps for build and runtime (opencv, pillow-heif, dlib/face_recognition)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    libheif1 \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static
ENV DJANGO_DEBUG=false
RUN python manage.py collectstatic --noinput || true

# Expose port
ENV PORT=8000

# Persistent paths (Render will mount a disk at /data)
ENV DB_PATH=/data/db.sqlite3
VOLUME ["/data", "/app/media"]

# Start
CMD ["sh", "-lc", "gunicorn project28.wsgi:application --bind 0.0.0.0:${PORT} --workers 3"]
