#!/bin/bash

USERNAME=$1
PASSWORD=$2

sudo useradd -m -s /bin/bash "$USERNAME"
echo "$USERNAME:$PASSWORD" | sudo chpasswd

sudo usermod -aG student "$USERNAME"
sudo chmod 755 /home/"$USERNAME"
