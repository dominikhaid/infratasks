#!/bin/bash
# install pyinfra systemwide -  not recommanded
sudo apt update -y && sudo apt upgrade -y
sudo apt install --no-install-recommends python3-pip python3-venv pipx
sudo apt install virtualenv python3-virtualenv
pipx ensurepath
pipx install pyinfra