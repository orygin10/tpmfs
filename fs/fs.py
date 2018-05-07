#!/usr/bin/env python2

from subprocess import Popen, PIPE
import yaml

from filetable import Filetable

def launch(bashCommand):
    process = Popen(bashCommand.split(), stdout=PIPE)
    stdout, _ = process.communicate()

    return stdout

def test():
    with open('filetable.yml', 'w') as f:
        f.write('files:\n')

    with Filetable() as ft:
        # Test list_files() with empty table
        assert ft.list_files()==False, "Listing all files should return False if table is empty"

        # Test add_file
        assert ft.add_file('data4.txt', 2004)==True, "Adding a non-existing file should return True"
        assert ft.add_file('data4.txt', 2004)==False, "Adding an already existing file should return False"

        # Test list_files
        assert ft.list_files()==True, "Listing all files should return True"

        # Test remove_file
        assert ft.remove_file('data4.txt')==True, "Removing an existing file should return True"
        assert ft.remove_file('data4.txt')==False, "Removing a non-existing file should return False"

    #print launch("./tpm.sh -r -i 0x1240000")
    
def main():
    test()

if __name__=='__main__':
    main()
