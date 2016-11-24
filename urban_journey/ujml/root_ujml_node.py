import os
import sys
from threading import Semaphore
from traceback import print_exception

from lxml import etree
import numpy as np
from PyQt5 import QtGui

from .module_node_base import NodeBase
from .interpreter import UJMLPythonInterpreter
from .data_container import DataContainer
from .attributes import String, Bool
from urban_journey import __version__ as uj_version
from .exceptions import IncompatibleUJVersion, IdMustBeUniqueError, PyQt4NotEnabledError

from urban_journey.pubsub.module_base import ModuleBase
from urban_journey.pubsub.channels.channel_register import ChannelRegister
from urban_journey.pubsub.ports.output import Output
from urban_journey.event_loop import get as get_event_loop


class UjmlNode(NodeBase):
    """
    Bases: :class:`urban_journey.NodeBase`

    Root node for ujml documents.
    """
    req_version = String(name="version")

    pyqt = Bool(optional_value=False)
    pyqt_quit_on_last_window_closed = Bool(optional_value=True)

    stop_on_exception = Bool(optional_value=True)
    stop_on_assertion_error = Bool(optional_value=True)

    def __init__(self, element: etree.ElementBase, file_name, globals=None):
        self.__data_container = DataContainer()

        self.interpreter = UJMLPythonInterpreter(globals or {})
        """
        Instance of :class:`urban_journey.UJMLPythonInterpreter` used as the embedded python interpreter to run the
        python code in the ujml file.
        """

        self.channel_register = ChannelRegister()
        """Instance of :class:`urban_journey.ChannelRegister` used as the main channel register."""

        self.__configure_interpreter()

        self.__file_name = os.path.abspath(file_name)

        self.node_dict_by_id = {}
        """A dictionary containing all already read nodes by id."""

        super().__init__(element, None)

        self.pyqt_app = None
        """If PyQt4 is enabled, it contains the :class:`PyQt4.QtGui.QApplication` instance. """
        if self.pyqt:
            self.pyqt_enable()
        self.__semaphore = Semaphore(0)

        self.ujml_module = UjmlModule(self.channel_register)

        self.__check_version()

        self.update_children()

        self.__exc_info = None

    def pyqt_enable(self):
        """Enable the use of PyQt4."""
        if self.pyqt_app is None:
            self.pyqt_app = QtGui.QApplication(sys.argv)
            self.pyqt_app.setQuitOnLastWindowClosed(self.pyqt_quit_on_last_window_closed)

    def pyqt_start(self, *, timeout=None):
        """
        .. warning:: Don't call this function directly, instead make sure PyQt4 is enabled and
           :func:`urban_journey.UjmlNode.start` will call this function.

           Timeout not implemented yet.

        Sends the start event and waits for the PyQt4 event loop to terminate. Returns ``False`` if timed out,
        otherwise ``True``.
        """
        # TODO: Implement timeout for pyqt_start. It should return False in case of timeout
        # The timeout is usefull tests.
        if self.pyqt_app is None:
            self.raise_exception(PyQt4NotEnabledError)
        self.pyqt_app.exec_()
        return True

    def pyqt_stop(self):
        """
        .. warning:: Don't call this function directly, instead make sure PyQt4 is enabled and
           :func:`urban_journey.UjmlNode.stop` will call this function.

        Sends the stop event and stops the PyQt4 event loop.
        """
        if self.pyqt_app is not None:
            self.pyqt_app.quit()

    def start(self, *, timeout=None, blocking=True):
        """
        Sends the start event. If blocking is True, the function will block until
        :func:`urban_journey.UjmlNode.stop` is called. If PyQt4 is enabled it will always be blocking.
        """
        # Reset exception information to None
        self.__exc_info = None

        # Trigger uj_start event
        self.ujml_module.uj_start.flush_threadsafe(None)

        # If PyQt is active start it's event loop. Otherwise just wait for the semaphore
        # timed_out_n is True if there was a timeout
        if self.pyqt:
            timed_out_n = self.pyqt_start(timeout=timeout)
        elif blocking:
            timed_out_n = self.__semaphore.acquire(timeout=timeout)

        # Execution was stopped.
        # Check whether it was stopped due to some exception.
        if self.__exc_info is not None:
            # If it was print the exception and exit with ext code 1.
            raise self.__exc_info[1]

        return timed_out_n

    def stop(self):
        """
        Sends a stop event to all modules subscribed to it, and releases :func:`urban_journey.UjmlNode.start` if it's
        blocking.
        """
        self.ujml_module.uj_stop.flush_threadsafe(None)
        if self.pyqt:
            self.pyqt_stop()
        self.__semaphore.release()

    def kill(self):
        """
        Same as :func:`urban_journey.UjmlNode.stop` but it also stop the asyncio event loop.
        """
        self.stop()
        loop = get_event_loop()
        loop.stop()

    def handle_exception(self, exc_info):
        """
        The data returned by :func:`sys.exc_info` can be passed to this function in order to stop a run or to log the exeption,
        depending on the current settings.
        """
        # If stop_on_exception is true, stop on all exceptions
        # If stop_on_assertion_error is true stop on all assertion errors
        # Otherwise just print/log the exception.
        if self.stop_on_exception:
            self.__exc_info = exc_info
            self.stop()
        elif self.stop_on_assertion_error and issubclass(exc_info[0], AssertionError):
            self.__exc_info = exc_info
            self.stop()
        else:
            print_exception(*exc_info)
            # TODO: Log the exception

    def __configure_interpreter(self):
        """
        Configures the embedded interpreter, by adding default members.
        """
        self.interpreter['abs_path'] = self.abs_path
        self.interpreter['np'] = np
        self.interpreter['data'] = self.data

    def __check_version(self):
        """
        Check if the required |name| version is satisfied.
        """
        rv = [int(x) for x in self.req_version.split('.')]
        dv = [int(x) for x in uj_version.split('.')]
        if not (rv[0] == dv[0] and
                rv[1] == dv[1] and
                rv[2] <= dv[2]):
            self.raise_exception(IncompatibleUJVersion, self.req_version, uj_version)

    def register_node(self, node: NodeBase):
        """
        Registers a node, by adding it to the :attr:`urban_journey.UjmlNode.node_dict_by_id list` if it has an id.

        :param node: The new node to register.
        :type node: urban_journey.NodeBase
        """
        # Register by id.
        if node.id is not None:
            if node.id in self.node_dict_by_id:
                node.raise_exception(IdMustBeUniqueError, node.id)
            else:
                self.node_dict_by_id[node.id] = node

    def deregister_node(self, node: NodeBase):
        """
        Deregisters a node.

        :param node: Node to deregister.
        :type node: urban_journey.NodeBase
        """
        self.node_dict_by_id.pop(node.id, None)

    @property
    def root(self):
        return self

    @property
    def file_name(self):
        return self.__file_name

    @property
    def data(self):
        """
        Instance of :class:`urban_journey.DataContainer` holding the data that has been loaded in by data nodes.
        """
        return self.__data_container


class UjmlModule(ModuleBase):
    # Ujml events
    uj_start = Output()
    """Event channel that transmits when :func:`UjmlNode.start` is called."""

    uj_stop = Output()
    """Event channel that transmits when :func:`UjmlNode.stop` is called."""

    def __init__(self, channel_register):
        super().__init__(channel_register)
        self.subscribe()