#!/bin/sh

python manage.py migrate

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())" | grep -q 'True'; then
        python manage.py createsuperuser \
            --noinput \
            --username $DJANGO_SUPERUSER_USERNAME \
            --email $DJANGO_SUPERUSER_EMAIL
    else
        echo "Superuser with username $DJANGO_SUPERUSER_USERNAME already exists."
    fi
fi

echo "Container finnhike_web is running, inserting data..."
python manage.py insert_data

exec "$@"