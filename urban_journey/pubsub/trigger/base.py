

class TriggerBase:
    """Base class for all triggers"""
    def __init__(self):
        super().__init__()
        self._activities = []

    def add_activity(self, activity):
        """Subscribe an activity to this trigger."""
        self._activities.append(activity)

    def remove_activity(self, activity):
        if activity in self._activities:
            self._activities.remove(activity)

    async def trigger(self, *args, **kwargs):
        """
        TriggerBase all activities subscribed to this trigger.

        """
        for activity in self._activities:
            await activity.trigger([self], {}, None, *args, **kwargs)

    def __and__(self, other):
        from urban_journey.pubsub.trigger.condition_and import ConditionAnd
        return ConditionAnd(self, other)
