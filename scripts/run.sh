#!/bin/sh
# deploying

set -e


# Ensure that necessary directories exist
mkdir -p /vol/web/logs

# Touch the error.log file
touch /vol/web/logs/error.log

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py makemigrations
python manage.py runserver 0.0.0.0:8000

uwsgi --socket :9000 --workers 4 --master --enable-threads --module PipeDriveAutomation.wsgi