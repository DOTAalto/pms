#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate

exec gunicorn --bind 0.0.0.0:8000 pms.wsgi
