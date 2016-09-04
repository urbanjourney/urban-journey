import os
import sys
from threading import Semaphore

from lxml import etree
import numpy as np
from PyQt4 import QtGui

from .node_base import NodeBase
from .interpreter import UJMLPythonInterpreter
from .data_container import DataContainer
from .attributes import String, Bool
from urban_journey import __version__ as uj_version
from .exceptions import IncompatibleUJVersion, IdMustBeUniqueError, PyQt4NotEnabledError

from urban_journey.pubsub.channels.channel_register import ChannelRegister


class UjmlNode(NodeBase):
    req_version = String(name="version")
    pyqt = Bool(optional_value=False)
    pyqt_quit_on_last_window_closed = Bool(optional_value=True)

    def __init__(self, element: etree.ElementBase, file_name, globals=None):
        super().__init__(element, None)
        self.pyqt_app = None
        if self.pyqt:
            self.pyqt_enable()
        self.__semaphore = Semaphore(0)

        self.node_dict_by_id = {}
        self.__data_container = DataContainer()
        self.interpreter = UJMLPythonInterpreter(globals or {})
        self.channel_register = ChannelRegister()

        self.configure_interpreter()
        self.__file_name = os.path.abspath(file_name)
        self.check_version()
        self.update_children()

    def pyqt_enable(self):
        print("sdfsdf")
        if self.pyqt_app is None:
            self.pyqt_app = QtGui.QApplication(sys.argv)
            self.pyqt_app.setQuitOnLastWindowClosed(self.pyqt_quit_on_last_window_closed)

    def pyqt_start(self, *, timeout=None):
        # TODO: Implement timeout for pyqt_start. It should return False in case of timeout
        # The timeout is usefull tests.
        if self.pyqt_app is None:
            self.raise_exception(PyQt4NotEnabledError)
        self.pyqt_app.exec_()
        return True

    def pyqt_stop(self):
        if self.pyqt_app is not None:
            self.pyqt_app.quit()

    def start(self, *, timeout=None, blocking=True):
        """
        Sends the start event. If blocking is True, then the function will block until UjmlNode.stop() is called. If
        PyQt4 is enabled it will always be blocking."""
        if self.pyqt:
            return self.pyqt_start(timeout=timeout)
        elif blocking:
            return self.__semaphore.acquire(timeout=timeout)

    def stop(self):
        """Sends a stop event to all modules subscribed to it, and releases the semaphore."""
        # For now this also kills.
        # TODO: Implement uj_start and uj_stop signals.
        if self.pyqt:
            self.pyqt_stop()
        self.__semaphore.release()

    def kill(self):
        """Sends stop event to all modules, stops PyQT4 if enabled and stops the main event loop."""
        pass

    def configure_interpreter(self):
        """Configures the embedded interpreter, by adding default members."""
        self.interpreter['abs_path'] = self.abs_path
        self.interpreter['np'] = np
        self.interpreter['data'] = self.data

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

    @property
    def data(self):
        return self.__data_container
