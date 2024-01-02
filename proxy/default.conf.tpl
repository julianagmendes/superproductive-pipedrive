upstream uwsgicluster {
  server unix:///tmp/uwsgi.sock;
  server 192.168.1.235:3031;
  server 10.0.0.17:3017;
}

server {
        listen ${LISTEN_PORT};

        location /static {
            alias /vol/static;
        }

        location / {
            uwsgi_pass uwsgicluster;
            include                 /etc/nginx/uwsgi_params;
            client_max_body_size    10M;
        }
    }



