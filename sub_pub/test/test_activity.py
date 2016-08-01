"""These tests are here to test the functions and classes in 'activity.py'"""

from sub_pub.base.activity import activity
from sub_pub.base.trigger import Trigger

import unittest

# Some global variables. Ugly but it solves the problem of passing information from an activity to a test.
bas = None
bas2 = None


class TestActivity(unittest.TestCase):
    def test_simple_trigger(self):
        """Creates one trigger and an activity and triggers it."""
        global bas
        foo = Trigger()
        bas = None

        @activity(foo)
        def bar():
            global bas
            bas = "Triggered"
        foo()
        self.assertEqual(bas, "Triggered")

    def test_direct_call(self):
        """Calls the activity directly."""
        """Creates one trigger and an activity and triggers it."""
        global bas
        foo = Trigger()
        bas = None

        @activity(foo)
        def bar():
            global bas
            bas = "Triggered"
        bar()
        self.assertEqual(bas, "Triggered")

    def test_parameters(self):
        """Triggers an activity and passes extra parameters."""
        global bas
        bas = None
        foo = Trigger()

        @activity(foo, "arg", k="kwarg")
        def bar(p, k):
            global bas
            bas = p + k

        foo()
        self.assertEqual(bas, "argkwarg")

    def test_multiple_activity(self):
        global bas, bas2
        bas = None
        bas2 = None
        foo = Trigger()

        @activity(foo)
        def bar1():
            global bas
            bas = "bar1"

        @activity(foo)
        def bar2():
            global bas2
            bas2 = "bar2"

        foo()
        self.assertEqual(bas, "bar1")
        self.assertEqual(bas2, "bar2")


if __name__ == '__main__':
    unittest.main()
