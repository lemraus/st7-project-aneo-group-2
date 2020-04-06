#!/bin/sh
sudo apt update -y &&
sudo apt install python3-pip -y &&
sudo pip3 install -r requirements.txt &&
sudo pip3 install azure-storage