from enum import Enum
from asyncio import Lock, iscoroutinefunction
import inspect
from copy import copy
import sys
from traceback import print_exception

from .trigger import TriggerBase


class ActivityMode(Enum):
    drop = 0
    schedule = 2


class ActivityBase:
    """This is the base class for all activities."""
    async def trigger(self, senders, sender_parameters, instance, *args, **kwargs):
        """TriggerBase handler"""
        pass


def activity(trigger: TriggerBase, *args, mode=ActivityMode.schedule, **kwargs):
    """Activity decorator factory. This function returns a function decorator class."""
    if not isinstance(trigger, TriggerBase) and trigger is not None:
        raise TypeError("trigger must inherit from TriggerBase")

    class ActivityDecorator(ActivityBase):
        def __init__(self, target):
            if not iscoroutinefunction(target):
                raise TypeError("I find your lack of async disturbing.")
            self.target = target

            self.__trigger_obj = None

            self.trigger_obj = trigger

            self.mode = mode

            self.lock = Lock()

            # Create empty parameter dictionary
            self.parameters = inspect.signature(target).parameters
            self.empty_param_dict = {}
            for param in self.parameters:
                if param != "self":
                    self.empty_param_dict[param] = None

            self._args = args
            self._kwargs = kwargs

        @property
        def trigger_obj(self):
            return self.__trigger_obj

        @trigger_obj.setter
        def trigger_obj(self, trigger):
            if trigger is not None:
                if self.__trigger_obj is not None:
                    self.__trigger_obj.remove_activity(self)
                self.__trigger_obj = trigger
                self.__trigger_obj.add_activity(self)

        async def trigger(self, senders, sender_parameters, instance, *args, **kwargs):
            """
            Called by the trigger.

            :param senders: Dictionary with string typed key containing
            """
            try:
                if self.lock.locked():
                    if self.mode is ActivityMode.drop:
                        return
                with (await self.lock):
                    # TODO: Remove support for "instance is None". This is currently only meant to be used in unittests.
                    if instance is None:
                        params = copy(self.empty_param_dict)
                        for param in params:
                            if param in sender_parameters:
                                params[param] = sender_parameters[param]
                        await self.target(*args, *self._args, **kwargs, **self._kwargs, **params)
                    else:
                        params = copy(self.empty_param_dict)
                        for param in params:
                            if param in sender_parameters:
                                params[param] = sender_parameters[param]
                        await self.target(instance, *args, *self._args, **kwargs, **self._kwargs, **params)

            except Exception as e:
                # TODO: Add something here to either call an error handler, stop execution or just ignore based on some
                # setting somewhere.
                if instance is None:
                    print_exception(*sys.exc_info())
                    raise e
                else:
                    instance.root.handle_exception(sys.exc_info())

        def __call__(self, *args, **kwargs):
            return self.target(*args, **kwargs)

    return ActivityDecorator
