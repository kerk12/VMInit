import unittest, tempfile, shutil
from VMInit import loadVMs, check_user


class TestVMInit(unittest.TestCase):
    def setUp(self):
        """ Creates a custom vmlist in a temporary directory, in order for tests to be performed. """
        contents = ["VM1\n","VM2::kerk12"]

        self.tempdir = tempfile.mkdtemp()
        shutil.copyfile("vmlist.txt", self.tempdir+"/vmlist.txt")

        with open(self.tempdir+"/vmlist.txt", "a") as vmlist:
            vmlist.writelines(contents)

        self.vms = loadVMs(vmlist_file=self.tempdir+"/vmlist.txt")

    def tearDown(self):
        """ Deletes tempdir, once a test is complete. """
        shutil.rmtree(self.tempdir)


    def test_vmdetection(self):
        """ Checks if the 2 VMs entered in the vmlist were detected successfully. """
        self.assertEqual(len(self.vms), 2)

    def test_userdetection(self):
        """ Checks if the correct user for each VM is detected successfully. """
        vm, user = check_user(self.vms[0])
        self.assertEqual(vm, "VM1")
        self.assertEqual(user, None)
        vm, user = check_user(self.vms[1])
        self.assertEqual(vm, "VM2")
        self.assertEqual(user, "kerk12")

if __name__ == "__main__":
    unittest.main()