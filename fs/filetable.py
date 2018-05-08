#!/usr/bin/env python2
import yaml
from operator import itemgetter
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class FTError(Exception):
    pass

class Filetable:
    def __init__(self, yml_plain):
        self.yml = yaml.load(yml_plain)
        self.yml['files'] = sorted(self.yml['files'], key=itemgetter('id'))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

##################################
    def update_yml(self):
        self.yml['files'] = self.files

    def list_files(self):
        """Make a list with all files in filetable.yml
        Returns True if there are files, else raise FTError
        e.g:
        """
        if len(self.yml['files']) == 0:
            raise FTError("There are no files")

        header = self.yml['files'][0].keys()
        ret = ''
        ret += '\t'.join([el.title() for el in header])
        for _file in self.yml['files']:
            ret += '\n' + '\t'.join([ str(_file[key]) for key in _file.keys() ])
        return ret

    def add_file(self, filename, size_bytes):
        """Add file to filetable.yml
        Returns True if file successfully added, raise FTError if file already exists
        e.g:
        """
        block_size = 2048

        for f in self.yml['files']:
            if f['filename'] == filename:
                raise FTError("{0} already exists".format(filename))
        try:
            lastfile = self.yml['files'][-1]
            _id = lastfile['id'] + 1
            offset = lastfile['offset'] + lastfile['size_b']
        except IndexError: # File table empty
            _id = 0
            offset = 1 # Offset 0 is 0x1500000 (Filetable index)
        finally:
            size = int(size_bytes / block_size) + (size_bytes % block_size > 0)

        self.yml['files'].append({'size_b': size, 'size_h': size_bytes, 'filename': filename, 'offset': offset, 'id': _id})
        return True

    def remove_file(self, filename):
        """Remove file from filetable.yml
        Return True if file successfully removed, False if file is not found or table empty
        """

        if len(self.yml['files']) == 0:
             raise FTError("There are no files")

        for n, _file in enumerate(self.yml['files']):
            if _file['filename'] == filename:
                self.yml['files'].pop(n)
                return True

        raise FTError("File {0} was not found".format(filename))

    def get_metadata(self, filename):
        """Retrieves file metadata
        Returns a dict containing file metadata if found, else return False
        """
        for _file in self.yml['files']:
            if _file['filename'] == filename:
                return _file
        raise FTError("File {0} does not exist".format(filename))
