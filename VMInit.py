"""
    VMInit
    A simple script for managing VirtualBox VMs when powering off/booting up a server.
    Coded by:
    Kyriakos Giannakis (kerk12gr@gmail.com)

    Licence: GNU GPLv3
    See the included LICENCE.md file for more info.
"""

import argparse
import subprocess
import re
import time

def loadVMs(vmlist_file="/etc/vmlist"):
    """ Loads the VMs from the vmlist """
    vmlist = open(vmlist_file, "r")
    vms = vmlist.readlines()
    vmlist.close()
    if len(vms) == 0:
        print "No VMs were specified. Edit the vmlist file in /etc/vmlist to specify your VMs"
        exit(1)

    # TODO Strip comment and empty lines.
    return vms

def checkForRunningVM(name, user=None):
    """ Checks if a VM is running. """
    # (VMs in 'VBoxManage list runningvms' use this format)
    reg = r'\"' + name + '" \{\w{8}-\w{4}-\w{4}-\w{4}-\w{12}\}'
    p = re.compile(reg)
    if user is not None:
        runningvms = subprocess.check_output(["sudo", "-u", user, "VBoxManage", "list", "runningvms"]).split("\n")
    else:
        runningvms = subprocess.check_output(["VBoxManage", "list", "runningvms"]).split("\n")

    # For each running VM, try to match p. If at least 1 VM matches, return True
    # ... This means that the VM is in the list of the running VMs.
    for vm in runningvms:
        if p.match(vm.rstrip()):
            return True
    return False

def check_user(vm_string):
    """ Checks the vmlist entry, to determine if the VM belongs to another user. """
    # VMs that belong to non-root users match this format:
    check_str = re.compile(r'(\w* ?)*::(\w)*')
    if check_str.match(vm_string):
        tmp = vm_string.split("::")
        vm = tmp[0]
        user = tmp[1]
        return vm, user

    return vm_string, None

if __name__ == "__main__":
    # The number of times that VMInit will try to check for a running VM.
    RETRIES = 10
    # After each try, VMInit sleeps for this amount of seconds.
    RETRY_TIME = 5

    parser = argparse.ArgumentParser(description="Starts up VirtualBox VMs at system boot, and shuts them down at powerdown respectively.")
    parser.add_argument("--start", help="Turns on all VMs specified in the vmlist file.", action="store_true")
    parser.add_argument("--stop", help="Stops (saves the state of) all the VMs specified in the vmlist file.", action="store_true")

    args = parser.parse_args()

    vms = loadVMs()

    if args.start:
        for vm in vms:
            # Strip empty lines and comments.
            if vm == "":
                continue

            if vm[0] == "#":
                continue

            # Check for the VM's owner.
            vm, user = check_user(vm.rstrip())

            # Start the VM by calling VBoxManage startvm.
            if user is not None:
                subprocess.call(["sudo", "-u", user, "VBoxManage", "startvm", vm, "--type", "headless"])
            else:
                subprocess.call(["VBoxManage", "startvm", vm, "--type", "headless"])

    elif args.stop:
        # 1. Check every VM in the list
        for vm in vms:
            if vm == "":
                continue
            if vm[0] == "#":
                continue

            vm, user = check_user(vm.rstrip())

            # Check if the VM is running, to begin with...
            if not checkForRunningVM(name=vm, user=user):
                continue

            # 2. Run VBoxManage controlvm ... acpipowerbutton
            print "Shutting down", vm

            if user is not None:
                subprocess.call(["sudo", "-u", user, "VBoxManage", "controlvm", vm, "acpipowerbutton"])
            else:
                subprocess.call(["VBoxManage", "controlvm", vm, "acpipowerbutton"])

            found = True
            # 3. Repeat RETRIES times, RETRY_TIME seconds of wait time each.
            for i in range(1,RETRIES):
                # 3.4 If a running VM with the name of the shutting-down VM wasn't found, then it's shut down successfully.
                # Move to the next one...
                if not checkForRunningVM(vm, user):
                    found = False
                    break
                else:
                    time.sleep(RETRY_TIME)

            # 4. If the VM is found even after 4 checks, then it didn't shut down successfully.
            if found:
                # The VM didn't shut down.
                # TODO Fallback...
                exit(1)
    else:
        print "No arguments specified."
        exit(1)

    exit(0)


