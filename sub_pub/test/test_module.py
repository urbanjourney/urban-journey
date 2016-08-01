import unittest

from sub_pub.base.module import Module
from sub_pub.base.activity import activity
from sub_pub.base.trigger import Trigger


class TestModule(unittest.TestCase):
    def test_simple_module(self):
        foo = Trigger()

        class Qux(Module):
            @activity()


if __name__ == '__main__':
    unittest.main()
