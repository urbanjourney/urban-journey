from enum import Enum
from asyncio import Lock
import inspect
from copy import copy
from collections import defaultdict
import sys
from traceback import print_tb, print_exception
from abc import ABCMeta, abstractmethod

from .trigger import TriggerBase
from urban_journey.pubsub.ports.output import OutputPort
from urban_journey.pubsub.ports.base import PortDescriptorBase


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
    if not isinstance(trigger, TriggerBase):
        raise TypeError("trigger must inherit from TriggerBase")

    class ActivityDecorator(ActivityBase):
        def __init__(self, target):
            # TODO: Check if target is a coroutine.
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

            # self._output_static_ports = []
            # self._output_data_holders = defaultdict(type(None))
            self._args = args  # changed [] to args
            self._kwargs = kwargs

            # Sort args and output ports.
            # for arg in args:
            #     if isinstance(arg, PortDescriptorBase):
            #         if issubclass(arg.instances_base_class, OutputPort):
            #             self._output_static_ports.append(arg)
            #         else:
            #             self._args.append(arg)
            #     else:
            #         self._args.append(arg)

        # def get_output_data_holders(self, obj):
        #     """
        #     The variable name of descriptor object cannot be known without either having the instance of the parent
        #     object or it's class. That is why we have to wait until we receive a trigger to get the name of the output
        #     ports.
        #     :param obj: Module object with output port descriptors.
        #     :return:
        #     """
        #     # This dictionary should not change during the run. So just cache it and always return the same dictionary.
        #     if self._output_data_holders[obj] is None:
        #         d = {}
        #         # Loop through all members of the object.
        #         for member_name in dir(obj):
        #             # check whether they are output ports.
        #             if inspect.getattr_static(obj, member_name) in self._output_static_ports:
        #                 # Add them to the list and remove them from the empty parameters dictionary.
        #                 d[member_name] = getattr(obj, member_name).data
        #                 self.empty_param_dict.pop(member_name, None)
        #         self._output_data_holders[obj] = d
        #     return self._output_data_holders[obj]

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
                        # ouput_data_holders = self.get_output_data_holders(instance)
                        params = copy(self.empty_param_dict)
                        for param in params:
                            if param in sender_parameters:
                                params[param] = sender_parameters[param]
                        await self.target(instance, *args, *self._args, **kwargs, **self._kwargs, **params)
                                          # **ouput_data_holders)

                        # for key, value in ouput_data_holders.items():
                        #     await value.flush()

            except Exception as e:
                # TODO: Add something here to either call an error handler, stop execution or just ignore based on some
                # setting somewhere.
                print_exception(*sys.exc_info())
                assert False

        def __call__(self, *args, **kwargs):
            return self.target(*args, **kwargs)

    return ActivityDecorator
