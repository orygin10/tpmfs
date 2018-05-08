#!/usr/bin/env python2
from filetable import Filetable, FTError
from interface import Interface, InterfaceError
import os
import sys
import yaml
import unittest
dir_path = os.path.dirname(os.path.realpath(__file__))


class FS:
    def __init__(self):
        self.i = Interface()
        try:
            yml = self.i.pull_offset(0)
        except InterfaceError:
            self.write_to_tmp("files:\n", "filetable.yml")
            self.i.push_offset(0, "{0}/tmp/filetable.yml".format(dir_path))
            yml = self.i.pull_offset(0)

        self.ft = Filetable(yml)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
    ############################

    def write_to_tmp(self, data, filename):
        with open("{0}/tmp/{1}".format(dir_path, filename), "w") as fd:
            fd.write(data)
        return True

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.i = Interface()

    def setUp(self):
        # Start with an empty TPM chip
        try:
            self.i.release_offset(0)
        except InterfaceError:
            pass
        
    def test_1_pull_filetable_error(self):
        # Should raise bc there is no filetable in index 0
        with self.assertRaises(InterfaceError):
            self.i.pull_offset(0)

    def test_2_pull_filetable(self):
       # Should not raise InterfaceError 
        with open('{0}/tmp/filetable.yml'.format(dir_path), 'w') as fd:
            fd.write('files:\n')
        self.i.push_offset(0, '{0}/tmp/filetable.yml'.format(dir_path))
        try:
            self.i.pull_offset(0)
        except InterfaceError:
            self.fail()


def tests():
    with FS() as fs:
        assert fs.i.pull_offset(0) != False, "Pulling offset 0 should not return False"

        # Pull filetable into yml_filetable
        filetable = fs.i.pull_offset(0)
        yml_filetable = yaml.load(filetable)

        yaml.dump(yml_filetable, open('{0}/tmp/filetable.yml'.format(dir_path), 'w'))
        assert fs.i.push_offset(0, '{0}/tmp/filetable.yml'.format(dir_path)), "Pushing filetable file to offset 0 should return True"

        # Test list_files() with empty table
        assert fs.ft.list_files(), "Listing all files should return False if table is empty"

        # Test add_file
        assert fs.ft.add_file('data4.txt', 2004), "Adding a non-existing file should return True"
        assert not fs.ft.add_file('data4.txt', 2004), "Adding an already existing file should return False"

        # Test list_files
        assert fs.ft.list_files(), "Listing all files should return True"

        # Test remove_file
        assert fs.ft.remove_file('data4.txt'), "Removing an existing file should return True"
        assert not fs.ft.remove_file('data4.txt'), "Removing a non-existing file should return False"

        # Test get_metadata
        assert not fs.ft.get_metadata('data.txt'), "Getting metadata for an non-existing file should return False"
        fs.ft.add_file('data.txt', 200)
        assert fs.ft.get_metadata('data.txt'), "Getting metadata for an existing file should not return False"

def main():
    unittest.main()

if __name__=='__main__':
    main()
