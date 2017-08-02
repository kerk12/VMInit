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
    for vm in vms:
        if vm.rstrip() == "":
            continue


        subprocess.call(["VBoxManage", "controlvm", vm.rstrip(), "acpipowerbutton"])
        reg = r'\"' + vm.rstrip() + '" \{\w{8}-\w{4}-\w{4}-\w{4}-\w{12}\}'
        found = True
        p = re.compile(reg)
        for i in range(1,5):
            runningvms = subprocess.check_output(["VBoxManage", "list", "runningvms"]).split("\n")
            j = 0
            foundLocal = False
            while j < len(runningvms):
                if p.match(runningvms[j].rstrip()):
                    foundLocal = True
                    break
                j += 1

            if not foundLocal:
                found = False
                break
            else:
                time.sleep(15)

        if found:
            # The VM didn't shut down.
            exit(1)
else:
    print "No arguments specified."
    exit(1)

exit(0)


