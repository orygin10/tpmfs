#!/usr/bin/env python2
from subprocess import Popen, PIPE
import os
import re
from common import print_stderr
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
        print_stderr('Enter password : ')
        self.password = raw_input()
        print_stderr('\n')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    ##########################

    def push_offset(self, offset, data):
        """Write 2048-bytes into TPM at chosen offset"""
        buf_path = '{0}/tmp/buffer'.format(dir_path)
        try:
            with open(buf_path, 'wb') as fd:
                fd.write(data)
        except IOError:
            raise InterfaceError("File {0} cannot be opened".format(buf_path))

        start = 1500000
        bash("tpm.sh -di 0x{0} -p {1}".format(start+offset, self.password))
        _, rc = bash("tpm.sh -i 0x{0} -p {1} -f {2}".format(start+offset, self.password, buf_path))
        if rc == 0:
            return True
        raise InterfaceError("Cannot push to offset {0}".format(offset))

    def pull_offset(self, offset, size_bytes):
        """Read 2048 bytes from TPM"""
        if not 0 < size_bytes <= 2048:
            raise InterfaceError("size must be between 1 and 2048 bytes")
        start = 1500000
        data, rc = bash("tpm.sh -i 0x{0} -p {1} -r".format(start+offset, self.password))
        if rc == 0:
            return data
        raise InterfaceError("Cannot pull from offset {0}".format(offset))

    def release_offset(self, offset):
        """Release an offset on TPM, raises InterfaceError if release fails"""
        start = 1500000
        _, rc = bash("tpm.sh -ui 0x{0} -p {1}".format(start+offset, self.password))
        if rc == 0:
            return True
        raise InterfaceError("Cannot release offset {0}".format(offset))

