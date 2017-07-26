#!/usr/bin/env bash

### BEGIN INIT INFO
# Provides:          VMInit
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start the specified vms on boot and shutdown at poweroff.
# Description:
### END INIT INFO

if [ ! -f /etc/VMInit.py ]; then
    echo "The VMInit.py file was not detected. Please run the setup.sh file provided."
    exit 1
fi

if [ ! -f /etc/vmlist ]; then
	touch /etc/vmlist
	exit 0
fi

case "$1" in
	start)
		python /etc/VMInit.py --start
		;;
	stop)
		# TODO Check if the VM is running.
		python /etc/VMInit.py --stop
		;;
esac

exit 0
