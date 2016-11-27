

class TriggerBase:
    """Base class for all triggers"""
    def __init__(self):
        # super().__init__()
        self._activities = []

    def add_activity(self, activity):
        """
        Connect an activity to this trigger.

        :param urban_journey.ActivityBase activity: Activity to add.
        """
        self._activities.append(activity)

    def remove_activity(self, activity):
        """
        Disconnect an activity to this trigger.

        :param urban_journey.ActivityBase activity: Activity to remove.
        """
        if activity in self._activities:
            self._activities.remove(activity)

    async def trigger(self, *args, **kwargs):
        """
        Trigger all activities connected to this trigger and pass all arguments to the activity.

        """
        for activity in self._activities:
            await activity.trigger([self], {}, None, *args, **kwargs)

    def __and__(self, other):
        from urban_journey.pubsub.trigger.condition_and import ConditionAnd
        return ConditionAnd(self, other)

    def __or__(self, other):
        from urban_journey.pubsub.trigger.condition_or import ConditionOr
        return ConditionOr(self, other)

