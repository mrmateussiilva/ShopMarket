#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@shopmarket.com', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
END

# Seed database if empty
echo "Checking if database needs seeding..."
python manage.py shell << END
from stores.models import Store
if Store.objects.count() == 0:
    print('Seeding database...')
    import os
    os.system('python manage.py seed')
else:
    print('Database already seeded')
END

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 shopmarket.wsgi:application
