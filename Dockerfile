# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN pip install uv

# Copy project files
COPY pyproject.toml ./
COPY manage.py ./
COPY shopmarket ./shopmarket
COPY stores ./stores
COPY catalog ./catalog
COPY pricing ./pricing
COPY cart ./cart
COPY orders ./orders
COPY lists ./lists
COPY cms ./cms
COPY templates ./templates
COPY static ./static

# Install dependencies
RUN uv pip install --system django pillow psycopg2-binary gunicorn

# Create directories for media and static files
RUN mkdir -p /app/media /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "shopmarket.wsgi:application"]
