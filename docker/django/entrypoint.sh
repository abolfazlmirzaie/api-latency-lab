#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

until python -c "
import os
import psycopg

try:
    psycopg.connect(
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
    )
except psycopg.OperationalError:
    raise SystemExit(1)
"; do
    sleep 1
done

echo "PostgreSQL is ready."

echo "Running migrations..."

python manage.py migrate --noinput

echo "Starting Django..."

exec "$@"