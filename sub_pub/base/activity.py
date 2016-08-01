from types import FunctionType

from .trigger import Trigger


def activity(trigger: Trigger, *args, **kwargs):
    """Activity decorator factory. This function returns a function decorator class."""
    class Activity:
        def __init__(self, target: FunctionType):
            self.target = target

            self.trigger_obj = trigger
            self.trigger_obj.add_activity(self)

            # TODO: Filter out outputs from args.
            # 'args' does not only contain the arguments that have to be passed to the target, but it also contains the
            # output tokens that have to be flushed after the target returns.
            self._outputs = []
            self._args = args
            self._kwargs = kwargs

        def trigger(self):
            """Called by the trigger."""
            self.target(*self._args, **self._kwargs)

        def __call__(self, *args, **kwargs):
            self.target(*args, **kwargs)

    return Activity


if __name__ == "__main__":
    foo = Trigger()

    @activity(foo)
    def bar():
        print("Heloo")

    foo.trigger()



