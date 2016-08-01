import asyncio

from sub_pub.base.trigger import Trigger


class Clock(Trigger):
    def __init__(self, frequency=1):
        super().__init__()
        self.__loop = asyncio.get_event_loop()
        self.__period = 1 / frequency
        self.___trigger_time = self.__loop.time()
        self.__running = False

    @property
    def __trigger_time(self):
        self.___trigger_time = self.__loop.time() + self.__period
        return self.___trigger_time

    def start(self):
        self.__running = True
        self.__loop.call_at(self.__trigger_time, self.timer_callback)

    def stop(self):
        self.__running = False

    def timer_callback(self):
        if self.__running:
            self()
            self.__loop.call_at(self.__trigger_time, self.timer_callback)
