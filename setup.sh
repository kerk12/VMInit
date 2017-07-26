#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
then
    echo 'The script needs to be run as root.'
fi

if [ ! -f /etc/VMInit.py ]; then
    cp ./VMInit.sh /etc/init.d/VMInit
    cp ./VMInit.py /etc/VMInit.py

    echo "The required files have been copied successfully. Please run the following command to enable the init script:"
    echo ""
    echo 'sudo update-rc.d VMInit defaults'
    exit 0
fi