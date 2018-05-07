#!/usr/bin/env python2
from subprocess import Popen, PIPE
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def bash(bashCommand):
    process = Popen(bashCommand.split(), stdout=PIPE)
    stdout, _ = process.communicate()
    return stdout


class Interface:
    def __init__(self):
        self.password = raw_input("Enter password: ")

    def push_offset(self, offset, file_path):
        """Write 2048-bytes file into TPM at chosen offset"""
        start = 1500000
        print bash("{0}/../tpm.sh -ui 0x{1} -p {2}".format(dir_path, start+offset, self.password))
        print bash("{0}/../tpm.sh -di 0x{1} -p {2}".format(dir_path, start+offset, self.password))
        print bash("{0}/../tpm.sh -i 0x{1} -p {2} -f {3}".format(dir_path, start+offset, self.password, file_path))

    def pull_offset(self, offset):
        """Write 2048-bytes file into TPM at chosen offset"""
        start = 1500000
        data = bash("{0}/../tpm.sh -i 0x{1} -p {2} -r".format(dir_path, start+offset, self.password))
        return str(data).replace('\0', '')

    def push(self):
        """Store a file into TPM Chip"""
        # Write into filetable


        # Push into TPM
        pass

    def pull(self):
        """Load a file from TPM Chip"""
        pass

    def delete(self):
        """Nuke a file in TPM Chip"""
        pass

    ############################

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Cleanup
        pass

