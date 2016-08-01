

class Trigger:
    def __init__(self):
        self._activities = []

    def add_activity(self, activity):
        self._activities.append(activity)

    def __call__(self):
        for activity in self._activities:
            activity.trigger()
