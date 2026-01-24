#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Wait for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser
echo "Ensuring superuser exists..."
# Django's createsuperuser --no-input uses DJANGO_SUPERUSER_USERNAME, 
# DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD env vars
python manage.py createsuperuser --no-input || echo "Superuser already exists or failed to create"

# Seed data if necessary
echo "Checking if seed is needed..."
python manage.py shell -c "from stores.models import ShopConfig; import os; ShopConfig.objects.count() == 0 and os.system('python manage.py seed')"

# Start the application
if [ "$ENVIRONMENT" = "dev" ]; then
    echo "Starting development server..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "Starting Gunicorn server..."
    exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 shopmarket.wsgi:application
fi
