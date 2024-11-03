#!/bin/bash

DOMAIN=$1
USERNAME=$2

NGINX_CONF="/etc/nginx/sites-available/$DOMAIN"
NGINX_CONF_LINK="/etc/nginx/sites-enabled/$DOMAIN"

sudo bash -c "cat <<EOL > '$NGINX_CONF'
server {
    listen 80;
    server_name $DOMAIN;

    root /home/$USERNAME/public;
    index index.html;

    location / {
      try_files \$uri \$uri/ =404;
    }
}
EOL"

sudo chown "$USERNAME":"$USERNAME" "$NGINX_CONF"
sudo chmod 644 "$NGINX_CONF"

sudo ln -s "$NGINX_CONF" "$NGINX_CONF_LINK"
sudo nginx -t && sudo systemctl reload nginx

sudo certbot --nginx -d "$DOMAIN"
