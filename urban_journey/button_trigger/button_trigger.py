import sys
import os
import asyncio


from PyQt4 import Qt, QtGui, QtCore, uic
# from urban_journey.enable_qt import enable_qt

if __name__ == "__main__":
    sys.path.append(os.path.abspath("../.."))

from urban_journey.common.load_ui import load_ui
from urban_journey.pubsub.trigger import TriggerBase


class ButtonWindow(QtGui.QWidget):
    def __init__(self, loop):
        super().__init__()
        load_ui(__file__, "button.ui", self)

        self.t = None
        self.loop = loop

        self.trigger_1 = TriggerBase()
        self.trigger_2 = TriggerBase()
        self.trigger_3 = TriggerBase()
        self.trigger_4 = TriggerBase()
        self.trigger_5 = TriggerBase()

        self.triggers = [self.trigger_1,
                         self.trigger_2,
                         self.trigger_3,
                         self.trigger_4,
                         self.trigger_5]

        self.button_1.pressed.connect(lambda: self.loop.call_soon_threadsafe(self.handle_trigger, 0))
        self.button_2.pressed.connect(lambda: self.loop.call_soon_threadsafe(self.handle_trigger, 1))
        self.button_3.pressed.connect(lambda: self.loop.call_soon_threadsafe(self.handle_trigger, 2))
        self.button_4.pressed.connect(lambda: self.loop.call_soon_threadsafe(self.handle_trigger, 3))
        self.button_5.pressed.connect(lambda: self.loop.call_soon_threadsafe(self.handle_trigger, 4))
        self.show()

    def handle_trigger(self, i):
        self.triggers[i]()


from PyQt4.QtGui import QApplication, QWidget
from PyQt4.QtCore import QThread, pyqtSignal
from urban_journey.event_loop import get, enable_event_loop, loop


if __name__ == "__main__":
    from urban_journey.pubsub.activity import activity
    enable_event_loop()

    app = QApplication(sys.argv)
    w = ButtonWindow(get())

    @activity(w.trigger_1)
    def foo():
        print("triggered")

    sys.exit(app.exec_())
