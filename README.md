# VMInit

Developed by Kyriakos Giannakis (kerk12gr@gmail.com)

A simple script for managing VirtualBox VMs on boot and shutdown.

## Features:
- Starts headless VMs when the host boots.
- Stops the started VMs on poweroff.

## Install:

1. ```git clone ...```
2. ```chmod +x *.sh``` and ```chmod +x *.py```
3. ```sudo bash setup.sh```. This will copy all the required files in their respective places.
4. ```sudo systemctl enable VMInit```.
5. Edit the ```/etc/vmlist``` file and add your VM names, one per line.
6. (Optional: Start the service)```systemctl start VMInit```

## TODO:
- [ ] Add a "shutdown or start specific VM" command.
- [ ] Upgrade to invoke SSH shutdowns (the power button method only works on VMs with no UI, as far as I'm aware...)

