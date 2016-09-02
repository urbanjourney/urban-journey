from enum import Enum
from asyncio import Lock
import inspect
from copy import copy
from collections import defaultdict
import sys
from traceback import print_tb, print_exception

from .trigger import Trigger
from urban_journey.pubsub.ports.output import OutputPort
from urban_journey.pubsub.ports.base import PortDescriptorBase


class ActivityMode(Enum):
    drop = 0
    schedule = 2


class ActivityBase:
    """This is the base class for all activities."""
    def trigger(self, *args, **kwargs):
        pass


def activity(trigger: Trigger, *args, mode=ActivityMode.schedule, **kwargs):
    """Activity decorator factory. This function returns a function decorator class."""
    if not isinstance(trigger, Trigger):
        raise TypeError("trigger must inherit from Trigger")

    class ActivityDecorator(ActivityBase):
        def __init__(self, target):
            self.target = target

            self.trigger_obj = trigger
            self.trigger_obj.add_activity(self)

            self.mode = mode

            self.lock = Lock()

            # Create empty parameter dictionary
            self.parameters = inspect.signature(target).parameters
            self.empty_param_dict = {}
            for param in self.parameters:
                if param != "self":
                    self.empty_param_dict[param] = None

            self._output_static_ports = []
            self._output_data_holders = defaultdict(type(None))
            self._args = []
            self._kwargs = kwargs

            # Sort args and output ports.
            for arg in args:
                if isinstance(arg, PortDescriptorBase):
                    if issubclass(arg.instances_base_class, OutputPort):
                        self._output_static_ports.append(arg)
                    else:
                        self._args.append(arg)
                else:
                    self._args.append(arg)

        def get_output_data_holders(self, obj):
            if self._output_data_holders[obj] is None:
                d = {}
                for member_name in dir(obj):
                    if inspect.getattr_static(obj, member_name) in self._output_static_ports:
                        d[member_name] = getattr(obj, member_name).data
                self._output_data_holders[obj] = d
            return self._output_data_holders[obj]

        async def trigger(self, senders, instance, *args, **kwargs):
            """Called by the trigger."""
            try:
                if self.lock.locked():
                    if self.mode is ActivityMode.drop:
                        return
                with (await self.lock):

                    if instance is None:
                        if senders[1] is None:
                            await self.target(*args, *self._args, **kwargs, **self._kwargs)
                        else:
                            params = copy(self.empty_param_dict)
                            for param in params:
                                if param in senders[1]:
                                    params[param] = senders[1][param]
                            await self.target(*args, *self._args, **kwargs, **self._kwargs, **params)
                    else:
                        ouput_data_holders = self.get_output_data_holders(instance)
                        if senders[1] is None:
                            await self.target(instance, *args, *self._args, **kwargs, **self._kwargs,
                                              **ouput_data_holders)
                        else:
                            params = copy(self.empty_param_dict)
                            for param in params:
                                if param in senders[1]:
                                    params[param] = senders[1][param]
                            await self.target(instance, *args, *self._args, **kwargs, **self._kwargs, **params,
                                              **ouput_data_holders)

                        for key, value in ouput_data_holders.items():
                            await value.flush()

            except Exception as e:
                # print_tb(sys.exc_info()[2])
                print_exception(*sys.exc_info())
                # print(sys.exc_info())

        def __call__(self, *args, **kwargs):
            return self.target(*args, **kwargs)

    return ActivityDecorator
