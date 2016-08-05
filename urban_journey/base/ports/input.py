"""

"""
from asyncio import Queue

from urban_journey.base.ports.base import PortBase
from urban_journey.base.trigger import Trigger
from urban_journey import event_loop


class InputPort(PortBase, Trigger):
    def __init__(self):
        super().__init__()
        self.q = Queue(loop=event_loop.get())
        # Fun fact:
        # A queue is just four silent letters waiting their turn. You could say those letters are... in a queue.
        # (•_•)  ( •_•)>⌐■-■  (⌐■_■)

    async def flush(self, data):
        await self.q.put(data)
        await self.trigger()

    @property
    async def data(self):
        return await self.q.get()
