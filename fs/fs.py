#!/usr/bin/env python2

import yaml

from filetable import Filetable
from interface import Interface
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


def test():
    # Nuke filetable
    with open('filetable.yml', 'w') as f:
        f.write('files:\n')

    with Filetable() as ft:
        # Test list_files() with empty table
        assert not ft.list_files(), "Listing all files should return False if table is empty"

        # Test add_file
        assert ft.add_file('data4.txt', 2004), "Adding a non-existing file should return True"
        assert not ft.add_file('data4.txt', 2004), "Adding an already existing file should return False"

        # Test list_files
        assert ft.list_files(), "Listing all files should return True"

        # Test remove_file
        assert ft.remove_file('data4.txt'), "Removing an existing file should return True"
        assert not ft.remove_file('data4.txt'), "Removing a non-existing file should return False"

        # Test get_metadata
        assert not ft.get_metadata('data.txt'), "Getting metadata for an non-existing file should return False"
        ft.add_file('data.txt', 200)
        assert ft.get_metadata('data.txt'), "Getting metadata for an existing file should not return False"

    with Interface() as i:
        i.push_offset(0, "{}/filetable.yml".format(dir_path))
        filetable = i.pull_offset(0)
        print yaml.load(filetable)

def main():
    test()

if __name__=='__main__':
    main()
