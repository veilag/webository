#!/bin/bash

GUNICORN_SERVICE="/etc/systemd/system/gunicorn-$USERNAME.service"

sudo bash -c "cat <<EOL > '$GUNICORN_SERVICE'
[Unit]
Description=Gunicorn daemon for $USERNAME
After=network.target

[Service]
User=$USERNAME
Group=www-data
WorkingDirectory=
ExecStart=

[Install]
WantedBy=multi-user.target
EOL"

sudo chown "$USERNAME":"$USERNAME" "$GUNICORN_SERVICE"
sudo chmod 644 "$GUNICORN_SERVICE"

sudo systemctl daemon-reload
