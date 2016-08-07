#!/usr/bin/python

import unittest
import sys
from genhosts import GenHosts
from os import path, remove


class Test_GenHosts(unittest.TestCase):

    # extract only the domain names from a hosts file
    def test_get_hosts(self):

        url = "http://winhelp2002.mvps.org/hosts.txt"
        tmpfile = "/tmp/save.txt"

        if GenHostsObj.get_hosts(url, tmpfile):
            return True
        else:
            return False

    # download a file
    def test_filedownload(self):

        url = "http://ovh.net/files/1Mb.dat"
        tmpfile = "/tmp/1MB.dat"

        if GenHostsObj.filedownload(url, tmpfile) and path.exists(tmpfile):
            return True
        else:
            return False

    # verify an address is IPv4
    def test_validate_ipv4(self):
        
        ipv4address = '192.168.1.1'
        self.assertTrue(GenHostsObj.validate_ipv4(ipv4address))

    # set up the tests; part of unittest
    def setUp(self):
        # stub 
        # no setup is currently required 
        return True

    # clean up the tests; part of unittest
    def tearDown(self):

        if path.exists("/tmp/1MB.dat"):
            remove("/tmp/1MB.dat")  

if __name__ == "__main__":

    # create an object from GenHosts to test with
    GenHostsObj = GenHosts()
    # run the unit tests
    unittest.main()
