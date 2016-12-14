import unittest
from time import time
from threading import Semaphore

from urban_journey.clock import Clock
from urban_journey.pubsub.activity import activity
from urban_journey.pubsub.trigger import DescriptorClassTrigger
from urban_journey.pubsub.module_base import ModuleBase


# This is the old clock. I don't care about this clock.

class TestClock(unittest.TestCase):
    def test_clock(self):
        bas = [0]
        clk = Clock(100)

        s = Semaphore(0)

        @activity(clk)
        async def foo():
            bas[0] += 1
            if bas[0] >= 5:
                clk.stop()
                s.release()

        t0 = time()
        clk.start()
        self.assertTrue(s.acquire(timeout=0.1))
        self.assertGreaterEqual(time() - t0, 0.05)
        self.assertEqual(bas[0], 5)
