import unittest
from time import time
from threading import Semaphore

from urban_journey.base.module import ModuleBase
from urban_journey.base.activity import activity
from urban_journey.base.trigger import DescriptorClassTrigger
from urban_journey.base.trigger import Trigger
from urban_journey.clock import Clock


class TestTrigger(unittest.TestCase):
    def test_simple_descriptor_trigger(self):
        bar = [None]

        class Foo(ModuleBase):
            trigger = DescriptorClassTrigger(Trigger)

            @activity(trigger)
            def activity(self):
                bar[0] = self

        foo = Foo()
        foo.trigger.trigger()

        self.assertEqual(bar[0], foo)

    def test_multiple_module_instances(self):
        bar = []

        class Foo(ModuleBase):
            trigger = DescriptorClassTrigger(Trigger)

            @activity(trigger)
            def activity(self):
                bar.append(self)

        # Trigger each instance individually
        foo = []
        for i in range(5):
            foo.append(Foo())
            foo[-1].trigger.trigger()
        self.assertListSameContent(foo, bar)

        # Trigger all instances of the Foo module class
        bar = []
        Foo.trigger.trigger()
        self.assertListSameContent(foo, bar)

    def test_descriptor_clock(self):
        """Tests the clock trigger as a descriptor."""
        semp = Semaphore(0)

        class Foo(ModuleBase):
            clk = DescriptorClassTrigger(Clock)

            def __init__(self):
                super().__init__()
                self.bar = 0
                self.clk.frequency = 100

            @activity(clk)
            def bas(self):
                self.bar += 1
                if self.bar >= 5:
                    self.clk.stop()
                    semp.release()

        foo = Foo()
        t0 = time()
        foo.clk.start()
        semp.acquire()
        self.assertGreaterEqual(time() - t0, 0.05)
        self.assertEqual(foo.bar, 5)

        # This will fail if the package name (urban_journey) is changed.
        self.assertEqual(repr(foo.clk).split("at")[0],
                         "<urban_journey.base.trigger.DescriptorInstanceTrigger<urban_journey.clock.Clock> object ")


    @staticmethod
    def assertListSameContent(list1, list2, msg=None):
        """Asserts that two lists have the same content without checking the order."""
        if len(list1) != len(list2):
            raise AssertionError("List length does not match. " + (msg or ""))
        for item in list1:
            if item not in list2:
                raise AssertionError("Content does not match. " + (msg or ""))

    def test_assertListSameContent(self):
        # Seemed useless when I started to write this function, but somehow it helped me catch a bug.
        l1 = [1, 2, 3]
        l2 = [3, 1, 2]
        l3 = [1, 2, 3, 4]
        l4 = [1, 2, 4]

        try:
            self.assertListSameContent(l1, l2)
            assert True
        except AssertionError:
            assert False

        try:
            self.assertListSameContent(l1, l3)
            assert False
        except AssertionError:
            assert True

        try:
            self.assertListSameContent(l1, l4)
            assert False
        except AssertionError:
            assert True


if __name__ == '__main__':
    unittest.main()
