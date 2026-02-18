#!/bin/bash
set -e  # stop on first error

echo "Activating virtualenv..."
source /var/app/venv/*/bin/activate

cd /var/app/current

echo ">>> Step 1: Running migrations..."
python manage.py migrate --noinput

# Only the first time you deploy, you might want to load initial data.
#echo ">>> Step 2: Loading initial data..."
#python manage.py loaddata initial_database.json

#echo ">>> Step 2: Creating candidate profiles..."
#python manage.py create_candidates

echo ">>> Step 3: Creating superuser if it doesn't exist..."
python manage.py createsu

echo ">>> Step 4: Collecting static files..."
python manage.py collectstatic --noinput

echo ">>> Step 5: Configuring WSGI..."
# only append once
if ! grep -q "WSGIPassAuthorization On" ../wsgi.conf; then
    echo "WSGIPassAuthorization On" >> ../wsgi.conf
fi
