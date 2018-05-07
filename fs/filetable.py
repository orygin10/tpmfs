#!/usr/bin/env python2
import yaml
from operator import itemgetter
from common import print_success, print_failure, print_info


class Filetable:
    def __init__(self):
        self.files = []
        self.yml = None

    def __enter__(self):
        with open('filetable.yml', 'r') as fd:
            self.yml = yaml.load(fd)
        try:
            self.files = sorted(self.yml['files'], key=itemgetter('id'))
        except TypeError: # filetable.yml is empty
            self.files = []
        return self

##################################
        
    def list_files(self):
        """Make a list with all files in filetable.yml"""
        """Returns True if there are files, else return False"""
        if len(self.files) == 0:
            return False
        header = self.files[0].keys()
        print '\t'.join([el.title() for el in header])
        for _file in self.files:
            print '\t'.join([ str(_file[key]) for key in _file.keys() ])
        return True

    def add_file(self, filename, size_bytes):
        """Add file to filetable.yml"""
        """Returns True if file successfully added, False if file already exists"""
        block_size = 2048

        for f in self.files:
            if f['filename'] == filename:
                print_failure("%s already exists" % filename)
                return False
        try:
            lastfile = self.files[-1]
            _id = lastfile['id'] + 1
            offset = lastfile['offset'] + lastfile['size_b']
        except IndexError: # File table empty
            _id = 0
            offset = 0
        finally:
            size = int(size_bytes / block_size) + (size_bytes % block_size > 0)

        self.files.append({'size_b': size, 'size_h': size_bytes, 'filename': filename, 'offset': offset, 'id': _id})
        return True

    def remove_file(self, filename):
        """Remove file from filetable.yml"""
        """Return True if file successfully removed, False if file is not found or table empty"""
        if len(self.files) == 0:
            return False

        for n, _file in enumerate(self.files):
            if _file['filename'] == filename:
                self.files.pop(n)
                print_success("Removed file %s" % filename)
                return True

        print_failure("File %s was not found" % filename)
        return False

##################################

    def __exit__(self, exc_type, exc_value, traceback):
        # Cleanup
        self.yml['files'] = self.files
        with open('filetable.yml', 'w') as fd:
            yaml.dump(self.yml, fd)
        
