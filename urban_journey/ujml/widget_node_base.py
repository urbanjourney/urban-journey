import inspect
import sys
from os.path import isabs, join, dirname
from traceback import print_exception

from urban_journey import ModuleNodeBase
from urban_journey.pubsub.activity import ActivityBase
from PyQt4 import QtGui, QtCore, uic


# Can't inherit from pyqtSignal. Will have to find some other way to do this.
class UjQtSignal(QtCore.QObject, ActivityBase):
    """Redirects uj triggers to qt signals"""
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

    async def trigger(self, senders, instance, *args, **kwargs):
        try:
            self.signal.emit(instance, senders[1])
        except Exception as e:
            print_exception(*sys.exc_info())


class WidgetNodeBase(ModuleNodeBase, QtGui.QWidget):
    def __init__(self, element, root):
        QtGui.QWidget.__init__(self)
        ModuleNodeBase.__init__(self, element, root)
        self.show()

    def load_ui(self, path: str):
        if not isabs(path):
            # If path is relative find ui file relative to file containing WidgetNodeBase child class.
            path = join(dirname(inspect.getfile(sys._getframe(1))), path)
        uic.loadUi(path, self)







