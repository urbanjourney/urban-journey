import unittest
from threading import Semaphore
import asyncio

from urban_journey.pubsub.ports.output import OutputPortDescriptorInstance
from urban_journey.pubsub.ports.input import InputPortStatic
from urban_journey.pubsub.descriptor.static import DescriptorStatic
from urban_journey.pubsub.module_base import ModuleBase
from urban_journey.pubsub.activity import activity
from urban_journey.pubsub.channels.channel_register import ChannelRegister
from urban_journey import event_loop


class TestChannelAndPorts(unittest.TestCase):
    def test_simple(self):
        class A(ModuleBase):
            op = DescriptorStatic(OutputPortDescriptorInstance)

            def __init__(self, channel_register):
                super().__init__(channel_register)
                self.op.subscribe()

            async def transmit(self):
                # print("transmitting:", self.op.channel_name)
                await self.op.flush("Some Data")

        class B(ModuleBase):
            ip = InputPortStatic(channel_name="op")

            def __init__(self, channel_register, semaphore):
                super().__init__(channel_register)
                self.semaphore = semaphore
                self.ip.subscribe()

            @activity(ip)
            async def foo(self, ip):
                assert ip == "Some Data"
                self.semaphore.release()

        semaphore = Semaphore(0)

        channel_register = ChannelRegister()

        a = A(channel_register)
        b = B(channel_register, semaphore)

        loop = event_loop.get()
        loop.set_debug(True)
        asyncio.run_coroutine_threadsafe(a.transmit(), loop=loop)
        assert semaphore.acquire(timeout=0.1)
