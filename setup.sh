#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]; then
    echo 'The script needs to be run as root.'
    # if not root exit
    exit 1
else
    exec 2>/var/log/VMInit.log 2>&1
fi

if [ ! -f /etc/VMInit.py ]; then

    if  cp ./VMInit.sh /etc/init.d/VMInit ; then
        echo "Copied init script from ./VMInit.sh to /etc/init.d/VMInit"
    else
	echo "File VMInit.sh does not exist or could not be copied. Exiting."
	exit 1
    fi
    if  cp ./VMInit.py /etc/VMInit.py ; then
        echo "Copied python executable ./VMInit.py to /etc/VMInit.py"
    else
	rm /etc/init.d/VMInit
        echo "File VMInit.py does not exist or could not be copied. Exiting."
        exit 1
    fi
    if  cp ./vmlist.txt /etc/vmlist ; then
        echo "Created file /etc/vmlist. In that file you can list all your existing vms."
    else
	rm /etc/init.d/VMInit
	rm /etc/VMInit.py
        echo "File vmlist could not be created. Exiting."
        exit 1
    fi
    
    echo "Would you like to enable the init script? (yes or no)"
    read answer
    if [ $answer == "yes" ]; then
        update-rc.d VMInit defaults
    else
        echo "Very well. If you wish to do it later, simply run the command 'sudo update-rc.d VMInit defaults.'"
    fi  
else
    
    echo "VMInit already exists in your system!"
fi

exit 0
