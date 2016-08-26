from os import unlink, remove
from os.path import isdir, islink, exists
from shutil import rmtree


def rm(path):
    """Deletes a file, directory or symlink."""
    if exists(path):
        if isdir(path):
            if islink(path):
                unlink(path)
            else:
                rmtree(path)
        else:
            if islink(path):
                unlink(path)
            else:
                remove(path)
