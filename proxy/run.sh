#!/bin/sh

set -e

# Generate Nginx configuration from template
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# Start Nginx in the foreground
nginx -g 'daemon off;'
