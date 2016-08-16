"""These tests are here to test the functions and classes in 'activity.py'"""

from urban_journey.pubsub.activity import activity
from urban_journey.pubsub.trigger import Trigger
from urban_journey import event_loop

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
        foo = Trigger()
        bas = [None]
        s = Semaphore(0)

        @activity(foo)
        async def bar():
            bas[0] = "Triggered"
            s.release()

        asyncio.run_coroutine_threadsafe(foo.trigger(), self.loop)
        s.acquire()

        self.assertEqual(bas[0], "Triggered")

    def test_direct_call(self):
        """Calls the activity directly."""
        """Creates one trigger and an activity and triggers it."""
        foo = Trigger()
        bas = [None]
        s = Semaphore(0)

        @activity(foo)
        async def bar():
            bas[0] = "Triggered"
            s.release()

        asyncio.run_coroutine_threadsafe(bar(), self.loop)
        s.acquire()

        self.assertEqual(bas[0], "Triggered")

    def test_parameters(self):
        """Triggers an activity and passes extra parameters."""
        bas = [None]
        foo = Trigger()

        s = Semaphore(0)

        @activity(foo, "arg", k="kwarg")
        async def bar(p, k):
            bas[0] = p + k
            s.release()

        asyncio.run_coroutine_threadsafe(foo.trigger(), self.loop)
        s.acquire()

        self.assertEqual(bas[0], "argkwarg")

    def test_multiple_activity(self):
        bas = [None, None]
        foo = Trigger()

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
        assert s.acquire(timeout=0.1)

        self.assertEqual(bas[0], "bar1")
        self.assertEqual(bas[1], "bar2")
