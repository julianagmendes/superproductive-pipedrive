
server {
        listen ${LISTEN_PORT};

        location /static {
            alias /vol/static/;
        }

        location / {
            uwsgi_pass              ${APP_HOST}:${APP_PORT};
            include                 /etc/nginx/uwsgi_params;
            proxy_read_timeout 300s;
            proxy_connect_timeout 75s;
            client_max_body_size    10M;
        }
    }



