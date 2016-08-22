import os

from lxml import etree
import numpy as np

from .node_base import NodeBase
from .interpreter import UJMLPythonInterpreter
from .attributes import String
from urban_journey import __version__ as uj_version
from .exceptions import IncompatibleUJVersion, IdMustBeUniqueError

from urban_journey.pubsub.channels.channel_register import ChannelRegister


class UjmlNode(NodeBase):
    req_version = String(name="version")

    def __init__(self, element: etree.ElementBase, file_name, globals=None):
        self.node_dict_by_id = {}
        self.interpreter = UJMLPythonInterpreter(globals or {})
        self.channel_register = ChannelRegister()
        super().__init__(element, None)
        self.configure_interpreter()
        self.__file_name = os.path.abspath(file_name)
        self.check_version()
        self.update_children()

        # Pubsub specific members


    def configure_interpreter(self):
        """Configures the embedded interpreter, by adding default members."""
        self.interpreter['abs_path'] = self.abs_path
        self.interpreter['np'] = np

    def check_version(self):
        rv = [int(x) for x in self.req_version.split('.')]
        dv = [int(x) for x in uj_version.split('.')]
        if not (rv[0] == dv[0] and
                rv[1] == dv[1] and
                rv[2] <= dv[2]):
            self.raise_exception(IncompatibleUJVersion, self.req_version, uj_version)

    def register_node(self, node: NodeBase):
        """Registers a node."""
        # Register by id.
        if node.id is not None:
            if node.id in self.node_dict_by_id:
                raise node.raise_exception(IdMustBeUniqueError, node.id)
            else:
                self.node_dict_by_id[node.id] = node

    def deregister_node(self, node: NodeBase):
        self.node_dict_by_id.pop(node.id, None)

    @property
    def root(self):
        return self

    @property
    def file_name(self):
        return self.__file_name
