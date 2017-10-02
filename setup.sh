#!/usr/bin/env bash

if [ "$EUID" -ne 0 ]
then
    echo 'The script needs to be run as root.'
    # if not root exit
    exit 0
fi

if [ ! -f /etc/VMInit.py ]; then
    cp ./VMInit.sh /etc/init.d/VMInit
    retval1=$?
    cp ./VMInit.py /etc/VMInit.py
    retval2=$?
    touch /etc/vmlist
    retval3=$?
    #check if the copy succeeded

    echo "Would you like to enable the init script? (yes or no)"
    read answer
    if [ $answer == "yes" ]; then
        update-rc.d VMInit defaults
    else
        echo "Very well. If you wish to do it later, simply run the command 'sudo update-rc.d VMInit defaults.'"
    fi
    #maybe there is better way for this
    success=$(($retval1 + $retval2 + $retval3))

    if [[ $success -eq 0 ]]; then
        #some details for the user, it's always nice to know where scripts are 
        echo "The required files have been copied successfully."
        echo "The init script at /etc/init.d/VMInit has beenn enabled with update-rc.d VMInit defaults"
        echo "The python executable resides at /etc/VMInit.py"
        echo "Your VMs list resides at /etc/vmlist" 
    else
        echo "Copying files failed"
    fi

    exit 0
fi

