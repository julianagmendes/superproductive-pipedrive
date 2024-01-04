#!/bin/sh
# deploying

set -e

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py runserver

uwsgi --socket :9000 --workers 4 --master --enable-threads --module PipeDriveAutomation.wsgi