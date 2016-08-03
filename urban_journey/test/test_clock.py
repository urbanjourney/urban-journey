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

        semp = Semaphore(0)

        @activity(clk)
        def foo():
            bas[0] += 1
            if bas[0] >= 5:
                clk.stop()
                semp.release()

        t0 = time()
        clk.start()
        semp.acquire()
        self.assertGreaterEqual(time() - t0, 0.05)
        self.assertEqual(bas[0], 5)


if __name__ == '__main__':
    unittest.main()
