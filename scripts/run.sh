#!/bin/sh
# deploying

set -e

touch /vol/web/logs/error.log
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module PipeDriveAutomation.wsgi