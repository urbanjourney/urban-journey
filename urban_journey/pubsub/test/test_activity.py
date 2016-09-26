"""These tests are here to test the functions and classes in 'activity.py'"""

from urban_journey.pubsub.activity import activity
from urban_journey.pubsub.trigger import TriggerBase
from urban_journey.pubsub.module_base import ModuleBase
from urban_journey.pubsub.channels.channel_register import ChannelRegister
from urban_journey import event_loop, Output, Clock, Input

import unittest
import asyncio
from threading import Semaphore


# Some global variables. Ugly but it solves the problem of passing information from an activity to a test.
bas2 = None


class TestActivity(unittest.TestCase):
    def setUp(self):
        self.loop = event_loop.get()

    def test_simple_trigger(self):
        """Creates one trigger and an activity and triggers it."""
        foo = TriggerBase()
        bas = [None]
        s = Semaphore(0)

        @activity(foo)
        async def bar():
            bas[0] = "Triggered"
            s.release()

        asyncio.run_coroutine_threadsafe(foo.trigger(), self.loop)
        assert s.acquire(timeout=0.1)

        self.assertEqual(bas[0], "Triggered")

    def test_direct_call(self):
        """Calls the activity directly."""
        """Creates one trigger and an activity and triggers it."""
        foo = TriggerBase()
        bas = [None]
        s = Semaphore(0)

        @activity(foo)
        async def bar():
            bas[0] = "Triggered"
            s.release()

        asyncio.run_coroutine_threadsafe(bar(), self.loop)
        s.acquire()

        self.assertEqual(bas[0], "Triggered")

    # Activities outside of modules where only meant to be used during early stages of development. The are officially
    # not supported.
    @unittest.skip
    def test_parameters(self):
        """Triggers an activity and passes extra parameters."""
        bas = [None]
        foo = TriggerBase()

        s = Semaphore(0)

        @activity(foo, "arg", k="kwarg")
        async def bar(p, k):
            bas[0] = p + k
            s.release()

        asyncio.run_coroutine_threadsafe(foo.trigger(), self.loop)
        assert s.acquire(timeout=0.1)

        self.assertEqual(bas[0], "argkwarg")

    def test_multiple_activity(self):
        bas = [None, None]
        foo = TriggerBase()

        s = Semaphore(0)

        @activity(foo)
        async def bar1():
            bas[0] = "bar1"

        @activity(foo)
        async def bar2():
            bas[1] = "bar2"
            await asyncio.sleep(0.01)
            s.release()

        asyncio.run_coroutine_threadsafe(foo.trigger(), self.loop)
        assert s.acquire(timeout=1)

        self.assertEqual(bas[0], "bar1")
        self.assertEqual(bas[1], "bar2")

    def test_output_handling(self):
        class Foo(ModuleBase):
            out = Output(channel_name="foo")
            inp = Input(channel_name="foo")
            clk = Clock()

            def __init__(self, cr, s):
                super().__init__(cr)
                self.s = s
                self.subscribe()

            def stop(self):
                self.clk.stop()

            def start(self):
                self.clk.frequency = 100
                self.clk.start()

            @activity(clk, out)
            async def tick(self, out):
                out["qwerty"] = "hello, is it me you're looking for."

            @activity(inp)
            async def qwerty(self, inp):
                assert inp["qwerty"] == "hello, is it me you're looking for."
                self.s.release()

        cr = ChannelRegister()
        s = Semaphore(0)
        foo = Foo(cr, s)
        foo.start()
        assert s.acquire(timeout=0.1)
        foo.stop()
