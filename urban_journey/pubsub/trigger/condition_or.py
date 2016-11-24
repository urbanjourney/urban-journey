from urban_journey.pubsub.trigger.base import TriggerBase


class ConditionOr(TriggerBase):
    def __init__(self, *args):
        super().__init__()

        # Add triggers to the list.
        self.triggers = []
        for trigger in args:
            self.add_trigger(trigger)

    def add_trigger(self, trigger):
        # If the trigger is a ConditionOr, concatenate.
        if isinstance(trigger, ConditionOr):
            for tr in trigger.triggers:
                self.triggers.append(tr)
                tr.add_activity(self)
                tr.remove_activity(trigger)

        # Check if it's actually a trigger
        if not isinstance(trigger, TriggerBase):
            raise TypeError("All parameters must inherit from urban_journey.TriggerBase")

        # Add the trigger.
        self.triggers.append(trigger)
        trigger.add_activity(self)

    async def trigger(self, senders, sender_params, instance, *args, **kwargs):
        for activity in self._activities:
            await activity.trigger([self] + senders, sender_params, instance, *args, **kwargs)

