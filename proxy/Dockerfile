# Use the official Nginx image as a base
FROM nginxinc/nginx-unprivileged:1-alpine

# Copy Nginx configuration template
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl

# Set environment variables
ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

# Switch to root user temporarily to perform setup
USER root

# Create directory for static files and set permissions
RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf

# Create log directory and set permissions
RUN mkdir -p /var/log/gunicorn && \
    chown nginx:nginx /var/log/gunicorn && \
    sudo chmod 666 /var/log/gunicorn.log

# Install Python3 and Gunicorn
RUN apk add --no-cache python3 py3-pip && \
    pip3 install gunicorn

# Switch back to the nginx user
USER nginx

# Expose the static volume
VOLUME /vol/static

# Start Nginx and Gunicorn
CMD ["sh", "-c", \
    "envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf && \
    touch /var/log/gunicorn.log && \
    chown nginx:nginx /var/log/gunicorn.log && \
    gunicorn PipeDriveAutomation.wsgi:application -b 0.0.0.0:${APP_PORT} --pythonpath /app 2>&1 | tee /var/log/gunicorn.log & \
    nginx -g 'daemon off;'"]
