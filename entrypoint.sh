#!/bin/bash

# Exit on error
set -e

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser if env vars are present
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "Ensuring superuser exists..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser created: {username}')
else:
    print(f'Superuser {username} already exists')
END
fi

# Seed database if empty
echo "Checking if database needs seeding..."
python manage.py shell << END
from stores.models import ShopConfig
if ShopConfig.objects.count() == 0:
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
