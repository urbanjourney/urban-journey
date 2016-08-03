import asyncio

from urban_journey.base.trigger import Trigger
from urban_journey import event_loop


class Clock(Trigger):
    def __init__(self, frequency=1):
        super().__init__()
        self.loop = event_loop.get()
        self.period = 1 / frequency
        self.trigger_time = None
        self.running = False

    @property
    def frequency(self):
        return 1 / self.period

    @frequency.setter
    def frequency(self, value):
        self.period = 1 / value

    def start(self):
        self.running = True
        self.trigger_time = self.loop.time() + self.period
        # There isn't a thread safe option for call_at, so the first clock trigger will happen immediately after start()
        self.loop.call_soon_threadsafe(self.start_callback)

    def stop(self):
        self.running = False

    def start_callback(self):
        if self.running:
            self.loop.call_at(self.trigger_time, self.timer_callback)

    def timer_callback(self):
        if self.running:
            self.trigger()
            self.trigger_time += self.period
            # If for some reason the execution time of the trigger is longer than the clock period then skip a trigger.
            while self.loop.time() >= self.trigger_time:
                self.trigger_time += self.period
            self.loop.call_at(self.trigger_time, self.timer_callback)
