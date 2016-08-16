import unittest

from urban_journey.pubsub.module import ModuleBase
from urban_journey.pubsub.activity import activity
from urban_journey.pubsub.trigger import Trigger, DescriptorClassTrigger


class TestModule(unittest.TestCase):
    def test_activities_triggers_properties(self):
        class Foo(ModuleBase):
            trigger1 = DescriptorClassTrigger(Trigger)
            trigger2 = DescriptorClassTrigger(Trigger)
            trigger3 = DescriptorClassTrigger(Trigger)

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
            "trigger3"
        ]

        activity_list = [
            "activity1",
            "activity2"
        ]

        foo = Foo()
        self.assertEqual(len(trigger_list), len(foo.triggers))
        self.assertEqual(len(activity_list), len(foo.activities))

        for name in Foo.triggers:
            self.assertIn(name, trigger_list)

        for name in foo.activities:
            self.assertIn(name, activity_list)
