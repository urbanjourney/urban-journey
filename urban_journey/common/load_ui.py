import os

from PyQt4 import uic


def load_ui(dir_path, path, obj):
    uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(dir_path)), path), obj)
