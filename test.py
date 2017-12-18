import unittest, tempfile, shutil
from VMInit import loadVMs, check_user


class TestVMInit(unittest.TestCase):
    def setUp(self):
        contents = ["VM1\n","VM2::kerk12"]

        self.tempdir = tempfile.mkdtemp()
        shutil.copyfile("vmlist.txt", self.tempdir+"/vmlist.txt")

        with open(self.tempdir+"/vmlist.txt", "a") as vmlist:
            vmlist.writelines(contents)

        self.vms = loadVMs(vmlist_file=self.tempdir+"/vmlist.txt")

    def tearDown(self):
        shutil.rmtree(self.tempdir)


    def test_vmdetection(self):
        self.assertEqual(len(self.vms), 2)

    def test_userdetection(self):
        vm, user = check_user(self.vms[0])
        self.assertEqual(vm, "VM1")
        self.assertEqual(user, None)
        vm, user = check_user(self.vms[1])
        self.assertEqual(vm, "VM2")
        self.assertEqual(user, "kerk12")

if __name__ == "__main__":
    unittest.main()