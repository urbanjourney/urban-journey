from types import FunctionType

from .trigger import Trigger


class ActivityBase:
    """This is the base class for all activities."""
    def trigger(self, *args, **kwargs):
        pass


def activity(trigger: Trigger, *args, **kwargs):
    """Activity decorator factory. This function returns a function decorator class."""
    class ActivityDecorator(ActivityBase):
        def __init__(self, target):
            self.target = target

            self.trigger_obj = trigger
            self.trigger_obj.add_activity(self)

            # TODO: Seperate outputs from args.
            # 'args' does not only contain the arguments that have to be passed to the target, but it also contains the
            # output tokens that have to be flushed after the target returns.
            self._outputs = []
            self._args = args
            self._kwargs = kwargs

        async def trigger(self, *args, **kwargs):
            """Called by the trigger."""
            await self.target(*args, *self._args, **kwargs,  **self._kwargs)

        def __call__(self, *args, **kwargs):
            return self.target(*args, **kwargs)

    return ActivityDecorator
