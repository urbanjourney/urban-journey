

class Trigger:
    """Base class for all triggers"""
    def __init__(self):
        super().__init__()
        self._activities = []

    def add_activity(self, activity):
        """Subscribe an activity to this trigger."""
        self._activities.append(activity)

    async def trigger(self, *args, **kwargs):
        """Trigger all activities subscribed to this trigger."""
        for activity in self._activities:
            await activity.trigger((self, None), None, *args, **kwargs)
