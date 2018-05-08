#!/usr/bin/env python2
from filetable import Filetable, FTError
from interface import Interface, InterfaceError
import os
import sys
import yaml
dir_path = os.path.dirname(os.path.realpath(__file__))

class FS:
    def __init__(self):
        self.i = Interface()
        try:
            ft_content_plain = self.i.pull_offset(0)
        except InterfaceError:
            self.i.push_offset(0, "files: []\n")
            ft_content_plain = self.i.pull_offset(0)

        self.ft = Filetable(ft_content_plain)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
    ############################

    def write_to_tmp(self, data, filename):
        with open("{0}/tmp/{1}".format(dir_path, filename), "w") as fd:
            fd.write(data)
        return True

def tests():
    with FS() as fs:
        pass

if __name__=='__main__':
    tests()
