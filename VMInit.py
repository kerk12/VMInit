import argparse
import subprocess  # TODO Switch to subprocess32
import re
import time

def loadVMs():
    vmlist = open("/etc/vmlist", "r")
    vms = vmlist.readlines()
    vmlist.close()
    if len(vms) == 0:
        print "No VMs were specified. Edit the vmlist file in /etc/vmlist to specify your VMs"
        exit(1)
    return vms

def checkForRunningVM(name):
    # (VMs in 'VBoxManage list runningvms' use this format)
    reg = r'\"' + name.rstrip() + '" \{\w{8}-\w{4}-\w{4}-\w{4}-\w{12}\}'
    p = re.compile(reg)
    runningvms = subprocess.check_output(["VBoxManage", "list", "runningvms"]).split("\n")
    for vm in runningvms:
        if p.match(vm.rstrip()):
            return True
    return False



parser = argparse.ArgumentParser(description="Starts up VirtualBox VMs at system boot, and shuts them down at powerdown respectively.")
parser.add_argument("--start", help="Turns on all VMs specified in the vmlist file.", action="store_true")
parser.add_argument("--stop", help="Stops (saves the state of) all the VMs specified in the vmlist file.", action="store_true")

args = parser.parse_args()

vms = loadVMs()

if args.start:
    for vm in vms:
        if vm == "":
            continue
        subprocess.call(["VBoxManage", "startvm", vm.rstrip(), "--type", "headless"])
elif args.stop:
    # 1. Check every VM in the list
    for vm in vms:
        if vm.rstrip() == "" or not checkForRunningVM(vm.rstrip()):
            continue

        # 2. Run VBoxManage controlvm ... acpipowerbutton
        print "Shutting down", vm.rstrip()
        subprocess.call(["VBoxManage", "controlvm", vm.rstrip(), "acpipowerbutton"])
        found = True
        # 3. Repeat 4 times, 15 seconds of wait time each
        for i in range(1,5):
            # 3.4 If a running VM with the name of the shutting-down VM wasn't found, then it's shut down successfully.
            # Move to the next one...
            if not checkForRunningVM(vm.rstrip()):
                found = False
                break
            else:
                time.sleep(15)

        # 4. If the VM is found even after 4 checks, then it didn't shut down successfully.
        if found:
            # The VM didn't shut down.
            # TODO Fallback...
            exit(1)
else:
    print "No arguments specified."
    exit(1)

exit(0)


