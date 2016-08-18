import os

from lxml import etree

from .node_base import NodeBase
from .interpreter import UJMLPythonInterpreter
from .attributes import string_t
from urban_journey import __version__ as uj_version
from .exceptions import IncompatibleUJVersion


class UjmlNode(NodeBase):
    req_version = string_t(name="version")

    def __init__(self, element: etree.ElementBase, file_name):
        super().__init__(element, None)
        self.interpreter = UJMLPythonInterpreter()
        self.__file_name = os.path.abspath(file_name)
        self.check_version()
        self.update_children()

    def configure_interpreter(self):
        """Configures the embedded interpreter, by adding default members."""
        self.interpreter['abs_path'] = self.abs_path

    def check_version(self):
        rv = [int(x) for x in self.req_version.split('.')]
        dv = [int(x) for x in uj_version.split('.')]
        if not (rv[0] == dv[0] and
                rv[1] == dv[1] and
                rv[2] <= dv[2]):
            self.raise_exception(IncompatibleUJVersion, self.req_version, uj_version)

    @property
    def root(self):
        return self

    @property
    def file_name(self):
        return self.__file_name
