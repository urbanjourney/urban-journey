import unittest
import asyncio

from time import time

from sub_pub.clock import Clock
from sub_pub.base.activity import activity

bas = None


class TestClock(unittest.TestCase):
    def test_clock(self):
        global bas
        bas = 0
        clk = Clock(1000)
        clk.start()

        @activity(clk)
        def foo():
            global bas
            bas += 1
            if bas >= 5:
                asyncio.get_event_loop().stop()

        t0 = time()
        loop = asyncio.get_event_loop()
        loop.run_forever()
        self.assertGreaterEqual(time() - t0, 0.005)
        self.assertEqual(bas, 5)


if __name__ == '__main__':
    unittest.main()
