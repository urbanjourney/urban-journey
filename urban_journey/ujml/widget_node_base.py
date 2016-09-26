import inspect
import sys
from os.path import isabs, join, dirname
from traceback import print_exception

from urban_journey import ModuleNodeBase
from urban_journey.pubsub.activity import ActivityBase
from PyQt4 import QtGui, QtCore, uic


# Can't inherit from pyqtSignal. Will have to find some other way to do this.
# Update: Found it.
class UjQtSignal(QtCore.QObject, ActivityBase):
    """
    Bases: :class:`urban_journey.ActivityBase`, :class:`PyQt4.QtCore.QObject`

    Qt signal like uj activity. It makes sure that the handler is called on the thread running the Qt event loop
    instead of the asyncio event loop.
    """
    signal = QtCore.pyqtSignal(object, object)

    def __init__(self, trigger):
        QtCore.QObject.__init__(self)
        ActivityBase.__init__(self)
        self.trigger_obj = trigger
        self.trigger_obj.add_activity(self)
        self.handles = {}
        self.signal.connect(self.signal_handler)

    def connect(self, instance, handle):
        self.handles[instance] = handle

    def signal_handler(self, instance, data):
        self.handles[instance](data)

    async def trigger(self, senders, sender_parameters, instance, *args, **kwargs):
        self.signal.emit(instance, sender_parameters)


class QWidgetNodeBase(ModuleNodeBase, QtGui.QWidget):
    """
    Bases: :class:`urban_journey.ModuleNodeBase`, :class:`PyQt4.QtGui.QWidget`

    Same as :class:`urban_journey.ModuleNodeBase`, but for modules with GUI's created with PyQt4. To connect uj triggers
    to QtSignals you can use a :class:`urban_journey.UjQtSignal`

    :param element: Lxml element in the ujml document
    :type element: etree.ElementBase
    :param root: Root ujml element
    :type root: :class: `urban_journey.UjmlNode`
    """
    def __init__(self, element, root):
        QtGui.QWidget.__init__(self)
        ModuleNodeBase.__init__(self, element, root)
        self.show()

    def load_ui(self, path: str):
        """Load in .ui file created by Qt Designer."""
        if not isabs(path):
            # If path is relative find ui file relative to file containing QWidgetNodeBase child class.
            path = join(dirname(inspect.getfile(sys._getframe(1))), path)
        uic.loadUi(path, self)
