from threading import current_thread

from urban_journey import QWidgetNodeBase, Clock, UjQtSignal, get_event_thread, Output


class k_stoff(QWidgetNodeBase):
    clk = Clock()
    signal = UjQtSignal(clk)
    out = Output()

    def __init__(self, element, root):
        super().__init__(element, root)
        self.load_ui("the_button.ui")
        self.signal.connect(self, self.handle_signal)
        self.clk.frequency = 2
        self.clk.start()
        self.subscribe()

    def handle_signal(self, obj):
        assert current_thread() is not get_event_thread()
        self.out.clear()
        self.out.data[0] = "qwertyuiop"
        self.out.flush_threadsafe()
