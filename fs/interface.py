#!/usr/bin/env python2
from subprocess import Popen, PIPE
import os
import sys
import re
dir_path = os.path.dirname(os.path.realpath(__file__))

def bash(bashCommand, debug = False):
    """Returns a tuple containing shell STDOUT and STATUS_CODE"""
    bashCommand = "{0}/../".format(dir_path) + bashCommand
    if debug:
        bashCommand = "bash -x " + bashCommand
        process = Popen(bashCommand.split(), stdout=PIPE)
    else:
        process = Popen(bashCommand.split(), stdout=PIPE, stderr=PIPE)

    stdout, _ = process.communicate()
    return stdout, process.returncode


class InterfaceError(Exception):
    pass


class Interface:
    def __init__(self):
        sys.stderr.write('Enter password : ')
        sys.stderr.flush()
        self.password = raw_input()
        sys.stderr.write('\n')
        sys.stderr.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    ##########################

    def push_offset(self, offset, file_path):
        """Write 2048-bytes file into TPM at chosen offset"""
        try:
            with open(file_path, "r") as fd:
                if fd.read() is None:
                    raise InterfaceError("File {0} is empty".format(file_path))
        except IOError:
            raise InterfaceError("File {0} does not exist".format(file_path))

        start = 1500000
        bash("tpm.sh -di 0x{0} -p {1}".format(start+offset, self.password))
        _, rc = bash("tpm.sh -i 0x{0} -p {1} -f {2}".format(start+offset, self.password, file_path))
        if rc == 0:
            return True
        raise InterfaceError("Cannot push to offset {0}".format(offset))

    def pull_offset(self, offset):
        """Write 2048-bytes file into TPM at chosen offset"""
        start = 1500000
        data, rc = bash("tpm.sh -i 0x{0} -p {1} -r".format(start+offset, self.password))
        if rc == 0:
            return str(data).replace('\0', '')
        raise InterfaceError("Cannot pull from offset {0}".format(offset))

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

    def release_offset(self, offset):
        """Release an offset on TPM, raises InterfaceError if release fails"""
        start = 1500000
        _, rc = bash("tpm.sh -ui 0x{0} -p {1}".format(start+offset, self.password))
        if rc == 0:
            return True
        raise InterfaceError("Cannot release offset {0}".format(offset))

