import unittest
from time import time
from threading import Semaphore

from urban_journey.clock import Clock
from urban_journey.base.activity import activity
from urban_journey.base.trigger import DescriptorClassTrigger
from urban_journey.base.module import ModuleBase


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
        assert s.acquire(timeout=0.1)
        self.assertGreaterEqual(time() - t0, 0.05)
        self.assertEqual(bas[0], 5)
