#!/bin/sh

if [ "$POSTGRES_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py collectstatic --no-input --clear

echo "Container finnhike_web is running, inserting data..."
python manage.py insert_data

exec "$@"