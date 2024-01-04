
server {
        listen ${LISTEN_PORT};

        location /static {
            alias /vol/static/;
        }

        location / {
            include                 /etc/nginx/uwsgi_params;
            client_max_body_size    10M;
        }
    }



