#!/usr/bin/env python2
from filetable import Filetable, FTError
from interface import Interface, InterfaceError
import os
import sys
import yaml
dir_path = os.path.dirname(os.path.realpath(__file__))

class FSError(Exception):
    pass

class FS:
    def __init__(self, t_interface = None):
        # t_interface is Tests() interface, with ownerpass set
        self.i = Interface() if t_interface is None else t_interface
        try:
            self.ft = self.pull_ft()
        except InterfaceError: # There no FT
            self.format_quick()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
    ############################
    def format_quick(self):
        """Whatever is in offset 0, rewrite is with an empty filetable"""
        self.ft.yml = {'files': []}
        self.push_ft()

    def push_ft(self):
        """Push str equivalent of filetable YML, can raise FTError"""
        self.i.push_offset(0, self.ft.as_str())

    def pull_ft(self):
        """Pull YML equivalent of bytes-like object in offset 0, can raise InterfaceError"""
        return Filetable( self.i.pull_offset(0, 2048).replace('\0','') )
                

    def push(self, filepath):
        """Store a file into TPM Chip"""
        # 1. File is divided into 2048-bytes chunks stored into a python list
        # 2. An entry is added to filetable with size=len of the list in 1)
        # 3. With offset returned by 2), push each chunk into offset [base offset+chunk_num]
        bs = 2048
        
        
        # 1.
        try:
            with open(filepath, 'r') as fd:
                data = fd.read()
        except IOError:
            raise FSError("Cannot open {0}".format(filepath))
        
        size_bytes = len(data)
        size_blocks = ( int(size_bytes / bs) + (size_bytes % bs > 0) )

        def chunks(l, n):
            # Thanks stackoverflow
            """Yield successive n-sized chunks from l."""
            for i in range(0, len(l), n):
                yield l[i:i + n]


        # 2.
        offset = self.ft.add_file(os.path.basename(filepath), size_blocks, size_bytes)

        # 3.
        for pos, chunk in enumerate(chunks(data, 2048)):
            self.i.push_offset(offset + pos, chunk)

        self.push_ft()
        return True

    def pull(self):
        """Load a file from TPM Chip"""
        pass

    def delete(self):
        """Nuke a file in TPM Chip"""
        pass

def tests():
    with FS() as fs:
        fs.format_quick()
        # TODO only write 5832 bytes maximum
        fs.push('/tmp/exist')

if __name__=='__main__':
    tests()
