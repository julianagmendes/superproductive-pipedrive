#!/bin/sh

set -e

# Generate Nginx configuration from template
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# Start Gunicorn with default settings
gunicorn your_django_app.wsgi:application -b 0.0.0.0:${APP_PORT} &

# Start Nginx in the foreground
nginx -g 'daemon off;'
