import asyncio

from urban_journey.pubsub.trigger import TriggerBase
from urban_journey.pubsub.trigger.descriptor_class_trigger import DescriptorClassTrigger
from urban_journey import event_loop


def clock_descriptor_factory():
    return DescriptorClassTrigger(Clock)


class Clock(TriggerBase):
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
        asyncio.run_coroutine_threadsafe(self.timer_callback(), loop=self.loop)

    def stop(self):
        self.running = False

    async def timer_callback(self):
        while self.running:
            await asyncio.sleep(self.period)
            await self.trigger()
