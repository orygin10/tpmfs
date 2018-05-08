#!/usr/bin/env python2
import yaml
from operator import itemgetter
from common import print_success, print_failure, print_info
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class FTError(Exception):
    pass

class Filetable:
    def __init__(self, yml_plain):
        self.yml = yaml.load(yml_plain)
        try:
            self.files = sorted(self.yml['files'], key=itemgetter('id'))
        except TypeError: # filetable.yml is empty
            self.files = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

##################################
    def update_yml(self):
        self.yml['files'] = self.files
        yaml.dump(self.yml)
        return self.yml

    def list_files(self):
        """Make a list with all files in filetable.yml
        Returns True if there are files, else raise FTError
        e.g:
        """
        if len(self.files) == 0:
            raise FTError("There are no files")

        header = self.files[0].keys()
        print '\t'.join([el.title() for el in header])
        for _file in self.files:
            print '\t'.join([ str(_file[key]) for key in _file.keys() ])
        return True

    def add_file(self, filename, size_bytes):
        """Add file to filetable.yml
        Returns True if file successfully added, raise FTError if file already exists
        e.g:
        """
        block_size = 2048

        for f in self.files:
            if f['filename'] == filename:
                raise FTError("{0} already exists".format(filename))
        try:
            lastfile = self.files[-1]
            _id = lastfile['id'] + 1
            offset = lastfile['offset'] + lastfile['size_b']
        except IndexError: # File table empty
            _id = 0
            offset = 1 # Offset 0 is 0x1500000 (Filetable index)
        finally:
            size = int(size_bytes / block_size) + (size_bytes % block_size > 0)

        self.files.append({'size_b': size, 'size_h': size_bytes, 'filename': filename, 'offset': offset, 'id': _id})
        return True

    def remove_file(self, filename):
        """Remove file from filetable.yml
        Return True if file successfully removed, False if file is not found or table empty
        e.g:
        >>> remove_file('existing.txt')
        True
        >>> remove_file('not_existing.txt')
        False
        """

        if len(self.files) == 0:
            return False

        for n, _file in enumerate(self.files):
            if _file['filename'] == filename:
                self.files.pop(n)
                print_success("Removed file %s" % filename)
                return True

        print_failure("File %s was not found" % filename)
        return False

    def get_metadata(self, filename):
        """Retrieves file metadata
        Returns a dict containing file metadata if found, else return False
        e.g:
        >>> get_metadata('an_existing_file')
        {'size_b': 1, 'size_h': 1024, 'filename': 'an_existing_file', 'offset': 0, 'id': 0}
        >>> get_metadata('non_existing_file')
        False
        """
        for _file in self.files:
            if _file['filename'] == filename:
                return _file
        return False
