import unittest
from threading import Semaphore
import asyncio

from urban_journey.base.channels.channel import Channel
from urban_journey.base.ports.output import OutputPort
from urban_journey.base.ports.input import InputPort
from urban_journey.base.activity import activity
from urban_journey import event_loop


class TestChannelAndPorts(unittest.TestCase):
    def test_simple(self):
        """
        Simplest possible test with channels and ports. It creates 1 input port, 1 output port and 1 channel. Then it
        adds the ports to the channel, Connects the input channel to an activity and flushes some data through the output
        port. """
        ch = Channel("foo")
        op = OutputPort()
        ip = InputPort()
        ch.add_port(op)
        ch.add_port(ip)

        qux = [None]

        s = Semaphore(0)

        @activity(ip)
        async def bar():
            qux[0] = "bar triggered: " + await ip.data
            s.release()

        op.data = "Random data"

        loop = event_loop.get()
        asyncio.run_coroutine_threadsafe(op.flush(), loop)

        s.acquire()
