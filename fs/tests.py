#!/usr/bin/env python2
from filetable import Filetable, FTError
from interface import Interface, InterfaceError
import os
import sys
import yaml
import unittest
dir_path = os.path.dirname(os.path.realpath(__file__))


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.i = Interface()
        self.ft_empty_content = 'files: []\n'

    def setUp(self):
        # Start with an empty TPM chip
        try:
            self.i.release_offset(0)
        except InterfaceError:
            pass
        # FT with file named data
        self.ft_f_data = Filetable("{'files': [{'offset': 1, 'size_h': 200, 'id': 0, 'size_b': 1, 'filename': 'data'}]}")
        
    def test_0_interface_pull_filetable_error(self):
        # Should raise bc there is no filetable in index 0
        with self.assertRaises(InterfaceError):
            self.i.pull_offset(0)

    def test_1_interface_pull_filetable(self):
        """Write empty filetable to TPM, then pull it
        it should not raise InterfaceError since it exists
        """
        self.i.push_offset(0, self.ft_empty_content)
        try:
            ft_content = self.i.pull_offset(0)
            self.assertEqual(ft_content, self.ft_empty_content)
        except InterfaceError:
            self.fail()

    def test_10_filetable_empty_list(self):
        """List files when filetable is empty
        it should raise FTError
        """
        with self.assertRaises(FTError):
            ft = Filetable(self.ft_empty_content)
            ft.list_files()

    def test_11_filetable_list(self):
        """List files when there is a file in filetable
        Should not return FTError since there is a file"""
        try:
            self.ft_f_data.list_files()
        except FTError:
            self.fail()
    
    def test_12_filetable_add_file_existing(self):
        """Add an existing file
        Should raise FTError since there is already an file with the
        same name in filetable yml"""
        with self.assertRaises(FTError):
            self.ft_f_data.add_file('data', 200)

    def test_13_filetable_add_file(self):
        """Add a non-existing file
        Should not raise FTError because file does not exist in ft"""
        try:
            self.ft_f_data.add_file('data2', 200)
        except FTError:
            self.fail()

    def test_14_filetable_remove_file_nonexisting(self):
        """Remove a file which does not exist in ft
        Should return FTError since the file does not exist"""
        with self.assertRaises(FTError):
            self.ft_f_data.remove_file('data_non_existing')

    def test_15_filetable_remove_file(self):
        """Remove an existing file
        Should not raise FTError since file exists"""
        try:
            self.ft_f_data.remove_file('data')
        except FTError:
            self.fail()

    def test_16_filetable_getmetadata_nonexisting_file(self):
        """Get metadata for a non existing file
        Should raise FTError since file does not exist"""
        with self.assertRaises(FTError):
            self.ft_f_data.get_metadata('file_not_exist')

    def test_17_filetable_getmetadata(self):
        """Get metadata from a file
        Should not raise FTError since file exists"""
        try:
            self.ft_f_data.get_metadata('data')
        except FTError:
            self.fail()

if __name__=='__main__':
    unittest.main()
