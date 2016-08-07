from enum import Enum
from asyncio import Lock

from .trigger import Trigger


class ActivityMode(Enum):
    drop = 0
    schedule = 2


class ActivityBase:
    """This is the base class for all activities."""
    def trigger(self, *args, **kwargs):
        pass


def activity(trigger: Trigger, *args, mode=ActivityMode.schedule, **kwargs):
    """Activity decorator factory. This function returns a function decorator class."""
    class ActivityDecorator(ActivityBase):
        def __init__(self, target):
            self.target = target

            self.trigger_obj = trigger
            self.trigger_obj.add_activity(self)

            self.mode = mode

            self.lock = Lock()

            # TODO: Separate outputs from args.
            # 'args' does not only contain the arguments that have to be passed to the target, but it also contains the
            # output tokens that have to be flushed after the target returns.
            self._outputs = []
            self._args = args
            self._kwargs = kwargs

        async def trigger(self, senders, *args, **kwargs):
            """Called by the trigger."""
            if self.lock.locked():
                if self.mode is ActivityMode.drop:
                    return

            # TODO: Add a check to check senders[1] contains all parameters self.target needs.
            with (await self.lock):
                if senders[1] is None:
                    await self.target(*args, *self._args, **kwargs, **self._kwargs)
                else:
                    await self.target(*args, *self._args, **kwargs, **self._kwargs, **senders[1])

        def __call__(self, *args, **kwargs):
            return self.target(*args, **kwargs)

    return ActivityDecorator
