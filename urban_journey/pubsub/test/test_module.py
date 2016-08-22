import unittest

from urban_journey.pubsub.module_base import ModuleBase
from urban_journey.pubsub.channels.channel_register import ChannelRegister
from urban_journey.pubsub.activity import activity
from urban_journey.pubsub.trigger import Trigger, DescriptorClassTrigger
from urban_journey import Input, Output


class TestModule(unittest.TestCase):
    def test_activities_triggers_properties(self):
        class Foo(ModuleBase):
            trigger1 = DescriptorClassTrigger(Trigger)
            trigger2 = DescriptorClassTrigger(Trigger)
            trigger3 = DescriptorClassTrigger(Trigger)

            ip = Input()
            op = Output()

            not_trigger1 = None
            not_trigger2 = None
            not_trigger3 = None

            @activity(trigger1)
            def activity1(self):
                pass

            @activity(trigger2)
            def activity2(self):
                pass

            def not_activity1(self):
                pass

            def not_activity2(self):
                pass

        trigger_list = [
            "trigger1",
            "trigger2",
            "trigger3",
            "ip"
        ]

        activity_list = [
            "activity1",
            "activity2"
        ]

        port_list = ['ip', 'op']

        foo = Foo(ChannelRegister())
        assert len(trigger_list) == len(foo.triggers)
        assert len(activity_list) == len(foo.activities)
        assert len(port_list) == len(foo.ports)

        for name in Foo.triggers:
            assert name in trigger_list

        for name in foo.activities:
            assert name in activity_list

        for name in foo.ports:
            assert name in port_list
