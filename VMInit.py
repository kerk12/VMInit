import argparse
import subprocess  # TODO Switch to subprocess32

def loadVMs():
    vmlist = open("/etc/vmlist", "r")
    vms = vmlist.readlines()
    vmlist.close()
    if len(vms) == 0:
        print "No VMs were specified. Edit the vmlist file in /etc/vmlist to specify your VMs"
        exit(1)
    return vms

parser = argparse.ArgumentParser(description="Starts up VirtualBox VMs at system boot, and shuts them down at powerdown respectively.")
parser.add_argument("start", help="Turns on all VMs specified in the vmlist file.", action="store_true")
parser.add_argument("stop", help="Stops (saves the state of) all the VMs specified in the vmlist file.", action="store_true")

args = parser.parse_args()

vms = loadVMs()

if args.start:
    for vm in vms:
        if vm == "":
            continue
        subprocess.call(["VBoxManage", "startvm", "\"" + vm + "\"", "--type", "headless"])
elif args.stop:
    for vm in vms:
        if vm == "":
            continue
        subprocess.call(["VBoxManage", "controlvm", "\"" + vm + "\"", "savestate"])
else:
    print "No arguments specified."
    exit(1)

exit(0)


